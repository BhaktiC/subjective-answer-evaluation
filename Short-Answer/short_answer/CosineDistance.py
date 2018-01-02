#answer evaluation using cosine distance between model answer and student answer
import nltk
import string
import math
from autocorrect import spell
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

stop_words = set(stopwords.words('english'))
ps = nltk.stem.PorterStemmer()

def remove_punctuation(sentence):
    st = str(sentence)
    return st.translate(None, string.punctuation)

def get_magnitude(vector):
    mag = 0
    for key in vector:
        mag = mag + (vector[key] * vector[key])
    mag = math.sqrt(mag)
    return mag

def remove_stopwords(word_tokens):
    filtered_sentence = []
    for w in word_tokens:
        if w.lower() not in stop_words:
            filtered_sentence.append(spell(w))
    return filtered_sentence

def autocorrect_and_stem(sentence):
    stemmed_sentence = []
    for w in sentence:
        stemmed_sentence.append(ps.stem(w))
    return stemmed_sentence

def get_synonyms(word):
    synonyms = []
    stemmedword = ps.stem(word)
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if ps.stem(l.name()) != stemmedword:
                synonyms.append(l.name())
    return synonyms


def generate_vector(sentence):
    vector = {}
    for w in sentence:
        if w not in vector:
            count = sentence.count(w)
            vector.update({w:count})
    return vector

def synonym_merge(vector1, vector2):
    vector2cp = {}
    for key in vector2:
        vector2cp.update({key:vector2[key]})

    for key in vector1:
        stemmedkey = ps.stem(key)
        if stemmedkey in vector2:
			continue
        synonyms = get_synonyms(key)
        for sy in synonyms:
            stemmedsy = ps.stem(sy)
            if stemmedsy in vector2:
                print "%s is being replaced by %s" % (stemmedsy, stemmedkey)
                count = vector2[stemmedsy]
                vector2cp.update({stemmedkey:count})
                del vector2cp[stemmedsy]
                del vector2[stemmedsy]
    return vector2cp

def stem_vector(vector):
    vector1 = {}
    for key in vector:
        stemmedkey = ps.stem(key)
        vector1.update({stemmedkey:vector[key]})
    return vector1

def get_cosine_dist(vector1, vector2):
    prod = 0
    for key in vector1:
        if key in vector2:
            prod = prod + vector1[key]*vector2[key]
    mag1 = get_magnitude(vector1)
    mag2 = get_magnitude(vector2)
    try:
        return prod/(mag1*mag2)
    except ZeroDivisionError:
        return 0



def main(stud_ans):
    ques = "Starting with mRNA leaving the nucleus, list and describe four major steps involved in protein synthesis."
    model_ans = "After the mRNA leave the nucleus, there are four other major steps involved in protein synthesis. First, a tRNA attaches to the strand of mRNA. The first codon of nucleotide bases on the mRNA match the codon on the tRNA. The tRNA codes for an amino acid. Next, another tRNA connects to the next codon, bringing in another amino acid. The first tRNA floats away, leaving the amino acid behind. The amino acids bond. This continues, creating a strand of amino acids, until a stop codon is reached. Then the chain of amino acids is released."
    model_ans = remove_punctuation(model_ans)
    word_tokens = word_tokenize(model_ans)
    filtered_sentence = remove_stopwords(word_tokens)
    #stemmed_sentence = autocorrect_and_stem(filtered_sentence)
    stemmed_sentence = filtered_sentence
    model_vector = generate_vector(stemmed_sentence)
    stud_ans = remove_punctuation(stud_ans)
    word_tokens = word_tokenize(stud_ans)
    filtered_sentence = remove_stopwords(word_tokens)
    stemmed_sentence = autocorrect_and_stem(filtered_sentence)
    stud_vector = generate_vector(stemmed_sentence)
    stud_vector = synonym_merge(model_vector, stud_vector)
    model_vector = stem_vector(model_vector)
    result = get_cosine_dist(model_vector, stud_vector)
    print "TF vector of model answer"
    print model_vector
    print "TF vector of student answer"
    print stud_vector
    print "Result using Cosine Distance"
    result = round(result*3,0)
    print result
    return result

if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main(stud_ans)
