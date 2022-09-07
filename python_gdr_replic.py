import pypyodbc  # doit être installé
from tkinter import *  # doit être installé
import datetime
import tkinter.ttk as ttk  # doit être installé
import winreg

list_dsn = []
i = 0
access_registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
hkey = winreg.OpenKey(access_registry, 'SOFTWARE\ODBC\ODBC.ini')

try:
    while True:
        if winreg.EnumKey(hkey, i) == "gdr":
            pass
        else:
            list_dsn.append(winreg.EnumKey(hkey, i))  # Récupére les noms des dsn disponibles
        i += 1
except OSError:
    pass

jourmodif = datetime.date.today()
jourmodif1 = str(jourmodif)
jourmodif1 = jourmodif1[:-6]  # Récupération de l'année
jourmodif1 = int(jourmodif1)
jourdebut, moisdebut, anneedebut = list(range(1, 32)), list(range(1, 13)), list(range(2010, jourmodif1 + 1))

print("Connexion à la base gdr locale")
connsource = pypyodbc.connect("DSN=GDR")
cursource = connsource.cursor()
print("Connexion ok")


def echappement_carac(mot):
    if mot.find("'"):
        mot = mot.replace("'", "\\'")
    return mot


def creation_date(jour, mois, an):
    if int(jour) < 10:
        jour = jour.zfill(2)
    if int(mois) < 10:
        mois = mois.zfill(2)
    date_recherche = an + mois + jour
    return date_recherche


def analyseproduit(curdistant, date):
    print("analyse des produits")
    print("détection des produits du serveur")
    cursource.execute(
        f"SELECT IDProduit FROM Produit WHERE idarrivage in (SELECT idarrivage from arrivage where date > {date})")
    retour = cursource.fetchall()
    produitslocaux = []
    for prod in retour:
        produitslocaux.append(prod[0])
    print("Détection et injection des produits distants")
    curdistant.execute(
        f"SELECT IDproduit,IDEtat_produit,IDCatégorie,IDSous_catégorie,IDFlux,IDSortie,IDSTockage,IDArrivage,IDLot,Désignation,Poids,Commentaire,Volume,Nombre,Etiquette,Niveau_Valorisation,to_char(Date_sortie,'YYYYMMDD'),Prix_Etiquette,hauteur,largeur,Profondeur,DonnéesModèle,IDUnité,Promo,PourcPromo,PrixPromo,PrixUnitCollecte,NumTVA,LBE,PrixUnitaire,PoidsUnitaire,VolumeUnitaire,stocRestant,bGestionLot,to_char(DateLimiteValidité,'YYYMMDD'),to_char(Datelimitedistrib,'YYYYMMDD'),bGestionDates FROM Produit WHERE idarrivage in (SELECT idarrivage from arrivage where date > {date})")
    produitsdistants = curdistant.fetchall()
    for pdist in produitsdistants:
        if pdist[0] not in produitslocaux:
            # for what are they for?
            """des = echappement_carac(pdist[9])
            comm = echappement_carac(pdist[9])"""
            # remplacer par un join les multiples inserts avec {value[i]}
            cursource.execute(
                f"INSERT INTO Produit(IDproduit,IDEtat_produit,IDCatégorie,IDSous_catégorie,IDFlux,IDSortie,IDSTockage,IDArrivage,IDLot,Poids,Volume,Nombre,Etiquette,Niveau_Valorisation,Date_sortie,Prix_Etiquette,hauteur,largeur,Profondeur,DonnéesModèle,IDUnité,Promo,PourcPromo,PrixPromo,PrixUnitCollecte,NumTVA,LBE,PrixUnitaire,PoidsUnitaire,VolumeUnitaire,stocRestant,bGestionLot,DateLimiteValidité,Datelimitedistrib,bGestionDates)values({pdist[0]},{pdist[1]},{pdist[2]},{pdist[3]},{pdist[4]},{pdist[5]},{pdist[6]},{pdist[7]},{pdist[8]},{pdist[10]},{pdist[12]},{pdist[13]},{pdist[14]},{pdist[15]},{pdist[16]},{pdist[17]},{pdist[18]},{pdist[19]},{pdist[20]},{pdist[21]},{pdist[22]},{pdist[23]},{pdist[24]},{pdist[25]},{pdist[26]},{pdist[27]},{pdist[28]},{pdist[29]},{pdist[30]},{pdist[31]},{pdist[32]},{pdist[33]},{pdist[34]},{pdist[35]},{pdist[36]})")
    connsource.commit()
    print("terminé")


