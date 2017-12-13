# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:13:47 2017

@author: matthieu
"""

import csv
import pickle

path = "/home/matthieu/Documents/Programmation/PSC/Chandelles_XXBTZEUR_candle_24h.csv"
with open(path, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    returnsMed = []
    returns = []
    PmedAvant = 1
    for row in reader:
        returns.append(float(row['return']))
        if row['Pmed'] != '':
            r = (float(row['Pmed']) - PmedAvant)/PmedAvant
            returnsMed.append(r)
            PmedAvant = float(row['Pmed'])

pathReturnsMedXBT = "/home/matthieu/Documents/Programmation/PSC/returnsMedXBT.txt"
pathReturnsXBT = "/home/matthieu/Documents/Programmation/PSC/returnsXBT.txt"
with open(pathReturnsMedXBT, "wb") as file:
    pickle.dump(returnsMed, file)
    file.close()
            
with open(pathReturnsXBT, "wb") as file:
    pickle.dump(returns, file)
    file.close()

print "Returns saved"