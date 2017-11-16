import numpy as np
import pandas as pd

dataset = pd.read_csv(open("C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/dataEther.csv"), index_col=0) #import fichier csv brut

df=dataset.iloc[:,[1,2,3,4,-3]] #crée un dataFrame à partir des collonees 'volume', 'market', 'price', 'candle_15min'


chandelles=pd.DataFrame(columns=['L','M','Pmin','PQ1','Pméd','PQ3','Pmax','return']) # L:volume échangé en limite; M: volume échangé en markets, Pmin,PQ1,Pméd,PQ3,Pmax:min, premier quartile, médiane, troisième qurtile, max des prix des échanges d'ordre 'market', 'return':(P_close-P_open)/P_open

d_lim=df[df.market=='l'].groupby('candle_15min')

d_market=df[df.market=='m'].groupby('candle_15min')

#Remplissage des colonnes

chandelles['L']=d_lim['volume'].apply(lambda x: x.sum())
chandelles['M']=d_market['volume'].apply(lambda x: x.sum())
chandelles['Pmin']=d_market['price'].apply(lambda x: x.min())
chandelles['PQ1']=d_market['price'].apply(lambda x: x.quantile(0.25))
chandelles['Pméd']=d_market['price'].apply(lambda x: x.quantile(0.5))
chandelles['PQ3']=d_market['price'].apply(lambda x: x.quantile(0.75))
chandelles['Pmax']=d_market['price'].apply(lambda x: x.max())



#fonction return : (P_close-P_open)/P_open

def f(P):
    if len(P)==0:
        return 0
    return ((P[-1]-P[0])/P[0])

#remplissage de la colonne return:

i=0

for groupe in d_lim:
    chandelles.iloc[i,-1]=f(np.array(groupe[1]['price']))
    i+=1

#enregistrement du nouveau fichier
chandelles.to_csv('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Chandelles_Ether.csv')