def arrivage(curdistant, date):
    print("analyse des arrivages")
    print("détection des arrivages du serveur")
    cursource.execute(f"SELECT IDarrivage FROM arrivage where date > {date}")
    retour = cursource.fetchall()
    arrivlocaux = []
    for ar in retour:
        arrivlocaux.append(ar[0])
    print("Détection et injection des arrivages distants")
    curdistant.execute(
        f"SELECT IDarrivage ,to_char(Date,'YYYYMMDD'),origine,poids_total,cast(heure as character(5)),idcommune,Nombre,idtournée,volume_total,idclient,Nomposte,idsite FROM Arrivage  where date > {date} ")
    arrivdistant = curdistant.fetchall()
    for ard in arrivdistant:
        if ard[0] not in arrivlocaux:
            cursource.execute(
                f"insert into arrivage (IDarrivage ,Date,origine,poids_total,heure,idcommune,Nombre,idtournée,volume_total,idclient,Nomposte,idsite)values ({ard[0]},{ard[1]},'{ard[2]}',{ard[3]},{ard[4]},{ard[5]},{ard[6]},{ard[7]},{ard[8]},{ard[9]},'{ard[10]}',{ard[11]})")
    cursource.commit()
    print("terminé")


def clients(curdistant, date):
    print("analyse des clients")
    print("détection des clients du serveur")
    cursource.execute("SELECT IDClient FROM client")
    retour = cursource.fetchall()
    clientlocaux = []
    for ct in retour:
        clientlocaux.append(ct[0])
    print("Détection et injection des clients distants")
    curdistant.execute(
        "SELECT Civilite,Idclient,Societe,Adresse,Pays,Nomclient,Telephone,EMail,Ville,Mobile,CodePostal,to_char(Saisile,'YYYYMMDD'),to_char(DateModif,'YYYYMMDD'),LivreMemeAdresse,FactureMemeadresse,Prénom,Ref_Magasin,TauxRemise,Mode_Réglement,Ref_collecte,Ref_sortiehorsmag,Habitation,Etage,longitude,latitude,Catégorie,IDGroupe_compte,IDcommune,CompteActif,IDSecteurCollecte,IDCedex,EtatAdhésion,Genre,indice FROM Client")
    clientsdistant = curdistant.fetchall()
    for clt in clientsdistant:
        if clt[1] not in clientlocaux:
            """society = echappement_carac(clt[2])
            name = echappement_carac(clt[5])
            name1 = echappement_carac(clt[15])
            city = echappement_carac(clt[8])"""
            cursource.execute(
                f" insert into client (Civilite,Idclient,Societe,Adresse,Pays,Nomclient,Telephone,EMail,Ville,Mobile,CodePostal,Saisile,DateModif,LivreMemeAdresse,FactureMemeadresse,Prénom,Ref_Magasin,TauxRemise,Mode_Réglement,Ref_collecte,Ref_sortiehorsmag,Habitation,Etage,longitude,latitude,Catégorie,IDGroupe_compte,IDcommune,CompteActif,IDSecteurCollecte,IDCedex,EtatAdhésion,Genre,indice) values ({clt[0]},{clt[1]},'society','{clt[3]}','{clt[4]}','name','{clt[6]}','{clt[7]}','city','{clt[9]}','{clt[10]}',{clt[11]},{clt[12]},{clt[13]},{clt[14]},'name1','{clt[16]}',{clt[17]},'{clt[18]}','{clt[19]}',{clt[20]},{clt[21]},{clt[22]},{clt[23]},{clt[24]},{clt[25]},{clt[26]},{clt[27]},{clt[28]},{clt[29]},{clt[30]},{clt[31]},{clt[32]},'{clt[33]}')")
    connsource.commit()
    print("terminé")


