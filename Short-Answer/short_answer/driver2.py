import CosineDistance as cd
import keyword_score as key
import lsa_score as lsa
import infogain as ig
import csv, os, sys
import numpy

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


def main(stud_ans):
    c, r = 5, len(stud_ans)
    result = [[0 for x in range(c)] for y in range(r)]
    i = 0 
    for ans in stud_ans:
        result[i][0] = key.main(ans)
        result[i][1] = cd.main(ans)
        lsaresult = lsa.main(ans)
        result[i][2] = lsaresult[0]
        result[i][3] = lsaresult[1]
        result[i][4] = ig.main(ans)
        i = i + 1
    return result

def test_accuracy(result, scores):
    print "accuracy"
    acc = [0.0, 0.0, 0.0, 0.0, 0.0]
    n = len(result)
    for i in range(0, n):
        for j in range(0,5):
            if(scores[i] == result[i][j]):
                acc[j] = acc[j] + 1
                #print "+1"
    for j in range (0, 5):
        acc[j] = (acc[j]/n)*100
    return acc

if __name__ == "__main__":
    testdata = []
    scores = []
    with open("test.tsv") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            testdata.append(str(line[4]))
            scores.extend(line[2])
    #blockPrint()
    result = main(testdata)
    #enablePrint()
    #a = numpy.asarray(result)
    #numpy.savetxt("foo.csv", a, delimiter=",")
    for i in range(0, len(result)):
        print result[i][2], result[i][3], result[i][4]
    acc = test_accuracy(result, scores)
    print "accuracy"
    for num in acc:
        print num
