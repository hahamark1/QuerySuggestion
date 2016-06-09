import pickle
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re
from operator import itemgetter
from difflib import SequenceMatcher
import sys
import datrie
import string
import math
from operator import itemgetter


#first open pickles

##grams = pickle.load( open( 'Final_Anchor_Dict_V7.p', "rb" ) )


##dt = datrie.Trie(string.ascii_lowercase)
##for key, val in grams.items():
##    dt[key] = val

##list_of_dictionairies = pickle.load( open( 'list_of_dics.p', "rb" ) )

#create tokenizer
tknzr = TweetTokenizer()

#preprocessing of data

def findCompletion(word,dt):
    newWords = dt.items(str(word))
##    newWords = sorted(newWords, key = lambda x: x[1], reverse = True)
    return newWords

def idf(word, doc_dict):
    i = 1
    for dic in doc_dict:
        if word in dic:
            i +=1
    x = len(doc_dict)/i
    outcome = math.log(1+x)
    return outcome

def vereken(phrase,long_word,long_char):
    x = phrase[1]
    y = len(phrase[0])
    z = len(tknzr.tokenize(phrase[0]))
    
    a = sigmoid(y/long_char)
    b = sigmoid(z/long_word)
    c = a*b*x
##    print(phrase, c)
    return c

def wordGivenPrefix(prefix,dt, list_of_dictionairies):
    words = findCompletion(prefix,dt)
    length = len(words)
    if length > 20:
        if length < 200:
            x = 20
        elif length >2000:
            x = 200
        else: x = round(length/10)
    else:
        x = length
    words = sorted(words, key=itemgetter(1), reverse=True)
    words = words[:x]
    scores = [[word[1],idf(word, list_of_dictionairies)] for word in words]
    total_scores = [score[0]*score[1] for score in scores]
    final_scores = [(score)/sum(total_scores) for score in total_scores]
    final_outcome = [[words[i], final_scores[i]] for i in range(len(words))]
    length = len(final_outcome)
    final_outcome = sorted(final_outcome, key=itemgetter(1), reverse=True)
    if length > 20:
        if length < 200:
            x = 20
        elif length >2000:
            x = 200
        else: x = round(length/10)
    else:
        x = length
    return final_outcome[:x]

def freqnorm(ngram,avg_freg_ngram):
    if ngram[2]-1 <8:
        outcome = ngram[1]/(math.log(avg_freg_ngram[ngram[2]-1]))
    else:
        outcome = ngram[1]/(math.log(avg_freg_ngram[8]))
    return [ngram[0], outcome]

def phraseGivenWord(word,grams,avg_freg_ngram):
    ngrams = [[key, value, len(tknzr.tokenize(key))] for key, value in grams.items() if word in key]
    ngrams_freqnorm = [freqnorm(ngram,avg_freg_ngram) for ngram in ngrams]
    sum_freq_norm = sum([freq_norm[1] for freq_norm in ngrams_freqnorm])
    final_outcome = [[freqnorm[0], freqnorm[1]/sum_freq_norm] for freqnorm in ngrams_freqnorm]
    length = len(final_outcome)
    long_word = max([len(tknzr.tokenize(x[0])) for x in final_outcome])
    long_char = max([len(x[0]) for x in final_outcome])
    final_outcome = [[final_outcome[i][0], vereken(final_outcome[i],long_word,long_char)] for i in range(len(final_outcome))]
    final_outcome = sorted(final_outcome, key=itemgetter(1), reverse=True)
    if length > 20:
        if length < 200:
            x = 20
        elif length >2000:
            x = 200
        else: x = round(length/10)
    else:
        x = length
    return final_outcome[:x]
    
def phraseSelectionProbability(prefix,avg_freg_ngram,dt, list_of_dictionairies, grams):
    words = wordGivenPrefix(prefix,dt, list_of_dictionairies)
    phrases = [phraseGivenWord(word[0][0],grams,avg_freg_ngram) for word in words]
##    print(phrases[:10])
    phraseSelectionProbabilities = [[[sent[0],sent[1] *words[i][1]] for sent in phrases[i]] for i in range(len(words))]
    return phraseSelectionProbabilities

