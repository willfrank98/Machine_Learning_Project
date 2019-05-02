import pandas as pd
import numpy as np
# import re
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
# from tensorflow import keras
import lightgbm as lgb

## Load Data ##

train = pd.read_hdf('Data/final_busfin_train_2010-2018.h5', key='train', index_col=False)
test = pd.read_hdf('Data/final_busfin_test_2010-2018.h5', key='test', index_col=False)

train_y = train['##Label##']
train_x = train.drop('##Label##', axis=1)
test_y = test['##Label##']
test_x = test.drop('##Label##', axis=1)
feature_names = list(train_x.columns)

# holdout_y = train.iloc[2009:]['##Label##']
# holdout_x = train.iloc[2009:].drop('##Label##', axis=1)

del train
del test

# split data into train and validation
train_x, valid_x, train_y, valid_y = train_test_split(train_x, train_y, test_size=0.2)


## LGBM ##

train_data = lgb.Dataset(train_x, train_y, feature_name=feature_names)
valid_data = lgb.Dataset(valid_x, valid_y, reference=train_data, feature_name=feature_names)

lgb_params = dict(
    objective = 'regression_l1',
    metric = ['mse'],
    seed = 42 # Change for better luck! :)
)

bst = lgb.train(lgb_params, train_data, 1000, valid_sets=[valid_data], early_stopping_rounds=50)

predictions = bst.predict(test_x)
# pred_dict = {}
right = 0.0
for i in range(len(predictions)):
    # pred_dict[str(predictions[i])] = True
    # print(predictions[i], test_y[i])
    if predictions[i] >= 0 and test_y.iloc[i] >= 0:
        right += 1
    if predictions[i] < 0 and test_y.iloc[i] < 0:
        right += 1

print(right/len(test_y))

## Build NN ##

# layers = [keras.layers.Dense(units=256, activation='relu', kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal(), input_dim=train_y.shape[1])]
# layers.extend([keras.layers.Dense(units=128, activation='relu', kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal()) for _ in range(3)])
# layers.append(keras.layers.Dense(units=1, kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal()))

# model = keras.Sequential(layers)

# model.compile(optimizer='adadelta', loss='mse')


# ## Train/Eval NN ##
   
# for _ in range(10):
#     model.fit(train_x, train_y, epochs=1)

#     score = model.evaluate(test_x, test_y)

#     predictions = model.predict(test_x)
#     # pred_dict = {}
#     right = 0.0
#     for i in range(len(predictions)):
#         # pred_dict[str(predictions[i])] = True
#         # print(predictions[i], test_y[i])
#         if predictions[i] >= 0 and test_y[i] >= 0:
#             right += 1
#         if predictions[i] < 0 and test_y[i] < 0:
#             right += 1

#     print(right/len(test_y))
