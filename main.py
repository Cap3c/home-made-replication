from db_interface.DatabaseODBC import DatabaseODBC
from user_interface.UI import UI
from Replication import Replication
from tkinter import Tk
import csv
from pypyodbc import Cursor, Connection
import re
import winreg


def get_dsn(gdr_dsn="gdr"):
    """
    Get all the names of the availables dsn, except the local one
    :param gdr_dsn: The local dsn
    :return: At least 'ODBC Data Sources', and all the other DNSes
    """
    list_dsn = []
    access_registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    hkey = winreg.OpenKey(access_registry, r'SOFTWARE\ODBC\ODBC.ini')
    try:
        i = 0
        while True:
            if winreg.EnumKey(hkey, i) == gdr_dsn:
                pass
            else:
                list_dsn.append(winreg.EnumKey(hkey, i))  # Récupére les noms des dsn disponibles
            i += 1
    except OSError:
        pass
    return list_dsn


def get_db_distant(dsn):
    distant = DatabaseODBC()
    distant.connect(dsn)
    return distant.DB


def creation_date(jour, mois, an):
    return f"{int(jour):02}{int(mois):02}{an}"


def find_table(table, rows):
    for i, row in enumerate(rows):
        if row[0] == table:
            return i
    raise ValueError(f"{table} is not in list")


def command_replicate(table, rows, db, ui):
    return lambda: Replication(db, get_db_distant(ui.list_dsn_combo.get())).replicate(table,
                                                                                      rows[find_table(table, rows)][1],
                                                                                      creation_date(ui.jour.get(),
                                                                                                    ui.mois.get(),
                                                                                                    ui.annee.get()))


if __name__ == "__main__":
    file = 'tables.csv'
    gdr = DatabaseODBC()
    gdr.connect("gdr")
    frame = Tk()
    ui = UI(frame, get_dsn())
    with open(file, 'r', encoding='windows-1252') as f:
        # reads the csv
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)
        #
        [print(r) for r in rows]
        ui.controle_caisse.configure(command=command_replicate("Caisse", rows, gdr.DB, ui))
        ui.controle_vente.configure(command=command_replicate("vente_magasin", rows, gdr.DB, ui))
        ui.controle_ligne.configure(command=command_replicate("lignes_vente", rows, gdr.DB, ui))
        ui.controle_reg.configure(command=command_replicate("reglementmultiple", rows, gdr.DB, ui))
        ui.controle_avoir.configure(command=command_replicate("Avoir", rows, gdr.DB, ui))
        ui.controle_monnaie.configure(command=command_replicate("MonnaieCaisse", rows, gdr.DB, ui))
        ui.controle_client.configure(command=command_replicate("Client", rows, gdr.DB, ui))
        ui.controle_arrivage.configure(command=command_replicate("Arrivage", rows, gdr.DB, ui))
        ui.controle_produit.configure(command=command_replicate("Produit", rows, gdr.DB, ui))

        ui.frame.mainloop()
