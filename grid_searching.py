import pandas as pd
import gc
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from pprint import pprint
from time import time

data = pd.read_csv("Data/combined_data_us2.csv")

pipeline = Pipeline([('vect', CountVectorizer(max_df=0.6, ngram_range=(1, 4), strip_accents='unicode')), 
                     ('tfidf', TfidfTransformer(norm='l2', sublinear_tf=False, use_idf=False)), 
                     ('clf', Perceptron(penalty='l2', alpha=0.0001, max_iter=25))
                    ])

parameters = {
    # 'vect__max_df': (0.59, 0.6, 0.61),
    # 'vect__strip_accents': ('ascii', 'unicode', None),
    # 'vect__max_features': (None),
    # 'vect__ngram_range': ((2, 5), (1, 4)),
    # 'tfidf__use_idf': (True, False),
    # 'tfidf__sublinear_tf': (True, False),
    # 'tfidf__norm': ('l1', 'l2', None),
    'clf__max_iter': (27, 30, 33),
    # 'clf__tol': (0.1, 0.01, 0.001),
    # 'clf__penalty': (None, 'l2', 'l1', 'elasticnet'),
    # 'clf__alpha': (0.001, 0.0001, 0.00001),
}

grid_search = GridSearchCV(pipeline, parameters, cv=5, n_jobs=-1, verbose=1)

print("Performing grid search...")
print("pipeline:", [name for name, _ in pipeline.steps])
print("parameters:")
pprint(parameters)
t0 = time()
grid_search.fit(data['Headlines'], data['Label'])
print("done in %0.3fs" % (time() - t0))
print()

print("Best score: %0.3f" % grid_search.best_score_)
print("Best parameters set:")
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]))