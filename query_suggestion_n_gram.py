import pickle
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re
from operator import itemgetter
from difflib import SequenceMatcher
import sys
import math
sys.setrecursionlimit(10000)

#first open pickles



##grams = pickle.load( open( 'n-gram-lijst-v-1.p', "rb

##create tokenizer
tknzr = TweetTokenizer()

##sentence1 = "hi I'm Mark"
##sentence2 = "Pingpong is an interesting thing"
##sentence3 = "hi what do you think of pingpong"
##
##sentences = [sentence1, sentence2, sentence3]

#preprocessing of data
def lengthNorm(count,len):
    count *= len/(len+1)
    return int(count)

#Set the threshold for a pair to enter set P.
threshold = 0.7

#Function to consider how many discs are the exact same.
def same():
    samediscs = []
    for i in range(477):
        for j in range(i+1, 477):
            if discs[i] == discs[j]:
                samediscs.append([i, j])
    return samediscs

#Function to determine longest string along splits.
def longest(s1, s2):
    if len(s2.split()) > len(s1.split()):
        x = s2
        s2 = s1
        s1 = x
    return s1, s2

#Function to determine if one string, represented as a set, is a subset of the other.
def subst(s1,s2):
    s1, s2 = longest(s1, s2)
    s1 = s1.split()
    s2 = s2.split()
    return int(set(s2).issubset(set(s1)))

#Function to determine similarity of two strings.
def similar(str1, str2):
    #Str1 will be the longest sentence along splits.
    str1, str2 = longest(str1, str2)
    #If the strings are nearly the same, retutn 1.
    if SequenceMatcher(None, str1, str2).ratio() > 0.8:
        return 1
    elif subst(str1, str2) == 1:
        return 1
    return SequenceMatcher(None, str1, str2).ratio()

def reform(queries, values):
    splitQueries = [query.split(' ') for query in queries]
    newValues = [lengthNorm(values[i],len(splitQueries[i])) for i in range(len(values))]
    return newValues

def freqnorm(ngram,avg_freg_ngram):
    ngram.append(len(tknzr.tokenize(ngram[0])))
    if ngram[2]-1 <8:
        outcome = ngram[1]/(math.log(avg_freg_ngram[ngram[2]-1]))
    else:
        outcome = ngram[1]/(math.log(avg_freg_ngram[8]))
    return [ngram[0], outcome]

def uniquelist(list1):
    print(len(list1))
    for word in list1:
        if newlist == []:
            newlist.append(word)
        elif max([similar(word, other) for other in newlist]) < threshold:
            newlist.append(word)
    print(len(newlist))
    return newlist


    
##def findallkeys(word):
##    possiblequeries = [[key,value] for key, value in grams.items() if word in key]
##    queries = [k for k,v in possiblequeries]
##    unique = uniquelist(queries)
##    possiblequeries = [[key,value] for key, value in possiblequeries if key in unique]
##    queries = [k for k,v in possiblequeries]
##    values = [v for k,v in possiblequeries]
##    values = reform(queries, values)
##    possiblequeries = [[queries[i],values[i]] for i in range(len(values))]
##    possiblequeries = sorted(possiblequeries, key=lambda x: int(x[1]), reverse=True)
##    queries = [k for k,v in possiblequeries]
##    unique = uniquelist(queries)
##    possiblequeries = [[key,value] for key, value in possiblequeries if key in unique]
##    print(possiblequeries[0:10])
##    if len(possiblequeries) < 10:
##        a = len(possiblequeries)
##    else:
##        a=10
##    if a ==0:
##        print("No possible completions found in the data set")
##        return
##    queries = [k for k,v in possiblequeries]
##    values = [v for k,v in possiblequeries]
##    i=0
##    while i <a:
##        print("Query " + str(i+1) + " = " + queries[i] )
##        print("total number of occurence: " + str(values[i]))
##        i+=1
##    return

def findkeys(word,grams,avg):
    possiblequeries = [[key,value] for key, value in grams.items() if word in key]
    possiblequeries = [freqnorm(possiblequery,avg) for possiblequery in possiblequeries]
    possiblequeries = sorted(possiblequeries, key=lambda x: int(x[1]), reverse=True)
    return possiblequeries[0:10]

def getOuput(input, grams, list_of_dictionairies):
    avg_freg_ngram = grams[1]    
    keys = findkeys(input,grams[0],avg_freg_ngram)
    keys = [key[0] for key in keys]
    return(keys)

    
def main():
    var = input("Please enter your query: ")
    print("The suggested queries for "+ var + " are: ")
    findallkeys(var)
    while True:
        rep = input("Do you want to do a new query? Y or N: ")
        if rep == "Y":
            main()
        elif rep == "N":
            return
        else:
            print("Please respond with Y or N")
