import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb

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

# split data into train and validation
train_x, valid_x, train_y, valid_y = train_test_split(train_x, train_y, test_size=0.2)


## LGBM ##

train_data = lgb.Dataset(train_x, train_y, feature_name=feature_names)
valid_data = lgb.Dataset(valid_x, valid_y, reference=train_data, feature_name=feature_names)

lgb_params = dict(
    objective = 'regression_l2',
    metric = ['l2', 'l1'],
    seed = 42
)

bst = lgb.train(lgb_params, train_data, 1000, valid_sets=[valid_data], early_stopping_rounds=50)

predictions = bst.predict(test_x, num_iteration=bst.best_iteration)
mse = (np.square(predictions - test_y)).mean(axis=None)
print(mse**0.5)
right = 0.0
# for i in range(len(predictions)):
#     # print(predictions[i], test_y[i])
#     if predictions[i] >= 0 and test_y.iloc[i] >= 0:
#         right += 1
#     if predictions[i] < 0 and test_y.iloc[i] < 0:
#         right += 1

# print(right/len(test_y))