# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 14:10:14 2017

@author: matthieu
"""
import csv
import pickle

path = "/home/matthieu/Documents/Programmation/PSC/Chandelles_Ether.csv"
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

pathReturnsMedETH = "/home/matthieu/Documents/Programmation/PSC/returnsMedEther.txt"
pathReturnsETH = "/home/matthieu/Documents/Programmation/PSC/returnsEther.txt"
with open(pathReturnsMedETH, "wb") as file:
    pickle.dump(returnsMed, file)
    file.close()
            
with open(pathReturnsETH, "wb") as file:
    pickle.dump(returns, file)
    file.close()

print "Returns saved"