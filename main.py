import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import Perceptron

data = pd.read_csv("combined_data.csv")

train = data[data['Date'] < '2018-01-02']
test = data[data['Date'] > '2017-12-29']

vectorizer = CountVectorizer(ngram_range=(1,2))
basictrain = vectorizer.fit_transform(train['Headlines'])

basicmodel = Perceptron()
basicmodel = basicmodel.fit(basictrain, train['Label'])

basictest = vectorizer.transform(test['Headlines'])

score = basicmodel.score(basictest, test['Label'])
print(score)