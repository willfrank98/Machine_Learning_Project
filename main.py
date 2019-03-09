import pandas as pd
import gc
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

data = pd.read_csv("Data/combined_data_us.csv")


train = data.sample(frac=.8)
test = data.drop(train.index)

vectorizer = CountVectorizer(ngram_range=(1,1), max_df=0.9)
train_vt = vectorizer.fit_transform(train['Headlines'])

model = Perceptron(n_iter='1000', tol='1e-3')
model = model.fit(train_vt, train['Label'])

test_vt = vectorizer.transform(test['Headlines'])

train_score = model.score(train_vt, train['Label'])
test_score = model.score(test_vt, test['Label'])
print(train_score)
print(test_score)