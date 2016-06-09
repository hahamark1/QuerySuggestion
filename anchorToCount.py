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
    newsentence = [word for word in sentence if word not in stops]
    sentence = [sentence, len(newsentence)]
    return sentence


sentences = [preprocess(sentence) for sentence in sentences]

sentences = [sent[0] for sent in sentences if sent[1] >1 and sent[1] <5]

dictSentences = [' '.join(sentence) for sentence in sentences]

outcome = Counter(dictSentences)

print("final dict done")
pickle.dump(outcome,open('Anchor_Counter_v2.p',"wb" ),)

