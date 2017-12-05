import knn
import CosineDistance as cd
import keyword_score as key

def main(stud_ans):
    keyresult = key.main(stud_ans)
    cdresult = cd.main(stud_ans)
    knnresult = knn.main(stud_ans)
    result = [keyresult, cdresult, knnresult]
    return result

if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main(stud_ans)

