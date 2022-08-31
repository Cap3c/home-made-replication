from tkinter import Tk, Label, Button
import tkinter.ttk as ttk
import datetime
import logging


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

        controle_caisse = Button(frame, text="Caisse")
        controle_caisse.grid(row=3, column=1)
        self.controle_caisse = controle_caisse

        controle_vente = Button(frame, text="ventes")
        controle_vente.grid(row=2, column=2)
        self.controle_vente = controle_vente

        controle_ligne = Button(frame, text="Lignes ventes")
        controle_ligne.grid(row=2, column=3)
        self.controle_ligne = controle_ligne

        controle_reg = Button(frame, text="reg multiples")
        controle_reg.grid(row=2, column=4)
        self.controle_reg = controle_reg

        controle_avoir = Button(frame, text="avoir")
        controle_avoir.grid(row=3, column=2)
        self.controle_avoir = controle_avoir

        controle_monnaie = Button(frame, text="Monnaie caisse")
        controle_monnaie.grid(row=3, column=3)
        self.controle_monnaie = controle_monnaie

        controle_client = Button(frame, text="clients")
        controle_client.grid(row=2, column=1)
        self.controle_client = controle_client

        controle_arrivage = Button(frame, text="arrivages")
        controle_arrivage.grid(row=4, column=1)
        self.controle_arrivage = controle_arrivage

        controle_produit = Button(frame, text="produits")
        controle_produit.grid(row=4, column=2)
        self.controle_produit = controle_produit

        # self.connexion = connexion
        self.frame = frame
        logging.info("Frame initialized")