def analysecaisse(curdistant, date):
    print("analyse des caisses")
    print("détection des caisses du serveur")
    cursource.execute(f"SELECT IDcaisse FROM Caisse WHERE Date > {date}")
    retour = cursource.fetchall()
    caisseslocales = []
    for caisse in retour:
        caisseslocales.append(caisse[0])
    print("Détection et injection des caisses distantes")
    curdistant.execute(
        f"SELECT idcaisse,to_char(date,'YYYYMMDD') , Montant,cast(heure as character(5)),nom_operateur,Prenom_operateur,Login_operateur,Operation,Ecart,cloture,caisse FROM caisse WHERE Date > {date} ")
    caissesdistantes = curdistant.fetchall()
    for caisse in caissesdistantes:
        if caisse[0] not in caisseslocales:
            cursource.execute(
                "insert into caisse (idcaisse,Date,Montant,heure,Nom_Operateur,Prenom_Operateur,Login_Operateur,Operation,Ecart,Cloture,caisse) values (%s,%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s')" % \
                (caisse[0], caisse[1], caisse[2], caisse[3], caisse[4], caisse[5], caisse[6], caisse[7], caisse[8],
                 caisse[9], caisse[10]))
    connsource.commit()
    print("terminé")


def avoir(curdistant, date):
    print("Analyse des avoirs")
    print("Détection des avoirs du serveur")
    cursource.execute("SELECT IDAvoir FROM avoir")
    retour = cursource.fetchall()
    avoirlocaux = []
    for avr in retour:
        avoirlocaux.append(avr[0])
    print("Détection et injection des avoirs distants")
    curdistant.execute(
        "SELECT IDavoir,Indice,to_char(date,'YYYYMMDD'),IDclient,Montant,Utilise,Saisipar,to_char(dateUtilise,'YYYYMMDD'),Observations,Signature,cast(heure as character(5)),Caisse,cast(heureUtilise as character(5)),IDvente_magasin FROM avoir")
    avoirsdistants = curdistant.fetchall()
    for avrdistant in avoirsdistants:
        if avrdistant[0] not in avoirlocaux:
            cursource.execute(
                f"insert into avoir (IDavoir,Indice,date,IDclient,Montant,Utilise,Saisipar,dateUtilise,Observations,Signature,heure,Caisse,heureUtilise,IDvente_magasin) values ({avrdistant[0]},'{avrdistant[1]}',{avrdistant[2]},{avrdistant[3]},{avrdistant[4]},{avrdistant[5]},'{avrdistant[6]}','{avrdistant[7]}','{avrdistant[8]}','{avrdistant[9]}','{avrdistant[10]}','{avrdistant[11]}','{avrdistant[12]}',{avrdistant[13]}) ")
    connsource.commit()
    print("terminé")


def regmultiple(curdistant, date):
    print("analyse des réglements multiples")
    print("détection des réglements multiples du serveur")
    cursource.execute("SELECT idrèglementmultiple FROM reglementmultiple")
    retour = cursource.fetchall()
    reglocales = []
    for reg in retour:
        reglocales.append(reg[0])
    print("Détection et injection des règlements multiples distants")
    curdistant.execute(
        "SELECT idrèglementmultiple,Modereglement,Montant,IDVente_magasin,Signature,IDAvoir FROM reglementmultiple")
    regdistants = curdistant.fetchall()
    for reg in regdistants:
        if reg[0] not in reglocales:
            cursource.execute(
                f"insert into Reglementmultiple(idrèglementmultiple,Modereglement,Montant,IDVente_magasin,Signature,IDAvoir) values ({reg[0]},'{reg[1]}',{reg[2]},{reg[3]},'{reg[4]}',{reg[5]})")
    connsource.commit()
    print("terminé")


def analysemonnaie(curdistant, date):
    print("analyse des monnaies caisses")
    print("détection des monnaies caisses du serveur")
    cursource.execute("SELECT idmonnaiecaisse from MonnaieCaisse")
    retour = cursource.fetchall()
    mcaisseslocales = []
    for moncaisse in retour:
        mcaisseslocales.append(moncaisse[0])
    print("Détection des monnaies caisses du serveur distant")
    curdistant.execute(
        "SELECT IDMonnaieCaisse,IDCaisse,P1c,P2c,P5c,P10c,P20c,P50c,P1e,P2e,B5e,B10e,B20e,B50e,B100e,B200e,B500e FROM MOnnaieCaisse")
    monnaiesdistantes = curdistant.fetchall()
    for mo in monnaiesdistantes:
        if mo[0] not in mcaisseslocales:
            cursource.execute(
                f"insert into monnaiecaisse(IDMonnaieCaisse,IDCaisse,P1c,P2c,P5c,P10c,P20c,P50c,P1e,P2e,B5e,B10e,B20e,B50e,B100e,B200e,B500e) values ({mo[0]},{mo[1]},{mo[2]},{mo[3]},{mo[4]},{mo[5]},{mo[6]},{mo[7]},{mo[8]},{mo[9]},{mo[10]},{mo[11]},{mo[12]},{mo[13]},{mo[14]},{mo[15]},{mo[16]})")
    connsource.commit()
    print("terminé")


