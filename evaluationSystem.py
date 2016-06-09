from nltk.tokenize import TweetTokenizer
import urllib
import webbrowser
import os
import pickle
import glob
import xlsxwriter
import re
import time
import codecs
import random
import query_suggestion_n_gram as qs
import requests
import collections
import benchmark as bm
import probabilisticModelForQuerySuggestion as pm
import probabilisticModelForQuerySuggestion_v1 as pm1
import probabilisticModelForQuerySuggestion_v3 as pm3
import hybrid_model as hs
##from selenium import webdriver
##chrome_options = webdriver.ChromeOptions()
##chrome_options.add_argument("--incognito")
##
##driver = webdriver.Chrome(chrome_options=chrome_options)
##driver.get('https://google.com')
workbook = xlsxwriter.Workbook('Outcomes_v_8.xlsx')

file_full = pickle.load( open( 'Final_Full_Dict_V8.p', "rb" ) )
listOfDics_full = pickle.load( open( 'list_of_dics_full_text.p', "rb" ) )
file_anchor = pickle.load( open( 'Final_Anchor_Dict_V8_stops.p', "rb" ) )
listOfDics_anchor = pickle.load( open( 'list_of_dics_anchor_text.p', "rb" ) )
anchors = pickle.load( open( 'Anchor_Counter_v2.p', "rb" ) )

    
numberOfOperations = 200
path = os.getcwd()
tknzr = TweetTokenizer()

# input is een query van de query log

def textToList(string):
    words = string.split(",")
    words = [string.strip('[]"') for string in words]
    return words

def query_suggestion_google(input):
##    url = driver.get("http://suggestqueries.google.com/complete/search?output=firefox&client=firefox&q=" + input)
    url = "http://suggestqueries.google.com/complete/search?output=firefox&client=firefox&q=" + input
    results = requests.get(url)
    output = results.json()[1]
    return output

def query_suggestion_ngram(input, file, listOfDics):
    output = qs.getOuput(input, file, listOfDics)
    return output

def query_suggestion_pm(input,file, listOfDics):
    output = pm.getOuput(input, file, listOfDics)
    return output

def query_suggestion_pm1(input,file, listOfDics):
    output = pm1.getOuput(input, file, listOfDics)
    return output

def query_suggestion_pm3(input,file, listOfDics):
    output = pm3.getOuput(input, file, listOfDics)
    return output

def getScores(input):
    print(input)
    length_query = len(input)
    words_query = tknzr.tokenize(input)
    length_words_query = len(words_query)
    maximal_length = length_query - 2
    if length_words_query > 1:
        minimal_length = len(words_query[0])
    elif len(words_query[0]) > 4:
        minimal_length = 2
    else:
        return (0,[],0,0,0,0,0,0,0,0,[],[],[],[],[],[],[],[],input)
    query_length = random.randint(minimal_length, maximal_length)
    input_query = input[:query_length]
    pm_outcomes_full = []
    
    newsystem_outcomes_full = query_suggestion_ngram(input_query, file_full,listOfDics_full)
    newsystem_outcomes_anchor = query_suggestion_ngram(input_query, file_anchor,listOfDics_anchor)
    google_outcomes = query_suggestion_google(input_query)
    pm_outcomes_anchor = query_suggestion_pm(input_query,file_anchor,listOfDics_anchor)
    pm_outcomes_anchor1 = query_suggestion_pm1(input_query,file_anchor,listOfDics_anchor)
    pm_outcomes_anchor3 = query_suggestion_pm3(input_query,file_anchor,listOfDics_anchor)
    hb_outcomes = hs.getOutput(input, file_anchor, file_full, listOfDics_anchor)
    bm_outcomes = bm.getOutput(input, anchors, file_anchor[1])
    if input in bm_outcomes:
        index = bm_outcomes.index(input)
        bm_score = 1/(index+1)
    else:
        bm_score = 0
    if input in newsystem_outcomes_full:
        index = newsystem_outcomes_full.index(input)
        newsystem_score_full = 1/(index+1)
    else:
        newsystem_score_full = 0
    if input in hb_outcomes:
        index = hb_outcomes.index(input)
        hb_outcomes_score = 1/(index+1)
    else:
        hb_outcomes_score = 0
    if input in newsystem_outcomes_anchor:
        index = newsystem_outcomes_anchor.index(input)
        newsystem_score_anchor = 1/(index+1)
    else:
        newsystem_score_anchor = 0
    if input in google_outcomes:
        index = google_outcomes.index(input)
        google_score = 1/(index+1)
    else:
        google_score = 0
    if input in pm_outcomes_full:
        index = pm_outcomes_full.index(input)
        pm_score_full = 1/(index+1)
    else:
        pm_score_full = 0
    if input in pm_outcomes_anchor:
        index = pm_outcomes_anchor.index(input)
        pm_score_anchor = 1/(index+1)
    else:
        pm_score_anchor = 0
    if input in pm_outcomes_anchor1:
        index = pm_outcomes_anchor1.index(input)
        pm_score_anchor1 = 1/(index+1)
    else:
        pm_score_anchor1 = 0
    if input in pm_outcomes_anchor3:
        index = pm_outcomes_anchor3.index(input)
        pm_score_anchor3 = 1/(index+1)
    else:
        pm_score_anchor3 = 0

    return (bm_score, bm_outcomes,hb_outcomes_score, newsystem_score_full, newsystem_score_anchor, google_score, pm_score_full, pm_score_anchor, pm_score_anchor1, pm_score_anchor3
            , newsystem_outcomes_full, newsystem_outcomes_anchor , google_outcomes, pm_outcomes_full, pm_outcomes_anchor, pm_outcomes_anchor1, pm_outcomes_anchor3
            ,hb_outcomes,input_query)

