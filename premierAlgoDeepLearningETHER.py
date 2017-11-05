from __future__ import division
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


#input = cours des 50 dernieres chandelles
#output = cours de la prochaine chandelle
batch_x = []
batch_y = []
for i in range(50, (len(chandelles)-400)//2) :
    batch_x.append(chandelles[2*i-100:2*i])
    batch_y.append(chandelles[2*i])
test_x = []
test_labels = []
for i in range((len(chandelles)-400)//2, len(chandelles)//2) :
    test_x.append(chandelles[2*i-100:2*i])
    test_labels.append(chandelles[2*i])

#gestion du modele Keras
model = Sequential()
model.add(Dense(units=50, input_dim=100))
model.add(Activation('relu'))
model.add(Dense(units=1))
model.compile(optimizer="adam", loss="mean_squared_error")

#entrainenement
model.fit(batch_x, batch_y, epochs=1000, batch_size = 200)

#test
loss_and_metrics = model.evaluate(test_x, test_labels)
print("loss :",loss_and_metrics)

#save the model
model_json = model.to_json()
pathJson = pathPSC+"model.json"
with open(pathJson, "w") as json_file:
    json_file.write(model_json)
    
#save the weights
pathWeights = pathPSC + "model.h5"
model.save_weights(pathWeights)
print("Saved model to disk")


