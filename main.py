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


def creation_date(jour, mois, an):
    return f"{int(jour):02}{int(mois):02}{an}"


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


def command_replicate(table, db, ui, file):
    rows = open_csv(file)[0]
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
    return Replication().replicate(db, distant, table,
                                   rows[find_table(table, rows)][1],
                                   date)


def main():
    #
    gdr = DatabaseODBC()
    gdr.connect("gdr")
    logging.info("Connected to local base, dns: gdr")
    # configure frame
    frame = Tk()
    frame.geometry("800x600")
    frame.title("Réplication")
    #
    ui = UI(frame, get_dsn())

    # configuring all the buttons
    ui.controle_caisse.configure(command=lambda: command_replicate("Caisse", gdr, ui, ui.versions.get()))
    ui.controle_vente.configure(
        command=lambda: command_replicate("vente_magasin", gdr, ui, ui.versions.get()))
    ui.controle_ligne.configure(
        command=lambda: command_replicate("lignes_vente", gdr, ui, ui.versions.get()))
    ui.controle_reg.configure(
        command=lambda: command_replicate("reglementmultiple", gdr, ui, ui.versions.get()))
    ui.controle_avoir.configure(command=lambda: command_replicate("Avoir", gdr, ui, ui.versions.get()))
    ui.controle_monnaie.configure(
        command=lambda: command_replicate("MonnaieCaisse", gdr, ui, ui.versions.get()))
    ui.controle_client.configure(command=lambda: command_replicate("Client", gdr, ui, ui.versions.get()))
    ui.controle_arrivage.configure(
        command=lambda: command_replicate("Arrivage", gdr, ui, ui.versions.get()))
    ui.controle_produit.configure(
        command=lambda: command_replicate("Produit", gdr, ui, ui.versions.get()))

    logging.info("Tkinter app launched")
    ui.frame.mainloop()
    logging.info("App closed")


if __name__ == "__main__":
    logging.info("App started")
    main()
