import CosineDistance as cd
import math
import csv

def get_closest_dist(vectors, scores):
    max = -1
    maxi = 0
    stud_vector = vectors[len(vectors)-1]
    for i in range(0,len(vectors)-1):
        vector = vectors[i]
        sim = cd.get_cosine_dist(vector, stud_vector)
        if sim > max:
            max = sim
            maxi = i
        if sim == 1:
            return i
    return maxi

def get_term_count(vectors):
    termcount = {}
    for vector in vectors:
        for term in vector:
            if term in termcount:
                termcount[term] = termcount[term] + 1
            else:
                termcount.update({term:1})
    return termcount

def generate_vector(sentence):
    vector = {}
    for w in sentence:
        if w not in vector:
            count = sentence.count(w)
            vector.update({w:count})
    return vector

def tfidf(vectors, termcount):
    m = len(vectors)
    for vector in vectors:
        n = len(vector)
        for term in vector:  
            tf = vector[term]
            idf = math.log(m/termcount[term])
            vector[term] = tf * idf
    return vectors


if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main(stud_ans)

def main(stud_ans):
    testdata = []
    scores = []
    with open("train2.csv") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            if line[1] != "5":
                break
            testdata.append(str(line[4]))
            scores.extend(line[2])
    vectors = []
    for data in testdata:
        model_ans = cd.remove_punctuation(data)
        word_tokens = cd.word_tokenize(model_ans)
        filtered_sentence = cd.remove_stopwords(word_tokens)
        stemmed_sentence = cd.autocorrect_and_stem(filtered_sentence)
        model_vector = cd.generate_vector(stemmed_sentence)
        vectors.append(model_vector)
    stud_ans = cd.remove_punctuation(stud_ans)
    word_tokens = cd.word_tokenize(stud_ans) 
    filtered_sentence = cd.remove_stopwords(word_tokens)
    stemmed_sentence = cd.autocorrect_and_stem(filtered_sentence)
    stud_vector = cd.generate_vector(stemmed_sentence) 
    vectors.append(stud_vector)
    termcount = get_term_count(vectors)
    vectors = tfidf(vectors, termcount)
    result = get_closest_dist(vectors, scores)
    print "TF-IDF matrix"
    print vectors[result]
    print "Result using knn"
    print scores[result]
    return float(scores[result])
    
    #print vectors[result], stud_vector

