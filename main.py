import pandas as pd
import gc
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

data = pd.read_csv("Data/combined_data_us2.csv")
output = open("Data/graph_4_raw.txt", "w")
output.write("T\tTrain\tTest\n")

train = data.iloc[0:371]
test = data.drop(train.index)

vector = CountVectorizer(max_df=0.6, ngram_range=(1, 4), strip_accents='unicode')
tfidf = TfidfTransformer(norm='l2', sublinear_tf=False, use_idf=False)
clf = Perceptron(penalty='l2', alpha=0.0001, max_iter=25)

train_vec = vector.fit_transform(train['Headlines'])
train_tf = tfidf.fit_transform(train_vec)
clf = clf.fit(train_tf, train['Label'])

words = vector.get_feature_names()
coeffs = clf.coef_.tolist()[0]
coeffdf = pd.DataFrame({'Word' : words, 
                        'Coefficient' : coeffs})
coeffdf = coeffdf.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
print(str(coeffdf.head(10)))
print(str(coeffdf.tail(10)))

vectorizer = CountVectorizer(max_df=0.6, ngram_range=(1, 4), strip_accents='unicode')
train_vt = vectorizer.fit_transform(train['Headlines'])

model = Perceptron(max_iter=1000, tol=1e-3)
model = model.fit(train_vt, train['Label'])

test_vt = vectorizer.transform(test['Headlines'])

train_score = model.score(train_vt, train['Label'])
test_score = model.score(test_vt, test['Label'])
# tol_train_err += train_score
# tol_test_err += test_score

# print("T" + "\t" + str(tol_train_err/avg) + "\t" + str(tol_test_err/avg) + "\n")
#print("done")