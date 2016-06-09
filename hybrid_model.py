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
    ngram.append(len(tknzr.tokenize(ngram[0])))
    if ngram[2]-1 <8:
        outcome = ngram[1]/(math.log(avg_freg_ngram[ngram[2]-1]))
    else:
        outcome = ngram[1]/(math.log(avg_freg_ngram[8]))
    return [ngram[0], outcome]

def findkeys(word,grams,avg):
    possiblequeries = [[key,value] for key, value in grams.items() if word in key]
    possiblequeries = [freqnorm(possiblequery,avg) for possiblequery in possiblequeries]
    possiblequeries = sorted(possiblequeries, key=lambda x: int(x[1]), reverse=True)
    return possiblequeries

def sigmoid(x):
    return 1/(1+(x))

def vereken(phrase,long_word,long_char):
    x = phrase[1]
    y = len(phrase[0])
    z = len(tknzr.tokenize(phrase[0]))
    
    a = sigmoid(y/long_char)
    b = sigmoid(z/long_word)
    c = a*b*x
##    print(phrase, c)
    return c

def phraseGivenWord(word,grams,avg_freg_ngram):
    ngrams = [[key, value, len(tknzr.tokenize(key))] for key, value in grams.items() if word in key]
    ngrams_freqnorm = [freqnorm(ngram,avg_freg_ngram) for ngram in ngrams]
    sum_freq_norm = sum([freq_norm[1] for freq_norm in ngrams_freqnorm])
    final_outcome = [[freqnorm[0], freqnorm[1]/sum_freq_norm] for freqnorm in ngrams_freqnorm]
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
    
def phraseSelectionProbability(prefix,avg_freg_ngram,dt, list_of_dictionairies, grams):
    words = wordGivenPrefix(prefix,dt, list_of_dictionairies)
    phrases = [phraseGivenWord(word[0][0],grams,avg_freg_ngram) for word in words]
##    print(phrases[:10])
    phraseSelectionProbabilities = [[[sent[0],sent[1] *words[i][1]] for sent in phrases[i]] for i in range(len(words))]
    return phraseSelectionProbabilities

def phraseInDocument(phrase,list_of_dictionairies):
    sentence = tknzr.tokenize(phrase[0])
    occurenceInDocuments = [math.floor(sum([1 if word in dict else 0 for word in sentence])/len(sentence)) for dict in list_of_dictionairies for word in sentence]
    numberOfDocuments = sum(occurenceInDocuments)
    return(occurenceInDocuments, numberOfDocuments)
    
def overlap(list1, list2):
    outcome = sum([1 for i in range(len(list1)) if list1[i] == list2[i] if list1[i] == 1])
    return outcome

def phraseQueryCorrelation(query, phrases, list_of_dictionairies):
    phraseOccurence = [[phrase,phraseInDocument(phrase, list_of_dictionairies)] for phrase in phrases]
##    print(phraseOccurence[0][1][1])
    queryOccurence = phraseInDocument(query,list_of_dictionairies)
##    print(queryOccurence[1])
    overlapOccurence = [[phraseOccur[0],overlap(queryOccurence[0], phraseOccur[1][0])/phraseOccur[1][1]] if phraseOccur[1][1] > 0 else [phraseOccur[0],0] for phraseOccur in phraseOccurence]
    return overlapOccurence

def probabilisticModel(query, grams_anchor, grams_full, dt,avg_freg_ngram, list_of_dictionairies):
    words = tknzr.tokenize(query)
    length = len(words)
    if length == 1:
        keys = findkeys(query,grams_anchor,avg_freg_ngram)
        
        if len(keys) == 0:
            keys = findkeys(query,grams_full,avg_freg_ngram)
            if len(keys) <1:
                return [[],[]]
            final_outcome = keys
            long_word = max([len(tknzr.tokenize(x[0])) for x in final_outcome])
            long_char = max([len(x[0]) for x in final_outcome])
            final_outcome = [[phrase[0],vereken(phrase,long_word,long_char)] for phrase in final_outcome]
            final_outcome = sorted(final_outcome, key=itemgetter(1), reverse=True)
        else:
            final_outcome = keys
            if len(keys) <1:
                return [[],[]]
            long_word = max([len(tknzr.tokenize(x[0])) for x in final_outcome])
            long_char = max([len(x[0]) for x in final_outcome])
            final_outcome = [[phrase[0],vereken(phrase,long_word,long_char)] for phrase in final_outcome]
            final_outcome = sorted(final_outcome, key=itemgetter(1), reverse=True)
        return([final_outcome[:10], []])
    else:
        phraseSelectionProbabilities = phraseSelectionProbability(words[-1] ,avg_freg_ngram,dt, list_of_dictionairies, grams_anchor)
        if len(phraseSelectionProbabilities) == 0:
            return [[],[]]
        phraseSelectionProbabilities = [phrase[i] for phrase in phraseSelectionProbabilities for i in range(len(phrase))]
        final_outcome = sorted(phraseSelectionProbabilities, key=itemgetter(1), reverse=True)
        long_word = max([len(tknzr.tokenize(x[0])) for x in final_outcome])
        long_char = max([len(x[0]) for x in final_outcome])
        final_outcome = [[phrase[0],vereken(phrase,long_word,long_char)] for phrase in final_outcome]
        final_outcome = sorted(final_outcome, key=itemgetter(1), reverse=True)
    return final_outcome[:10], words[:-1]   

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

def getOutput(input, grams_anchor, grams_full, list_of_dictionairies):
    avg_freg_ngram = grams_anchor[1]
    grams_anchor = grams_anchor[0]
    grams_full = grams_full[0]
    dt = datrie.Trie(string.ascii_lowercase)
    for key, val in grams_anchor.items():
        dt[key] = val
    keys, words = probabilisticModel(input,grams_anchor, grams_full,dt,avg_freg_ngram, list_of_dictionairies)
    keys = [key[0] for key in keys]
    if len(words) > 0:
        keys = [' '.join(words) + ' ' + key for key in keys]        
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

