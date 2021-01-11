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

tokenizer = RegexpTokenizer(r'\w+')
f = open("corpus", encoding="utf8")
file_content = f.read()
f.close()
f = open("corpus", encoding="utf8")

doc_id =[]
for line in f.readlines():
    if '<doc' in line:
        tmp = line.split('\"')
        doc_id.append([int(tmp[1]),tmp[1]])

raw= re.sub(r'<doc.*?>','&&&START&&&',file_content)
raw= re.sub(r'<.*?>','',raw)
raw = raw.split('&&&START&&&')
raw=list(filter(lambda x: x != "",raw))

main_dict={}
doc_counter=[]

for line in raw:
    tokenize = tokenizer.tokenize(line)
    tokenize = [w.lower() for w in tokenize ]
    tokenize = Counter(tokenize)
    doc_counter.append(tokenize)

# print(doc_counter[0]['ministry'],'\n')

cnt=0
for doc_dict in doc_counter:
	for local in doc_dict.keys():
		if(local in main_dict.keys()):
			main_dict[local].append((doc_id[cnt][0],doc_dict[local]))
		else:
			main_dict[local]=[]
			main_dict[local].append((doc_id[cnt][0],doc_dict[local]))
	cnt+=1
# print(main_dict['ministry'])

