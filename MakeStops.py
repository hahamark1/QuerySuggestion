from nltk.corpus import stopwords

file = open("stops.txt", "w")

stopsEng = [word for word in stopwords.words('english')]
stopsGer = [word for word in stopwords.words('german')]
stopsDut = [word for word in stopwords.words('dutch')]
stopsFre = [word for word in stopwords.words('french')]

stops = stopsEng + stopsGer + stopsDut + stopsFre

for word in stops:
    file.write(word+ ' ')
    
file.close()
