import csv

if __name__ == "__main__":
    header = ['names', 'lines']
    #
    # IMPORTANT: THE FIRST INDEX NEEDS TO BE THE ID
    #
    tables = [
        ['Produit',
         "IDproduit,IDEtat_produit,IDCatégorie,IDSous_catégorie,IDFlux,IDSortie,IDSTockage,IDArrivage,IDLot,Désignation,Poids,Commentaire,Volume,Nombre,Etiquette,Niveau_Valorisation,to_char(Date_sortie,'YYYYMMDD'),Prix_Etiquette,hauteur,largeur,Profondeur,DonnéesModèle,IDUnité,Promo,PourcPromo,PrixPromo,PrixUnitCollecte,NumTVA,LBE,PrixUnitaire,PoidsUnitaire,VolumeUnitaire,stocRestant,bGestionLot,to_char(DateLimiteValidité,'YYYMMDD'),to_char(Datelimitedistrib,'YYYYMMDD'),bGestionDates", ],
        ['Arrivage',
         "IDarrivage ,to_char(Date,'YYYYMMDD'),origine,poids_total,cast(heure as character(5)),idcommune,Nombre,idtournée,volume_total,idclient,Nomposte,idsite", ],
        ['Client',
         "IDClient,Civilite,Societe,Adresse,Pays,Nomclient,Telephone,EMail,Ville,Mobile,CodePostal,to_char(Saisile,'YYYYMMDD'),to_char(DateModif,'YYYYMMDD'),LivreMemeAdresse,FactureMemeadresse,Prénom,Ref_Magasin,TauxRemise,Mode_Réglement,Ref_collecte,Ref_sortiehorsmag,Habitation,Etage,longitude,latitude,Catégorie,IDGroupe_compte,IDcommune,CompteActif,IDSecteurCollecte,IDCedex,EtatAdhésion,Genre,indice", ],
        [
            'Caisse',
            "idcaisse,to_char(date,'YYYYMMDD') , Montant,cast(heure as character(5)),nom_operateur,Prenom_operateur,Login_operateur,Operation,Ecart,cloture,caisse", ],
        [
            'Avoir',
            "IDavoir,Indice,to_char(date,'YYYYMMDD'),IDclient,Montant,Utilise,Saisipar,to_char(dateUtilise,'YYYYMMDD'),Observations,Signature,cast(heure as character(5)),Caisse,cast(heureUtilise as character(5)),IDvente_magasin", ],
        ['reglementmultiple', "idrèglementmultiple,Modereglement,Montant,IDVente_magasin,Signature,IDAvoir", ],
        [
            'MonnaieCaisse',
            "IDMonnaieCaisse,IDCaisse,P1c,P2c,P5c,P10c,P20c,P50c,P1e,P2e,B5e,B10e,B20e,B50e,B100e,B200e,B500e", ],
        [
            'vente_magasin',
            "idvente_magasin, to_char(date,'YYYYMMDD'), idclient,code_postal,ville,cast(heure as character(5)) ,montant_total,tauxremise,mode_reglement,poids_total,montant_especes,tauxtva,etat,Caisse,idavoir,idcaisse,signature,Montanttva,idacompte,idsite", ],
        [
            'lignes_vente',
            "IDLignes_Vente,IDproduit,IDcatégorie,IDSous_catégorie,IDVente_magasin,Montant,Nombre,Poids,Saisie_CatégorieProduit,Volume,Hauteur,Largeur,Profondeur,Tauxremise,Montant_Remise,IDunité,Promo,Signature,Etat,TauxTva,MontantTva", ]
    ]
    # special encoding needed because some table names includes accents
    with open('tables.csv', 'w+', encoding='windows-1252', newline='') as f:
        writer = csv.writer(f)
        # header
        writer.writerow(header)
        # lines
        for lines in tables:
            writer.writerow(lines)
