import sys
import nltk
from nltk import word_tokenize
from nltk import ngrams
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import re
import csv
import math

with open('Inverted Index.csv', 'r', encoding = 'utf8') as csv_file:
    reader = csv.reader(csv_file)
    index = dict(reader)

for ele in index:
    tmp = index[ele][1:len(index[ele])-1]
    tmp = tmp.replace('(','')
    tmp = tmp.replace(')','')
    tmp = tmp.replace(' ','')
    tmp = tmp.split(",")
    index[ele] = []
    for i in range(0, len(tmp), 2):
        index[ele].append([int(tmp[i]), int(tmp[i+1])])


doc_id=[]
map_doc_id_to_number_of_doc={} #basically hashing a huge int to a small number to store in vector later
map_word_to_number_of_word={}	#basically hashing a word to a small number to store in vector later
doc_count=0
word_count=0

f=open('Document IDs.txt','r')
lines=f.readlines()

for line in lines:
	line=line.strip()
	doc_id.append(int(line))
	map_doc_id_to_number_of_doc[int(line)]=doc_count
	doc_count+=1



for word in index:
	map_word_to_number_of_word[word]=word_count
	word_count+=1

	
documents_as_vectors=[[0 for _ in range(int(doc_count))] for _ in range(word_count)]
        

def vectorizeDocuments():
    for word in index:
        for ele in index[word]:
            tf = ele[1]
            tf_wt = 1 + math.log10(tf)
            documents_as_vectors[map_word_to_number_of_word[word]][map_doc_id_to_number_of_doc[ele[0]]]=round(tf_wt, 3)



def cosine_generation():
    for i in range(doc_count):
        sum = 0
        for j in range(word_count):
            sum += documents_as_vectors[j][i] ** 2
        cos = 1/math.sqrt(sum)
        for j in range(word_count):
            documents_as_vectors[j][i] = round(documents_as_vectors[j][i] * cos, 3)

def evaluateQuery(str):
    array=str.split(' ')
    c=Counter(array)
    tmp = [0 for _ in range(word_count)]
    for key,value in c.items():
        tmp[map_word_to_number_of_word[key]]=1+math.log10(value)
        df=len(index[key])
        idf=math.log10(doc_count/df)
        tmp[map_word_to_number_of_word[key]]*=idf
    sum = 0
    for j in range(word_count):
        sum += tmp[j] ** 2
    cos = 1/math.sqrt(sum)
    for j in range(word_count):
        tmp[j]*=cos
    score = []
    for i in range(doc_count):
        sum=0
        for j in range(word_count):
            sum+=tmp[j]*documents_as_vectors[j][i]
        score.append([sum, doc_id[i]])
    score.sort(key = lambda x:x[0], reverse = True)
    return score[:10]



vectorizeDocuments()
cosine_generation()

Query = ["ministry of zambia", "Lowpel and Geowaltek Nigeria Limited founder", ]

def print_query_result(query):
    top_k = evaluateQuery(query.lowercase())
    print("Query".ljust(50 - len("Query"), ' '),end="")
    print("Top K Documents".ljust(50 - len("Top K Documents"), ' '),end="")
    print("Score".ljust(50 - len("Score"), ' '),end="")
    print("Is the document relevant to the query?".ljust(50 - len("Is the document relevant to the query?"), ' '),end="")
    print("\n",end="")
    for i in range(10):
        if i == 4:
            print(query.ljust(50 - len(query), ' '),end="")
        if i!=4:
            print("".ljust(50 - len(""), ' '),end="")
        print("Document ID: "+str(top_k[i][1]).ljust(50 - len("Document ID: "+str(top_k[i][1])), ' '),end="")
        print(str(top_k[i][0]).ljust(50 - len(str(top_k[i][0])), ' '),end="")
        print("\n",end="")

print_query_result("ministry of zambia")

