#ref - https://stackoverflow.com/questions/46752650/information-gain-calculation-with-scikit-learn
#ref - https://stackoverflow.com/questions/43643278/how-do-i-selectkbest-using-mutual-information-from-a-mixture-of-discrete-and-con

from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest
import numpy as np
import csv, os, scipy
import operator
from sklearn.neighbors import KNeighborsClassifier


from sklearn.utils import check_X_y

class SelectKBestCustom(SelectKBest):

    # Changed here
    def fit(self, X, y, discrete_features='auto'):
        X, y = check_X_y(X, y, ['csr', 'csc'], multi_output=True)

        if not callable(self.score_func):
            raise TypeError("The score function should be a callable, %s (%s) "
                        "was passed."
                        % (self.score_func, type(self.score_func)))

        self._check_params(X, y)

        # Changed here also
        score_func_ret = self.score_func(X, y, discrete_features)
        if isinstance(score_func_ret, (list, tuple)):
            self.scores_, self.pvalues_ = score_func_ret
            self.pvalues_ = np.asarray(self.pvalues_)
        else:
            self.scores_ = score_func_ret
            self.pvalues_ = None

        self.scores_ = np.asarray(self.scores_)
        return self

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

def main(stud_ans):
    BASE = os.path.dirname(os.path.abspath(__file__))
    target = []
    data = []
    data.append(stud_ans)
    target.extend("0")
    with open(os.path.join(BASE, "train.tsv")) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            if line[1] != "5":
                break
            data.append(str(line[4]))
            target.extend(line[2])

    cv = CountVectorizer(max_df=1.0, min_df=2,
                                     max_features=10000,
                                     stop_words='english')
    X_vec = cv.fit_transform(data)
    #print X_vec.shape
    #mutual_info_classif(X_vec, target, discrete_features=True)
    X_new = SelectKBestCustom(mutual_info_classif, k=100).fit_transform(X_vec, target)
    #print X_new.shape
    X_test = X_new[0]
    delete_row_csr(X_new, 0)
    del target[0]
    knn = KNeighborsClassifier(n_neighbors=1, algorithm='brute', metric='cosine')
    knn.fit(X_new, target)

    p = []
    # Classify the test vectors.
    p.extend(knn.predict(X_test))
    float(p[0])
    print "infogain", p[0]
    return p[0]

   
if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main(stud_ans)
