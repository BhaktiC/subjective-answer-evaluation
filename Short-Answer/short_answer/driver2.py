import CosineDistance as cd
import keyword_score as key
import lsa_score as lsa
import infogain as ig
import modif
import csv, os, sys
import time
import read_data as rd
from numpy import std

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


def main(train_file, stud_ans):
    #key_res = []
    #cd_res = []
    tfidf_res = []
    lsa_res = []
    #i = 0
    ig_res = ig.main(stud_ans, train_file)
    #for ans in stud_ans:
    #    key_res.extend(str(key.main(ans)))
    #    cd_res.extend(str(cd.main(ans)))
    #    i = i + 1
    res = lsa.main(stud_ans, train_file)
    tfidf_res = res[0]
    lsa_res = res[1]
    n = len(ig_res)
    #return {"key":key_res, "cd":cd_res, "tfidf":tfidf_res, "lsa": lsa_res, "ig":ig_res}
    #return {"tfidf":tfidf_res, "lsa": lsa_res, "ig":ig_res, "modif":modif_res}
    result = [tfidf_res, lsa_res, ig_res]
    return result

def test_accuracy(result, scores, testdata):
    #acc = {"key": 0.0, "cd": 0.0, "tfidf": 0.0, "lsa": 0.0, "ig":0.0}
    #acc = {"tfidf": 0.0, "lsa": 0.0, "ig":0.0, "modif":0.0}
    acc = {"tfidf": 0.0, "lsa": 0.0, "ig":0.0}
    n = len(scores)
    err = []
    count = 0
    for i in range(0, n):
        for key in result:
            if key == "lsa":
                err.append(abs(int(scores[i])-int(result[key][i])))
            if scores[i] == result[key][i]:
                acc[key] = acc[key] + 1

    print "SD"
    print std(err)
    for key in acc:
        acc[key] = (acc[key]/n)*100

    return acc

if __name__ == "__main__":
    start = time.time()
    testdata = []
    scores = []
    op = rd.read_data("testans1.tsv")
    testdata = op[0]
    scores = op[1]
    blockPrint()
    result = main(testdata)
    enablePrint()
    acc = test_accuracy(result, scores, testdata)
    print "accuracy"
    for key in acc:
        print key, acc[key]
    end = time.time()
    #print end - start
