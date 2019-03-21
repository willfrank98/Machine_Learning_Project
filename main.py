import pandas as pd
import gc
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

data = pd.read_csv("Data\combined_busfin_2000-2015.csv", sep=';')
# output = open("Data/graph_4_raw.txt", "w")
# output.write("T\tTrain\tTest\n")

train = data.iloc[0:2600]
test = data.drop(train.index)

vector = CountVectorizer()
tfidf = TfidfTransformer()
clf = Perceptron()

train_vec = vector.fit_transform(train['Headlines'])
train_tf = tfidf.fit_transform(train_vec)
clf = clf.fit(train_tf, train['LabelCategorical'])

test_vec = vector.transform(test['Headlines'])
test_tf = tfidf.transform(test_vec)

train_score = clf.score(train_tf, train['LabelCategorical'])
test_score = clf.score(test_tf, test['LabelCategorical'])

words = vector.get_feature_names()
coeffs = clf.coef_.tolist()[0]
coeffdf = pd.DataFrame({'Word' : words, 
                        'Coefficient' : coeffs})
coeffdf = coeffdf.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
print(str(coeffdf.head(10)))
print(str(coeffdf.tail(10)))