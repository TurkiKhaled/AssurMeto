from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from webscrapping import web_scraping
from matplotlib import legend
from matplotlib.pyplot import *
from matplotlib  import *
import matplotlib.pyplot as plot


# Liste des mois en français
mois = ["janvier", "février", "mars", "avril", "mai", "juin", 
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

# Liste des villes et codes associés
villes = [
    ("07690", "nice-cote-d-azur"), ("07481", "lyon-st-exupery"), ("07156", "paris-montsouris"),
    ("07110", "brest-guipavas"), ("07015", "lille-lesquin"), ("07190", "strasbourg-entzheim"),
    ("07631", "toulouse-francazal"), ("07130", "rennes-st-jacques"), ("07650", "marseille-marignane-marseille-provence"),
    ("000Z8", "aix-en-provence"), ("07747", "perpignan-rivesaltes"), ("07486", "grenoble-st-geoirs"),
    ("07510", "bordeaux-merignac"), ("07645", "nimes-courbessac"), ("000U5", "cannes"),
    ("07230", "angers-beaucouze"), ("07563", "avignon"), ("07280", "dijon-longvic"),
    ("07460", "clermont-ferrand-aulnat"), ("07602", "biarritz-anglet"), ("07090", "metz-frescaty"),
    ("07249", "orleans-bricy"), ("07494", "annecy-meythet"), ("07168", "troyes-barberey"),
    ("07610", "pau-uzein"), ("07201", "quimper-pluguffan"), ("07027", "caen-carpiquet"),
    ("07037", "rouen-boos"), ("07434", "limoges-bellegarde")
]

# Fonction d'analyse rétro
def Analyse_Retro(ville1, chiffre_affaire, choix_pivot, couts_fixes):
    CA_Assuré, CA_NonAssuré, P = [], [], []
    
    # Mapping des villes
    ville_map = {
        'Nice': "nice-cote-d-azur", 'Lyon': "lyon-st-exupery", 'Paris': "paris-montsouris",
        'Brest': "brest-guipavas", 'Lille': "lille-lesquin", 'Strasbourg': "strasbourg-entzheim",
        'Toulouse': "toulouse-francazal", 'Rennes': "rennes-st-jacques", 'Marseille': "marseille-marignane-marseille-provence",
        'Aix-en-Provence': "aix-en-provence", 'Perpignan': "perpignan-rivesaltes", 'Grenoble': "grenoble-st-geoirs",
        'Bordeaux': "bordeaux-merignac", 'Nîmes': "nimes-courbessac", 'Cannes': "cannes",
        'Angers': "angers-beaucouze", 'Avignon': "avignon", 'Dijon': "dijon-longvic",
        'Clermont-Ferrand': "clermont-ferrand-aulnat", 'Biarritz': "biarritz-anglet", 'Metz': "metz-frescaty",
        'Orléans': "orleans-bricy", 'Annecy': "annecy-meythet", 'Troyes': "troyes-barberey",
        'Pau': "pau-uzein", 'Quimper': "quimper-pluguffan", 'Caen': "caen-carpiquet",
        'Rouen': "rouen-boos", 'Limoges': "limoges-bellegarde"
    }
    
    # Utilisation de la ville depuis le dictionnaire
    ville = ville_map.get(ville1, None)
    if ville is None:
        print(f"Ville '{ville1}' non trouvée dans la liste.")
        return  # Arrêt de la fonction si la ville n'est pas trouvée

    # Date de début et fin
    datedeb = datetime.strptime('01/01/2015', '%d/%m/%Y').date()
    datefin = datedeb.replace(year=datedeb.year + 1)
    
    for y in range(9):  # Cette boucle pourrait être ajustée selon la période souhaitée
        vardate = datedeb.replace(year=datedeb.year + y)
        print(vardate)
        
       
        moisj = vardate.month  # Mois en chiffres
         # Mois en lettres
        
        data, appdata = [], []
        
        # Scraping des données climatiques pour la ville donnée
        code = next((v[0] for v in villes if v[1] == ville), None)
        if code is None:
            print(f"Code pour la ville {ville1} non trouvé.")
            continue

        # Collecte des données mensuelles
        for m in range(12):
            s = moisj + m
            if s > 12:
                s -= 12
            month_data = web_scraping(code, s, vardate.year, ville)
            if month_data is not None:  # Vérifier que les données ont été récupérées
                appdata.append(month_data)
            else:
                print(f"Aucune donnée disponible pour le mois {mois[s-1]} en {vardate.year}")

        if appdata:
            appdata = pd.concat(appdata, ignore_index=True)  # Concatenation des données
        else:
            print("Aucune donnée à concaténer.")
            continue

        # Traitement des données climatiques (calculs CAplt, Rplt, pertes, etc.)
        pluie = appdata.copy()
        pluie['jour'] = ''
        dd = vardate
        for s in range(len(pluie)):
            pluie['jour'].values[s] = dd
            dd = dd + timedelta(days=1)
            
        # Initialiser les colonnes avant la boucle
        pluie["ft"] = ""  
        pluie['CAplt'] = 0
        pluie['Rplt'] = 0
        pluie['Pertes'] = 0
        pluie['Rplt_Prime'] = 0

        # Remplir les valeurs dans la boucle
        CAplt=0
        for i in range(len(pluie)):
            plt = float(pluie['Precip'].values[i]) if pluie['Precip'].values[i] != '' else 0
            ft = (choix_pivot - plt) / choix_pivot
            
            # Calcul des autres valeurs
            if plt > choix_pivot:
                CAplt = 0
                Rplt = -couts_fixes
                Pertes = -couts_fixes
                Rplt_Prime = 0
            elif plt > 0 and plt < choix_pivot:
                CAplt = chiffre_affaire * ft
                Rplt = chiffre_affaire * ft - couts_fixes
                Pertes = 0
                Rplt_Prime = CAplt - couts_fixes
            else:
                CAplt = chiffre_affaire
                Rplt = chiffre_affaire - couts_fixes
                Pertes = 0
                Rplt_Prime = chiffre_affaire - couts_fixes

            # Remplir les valeurs calculées dans les colonnes
            pluie['CAplt'].values[i] = CAplt
            pluie['Rplt'].values[i] = Rplt
            pluie['Pertes'].values[i] = Pertes
            pluie['Rplt_Prime'].values[i] = Rplt_Prime if Rplt >= 0 else 0
            if pluie['Rplt'].values[i]<0:
                pluie['Rplt_Prime'].values[i]=0
            else:
                pluie['Rplt_Prime'].values[i]=Rplt_Prime

        # Affichage des résultats
        pluie = pluie.reindex(columns=['Date', 'jour', 'Precip', 'ft', 'CAplt', 'Rplt', 'Pertes', 'Rplt_Prime'])
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(pluie)  # ou toute autre valeur par défaut

        # Calcul de la prime à payer
        somme = 0
        taux = 0.02
        for h in range(len(pluie)):
            if pluie['Rplt'].values[h] < 0:
                somme += abs(pluie['Rplt'].values[i]) * (1 / (1 + taux) ** h)

        print("Prime à payer:", somme, "euros")

        CA_Assuré.append(pluie['Rplt_Prime'].sum())
        CA_NonAssuré.append(pluie['Rplt'].sum())
        P.append(somme - abs(pluie['Pertes'].sum()))

    # Affichage des résultats finaux
    print('CA assuré:', CA_Assuré)
    print('CA non assuré:', CA_NonAssuré)
    print('Bénéfice/Déficit:', P)
    print(CA_Assuré,'\n')
        
    periode=np.arange(2015,2024,1)
    
    plot.figure("Comparaison du chiffre d'affaires")
    plot.plot(periode, CA_Assuré, label='CA annuel en étant assuré', color="green")
    plot.plot(periode, CA_NonAssuré, label='CA annuel sans assurance', color="blue")
    plot.ylabel("Montant (en €)")
    plot.xlabel('Années')
    plot.title("Comparaison du chiffre d'affaires annuel")
    plot.legend()
    plot.show()  

# Création de la deuxième figure
    plot.figure("Bénéfice/Déficit")
    plot.plot(periode, P, "-rs")
    plot.ylabel("Montant (en €)")
    plot.xlabel('Années')
    plot.title("Bénéfice/Déficit")
    plot.show()

    results = {
        'prime': somme,
        'ca_assure': CA_Assuré,
        'ca_non_assure': CA_NonAssuré,
        'benefice': P
    }

    return results    # Retourner le montant de la prime calculée