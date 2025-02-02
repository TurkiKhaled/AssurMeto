import datetime
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import calendar
from ville import lieux
from webscrapping import web_scraping

mois = ['test', 'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
villes = [("07690", "nice-cote-d-azur"), ("07481", "lyon-st-exupery"), ("07156", "paris-montsouris"), ("07110", "brest-guipavas"),
          ("07015", "lille-lesquin"), ("07190", "strasbourg-entzheim"), ("07631", "toulouse-francazal"), ("07130", "rennes-st-jacques"),
          ("07650", "marseille-marignane-marseille-provence"), ("000Z8", "aix-en-provence"), ("07747", "perpignan-rivesaltes"),
          ("07486", "grenoble-st-geoirs"), ("07510", "bordeaux-merignac"), ("07645", "nimes-courbessac"), ("000U5", "cannes"),
          ("07230", "angers-beaucouze"), ("07563", "avignon"), ("07280", "dijon-longvic"), ("07460", "clermont-ferrand-aulnat"),
          ("07602", "biarritz-anglet"), ("07090", "metz-frescaty"), ("07249", "orleans-bricy"), ("07494", "annecy-meythet"),
          ("07168", "troyes-barberey"), ("07610", "pau-uzein"), ("07201", "quimper-pluguffan"), ("07027", "caen-carpiquet"),
          ("07037", "rouen-boos"), ("07434", "limoges-bellegarde")]

def prix(CA, pivot, cf, datedeb1, ville1, w):
    datedeb = datetime.strptime(datedeb1, '%d/%m/%Y').date()
    date_a = datedeb - timedelta(days=365)
    datefin = datedeb.replace(year=datedeb.year + 1)
    # Extraction du mois, jour, année de la date de début
    annee = datedeb.year
    moisj = date_a.month   # Mois en chiffres
    jour = datedeb.day
    moisl = mois[moisj]     # Mois en lettres

    # Initialisation des listes utilisées
    data = []
    appdata = []
    l = []
    ville = lieux(ville1)
    # Extraction de données : plt par webscraping
    for v in range(len(villes)):
        if villes[v][1] == ville:
            code = villes[v][0]
    
    for m in range(12):
        s = moisj + m
        d = date_a
        if s > 12:  # Si le mois dépasse 12 (décembre), on réinitialise le mois et l'année
            s = s - 12
            d = date_a.replace(year=date_a.year + 1)  # Incrémente l'année de 1
        dernier_jour_du_mois = calendar.monthrange(d.year, s)[1]  # Récupère le dernier jour du mois
        jour_valide = min(d.day, dernier_jour_du_mois)  # Ajuste le jour si nécessaire

        l.append(d.replace(month=s, day=jour_valide))  # Remplace avec un jour valide
    print(moisj)
    for y in range(len(l)):  # len(l) 
        try:
            # Appel du scraping pour chaque mois et année
            mois_str = str(moisj).zfill(2) 
            print(mois_str) # Format du mois avec 2 chiffres
            year_str = str(l[y].year)
            appdata.append(web_scraping(code, mois_str, year_str, ville))  # Remplacez cette ligne par votre fonction
        except Exception as e:
            print(f"Erreur lors du scraping pour {l[y]}: {e}")
        
    appdata = pd.concat(appdata)   # Concatenation des df de tous les mois de l'année

    # Réorganisation de la dataframe
    pluie = appdata
    pluie['jour'] = ''
    dd = datedeb
    for s in range(len(pluie)):
        pluie['jour'].values[s] = dd
        dd = dd + timedelta(days=1)

    pluie["ft"] = ""  
    pluie["CAplt"] = ""
    pluie["Rplt"] = ""
# Remplacer les valeurs vides par NaN dans la colonne 'Precip'
    pluie['Precip'].replace('', np.nan, inplace=True)

        # Convertir la colonne 'Precip' en flottants
    pluie['Precip'] = pluie['Precip'].astype(float)
    
    # Calcul CAplt et Rplt
    CAplt = 0
    for i in range(len(pluie)):
        plt=float(pluie['Precip'].values[i])
        ft=(pivot-plt)/pivot
        pluie['ft'].values[i] = ft
        if plt > pivot:
            CAplt = 0
            Rplt = -cf
        elif (plt > 0) & (plt < pivot):
            CAplt = CA * ft
            Rplt = CA * ft - cf
        elif plt == 0:
            CAplt = CA
            Rplt = CA - cf
        pluie['CAplt'].values[i] = CAplt
        pluie['Rplt'].values[i] = Rplt

    # Affichage de la Dataframe
    pluie = pluie.reindex(columns=['Date', 'jour', 'Precip', 'ft', 'CAplt', 'Rplt'])
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # More options can be specified also
        print(pluie)

    # Calcul de la prime annuelle à payer
    somme = 0
    taux = 0.02
    for h in range(len(pluie)):
        if pluie['Rplt'].values[h] < 0:
            somme += abs(pluie['Rplt'].values[i]) * (1 / (1 + taux) ** h)
    return round(somme, 2)