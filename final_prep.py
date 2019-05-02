import pandas as pd
import numpy as np
from re import sub
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import RobustScaler

## Load/Format Data ##
years = '2005-2018'
data = pd.read_csv('Data/combined_busfin_' + years + '.csv', sep=';', index_col=False)

# set label to be 10-day-out performance
data['Label'] = data['prev10Day'].shift(-10)
data = data[:-10]

# split into train (2005-2016) and test (2017-2018)
split = 695+347+347+347+347+347+347+347
train = data[:split]
test = data[split:]
del data

# tokenize and tfidf 
vector = CountVectorizer(max_df=0.5)
tfidf = TfidfTransformer()

train_vec = vector.fit_transform(train['Text'])
train_tf = tfidf.fit_transform(train_vec)

test_vec = vector.transform(test['Text'])
test_tf = tfidf.transform(test_vec)

words = ['word:' + word for word in vector.get_feature_names()]

train_dense = train_tf.toarray()
test_dense = test_tf.toarray()

# extract date features
def add_datepart(df, fldname, drop=True, time=False):
    "Helper function that adds columns relevant to a date."
    fld = df[fldname]
    fld_dtype = fld.dtype
    if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        fld_dtype = np.datetime64
    targ_pre = sub('[Dd]ate$', '', fldname)
    attr = ['Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear', 'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    if time: attr = attr + ['Hour', 'Minute', 'Second']
    for n in attr: df[targ_pre + n] = getattr(fld.dt, n.lower())
    df[targ_pre + 'Elapsed'] = fld.astype(np.int64) // 10 ** 9
    if drop: df.drop(fldname, axis=1, inplace=True)

train['Date'] = train['Date'].astype('datetime64[D]')
add_datepart(train, 'Date')
test['Date'] = test['Date'].astype('datetime64[D]')
add_datepart(test, 'Date')


# recombine tfidf values with other data
train_y = np.array(train['Label'].values)
test_y = np.array(test['Label'].values)

temp_train = train.drop(['Label', 'Text'], axis=1)
train_x = np.append(train_dense, temp_train.values, axis=1)
temp_test = test.drop(['Label', 'Text'], axis=1)
test_x = np.append(test_dense, temp_test.values, axis=1)
feature_names = list(temp_train.columns)
feature_names.extend(words)

# scale features and labels to gaussian distribution
scaler = RobustScaler()
train_x = scaler.fit_transform(train_x)
test_x = scaler.transform(test_x)
train_y = scaler.fit_transform(train_y.reshape(-1, 1))
test_y = scaler.transform(test_y.reshape(-1, 1))

final_train = pd.DataFrame(train_x, columns=feature_names)
final_train['##Label##'] = train_y
final_train = final_train.astype('float16')
final_train.to_hdf('Data/final_busfin_train_' + years + '.h5', key='train')
final_test = pd.DataFrame(test_x, columns=feature_names)
final_test['##Label##'] = test_y
final_test = final_test.astype('float16')
final_test.to_hdf('Data/final_busfin_test_' + years + '.h5', key='test')
