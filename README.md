# QuerySuggestion

In the following paragraphs, the different files in this repository are explained, first the preprocessing files are shown, these are not of much use as the pickle files are in place. After, the models are given and finally the evaluation files are explained.

##Preprocessing

The following files contain all scripts that work on producing the pickle files needed to run the models. THese are create from the UTcrawl dataset consisting of HTML files

###htmlToAnchor.py
This file takes the html text and from this extracts all text in the anchors. It does this with the use of several toolboxes. _Beautiful soup_ extracts the anchors and nltk is used to split the data into sentences.

###htmlToText.py
This file takes the html text and from this extracts all text including the anchors. It does this with the use of several toolboxes. _Beautiful soup_ extracts the anchors and nltk is used to split the data into sentences.

###anchorToDict.py
This file takes the anchor text given by the htmlToAnchor.py file and for each sentence, it removes stopwords and non-alphabetical symbols. It then constructs all n-grams for n=1...8 and puts these with a set of all total sentences into a dictionary in which the occurrence of each phrase is counted. Included with this a list with the average count of the n-grams of the different lengths.

###fullToDict.py
This file takes the full text given by the htmlToTextpy file and for each sentence, it removes stopwords and non-alphabetical symbols. It then constructs all n-grams for n=1...8 and puts these with a set of all total sentences into a dictionary in which the occurrence of each phrase is counted. Included with this a list with the average count of the n-grams of the different lengths.

###MakeStops.py
Takes all stopwords in English, German and Dutch, the languages on the website of the UT, and puts these in a text containing all stopwords to use later.

###readQueryLog.py
Extracts the queries for the test set. Does this by taking the phrases from the json file and saves them in a text and pickle file for use as test set. It only takes phrase longer than 3 characters to be sure that the systems work and also does not ake sentences longer than 8 words, as these are not good queries to suggest.

##Models

Below all models will be explained. 

###query_suggestion_n_gram.py
This model produces the 10 suggestions for the n-gram model. Takes a set of n-grams as data. For a given input query, it finds all ngrams of which the input query is a substring. for these it calculates the real counter by dividing over the log of the average length of this n-gram. From this set the 10 highest probabilities are chosen and returned.

###probabilisticModelForQuerySuggestion.py
This model produces the 10 suggestions for the probabilistic model. It also takes the n-grams as data. From this first the input query is split into the first words and the final word. Then completions of this final word are found and th chance of this word given the final word is found. From this all phrase and their probability of occurrence are found. Finally these phrase and the first words of the input query are compared and a chance of them fitting in one sentence is found. These proabilities are all found and multiplied. Finally a length normalization is done aiming at short sentences.

###hybrid_model.py
In this file the suggestions for the hybrid model are generated. The system uses both the anchor and the full text as input. It now looks into the input query and from the length it decides which method to take. If the wordlength < 2 it takes the n-gram approach.
Else it takes the completion method of the probabilistic model. It however doesn't do the sentence phrase comparison. It returns the 10 best suggestions.

##Evaluation

###evaluationSystem.py

This is the main body of the program. It generates for all models and it uses Google's suggestion engine to generate reference suggestions. It then counts the scores to get the mean reciprocal rank. Finally it saves all output for later use.

###getScores.py
To generate all data for the final report, this files takes the data as input and from this it generates the coverage, the MRR and also plots these. 

###error_analysis.py
To finally see what errors occur in the output, this file takes all cases and looks into the different cases of errors.
These can be found in the file.

#Contact
If there are any questions concerning the programs, please contact the author: m.h.g.romme@student.utwente.nl

