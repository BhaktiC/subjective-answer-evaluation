import lsa_score as lsa
import infogain as ig
import csv, os, sys
#Sample comment to understand branching in git

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


def main(stud_ans):
    train_file = "trainans1.tsv"
    lsa_res = []
    blockPrint()
    ig_res = ig.main(stud_ans, train_file)
    res = lsa.main(stud_ans, train_file)
    lsa_res = res[1]
    enablePrint()
    print "IG result is : "
    print ig_res
    print "LSA result is: "
    print lsa_res

if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main([stud_ans])
