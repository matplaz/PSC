import requests
import json
import pandas as pd
import numpy as np
import time
from datetime import date

#pair à charger
i=1 #choix de la paire
pairs=['XXBTZEUR','XETHZEUR']
pair=pairs[i]

#Chargement des opérations sur Kraken via l'API
def f(j=1):
    
    #paramètres
    current=time.time()
    
    
    #récupération du dernier id chargé
    file = open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/last_id_'+pair+'.txt',"r") 
    
    last_id= file.readlines()[0]
    
    file.close()
    
    #charger données déjà existantes
    dataset = pd.read_csv(open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/New_Data_'+pair+'.csv'), index_col=0)
    
    while(int(last_id)/10**9<current):#tant que l'on n'a pas toute les données jusqu'aujourd'hui
        #initialisation
        data=pd.DataFrame()
        try:
            while(True):#on ajoute les blocs de 1000 données un par un jusqu'à obtenir une exception
                url='https://api.kraken.com/0/public/Trades?pair='+pair+'&since='+last_id
                new_data=requests.get(url)
                last_id=new_data.json()['result']['last']
                data=data.append(new_data.json()['result']['XXBTZEUR'], ignore_index=True)
                print(last_id)
        except Exception: #on profite de l'exception pour enregistrer les données chargées et relancer le programme
            print()
            print(str(j)+" crash"+'\n')
            data.columns=['price', 'volume', 'time', 'buy/sell', 'market/limit', 'miscellaneous']
            dataset=dataset.append(data,ignore_index=True)
            dataset.to_csv('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/New_Data_'+pair+'.csv')
            file = open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/last_id_'+pair+'.txt',"w")
            file.write(last_id)
            file.close()
            time.sleep(j%30)
            f(j+1)
    
    print("The end")


def transfert():#transfert des données chargées depuis un certain temps vers le fichier contenant toutes les opérations
    
    dataset = pd.read_csv(open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/Data_'+pair+'.csv'), index_col=0)

    data_add = pd.read_csv(open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/New_Data_'+pair+'.csv'), index_col=0)
    
    
    
    dataset=dataset.append(form(data_add,dataset.shape[0]),ignore_index=True)
    
    data_add=pd.DataFrame(columns=['price', 'volume', 'time', 'buy/sell', 'market/limit', 'miscellaneous'])
    data_add.to_csv('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/New_Data_'+pair+'.csv')
    
    
    dataset.to_csv('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/Data_'+pair+'.csv')
    
    file = open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/last_id_'+pair+'.txt',"r") 
    last_id= file.readlines()[0]
    file.close()
    
    file = open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/previous_last_id_'+pair+'.txt',"w")
    file.write(last_id)
    file.close()


def form(dataset,decalage=0):
    data=pd.DataFrame(columns=['time','price','volume','buy','market','candle_24h','candle_4h','candle_1h','candle_15min','candle_1min','batch_id'])
    
    data[['time','price','volume','buy','market']]=dataset[['time','price','volume','buy/sell','market/limit']]
    data['candle_24h']=data['time'].apply(lambda x: int(x/(24*3600)))
    data['candle_4h']=data['time'].apply(lambda x: int(x/(4*3600)))
    data['candle_1h']=data['time'].apply(lambda x: int(x/(3600)))
    data['candle_15min']=data['time'].apply(lambda x: int(x/(15*60)))
    data['candle_1min']=data['time'].apply(lambda x: int(x/60))
    data['batch_id']=data.index.values
    data['batch_id']=data['batch_id'].apply(lambda x: int((x+decalage)/1000))

    return data


def formater():#met les données au format ['time','price','volume','buy','market','candle_24h','candle_4h','candle_1h','candle_15min','candle_1min','batch_id'] en vue de former les chandelles
    datest = pd.read_csv(open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/Data_'+pair+'.csv'), index_col=0)

    data=pd.DataFrame(columns=['time','price','volume','buy','market','candle_24h','candle_4h','candle_1h','candle_15min','candle_1min','batch_id'])
    
    data[['time','price','volume','buy','market']]=datest[['time','price','volume','buy/sell','market/limit']]
    data['candle_24h']=data['time'].apply(lambda x: int(x/(24*3600)))
    data['candle_4h']=data['time'].apply(lambda x: int(x/(4*3600)))
    data['candle_1h']=data['time'].apply(lambda x: int(x/(3600)))
    data['candle_15min']=data['time'].apply(lambda x: int(x/(15*60)))
    data['candle_1min']=data['time'].apply(lambda x: int(x/60))
    data['batch_id']=data.index.values
    data['batch_id']=data['batch_id'].apply(lambda x: int(x/1000))
    
    data.to_csv('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/Data_'+pair+'.csv')



def candel(x):#x:sélection de la chandelle [24,4,15,1]
    dataset = pd.read_csv(open('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/Data_'+pair+'.csv'), index_col=0) #import fichier csv brut
    
    if(x==24 or x==4 or x==1):
        can='candle_'+str(x)+'h'
        if x==24:
            ind=-6
        elif ind==4:
            ind=-5
        else:
            ind=-4
    else:
        can='candle_'+str(x)+'min'
        if x==15:
            ind=-3
        else:
            ind=-2
    
    
    df=dataset.iloc[:,[1,2,3,4,ind]] #crée un dataFrame à partir des collonees 'volume', 'market', 'price', 'candle_15min'
    
    
    chandelles=pd.DataFrame(columns=['nb','V','Pmin','PQ1','Pmed','PQ3','Pmax','P_open','P_close','return']) # nb : nombre d'opération, V:volume echange , Pmin,PQ1,Pmed,PQ3,Pmax:min, premier quartile, médiane, troisième quartile, max des prix des échanges d'ordre 'market', 'return':(P_close-P_open)/P_open, P_open : premier prix de la journée
    
    d_group=df.groupby(can)

    
    #Remplissage des colonnes
    
    chandelles['nb']=d_group['volume'].count()
    chandelles['V']=d_group['volume'].apply(lambda x: x.sum())
    chandelles['Pmin']=d_group['price'].apply(lambda x: x.min())
    chandelles['PQ1']=d_group['price'].apply(lambda x: x.quantile(0.25))
    chandelles['Pmed']=d_group['price'].apply(lambda x: x.quantile(0.5))
    chandelles['PQ3']=d_group['price'].apply(lambda x: x.quantile(0.75))
    chandelles['Pmax']=d_group['price'].apply(lambda x: x.max())
    chandelles['P_open']=d_group['price'].apply(lambda x: x.iloc[0])
    chandelles['P_close']=d_group['price'].apply(lambda x: x.iloc[-1])
    chandelles['return']=(chandelles['P_close']-chandelles['P_open'])/chandelles['P_open']
    
    
    
    #enregistrement du nouveau fichier
    chandelles.to_csv('C:/Users/antoine/Desktop/Polytechnique/Travail/2A/PSC/Données EY/Data_'+pair+'/Chandelles_'+pair+'_'+can+'.csv')