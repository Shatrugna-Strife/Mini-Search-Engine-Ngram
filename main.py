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
f = open("wiki_06", encoding="utf8")
file_content = f.read()
f.close()
f = open("wiki_06", encoding="utf8")
doc_id =[]
for line in f.readlines():
    if '<doc' in line:
        tmp = line.split('\"')
        doc_id.append(int(tmp[1]))

raw= re.sub(r'<doc.*?>','&&&START&&&',file_content)
raw= re.sub(r'<.*?>','',raw)
raw = raw.split('&&&START&&&')
raw=list(filter(lambda x: x != "",raw))

doc_counter=[]

for line in raw:
    tokenize = tokenizer.tokenize(line)
    tokenize = [w.lower() for w in tokenize ]
    tokenize = Counter(tokenize)
    doc_counter.append(tokenize)

dict = {}
dict['the'] = [(1,2),(2,3)]

# for i 