def phraseInDocument(phrase,list_of_dictionairies):
    sentence = tknzr.tokenize(phrase)
    occurenceInDocuments = [math.floor(sum([1 if word in dict else 0 for word in sentence])/len(sentence)) for dict in list_of_dictionairies]
    numberOfDocuments = sum(occurenceInDocuments)
    return(occurenceInDocuments, numberOfDocuments)
    
def overlap(list1, list2):
    outcome = sum([1 for i in range(len(list1)) if list1[i] == list2[i] if list1[i] == 1])
    return outcome

def phraseQueryCorrelation(query, phrases, list_of_dictionairies):
    phraseOccurence = [[phrase,phraseInDocument(phrase, list_of_dictionairies)] for phrase in phrases]
    queryOccurence = phraseInDocument(query,list_of_dictionairies)
    overlapOccurence = [[phraseOccur[0],overlap(queryOccurence[0], phraseOccur[1][0])/phraseOccur[1][1]] if phraseOccur[1][1] > 0 else [phraseOccur[0],0] for phraseOccur in phraseOccurence]
    return overlapOccurence

def sigmoid(x):
    return 1/(1+(x))



def probabilisticModel(query, grams, dt,avg_freg_ngram, list_of_dictionairies): 
    words = tknzr.tokenize(query)
    phraseSelectionProbabilities = phraseSelectionProbability(words[-1] ,avg_freg_ngram,dt, list_of_dictionairies, grams)
    if len(phraseSelectionProbabilities) == 0:
        return [[],[]]
    phraseSelectionProbabilities = [phrase[i] for phrase in phraseSelectionProbabilities for i in range(len(phrase))]
    phrases = [phrase[0] for phrase in phraseSelectionProbabilities]
    if len(' '.join(words[:-1])) > 0:
        phraseQueryCorrelations = phraseQueryCorrelation((' '.join(words[:-1])), phrases, list_of_dictionairies)
        phraseProbability = [[(' '.join(words[:-1])+ ' ' + phraseQueryCorrelations[i][0]), (phraseQueryCorrelations[i][1]*phraseSelectionProbabilities[i][1])] for i in range(len(phraseQueryCorrelations))]
        final_outcome = sorted(phraseProbability, key=itemgetter(1), reverse=True)
        long_word = max([len(tknzr.tokenize(x[0])) for x in final_outcome])
        long_char = max([len(x[0]) for x in final_outcome])
        final_outcome = [[phrase[0],vereken(phrase,long_word,long_char)] for phrase in final_outcome]
        final_outcome = sorted(final_outcome, key=itemgetter(1), reverse=True)        
        return final_outcome[:10]
    else:
        
        phraseProbability = phraseSelectionProbabilities
        final_outcome = sorted(phraseProbability, key=itemgetter(1), reverse=True)
        long_word = max([len(tknzr.tokenize(x[0])) for x in final_outcome])
        long_char = max([len(x[0]) for x in final_outcome])
        final_outcome = [[phrase[0],vereken(phrase,long_word,long_char)] for phrase in final_outcome]
        final_outcome = sorted(final_outcome, key=itemgetter(1), reverse=True)       
        return final_outcome[:10]

        

def writeToScreen(var, outcomes):
    if len(outcomes) < 10:
        a = len(outcomes)
    else:
        a=10
    if a ==0:
        print("No possible completions found in the data set")
        return
    print("The suggested queries for "+ var + " are: ")
    i=0
    while i <a:
        print("Query " + str(i+1) + " = " + var + ' ' + outcomes[i][0] )
        print("The probability is: " + str(outcomes[i][1]))
        i+=1
    return

def getOuput(input, grams, list_of_dictionairies):
    avg_freg_ngram = grams[1]
    
    grams = grams[0]
    dt = datrie.Trie(string.ascii_lowercase)
    for key, val in grams.items():
        dt[key] = val
    keys = probabilisticModel(input,grams,dt,avg_freg_ngram, list_of_dictionairies)
##    print('keys v0')
##    print(keys)
    if len(keys[0]) == 0:
        return([])
    else:
        keys = [key[0] for key in keys]
        return(keys)


def main():
    var = input("Please enter your query: ") 
    
    outcomes = probabilisticModel(var)
    writeToScreen(' '.join(tknzr.tokenize(var)[:-1]), outcomes)
    
    while True:
        rep = input("Do you want to do a new query? Y or N: ")
        if rep == "Y":
            main()
        elif rep == "N":
            return
        else:
            print("Please respond with Y or N")