def analysevente(curdistant, date):
    print("Analyse des ventes")
    print("détection des ventes du serveur")
    cursource.execute(f"SELECT idvente_magasin from vente_magasin WHERE Date > {date} ")
    retour = cursource.fetchall()
    venteslocales = []
    for ventes in retour:
        venteslocales.append(ventes[0])
    print("Détection et injection des ventes du serveur distant")
    curdistant.execute(
        f"select idvente_magasin, to_char(date,'YYYYMMDD'), idclient,code_postal,ville,cast(heure as character(5)) ,montant_total,tauxremise,mode_reglement,poids_total,montant_especes,tauxtva,etat,Caisse,idavoir,idcaisse,signature,Montanttva,idacompte,idsite from vente_magasin WHERE Date > {date}")
    ventesdistantes = curdistant.fetchall()
    for vt in ventesdistantes:
        if vt[0] not in venteslocales:
            cursource.execute(
                f"insert into vente_magasin (idvente_magasin,date,idclient,code_postal,ville,heure,montant_total,tauxremise,mode_reglement,poids_total,montant_especes,idcaisse,caisse,tauxtva,etat,idavoir,signature,montanttva,idacompte,idsite) values({vt[0]},{vt[1]},'{vt[2]}','{vt[3]}','{vt[4]}','{vt[5]}',{vt[6]},'{vt[7]}','{vt[8]}','{vt[9]}','{vt[10]}','{vt[15]}','{vt[13]}',{vt[11]},{vt[12]},{vt[14]},'{vt[16]}',{vt[17]},{vt[18]},{vt[19]}) ")
    connsource.commit()
    print("terminé")


def lignevente(curdistant, date):
    print("Analyse des lignes de vente")
    print("détection des lignes ventes du serveur")
    cursource.execute(
        f"SELECT idlignes_vente from lignes_vente where idvente_magasin in (SELECT idvente_magasin from Vente_magasin WHERE date > {date})")
    retour = cursource.fetchall()
    lignesventeslocales = []
    for lignes in retour:
        lignesventeslocales.append(lignes[0])
    print("Détection et injection des lignes ventes du serveur distant")
    curdistant.execute(
        f"SELECT IDLignes_Vente,IDproduit,IDcatégorie,IDSous_catégorie,IDVente_magasin,Montant,Nombre,Poids,Saisie_CatégorieProduit,Volume,Hauteur,Largeur,Profondeur,Tauxremise,Montant_Remise,IDunité,Promo,Signature,Etat,TauxTva,MontantTva from lignes_Vente where idvente_magasin in (SELECT idvente_magasin from Vente_magasin WHERE date > {date})")
    lignesdistantes = curdistant.fetchall()
    for ld in lignesdistantes:
        if ld[0] not in lignesventeslocales:
            print(
                f"{ld[0]},{ld[1]},{ld[2]},{ld[3]},{ld[4]},{ld[5]},{ld[6]},{ld[7]},{ld[8]},{ld[9]},{ld[10]},{ld[11]},{ld[12]},{ld[13]},{ld[14]},{ld[15]},{ld[16]},'{ld[17]}',{ld[18]},{ld[19]},{ld[20]}")
            cursource.execute(
                f"insert into Lignes_vente(IDLignes_Vente,IDproduit,IDcatégorie,IDSous_catégorie,IDVente_magasin,Montant,Nombre,Poids,Saisie_CatégorieProduit,Volume,Hauteur,Largeur,Profondeur,Tauxremise,Montant_Remise,IDunité,Promo,Signature,Etat,TauxTva,MontantTva) values ({ld[0]},{ld[1]},{ld[2]},{ld[3]},{ld[4]},{ld[5]},{ld[6]},{ld[7]},{ld[8]},{ld[9]},{ld[10]},{ld[11]},{ld[12]},{ld[13]},{ld[14]},{ld[15]},{ld[16]},'{ld[17]}',{ld[18]},{ld[19]},{ld[20]})")
    connsource.commit()
    print("terminé")


