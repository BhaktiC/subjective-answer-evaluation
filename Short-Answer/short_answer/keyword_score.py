from __future__ import division
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import CosineDistance as cs


def main(s):
    stop_words=set(stopwords.words("english"))
    t=" After the mRNA leave the nucleus, there are four other major steps involved in protein synthesis. First, a tRNA attaches to the strand of mRNA. The first codon of nucleotide bases on the mRNA match the codon on the tRNA. The tRNA codes for an amino acid. Next, another tRNA connects to the next codon, bringing in another amino acid. The first tRNA floats away, leaving the amino acid behind. The amino acids bond. This continues, creating a strand of amino acids, until a stop codon is reached. Then the chain of amino acids is released"
    t = cs.remove_punctuation(t)
    s = cs.remove_punctuation(s)
    t_words = word_tokenize(t)
    s_words = word_tokenize(s)

    t_filtered = cs.remove_stopwords(t_words)
    t_filtered = cs.autocorrect_and_stem(t_filtered)
    s_filtered = cs.remove_stopwords(s_words)
    s_filtered = cs.autocorrect_and_stem(s_filtered)


    #print "Keywords of Teacher's answer"     
    #print t_filtered
    #print "Keywords of Student's answer"
    #print s_filtered


    list_t1 = []
    c = 0
    for word in s_filtered:
        if word.lower() in t_filtered:
            c = c + 1
            
            
    #print "Final Score"
    c1 = c/len(t_filtered)
    #print "keyword", round(c1 * 3)
    return round(c1 * 3)



if __name__ == "__main__":
    stud_ans = raw_input("Enter answer: ")
    main(stud_ans)


