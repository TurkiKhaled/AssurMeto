import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import warnings
from time import sleep

warnings.filterwarnings('ignore')

def web_scraping(code, mois, annee, ville, retries=3, delay=2):
    """
    Fonction de web scraping pour récupérer les données de précipitations depuis Infoclimat.
    
    :param code: Code de la station météo
    :param mois: Mois à récupérer
    :param annee: Année à récupérer
    :param ville: Ville ciblée
    :param retries: Nombre d'essais en cas d'échec de la requête (par défaut 3)
    :param delay: Délai en secondes entre chaque tentative (par défaut 2)
    :return: DataFrame contenant les dates et précipitations, ou None en cas d'erreur
    """

    # Dictionnaire pour convertir les mois en lettres
    mois_les = {
    "01": "janvier",
    "02": "fevrier",
    "03": "mars",
    "04": "avril",
    "05": "mai",
    "06": "juin",
    "07": "juillet",
    "08": "aout",
    "09": "septembre",
    "10": "octobre",
    "11": "novembre",
    "12": "decembre"
}

    mois = str(mois).zfill(2)  # S'assurer que le mois est toujours sous format "01", "02", ..., "12"
    mois_lettre = mois_les.get(mois, None)

    if not mois_lettre:
     print(f"Erreur : le mois '{mois}' ne peut pas être converti.")
    else:
     url = f'https://www.infoclimat.fr/climatologie-mensuelle/{code}/{mois_lettre}/{annee}/{ville}.html'
     print(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for attempt in range(retries):
        try:
            # Effectuer la requête HTTP
            req = requests.get(url, headers=headers)
            req.raise_for_status()  # Vérifie si la requête a réussi (code 200)
            
            # Parse le contenu de la page avec BeautifulSoup
            soup = BeautifulSoup(req.content, 'html.parser', from_encoding="iso-8859-1")
            
            # Extraire les dates et les précipitations
            date = []
            precip = []
            
            # Récupérer les liens pour les dates et précipitations
            links = soup.find_all("a", {"class": "tipsy-trigger-right", "target": "_blank"})
            table_cells = soup.find_all("td", {"style": "white-space: nowrap"})
            
            nombre = len(links)
            h = 2
            
            if 2 * nombre > len(table_cells):
                h = 1
            
            # Collecte des données de date et de précipitations
            for j in range(nombre):
                date_string = links[j].text.strip()
                date.append(date_string)
                
                # Extraction de la précipitation correspondante
                precip_string = table_cells[j * h].find_all("span", {"style": "font-weight:bold;display:inline-block;font-size:16px"})
                
                if precip_string:
                    precip.append(precip_string[0].text.strip())
                else:
                    precip.append(None)  # Si la précipitation n'est pas trouvée, ajouter None
            
            # Création d'un DataFrame
            data = {'Date': date, 'Precip': precip}
            df = pd.DataFrame(data)
            return df
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération de la page (tentative {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                sleep(delay)  # Attendre un peu avant de réessayer
            else:
                return None
            
        except Exception as e:
            print(f"Une erreur s'est produite lors du scraping: {e}")
            return None