def connexion(fichier, day, month, year, nom_dsn):
    print(nom_dsn)
    dte = creation_date(day, month, year)
    print("Connexion à la base gdr distante")
    conndistant = pypyodbc.connect(f"DSN={nom_dsn}")
    curdistant = conndistant.cursor()
    print("Connexion ok")
    if fichier == "caisse":
        analysecaisse(curdistant, dte)
    if fichier == "vente":
        analysevente(curdistant, dte)
    if fichier == "lignes":
        lignevente(curdistant, dte)
    if fichier == "reg":
        regmultiple(curdistant, dte)
    if fichier == "avoir":
        avoir(curdistant, dte)
    if fichier == "monnaie_caisse":
        analysemonnaie(curdistant, dte)
    if fichier == "clientele":
        clients(curdistant, dte)
    if fichier == "arrivee":
        arrivage(curdistant, dte)
    if fichier == "prods":
        analyseproduit(curdistant, dte)


fen = Tk()
for i in range(5):
    fen.columnconfigure(i, weight=1)
for i in range(4):
    fen.rowconfigure(i, weight=1)

fen.geometry("800x600")
fen.title("replication")
dsn_label = Label(fen, text="choix du dsn distant")
dsn_label.grid(row=0, column=1)
list_dsn_combo = ttk.Combobox(fen, values=list_dsn)
list_dsn_combo.grid(row=0, column=2)
# sai_dsn=Entry(fen)
# sai_dsn.grid(row=1,column=1)
dateanalyse = Label(fen, text="Date de début analyse")
dateanalyse.grid(row=1, column=1)
saisiejour = ttk.Combobox(fen, values=jourdebut, width=5)
saisiejour.grid(row=1, column=2)
saisiemois = ttk.Combobox(fen, values=moisdebut, width=5)
saisiemois.grid(row=1, column=3)
saisieannee = ttk.Combobox(fen, values=anneedebut, width=10)
saisieannee.grid(row=1, column=4)
controle_caisse = Button(fen, text="Caisse",
                         command=lambda: connexion("caisse", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                   list_dsn_combo.get()))
controle_caisse.grid(row=3, column=1)
controle_vente = Button(fen, text="ventes",
                        command=lambda: connexion("vente", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                  list_dsn_combo.get()))
controle_vente.grid(row=2, column=2)
controle_ligne = Button(fen, text="Lignes ventes",
                        command=lambda: connexion("lignes", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                  list_dsn_combo.get()))
controle_ligne.grid(row=2, column=3)
controle_reg = Button(fen, text="reg multiples",
                      command=lambda: connexion("reg", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                list_dsn_combo.get()))
controle_reg.grid(row=2, column=4)
controle_avoir = Button(fen, text="avoir",
                        command=lambda: connexion("avoir", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                  list_dsn_combo.get()))
controle_avoir.grid(row=3, column=2)
controle_monnaie = Button(fen, text="Monnaie caisse",
                          command=lambda: connexion("monnaie_caisse", saisiejour.get(), saisiemois.get(),
                                                    saisieannee.get(), list_dsn_combo.get()))
controle_monnaie.grid(row=3, column=3)
controle_client = Button(fen, text="clients",
                         command=lambda: connexion("clientele", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                   list_dsn_combo.get(), list_dsn_combo.get()))
controle_client.grid(row=2, column=1)
controle_arrivage = Button(fen, text="arrivages",
                           command=lambda: connexion("arrivee", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                     list_dsn_combo.get()))
controle_arrivage.grid(row=4, column=1)
controle_produit = Button(fen, text="produits",
                          command=lambda: connexion("prods", saisiejour.get(), saisiemois.get(), saisieannee.get(),
                                                    list_dsn_combo.get()))
controle_produit.grid(row=4, column=2)
fen.mainloop()
