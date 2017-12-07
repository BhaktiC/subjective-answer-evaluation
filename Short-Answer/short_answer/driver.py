import knn
import CosineDistance as cd
import keyword_score as key
import lsa_score as lsa
#Sample comment to understand branching in git
def main(stud_ans):
    keyresult = key.main(stud_ans)
    cdresult = cd.main(stud_ans)
    knnresult = knn.main(stud_ans)
    lsaresult = lsa.main(stud_ans)
    result = [keyresult, cdresult, knnresult]
    result.extend(lsaresult)
    print result
    return result

if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main(stud_ans)
