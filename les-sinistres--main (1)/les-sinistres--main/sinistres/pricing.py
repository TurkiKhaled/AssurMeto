import datetime
from distutils.text_file import TextFile
import warnings
import pandas as pd 
from datetime import datetime
from datetime import timedelta
from matplotlib import legend
from matplotlib.pyplot import *
import numpy as np
import pandas as pd
from matplotlib  import *
import matplotlib.pyplot as plt

from calcul import prix
from ville import lieux
from webscrapping import web_scraping


mois=['test','janvier','fevrier','mars','avril','mai','juin','juillet','aout','septembre','octobre','novembre','decembre']
villes=[("07690","nice-cote-d-azur"),("07481","lyon-st-exupery"),("07156","paris-montsouris"),("07110","brest-guipavas"),("07015","lille-lesquin"),("07190","strasbourg-entzheim"),("07631","toulouse-francazal"),("07130","rennes-st-jacques"),("07650","marseille-marignane-marseille-provence"),("000Z8","aix-en-provence"),("07747","perpignan-rivesaltes"),("07486","grenoble-st-geoirs"),("07510","bordeaux-merignac"),("07645","nimes-courbessac"),("000U5","cannes"),("07230","angers-beaucouze"),("07563","avignon"),("07280","dijon-longvic"),("07460","clermont-ferrand-aulnat"),("07602","biarritz-anglet"),("07090","metz-frescaty"),("07249","orleans-bricy"),("07494","annecy-meythet"),("07168","troyes-barberey"),("07610","pau-uzein"),("07201","quimper-pluguffan"),("07027","caen-carpiquet"),("07037","rouen-boos"),("07434","limoges-bellegarde")]


    

def total(CA,pivot,cf,datedeb1,ville1): 
    ville=lieux(ville1)
    x=0
    for i in range(4):
        x=x+prix(CA,pivot,cf,datedeb1,ville1,i)
    print(x)
    return (x/4)
  
    
    
if __name__ == '__main__':
   # datedeb = datetime.strptime('01/02/2019','%d/%m/%Y').date()
   print (total (20,71,12,"01/02/2019","Nice"))
   

3
