from db_interface.DatabaseODBC import DatabaseODBC
from user_interface.UI import UI
from Replication import Replication
from tkinter import Tk
import csv
import winreg
import logging

logging.basicConfig(filename="app.log", filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)


def get_dsn():
    """
    Get all the names of the availables dsn
    :return: At least 'ODBC Data Sources', and all the DNSes
    """
    list_dsn = []
    try:
        access_registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        hkey = winreg.OpenKey(access_registry, r'SOFTWARE\ODBC\ODBC.ini')
    except OSError as OSEr:
        logging.critical(f"Registry failed to open : {OSEr}")
        raise OSEr
    logging.info("Registry opened")
    # if winreg.EnumKey(hkey, i) == gdr_dsn:
    try:
        i = 0
        while True:
            list_dsn.append(winreg.EnumKey(hkey, i))  # Récupère les noms des dsn disponibles
            i += 1
    except OSError:
        pass
    logging.info(f"All DSNs : {list_dsn}")
    return list_dsn


def creation_date(day, month, year):
    """
    Pads the day and month to respect the DDMMYYYY format
    """
    return f"{int(day):02}{int(month):02}{year}"


def find_table(table, rows):
    for i, row in enumerate(rows):
        if row[0] == table:
            return i
    logging.error(f"{table} not in list")
    raise ValueError(f"{table} is not in list")


def open_csv(file):
    rows = []
    header = []
    try:
        with open(file, 'r', encoding='windows-1252') as f:
            logging.info(f"Opened successfully {file}")
            # reads the csv
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                rows.append(row)
    except IOError as IOEr:
        logging.critical(f"{file} failed to open : {IOEr}")
        raise IOEr
    logging.info(f"Read {len(rows)} tables")
    return rows, header


def command_replicate(table, db, ui, lines):
    # default date, this allows for a minimum of data filtering
    date = creation_date(1, 1, 2020)
    try:
        date = creation_date(ui.jour.get(), ui.mois.get(), ui.annee.get())
    except ValueError:
        logging.error(f"Date is invalid, default minimum date is {date}")
    logging.info(f"Minimum date is {date}")
    # Connection à la base de données distante
    distant = DatabaseODBC()
    if not distant.connect(ui.list_dsn_combo.get()):
        logging.error(f"Connection to {ui.list_dsn_combo.get()} database failed")
    #
    return Replication(ui).replicate(db, distant, table, lines, date)


def replicate_all(db, ui, file):
    """
    Replicates all the tables from the file into the db
    :param db: The database the data is replicated in
    :param ui: The user interface
    :param file: The file indicating the format of the base
    """
    rows = open_csv(file)[0]
    # lines = rows[find_table(table, rows)][1]
    return [command_replicate(row[0], db, ui, row[1]) for row in rows]


def configure_buttons(btn_str, gdr, ui):
    for btn, table in btn_str.items():
        btn.configure(command=lambda: command_replicate(table, gdr, ui, ui.versions.get()))


def main():
    # accessing the local db
    dsn = "gdr"
    gdr = DatabaseODBC()
    gdr.connect(dsn)
    logging.info(f"Connected to local base, dsn: {dsn}")
    # configure frame
    frame = Tk()
    frame.geometry("800x600")
    frame.title("Réplication")
    ui = UI(frame, get_dsn())
    ui.create_browse_tables()
    # configuring all the buttons
    btn_name = {
        ui.controle_caisse: "Caisse",
        ui.controle_vente: "vente_magasin",
        ui.controle_ligne: "lignes_vente",
        ui.controle_reg: "reglementmultiple",
        ui.controle_avoir: "Avoir",
        ui.controle_monnaie: "MonnaieCaisse",
        ui.controle_client: "Client",  # this table is protected by a password, and can't be read
        ui.controle_arrivage: "Arrivage",
        ui.controle_produit: "Produit",
    }
    # configure_buttons(btn_name, gdr, ui)
    #
    ui.start_rep.configure(command=lambda: replicate_all(gdr, ui, ui.versions.get()))
    logging.info("Tkinter app launched")
    ui.frame.mainloop()
    logging.info("App closed")


if __name__ == "__main__":
    logging.info("App started")
    main()
