import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras

## Load Data ##

train = pd.read_hdf('Data/final_busfin_train_2005-2018.h5', key='train', index_col=False)
test = pd.read_hdf('Data/final_busfin_test_2005-2018.h5', key='test', index_col=False)

train_y = train['##Label##']
train_x = train.drop('##Label##', axis=1)
test_y = test['##Label##']
test_x = test.drop('##Label##', axis=1)
feature_names = list(train_x.columns)

del train
del test

## Build NN ##

layers = [keras.layers.Dense(units=256, activation='relu', kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal(), input_dim=train_x.shape[1])]
layers.extend([keras.layers.Dense(units=128, activation='relu', kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal()) for _ in range(3)])
layers.append(keras.layers.Dense(units=1, kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal()))

model = keras.Sequential(layers)

model.compile(optimizer='adadelta', loss='mse')


## Train/Eval NN ##
   
for _ in range(10):
    model.fit(train_x.values, train_y.values, epochs=1)

    score = model.evaluate(test_x.values, test_y.values)

    predictions = model.predict(test_x.values)
    right = 0.0
    for i in range(len(predictions)):
        # pred_dict[str(predictions[i])] = True
        if predictions[i] >= 0 and test_y.values[i] >= 0:
            right += 1
        if predictions[i] < 0 and test_y.values[i] < 0:
            right += 1

    print(right/len(test_y))
