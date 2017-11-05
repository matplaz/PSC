# -*- coding: utf-8 -*-
"""Ce script initialise une classe Chandelles, capable de créer les chandelles sous format liste a partir des 
donnees de trading CSV, et de les sauver sur le disque"""

from __future__ import division
import csv
import pickle
#classe enregistrant des chandelles a l'endroit pathChandelles, a partir du csv d'EY
class Chandelles:

    pathChandelles="/home/matthieu/Documents/Programmation/PSC/chandelles.txt"

    def __init__(self):
        self.chandelles = []
    
    #import des chandelles à partir du csv
        #MARCHE
    def importChandelles(self):
        path = "/home/matthieu/Documents/Polytechnique/2A/PSC/DonnéesEY/kraken_trades_historyMANIP.csv" #chemin vers le csv de EY
        with open(path, "rb") as csvfile:
            reader = csv.DictReader(csvfile, delimiter =",")
            mean = 0
            volume = 0
            c = 0
            candle = 0
            for row in reader:
                sgn = 1
                if row["buy"]=="s":
                    sgn = -1
                if candle != row["candle_15min"]:
                    candle = row["candle_15min"]
                    self.chandelles.append(mean)
                    self.chandelles.append(volume)
                    mean = float(row["price"])
                    volume = sgn * float(row["volume"].replace(',', '.'))            
                    c = 1
                else:                   
                    mean = (mean * c +float(row["price"])) / (c+1)
                    volume += sgn * float(row["volume"].replace(',', '.'))
                    c+=1
        self.chandelles.pop(0)
        self.chandelles.pop(0)
        #le premier élément est 0, à enlever car juste du a l'initialisation
        
    #Sauve la liste des chandelles dans le fichier texte situé à path
        #MARCHE
    def writeChandelles(self):
        with open(Chandelles.pathChandelles, "wb") as file:
            pickle.dump(self.chandelles, file)
    
candle = Chandelles()
candle.importChandelles()
candle.writeChandelles()
print("Candles saved to disk")

