#ref - https://stackoverflow.com/questions/46752650/information-gain-calculation-with-scikit-learn
#ref - https://stackoverflow.com/questions/43643278/how-do-i-selectkbest-using-mutual-information-from-a-mixture-of-discrete-and-con

from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from scipy.sparse import lil_matrix
import numpy as np
import read_data as rd
import csv, os, scipy
import operator
import nltk
from sklearn.neighbors import KNeighborsClassifier
from nltk.tokenize import word_tokenize
import string
import CosineDistance as cd
import lsa_score as lsa

from sklearn.utils import check_X_y

ps = nltk.stem.PorterStemmer()

def preprocessor(s):
    s = s.translate(string.punctuation)
    news = ""
    word_tokens = word_tokenize(s)
    cd.remove_stopwords(word_tokens)
    for word in word_tokens:
         news = news + " " + ps.stem(s)
    return news

def delete_row_csr(mat, i):
    if not isinstance(mat, scipy.sparse.csr_matrix):
        raise ValueError("works only for CSR format -- use .tocsr() first")
    n = mat.indptr[i+1] - mat.indptr[i]
    if n > 0:
        mat.data[mat.indptr[i]:-n] = mat.data[mat.indptr[i+1]:]
        mat.data = mat.data[:-n]
        mat.indices[mat.indptr[i]:-n] = mat.indices[mat.indptr[i+1]:]
        mat.indices = mat.indices[:-n]
    mat.indptr[i:-1] = mat.indptr[i+1:]
    mat.indptr[i:] -= n
    mat.indptr = mat.indptr[:-1]
    mat._shape = (mat._shape[0]-1, mat._shape[1])

def main(stud_ans, train_file):
    n = len(stud_ans)
    target = []
    data = []
    data.extend(stud_ans)
    for i in range(0,n):
        target.extend("4")
    op = rd.read_data(train_file)
    data.extend(op[0])
    data1 = []
    for ans in data:
        modif_ans = lsa.replace_with_syn(ans)
        data1.append(modif_ans)
    data = data1
    target.extend(op[1])
    cv = CountVectorizer(max_df=0.75, min_df=2,ngram_range=(1, 1),
                                     max_features=10000,
                                     stop_words='english',
                                     preprocessor=preprocessor)
    X_vec = cv.fit_transform(data)
    print X_vec.shape
    #mutual_info_classif(X_vec, target, discrete_features=True)
    selector = SelectKBest(mutual_info_classif, k=450)
    X_new = selector.fit_transform(X_vec, target)
    print X_new.shape
    q = X_new.shape[1]
    #X_new.get_support()
    #X_test = [[0 for x in range(m)] for y in range(n)]

    X_test = lil_matrix((n,q))  

    for i in range(0,n):
        X_test[i] = X_new[i]
    for i in range(0,n):
        delete_row_csr(X_new, 0)
        del target[0]
    knn = KNeighborsClassifier(n_neighbors=2, algorithm='brute', metric='cosine')
    knn.fit(X_new, target)
    #print X_test
    # Classify the test vectors.
    p = knn.predict(X_test)
    float(p[0])
    print "infogain", p[0]
    #print cv.vocabulary_
    return p


if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main([stud_ans], "train.tsv")
