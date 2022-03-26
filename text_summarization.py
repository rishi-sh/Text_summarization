

import spacy
from spacy.lang.en.stop_words import STOP_WORDS 
from string import punctuation
import warnings
warnings.filterwarnings('ignore')

f = open('brown.txt','r',errors='ignore')
text = f.read()

stopwords = list(STOP_WORDS)
#print(stopwords)

nlp = spacy.load('en_core_web_sm')#en_core_web_sm is from the english lib used for lemmatization process

doc = nlp(text)

tokens = [token.text for token in doc]
#print(tokens)

#print(punctuation)

#finding the frequency of the word
word_frequencies = {}
for word in doc:
    if word.text.lower() not in stopwords: #take those not in stopwords
        if word.text.lower() not in punctuation:#take those which are not in punctuation
             if word.text not in word_frequencies.keys():
                  word_frequencies[word.text]=1 # if the word in new or rare append it
             else:
                    word_frequencies[word.text] += 1
                
                           
#print(word_frequencies)            

#to find the num pf frequency of word in the text
max_frequency  = max(word_frequencies.values())
#print(max_frequency)


# now we perform normalization
# As we know in a corpus we have diff words with diff lenghts so to align them in a range or a scale
#in a range of 0 to 1
for  word in word_frequencies.keys():
    word_frequencies[word] =  word_frequencies[word]/max_frequency
    
#print(word_frequencies) 


#as per now we have done the preprossing on the words and removed 
#all the unwanted things
#now from the preprossed words we will create sentence   
sentence_tokens=[sent for sent in doc.sents]
#print(sentence_tokens)


#here we will count the scores for the sentence
sentence_scores={}
for sent in sentence_tokens: #above new corpus we made
    for word in sent: #from sent_tokens we take a  sentence 
        if word.text.lower() in word_frequencies.keys(): #from each word in the particular sent we are converting it to lower
            
            if sent not in sentence_scores.keys():# if sentence not there in  sent keys
                 sentence_scores[sent] = word_frequencies[word.text.lower()] # then sentence will append  which is done using word_frequencies,from word we built sentence
            else:
                 sentence_scores[sent] += word_frequencies[word.text.lower()]
           
            
#print(sentence_scores)

 # to summarize we create a certain rules
 #every corpus cannot have same set of rule
 #here i
 # obtain 30% of sentence with maximum score and is done by heapq
 # if you want to have more summary keep the percentage value low
 #with the  maximum score from sentence score i will weight the sentence from the corpus
 
 

#Heap queue is a special tree structure in which each parent node is less than or equal to its child node.
# In python it is implemented using the heapq module.
from heapq import nlargest

select_lenght = int(len(sentence_tokens)*0.3)
#print(select_lenght)
#for my corpus the output is 15 
#which means there are 15 sentence matching with more than 30%

summary = nlargest(select_lenght,sentence_scores,key=sentence_scores.get)
#print(summary) #here the summary is in a list

final_summary = [word.text for word in summary]
summary = ''.join(final_summary)
print(summary)


#checking the lenght of the orignal text vs summary
print(len(text))
print(len(summary))