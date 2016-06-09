import os
import sys
import json
from pprint import pprint
import pickle
from nltk.tokenize import TweetTokenizer
import re

file = open("stops.txt", "r")

stops = file.read()
file.close()

regex = re.compile('[^a-zA-Z]')
tknzr = TweetTokenizer()
queries = []
inputdir = 'M:\\UTCrawl\\Query Log\\local_utwente_log'
path=os.getcwd()
count =  0
first = os.path.join(path,"Query Log/local_utwente_log")
for file in os.listdir(inputdir):
    abs_file_path = os.path.join(first, file)
    f=open(abs_file_path, 'r')
    try:
        for line in f:
            count +=1

            line1 = line[1:-2]
####        print(line1)
            line1 = line1.split(',')
    ##        print(line1)
            if len(line1)> 2 and line1[-1][-2] == '"' and line1[1][9:-1] != "":
                queries.append(line1[1][9:-1])
    except UnicodeDecodeError:
        print(count)
            
print(len(queries))
def preprocess(sentence):
    sentence = sentence.lower()
    sentence = regex.sub(' ', sentence)
    sentence = tknzr.tokenize(sentence)
##    sentence = [word for word in sentence if word not in stops]
    sentence = ' '.join(sentence)
    return sentence

queries = [preprocess(query) for query in queries]

file = open("Query_Log_v_9.txt", "w")
for line in queries:
    file.write(line + "\n")
file.close()

##final_queries = []
##
##for line in queries:
##    sent = tknzr.tokenize(line)
##    if len(line) > 4 and len(sent) < 5 :
##        final_queries.append(line)
##
##
##pickle.dump(final_queries,open('Query_Log_v_7.p',"wb" ),)
##
##longline = []
##for line in queries:
##    line1 = line.split(" ")
##    if len(line1) > 2:
##        longline.append(line)
##        
##file = open("Lone_Query_Log_v_2.txt", "w")
##for line in longline:
##    file.write(line + "\n")
##file.close()
##
##
