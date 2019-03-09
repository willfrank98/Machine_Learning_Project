import pandas as pd
import gc
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC

data = pd.read_csv("Data/combined_data_us.csv")
output = open("Data/graph_3_raw.txt", "w")
output.write("T\tTrain\tTest\n")

avg = 20

#algs = [Perceptron(), SGDClassifier(), RandomForestClassifier(), AdaBoostClassifier(), SVC()]

#for T in range(1, 4):
tol_train_err = 0.
tol_test_err = 0.
for _ in range (0, avg):
    train = data.sample(frac=.8)
    test = data.drop(train.index)

    vectorizer = CountVectorizer(ngram_range=(1, 1), max_df=0.8)
    train_vt = vectorizer.fit_transform(train['Headlines'])

    model = Perceptron(max_iter=1000, tol=1e-3)
    model = model.fit(train_vt, train['Label'])

    test_vt = vectorizer.transform(test['Headlines'])

    train_score = model.score(train_vt, train['Label'])
    test_score = model.score(test_vt, test['Label'])
    tol_train_err += train_score
    tol_test_err += test_score

print("T" + "\t" + str(tol_train_err/avg) + "\t" + str(tol_test_err/avg) + "\n")
#print("done")