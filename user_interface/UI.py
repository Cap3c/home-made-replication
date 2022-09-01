from tkinter import Tk, Label, Button, Text, END, Scrollbar
import tkinter.ttk as ttk
import datetime
import logging
from os import listdir
from os.path import isfile, join


class UI:
    def __init__(self, frame: Tk, list_dsn):
        # print(list_dsn)

        for i in range(5):
            frame.columnconfigure(i, weight=1)
        for i in range(4):
            frame.rowconfigure(i, weight=1)

        # Récupération de l'année
        jourmodif1 = int(str(datetime.date.today())[:-6])
        jourdebut, moisdebut, anneedebut = list(range(1, 32)), list(range(1, 13)), list(range(2010, jourmodif1 + 1))

        dsn_label = Label(frame, text="choix du dsn distant")
        dsn_label.grid(row=0, column=1)
        self.dsn_label = dsn_label

        list_dsn_combo = ttk.Combobox(frame, values=list_dsn)
        list_dsn_combo.grid(row=0, column=2)
        self.list_dsn_combo = list_dsn_combo

        versions_label = Label(frame, text="Fichier schéma")
        versions_label.grid(row=0, column=3)
        self.versions_label = versions_label

        tables_versions = [f for f in listdir('./') if isfile(join('./', f)) if
                           f.startswith("tables") and f.endswith(".csv")]
        # tables_versions = [f.lstrip("tables").rstrip(".csv") for f in tables_versions]
        versions = ttk.Combobox(frame, values=tables_versions, width=20)
        versions.grid(row=0, column=4)
        self.versions = versions
        # sai_dsn=Entry(frame)
        # sai_dsn.grid(row=1,column=1)
        dateanalyse = Label(frame, text="Date de début analyse")
        dateanalyse.grid(row=1, column=1)
        self.dateanalyse = dateanalyse

        jour = ttk.Combobox(frame, values=jourdebut, width=5)
        jour.grid(row=1, column=2)
        self.jour = jour

        mois = ttk.Combobox(frame, values=moisdebut, width=5)
        mois.grid(row=1, column=3)
        self.mois = mois

        annee = ttk.Combobox(frame, values=anneedebut, width=10)
        annee.grid(row=1, column=4)
        self.annee = annee

        self.controle_caisse = None
        self.controle_vente = None
        self.controle_ligne = None
        self.controle_reg = None
        self.controle_produit = None
        self.controle_arrivage = None
        self.controle_client = None
        self.controle_monnaie = None
        self.controle_avoir = None

        self.start_rep = Button(frame, text="Commencer réplication")
        text_tables = Text(frame, wrap='word')
        text_tables.insert(END, '')
        text_tables.configure(state='disabled')
        self.text_tables = text_tables

        # self.connexion = connexion
        self.frame = frame
        logging.info("Frame initialized")

    def create_line_by_line(self):
        controle_caisse = Button(self.frame, text="Caisse")
        controle_caisse.grid(row=3, column=1)
        self.controle_caisse = controle_caisse

        controle_vente = Button(self.frame, text="ventes")
        controle_vente.grid(row=2, column=2)
        self.controle_vente = controle_vente

        controle_ligne = Button(self.frame, text="Lignes ventes")
        controle_ligne.grid(row=2, column=3)
        self.controle_ligne = controle_ligne

        controle_reg = Button(self.frame, text="reg multiples")
        controle_reg.grid(row=2, column=4)
        self.controle_reg = controle_reg

        controle_avoir = Button(self.frame, text="avoir")
        controle_avoir.grid(row=3, column=2)
        self.controle_avoir = controle_avoir

        controle_monnaie = Button(self.frame, text="Monnaie caisse")
        controle_monnaie.grid(row=3, column=3)
        self.controle_monnaie = controle_monnaie

        controle_client = Button(self.frame, text="clients")
        controle_client.grid(row=2, column=1)
        self.controle_client = controle_client

        controle_arrivage = Button(self.frame, text="arrivages")
        controle_arrivage.grid(row=4, column=1)
        self.controle_arrivage = controle_arrivage

        controle_produit = Button(self.frame, text="produits")
        controle_produit.grid(row=4, column=2)
        self.controle_produit = controle_produit

    def create_browse_tables(self):

        self.start_rep.grid(row=2, column=0)

        self.text_tables.grid(row=3, column=0, columnspan=5)

        log_scroll = Scrollbar(self.frame, command=self.text_tables.yview)
        log_scroll.grid(row=2, column=4, sticky='nse')
        self.text_tables['yscrollcommand'] = log_scroll.set

    def configure_buttons(self):
        pass
