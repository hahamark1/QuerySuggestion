import os
import sys
import string
import nltk
import codecs
from bs4 import BeautifulSoup
import html2text
import time
import pickle
import re

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def getfromfile(file, subdirectory):
    html = open(subdirectory+ '\\'+ file, 'rb')
    soup = BeautifulSoup(html, "lxml")
    for m in soup.find_all('a'):
        m.replaceWithChildren()
##    print(soup)
    soup1 = soup
    html  = str(soup)
    soup = BeautifulSoup(html, "lxml")
    text = soup.findAll(text=True)
    text = [(line.lstrip()).rstrip() for line in text if visible(line) if line != '\n' if line != ' ']

    if text != '':
        return text

def main():
    t = time.time()
    inputdir = 'M:\\UTCrawl'
    subdirectories = [x[0] for x in os.walk(inputdir)]
    lijst = []
    for subdirectory in subdirectories:
    ##    while (time.time()-t <20):
            for filename in os.listdir(subdirectory):
##                    print(time.time()-t)
                    if filename.endswith('.html'):
##                            print(filename)
                            text = getfromfile(filename, subdirectory)
                            if text != None:
                                lijst.append(text)              
    pickle.dump(lijst,open('Final_Full_V7.p',"wb" ),)
main()
