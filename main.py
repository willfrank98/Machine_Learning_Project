import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

## Load/Format Data ##

data = pd.read_csv("Data/combined_busfin_1995-2018.csv", sep=';', index_col=False)

# remove data during subprime mortgage crisis
data.set_index('Date', inplace=True)
crisis = data[(data.index >= '2007-12-01') & (data.index <= '2009-06-31')]
data = data.drop(crisis.index)
data.reset_index(inplace=True)

# split train and test data
train = data.iloc[0:int(data.shape[0] * 0.9)]
test = data.drop(train.index)

# tokenize and tfidf 
vector = CountVectorizer(max_df=0.2)
tfidf = TfidfTransformer()

train_vec = vector.fit_transform(train['Text'])
train_tf = tfidf.fit_transform(train_vec)

test_vec = vector.transform(test['Text'])
test_tf = tfidf.transform(test_vec)

train_dense = train_tf.toarray()
test_dense = test_tf.toarray()

# extract date features
def add_datepart(df, fldname, drop=True, time=False):
    "Helper function that adds columns relevant to a date."
    fld = df[fldname]
    fld_dtype = fld.dtype
    if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        fld_dtype = np.datetime64
    targ_pre = re.sub('[Dd]ate$', '', fldname)
    attr = ['Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear', 'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    if time: attr = attr + ['Hour', 'Minute', 'Second']
    for n in attr: df[targ_pre + n] = getattr(fld.dt, n.lower())
    df[targ_pre + 'Elapsed'] = fld.astype(np.int64) // 10 ** 9
    if drop: df.drop(fldname, axis=1, inplace=True)

train['Date'] = train['Date'].astype('datetime64[D]')
test['Date'] = test['Date'].astype('datetime64[D]')
add_datepart(train, 'Date')
add_datepart(test, 'Date')

# re-concat rows from input
prev_days_train = [train[label].values[...,None] for label in train if label not in ['Date', 'Label', 'Text']]
prev_days_test = [test[label].values[...,None] for label in test if label not in ['Date', 'Label', 'Text']]

train_temp = [train_dense]
train_temp.extend(prev_days_train)
test_temp = [test_dense]
test_temp.extend(prev_days_test)

# build np.array inputs
train_x = np.concatenate(train_temp, axis=1)
test_x = np.concatenate(test_temp, axis=1)

train_y = np.array(train['Label'].values)
test_y = np.array(test['Label'].values)

# scale features and labels to gaussian distribution
scaler = StandardScaler()
train_x = scaler.fit_transform(train_x)
test_x = scaler.transform(test_x)

train_y = scaler.fit_transform(train_y.reshape(-1, 1))
test_y = scaler.transform(test_y.reshape(-1, 1))


## Build NN ##

layers = [keras.layers.Dense(units=128, activation='relu', kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal(), input_dim=train_x.shape[1])]
layers.extend([keras.layers.Dense(units=64, activation='relu', kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal()) for _ in range(3)])
layers.append(keras.layers.Dense(units=1, kernel_initializer=keras.initializers.TruncatedNormal(), bias_initializer=keras.initializers.TruncatedNormal()))

model = keras.Sequential(layers)

model.compile(optimizer='adadelta', loss='mse')


## Train/Eval NN ##
define accuracy(y_pred, y_true):
    right = sum([1 if y[predictions[i] >= 0 and test_y[i]]])
for _ in range(10):
    model.fit(train_x, train_y, epochs=1)

    score = model.evaluate(test_x, test_y)

    predictions = model.predict(test_x)
    pred_dict = {}
    right = 0.0
    for i in range(len(predictions)):
        pred_dict[str(predictions[i])] = True
        # print(predictions[i], test_y[i])
        if predictions[i] >= 0 and test_y[i] >= 0:
            right += 1
        if predictions[i] < 0 and test_y[i] < 0:
            right += 1

    print(right/len(test_y))
