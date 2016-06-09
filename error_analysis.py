from nltk.tokenize import TweetTokenizer
import pickle
from collections import Counter
tknzr = TweetTokenizer()
from stemming.porter2 import stem
from nltk.tokenize import TweetTokenizer

def main( text):
    tknzr = TweetTokenizer()

    filelength = 16

    count = 0
    whichLine = 0

    query = []
    input1 = []
    outcomes = []
    scores = []
    IBscores = []
    googleOutcome = []
    ngram_anchor = []
    ngram_full = []
    pm=[]
    pm1 = []
    pm2 = []
    hb = []
    bm = []

    outcome = []
    text = text.splitlines()
    newtext = []
    for line in text:
        list = line.split('/n')
        for line in list:
            newtext.append(line)
    newoutcome = []
    text = newtext
    for line in text:
    ##    print(line)
        newopen = False
        
        count+=1
        whichLine+=1
    ##    print(whichLine)
        if whichLine > filelength:
            whichLine = 1
            final_out = []
            newoutcome = []
            
            
        if whichLine ==1:
            query.append(line)
        elif whichLine ==2:
            input1.append(line)
        elif whichLine ==3:
    ##        print(line)
    ##        print(whichLine)
            newline = [(float(x)) for x in line.split(', ')]
            newline1 = [newline[0], newline[1], newline[3], newline[4]]
            scores.append(newline)
            if min(newline1) >0:
                newoutcome.append(1)
            if min([newline1[2],newline1[3]]) >0.2:
                newoutcome.append(8)
                   
            if newline1[0] >0.4 and sum(newline1[1:]) == 0:
                newoutcome.append(4)
            if sum(newline1) >0.5 and max(newline1)<0.2:
                newoutcome.append(6)
                print(newline1)
                                          
        elif whichLine ==4:
            IBscores.append([(float(x)) for x in line.split(', ')])
        elif whichLine ==5:
            googleOutcome.append(line.split(', '))
        elif whichLine ==6:
            if line == '':
                ngram_anchor.append('')
            else:
                ngram_anchor.append(line.split(', '))
    ##    elif whichLine ==7:
    ##        if line == '':
    ##            ngram_full.append('')
    ##        else:
    ##            ngram_full.append(line.split(', '))
        elif whichLine ==8:
            if line == '':
                pm2.append('')
            else:
                pm2.append(line.split(', '))
    ##    elif whichLine ==9:
    ##        if line == '':
    ##            pm.append('')
    ##        else:
    ##            pm.append(line.split(', '))
    ##    elif whichLine ==10:
    ##        if line == '':
    ##            pm1.append('')
    ##        else:
    ##            pm1.append(line.split(', '))
        elif whichLine ==11:
            if line == '':
                hb.append('')
            else:
                hb.append(line.split(', '))
        
    ##    elif whichLine ==12:
    ##        if line == '':
    ##            bm.append('')
    ##        else:
    ##            bm.append(line.split(', '))
        elif whichLine == 16:
            open_ans = []
            if len(pm2[-1]) ==0 and len(ngram_anchor[-1]) == 0:
                newoutcome.append(2)
                if 4 in newoutcome:
                    newoutcome.remove(4)
            if len(hb[-1]) == 0 and 6 not in newoutcome and 2 not in newoutcome:
                newoutcome.append(3)
                if 4 in newoutcome:
                    newoutcome.remove(4)
            if len(hb[-1]) == 0 and len(tknzr.tokenize(input1[-1])) ==1 and 3 not in newoutcome and 6 not in newoutcome and 2 not in newoutcome:
                if 4 in newoutcome:
                    newoutcome.remove(4)
                newoutcome.append(5)
            if scores[-1][3] <0.2 and [stem(word) for word in tknzr.tokenize(query[-1])] in [[stem(word) for word in tknzr.tokenize(hb1)] for hb1 in hb[-1]]:
                if 4 in newoutcome:
                    newoutcome.remove(4)
                newoutcome.append(5)
    ##        print(scores[-1][1:])
    ##        if sum(scores[-1][1:]) > 0 and max(scores[-1][1:]) < 0.3:
    ##            newoutcome.append(7)
            if len(newoutcome)==0:
    ##            print(len(newoutcome))
                newoutcome.append(7)
    ##            newopen = True
    ##            open_ans.append([query[-1], input1[-1], scores[-1], googleOutcome[-1], ngram_anchor[-1], ngram_full[-1], pm[-1], hb[-1], bm[-1]])
            final_out = newoutcome
            if newopen:
                final_out.append(10)
    ##            = input('What do you think of this sentence? Press 1-8')
            outcome.append([query[-1],input1[-1],final_out])


    ##for line in outcome:
    ##    print(line)
    ##print(len(outcome))
    ##print(len([x for x in outcome if 10 in x[2]]))
    pickle.dump(outcome,open('error_analysis.p',"wb" ),)
    out =[]
    for x in outcome:
        out.append(x[2][0])
    return sorted(Counter(out).items())
        

    

##    f = open('error_analysis_v2.txt', 'w')
##    for line in outcome:
##        if len(line[2]) == 1:
##            line = line[:2] + [str(line[2][0])]
##        else:
##            line = line[:2] + [str(line[2][0])] + [str(line[2][1])]
##        
##        f.write(', '.join(line))
##        f.write("\n")
##    f.close()


    
    
    
