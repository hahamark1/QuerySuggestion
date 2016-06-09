import pickle
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re
import nltk
sent_tokenize = nltk.data.load('tokenizers/punkt/english.pickle')
from operator import itemgetter
import itertools
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

#first open pickles
tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
regex = re.compile('[^a-zA-Z]')

sentences = pickle.load( open( "Final_Anchor_V7.p", "rb" ) )


print("sentences loaded")

sentences = [sent for sentence in sentences for sent in sentence]

print("sentences split")

#create tokenizer
tknzr = TweetTokenizer()

file = open("stops.txt", "r")

stops = file.read()
file.close()

def preprocess(sentence):
    sentence = sentence.lower()
    sentence = regex.sub(' ', sentence)
    sentence = tknzr.tokenize(sentence)
##    sentence = [word for word in sentence if word not in stops]

    return sentence

#make all n-grams
def unigrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    unidict = Counter(sentence)
    return unidict

def bigrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    if len(sentence) > 1:
        bigrams = [sentence[i] + " " + sentence[i+1] for i in range(len(sentence)-1)]
        bidict = Counter(bigrams)
        return bidict

def trigrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    if len(sentence) > 2:
        
        trigrams = [sentence[i] + " " + sentence[i+1] + " " + sentence[i+2] for i in range(len(sentence)-2)]
        tridict = Counter(trigrams)
        return tridict

def quadgrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    if len(sentence) > 3:
        quadgrams = [sentence[i] + " " + sentence[i+1] + " " + sentence[i+2] + " " + sentence[i+3] for i in range(len(sentence)-3)]
        quaddict = Counter(quadgrams)
        return quaddict

def fivegrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    if len(sentence) > 4:
        quadgrams = [sentence[i] + " " + sentence[i+1] + " " + sentence[i+2] + " " + sentence[i+3] + " " + sentence[i+4] for i in range(len(sentence)-4)]
        quaddict = Counter(quadgrams)
        return quaddict

def sixgrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    if len(sentence) > 5:
        quadgrams = [sentence[i] + " " + sentence[i+1] + " " + sentence[i+2] + " " + sentence[i+3] + " " + sentence[i+4] + " " + sentence[i+5] for i in range(len(sentence)-5)]
        quaddict = Counter(quadgrams)
        return quaddict

def sevengrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    if len(sentence) > 6:
        quadgrams = [sentence[i] + " " + sentence[i+1] + " " + sentence[i+2] + " " + sentence[i+3] + " " + sentence[i+4] + " " + sentence[i+5] + " " + sentence[i+6]  for i in range(len(sentence)-6)]
        quaddict = Counter(quadgrams)
        return quaddict

def eightgrams(sentence):
##    sentence = tknzr.tokenize(sentence)
    if len(sentence) > 7:
        quadgrams = [sentence[i] + " " + sentence[i+1] + " " + sentence[i+2] + " " + sentence[i+3] + " " + sentence[i+4] + " " + sentence[i+5] + " " + sentence[i+6] + " " + sentence[i+7] for i in range(len(sentence)-7)]
        quaddict = Counter(quadgrams)
        return quaddict
    
#first save all dicts in a list and afterwrds merge dicts with:

def mergedict(list):
    count = Counter()
    for y in list:
      count += Counter(y)
    return count

def concatlist(list):
    totaldict = dict()
    for x in totlist:
        totaldict.update(x)
    return totaldict

sentences = [preprocess(sentence) for sentence in sentences]

dictSentences = [' '.join(sentence) for sentence in sentences]

sentDict = Counter(dictSentences)

print("sentences preprocessed")

# produce the dictionaries with their count of different n-grams

unigrams = mergedict([unigrams(sentence) for sentence in sentences if unigrams(sentence) is not None])
print("unigrams made")
bigrams = mergedict([bigrams(sentence) for sentence in sentences if bigrams(sentence) is not None])
print("bigrams made")
trigrams = mergedict([trigrams(sentence) for sentence in sentences if trigrams(sentence) is not None])
print("trigrams made")
quadgrams = mergedict([quadgrams(sentence) for sentence in sentences if quadgrams(sentence) is not None])
print("quadgrams made")
fivegrams = mergedict([fivegrams(sentence) for sentence in sentences if fivegrams(sentence) is not None])
print("fivegrams made")
sixgrams = mergedict([sixgrams(sentence) for sentence in sentences if sixgrams(sentence) is not None])
print("sixgrams made")
sevengrams = mergedict([sevengrams(sentence) for sentence in sentences if sevengrams(sentence) is not None])
print("sevengrams made")
eightgrams = mergedict([eightgrams(sentence) for sentence in sentences if eightgrams(sentence) is not None])
print("eightgrams made")

totlist = [unigrams,bigrams,trigrams,quadgrams,fivegrams,sixgrams,sevengrams,eightgrams, sentDict]

overview = [sum(x.values())/len(x) for x in totlist]



to = concatlist(totlist)
print("final dict done")
pickle.dump([to,overview],open('Final_Anchor_Dict_V8_stops.p',"wb" ),)

def findallkeys(word):
    possiblequeries = [[key,value] for key, value in to.items() if word in key]

    possiblequeries = sorted(possiblequeries, key=itemgetter(1))
    if len(possiblequeries) < 10:
        a = 10-len(possiblequeries)
    else:
        a=10
    queries = [k for k,v in possiblequeries]
    i=0
    while i <a:
        print("Query " + str(i) + " = " + queries[i] + "\n")
        i+=1
    return

var = input("Please enter your query: ")
print("The suggested queries for "+ var + " are: \n")
findallkeys(var)