queries = pickle.load( open( "Query_Log_v_edit.p", "rb" ) )

numbers = random.sample(range(0, len(queries)-1), numberOfOperations)


random_queries = []
for number in numbers:
    random_queries.append(queries[number])

googleScore = 0 
ngramfullScore = 0
ngramanchorScore = 0
pmfullScore = 0
pmanchorScore = 0
pmanchor1Score = 0
pmanchor3Score = 0
hbScore=0
bmScore = 0

googleScoreIB = 0 
ngramfullScoreIB = 0
ngramanchorScoreIB = 0
pmfullScoreIB = 0
pmanchorScoreIB = 0
pmanchor1ScoreIB = 0
pmanchor3ScoreIB = 0
hbScoreIB = 0
bmScoreIB = 0

savefile = codecs.open('score_file_v16.txt', 'w', encoding='utf8')
worksheet = workbook.add_worksheet('Outcomes')
row = 0
operation = 0
for query in random_queries:
    t = time.time()
    row+=1
    col = 0
    operation += 1

    bm_score, bm_outcomes,hb_outcomes_score, newsystem_score_full, newsystem_score_anchor, google_score, pm_score_full, pm_score_anchor, pm_score_anchor1, pm_score_anchor3, newsystem_outcomes_full, newsystem_outcomes_anchor , google_outcomes, pm_outcomes_full, pm_outcomes_anchor, pm_outcomes_anchor1, pm_outcomes_anchor3,hb_outcomes,input = getScores(query)
##    worksheet.write(row,col, 'Query :')
##    col+=1
##    worksheet.write(row,col,input)
##    row +=1
##    col = 0
##    worksheet.write(row,col,'Test suggestion :')
##    col+=1
##    worksheet.write(row,col,query)
##    row +=2
##    col = 0
##    
##    worksheet.write(row,col,'Google output:')
##    for x in google_outcomes:
##        col +=1
##        worksheet.write(row,col, x)
##    row +=2
##    col = 0
##    worksheet.write(row,col,'n_gram_anchor output:')
##    for x in newsystem_outcomes_anchor:
##        col +=1
##        worksheet.write(row,col, x)
##    row +=2
##    col = 0
##    worksheet.write(row,col,'n_gram_full output:')
##    for x in newsystem_outcomes_full:
##        col +=1
##        worksheet.write(row,col, x)
##    row +=2
##    col = 0
##    worksheet.write(row,col,'pm_anchor output:')
##    for x in pm_outcomes_anchor:
##        col +=1
##        worksheet.write(row,col, x)
##    row +=2
##    col = 0
##    worksheet.write(row,col,'hb_system output:')
##    for x in hb_outcomes:
##        col +=1
##        worksheet.write(row,col, x)
##    worksheet.write(row,col,'bm_system output:')
##    for x in bm_outcomes:
##        col +=1
##        worksheet.write(row,col, x)
##
##
##    row +=2
##    col=0
##    worksheet.write(row,col,'Scores:')
##    col+=1
##    worksheet.write(row,col,'Google')
##    col+=1
##    worksheet.write(row,col,'n_gram')
##    col+=1
##    worksheet.write(row,col,'PM\hb system')
##    col+=1
##    worksheet.write(row,col,'bm system')
##    row+=1
##    col = 0
##    worksheet.write(row,col,'Anchor:')
##    col+=1
##    worksheet.write(row,col,google_score)
##    col+=1
##    worksheet.write(row,col,newsystem_score_anchor)
##    col+=1
##    worksheet.write(row,col,pm_score_anchor)
##    col+=1
##    worksheet.write(row,col,bm_score)
##    row+=1
##    col = 0
##    worksheet.write(row,col,'Full\hb system:')
##
##    col+=2
##    worksheet.write(row,col,newsystem_score_full)
##    col+=1
##    worksheet.write(row,col,hb_outcomes_score)

        
##    print(str(newsystem_outcomes) + ', ' + str(google_outcomes) + ', ' + str(pm_outcomes) + ', ' + str(score))
##    print(query, input)
##    save_file.write(query + ', ' + input + ', ' + str(newsystem_outcomes) + ', ' + str(google_outcomes) + ', ' + str(pm_outcomes) + ', ' + str(score))
##    print("query: " + query + " is done!")
    googleScore += google_score
    ngramfullScore += newsystem_score_full
    ngramanchorScore += newsystem_score_anchor
    pmfullScore += pm_score_full
    pmanchorScore += pm_score_anchor
    pmanchor1Score += pm_score_anchor1
    pmanchor3Score += pm_score_anchor3
    hbScore += hb_outcomes_score
    bmScore += bm_score
    
    
    googleScoreIB = googleScore/operation
    ngramfullScoreIB = ngramfullScore/operation
    ngramanchorScoreIB = ngramanchorScore/operation
    pmfullScoreIB = pmfullScore/operation
    pmanchorScoreIB = pmanchorScore/operation
    pmanchor1ScoreIB = pmanchor1Score/operation
    pmanchor3ScoreIB = pmanchor3Score/operation
    hbScoreIB = hbScore /operation
    bmScoreIB = bmScore / operation

