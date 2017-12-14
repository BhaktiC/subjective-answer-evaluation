import CosineDistance as cd
import keyword_score as key
import lsa_score as lsa
import infogain as ig
import csv, os, sys
import time


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


def main(stud_ans):
    key_res = []
    cd_res = []
    tfidf_res = []
    lsa_res = []
    i = 0
    ig_res = ig.main(stud_ans)
    for ans in stud_ans:
        key_res.extend(str(key.main(ans)))
        cd_res.extend(str(cd.main(ans)))
        i = i + 1
    res = lsa.main(stud_ans)
    tfidf_res = res[0]
    lsa_res = res[1]
    return {"key":key_res, "cd":cd_res, "tfidf":tfidf_res, "lsa": lsa_res, "ig":ig_res}

def test_accuracy(result, scores):
    acc = {"key": 0.0, "cd": 0.0, "tfidf": 0.0, "lsa": 0.0, "ig":0.0}
    n = len(scores)
    for i in range(0, n):
        for key in result:
            if(scores[i] == result[key][i]):
                acc[key] = acc[key] + 1
    for key in acc:
        acc[key] = (acc[key]/n)*100
    return acc

if __name__ == "__main__":
    start = time.time()
    testdata = []
    scores = []
    with open("test.tsv") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            testdata.append(str(line[4]))
            scores.extend(line[2])
    blockPrint()
    result = main(testdata)
    enablePrint()
    acc = test_accuracy(result, scores)
    print "accuracy"
    for key in acc:
        print key, acc[key] 
    end = time.time()
    print end - start