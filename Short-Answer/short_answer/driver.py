import lsa_score as lsa
import infogain as ig
import csv, os, sys
#Sample comment to understand branching in git

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


def main(stud_ans, train_file):
    lsa_res = []
    # blockPrint()
    ig_res = ig.main(stud_ans, train_file)
    res = lsa.main(stud_ans, train_file)
    lsa_res = res[1]
    enablePrint()
    print "LSA result is: "
    print lsa_res
    print "IG result is : "
    print ig_res
    return {"lsa": lsa_res, "ig":ig_res}


if __name__ == "__main__":
    train_file = raw_input("Enter train file ")
    stud_ans = raw_input("Enter answer: ")
    print stud_ans
    main([stud_ans], train_file)