##    row +=2
##    col=0
##    worksheet.write(row,col,'IBScores:')
##    col+=1
##    worksheet.write(row,col,'Google')
##    col+=1
##    worksheet.write(row,col,'n_gram')
##    col+=1
##    worksheet.write(row,col,'PM\hb system')
##    col+=1
##    worksheet.write(row,col,'bm system')
##    row+=1
##    col = 0
##    worksheet.write(row,col,'Anchor:')
##    col+=1
##    worksheet.write(row,col,googleScoreIB)
##    col+=1
##    worksheet.write(row,col,ngramanchorScoreIB)
##    col+=1
##    worksheet.write(row,col,pmanchorScoreIB)
##    col+=1
##    worksheet.write(row,col,bmScoreIB)
##    row+=1
##    col = 0
##    worksheet.write(row,col,'Full\hb system:')
##    col+=2
##    worksheet.write(row,col,ngramfullScoreIB)
##    col+=1
##    worksheet.write(row,col,hbScoreIB)

    scores = [google_score, newsystem_score_full, newsystem_score_anchor, hb_outcomes_score, pm_score_anchor, pm_score_anchor1, pm_score_anchor3, bm_score]
    scores = [str(x) for x in scores]
    scoresIB = [googleScoreIB, ngramfullScoreIB, ngramanchorScoreIB, hbScoreIB, pmanchorScoreIB, pmanchor1ScoreIB ,pmanchor3ScoreIB , bmScoreIB]
    scoresIB = [str(x) for x in scoresIB]
    savefile.write(query + "\n")
    savefile.write(input+ "\n")
    t = time.time() - t
    print(query, input)
    print("time = " ,t)
    print(", ".join(scores))
    print(", ".join(scoresIB))
##    print(", ".join(pm_outcomes_anchor))
##    print(", ".join(pm_outcomes_anchor1))
    savefile.write(", ".join(scores)+ "\n")
    savefile.write(", ".join(scoresIB)+ "\n")
    savefile.write(", ".join(google_outcomes)+ "\n")
    savefile.write(", ".join(newsystem_outcomes_anchor)+ "\n")

    savefile.write(", ".join(newsystem_outcomes_full)+ "\n")
    savefile.write(", ".join(pm_outcomes_anchor)+ "\n")
    savefile.write(", ".join(pm_outcomes_anchor1)+ "\n")
    savefile.write(", ".join(pm_outcomes_anchor3)+ "\n")
    savefile.write(", ".join(hb_outcomes)+ "\n")
    savefile.write(", ".join(bm_outcomes)+ "\n")
    savefile.write("New Query \n \n \n")
savefile.close()


workbook.close()


# guideline
# Query
# Input
# Scores
# Outcome Scores
# Google
# n-gram anchor
# n-gram full
# pm anchor with 2 length normalizations
# pm anchor with 1 length normalization
# pm anchor without normalization
# hybrid system
# benchmark system

# scores: Google - n-gram full - n-gram anchor - hybrid - pm anchor with 2 - pm anchor - pm anchor without with 1  - benchmark
    

    
