# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 18:17:00 2017

@author: matthieu

Ce script permet d'importer un modele de Deep Learning, ainsi que ses poids, et de l'appliquer pour predire le cours de la futur chandelle
"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.models import model_from_json
import pickle

pathPSC = "/home/matthieu/Documents/Programmation/PSC/"

#import des chandelles
chandelles = []
pathChandelles = pathPSC + "chandelles.txt"
with open(pathChandelles, "rb") as file:
    chandelles = pickle.load(file)
test_x = []
test_labels = []
for i in range(len(chandelles)-200, len(chandelles)) :
    test_x.append(chandelles[i-50:i])
    test_labels.append(chandelles[i])
print("Loaded candles from disk")

#load the model
json_file = open(pathPSC+"model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

#load weights
model.load_weights(pathPSC+"model.h5")
print("Loaded model from disk")

#predict the price 
y = model.predict(test_x, batch_size=1, verbose=0)
for i in range(len(test_x)):    
    label = test_labels[i]
    print("Predit :",y[i],"      Reel :",label)
