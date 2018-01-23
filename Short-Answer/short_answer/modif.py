import time
import csv
import os.path
import read_data as rd
from sklearn.feature_selection import mutual_info_classif, SelectKBest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import lil_matrix
import numpy as np
import operator, scipy

def main(stud_ans):

    op = rd.read_data("train.tsv")
    X_train_raw = op[0]
    y_train = op[1]
    X_test_raw = []
    X_test_raw.extend(stud_ans)

    cv = CountVectorizer(max_df=1.0, min_df=2,ngram_range=(1, 2),
                                     max_features=10000,
                                     stop_words='english')

    X_vec = cv.fit_transform(X_train_raw)
    selector = SelectKBest(mutual_info_classif, k=300)
    X_vec = selector.fit_transform(X_vec, y_train)
    Y_vec = cv.transform(X_test_raw)
    Y_vec = selector.transform(Y_vec)
    svd = TruncatedSVD(100)
    lsa = make_pipeline(svd, Normalizer(copy=False))

    print "shape", X_vec.shape, Y_vec.shape
    X_train_lsa = lsa.fit_transform(X_vec)
    X_test_lsa = lsa.transform(Y_vec)
    p = []
    knn_lsa = KNeighborsClassifier(n_neighbors=1, algorithm='brute', metric='cosine')
    knn_lsa.fit(X_train_lsa, y_train)
    p.extend(knn_lsa.predict(X_test_lsa))
    float(p[0])
    print "answers modified", p[0]

    return p

if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main([stud_ans])
