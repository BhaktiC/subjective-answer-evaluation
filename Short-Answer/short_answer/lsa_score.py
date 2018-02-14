
#!/usr/bin/env python
"""
Run k-NN classification on the Reuters text dataset using LSA.

This script leverages modules in scikit-learn for performing tf-idf and SVD.

Classification is performed using k-NN with k=5 (majority wins).

The script measures the accuracy of plain tf-idf as a baseline, then LSA to
show the improvement.

@author: Chris McCormick
"""

import time
import csv
import os.path
import read_data as rd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer


def main(stud_ans, train_ans):

    op = rd.read_data(train_ans)
    X_train_raw = op[0]
    y_train_labels = op[1]
    X_test_raw = []

    X_test_raw.extend(stud_ans)
    y_train = y_train_labels


    # pipeline = Pipeline([
    # ('tfidf', TfidfVectorizer(max_df=0.75, max_features=10000,
    #                          min_df=0.01, stop_words='english', ngram_range=(1, 1),
    #                          use_idf=True)),
    # ('trunc', TruncatedSVD(100)),
    # ('n', Normalizer(copy=False)),
    # ('knn', KNeighborsClassifier(n_neighbors=3, algorithm='brute', metric='cosine'))
    # ])
    # parameters = {
    # 'vect__max_df': (0.5, 0.75, 1.0),
    # 'vect__max_features': (None, 5000, 10000, 50000),
    # 'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    # 'tfidf__use_idf': (True, False),
    # 'tfidf__norm': ('l1', 'l2'),
    # 'clf__alpha': (0.00001, 0.000001),
    # 'clf__penalty': ('l2', 'elasticnet'),
    # 'clf__n_iter': (10, 50, 80),
    # }
###############################################################################
#  Use LSA to vectorize the articles.
###############################################################################

# Tfidf vectorizer:
#   - Filters out terms that occur in more than half of the docs (max_df=0.5)
#   - Filters out terms that occur in only one document (min_df=2).
#   - Selects the 10,000 most frequently occuring words in the corpus.
#   - Normalizes the vector (L2 norm of 1.0) to normalize the effect of
#     document length on the tf-idf values.
    vectorizer = TfidfVectorizer(max_df=0.75, max_features=10000,
                             min_df=0.01, stop_words='english', ngram_range=(1, 1),
                             use_idf=True)
    # vectorizer = CountVectorizer(max_df=0.5, min_df=0.01, ngram_range=(1, 1),
    #                                  max_features=10000,
    #                                  stop_words='english')

# Build the tfidf vectorizer from the training data ("fit"), and apply it
# ("transform").
    X_train_tfidf = vectorizer.fit_transform(X_train_raw)

    # print("  Actual number of tfidf features: %d" % X_train_tfidf.get_shape()[1])

    #print("\nPerforming dimensionality reduction using LSA")

# Project the tfidf vectors onto the first N principal components.
# Though this is significantly fewer features than the original tfidf vector,
# they are stronger features, and the accuracy is higher.
    svd = TruncatedSVD(100)
    lsa = make_pipeline(svd, Normalizer(copy=False))

# Run SVD on the training data, then project the training data.
    X_train_lsa = lsa.fit_transform(X_train_tfidf)


    #explained_variance = svd.explained_variance_ratio_.sum()
    #print("  Explained variance of the SVD step: {}%".format(int(explained_variance * 100)))


# Now apply the transformations to the test data as well.
    X_test_tfidf = vectorizer.transform(X_test_raw)
    X_test_lsa = lsa.transform(X_test_tfidf)


###############################################################################
#  Run classification of the test articles
###############################################################################

    #print("\nClassifying tfidf vectors...")


# Build a k-NN classifier. Use k = 5 (majority wins), the cosine distance,
# and brute-force calculation of distances.
    knn_tfidf = KNeighborsClassifier(n_neighbors=3, algorithm='brute', metric='cosine')
    knn_tfidf.fit(X_train_tfidf, y_train)
    p1 = []
    p2 = []
# Classify the test vectors.
    p1.extend(knn_tfidf.predict(X_test_tfidf))
    float(p1[0])
    print "answers tfidf", p1[0]


    #print("\nClassifying LSA vectors...")

# Build a k-NN classifier. Use k = 5 (majority wins), the cosine distance,
# and brute-force calculation of distances.
    knn_lsa = KNeighborsClassifier(n_neighbors=2, algorithm='brute', metric='cosine')
    knn_lsa.fit(X_train_lsa, y_train)

# Classify the test vectors.
    p2.extend(knn_lsa.predict(X_test_lsa))
    float(p2[0])
    print "answers lsa", p2[0]

    return (p1, p2)

if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main([stud_ans])
