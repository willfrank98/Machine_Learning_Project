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

data = pd.read_csv("Data/combined_data_us.csv")

pipeline = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer(use_idf=True)), ('clf', Perceptron())])
parameters = {
    'vect__max_df': (0.6, 0.7, 0.75),
    # 'vect__max_features': (None),
    'vect__ngram_range': ((2, 4), (1, 4)),
    # 'tfidf__use_idf': (True, False),
    # 'tfidf__norm': ('l1'),
    # 'clf__max_iter': (5, 50, 500),
    'clf__tol': (1e-3, 1e-4),
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