

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math
import os
import random
import zipfile
import urllib.request
from bs4 import BeautifulSoup
from operator import itemgetter
from nltk.stem import PorterStemmer
import difflib
import numpy as np
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import re
nltk.download('wordnet')
from nltk import pos_tag
from nltk.corpus import wordnet as wn
import string
import operator
import json
from nltk.tokenize import word_tokenize, sent_tokenize
ps = PorterStemmer()
#import gensim
from collections import Counter

def text_process(text):
     nopunc = [char for char in text if char not in string.punctuation ]
     
     nopunc = ''.join(nopunc)
    
             
     
     
     return [word for word in nopunc.split() if word.lower() not in stopwords.words('english') ]

def remove_punc(text):
           text= ' '.join(text)
           rt=['tell','guess']
           for w in rt:
              return [w for w, pos in pos_tag(word_tokenize(text)) if not pos.startswith('V')]
           #[token for token, pos in pos_tag(word_tokenize(text)) if not pos.startswith('V')]
           
# =============================================================================
#         for w in text.split():
#             if w in wn.synsets(w).name():
#               tmp = wn.synsets(w)[0].pos()
#             
#          
#             if tmp =='v':
#               print(w,tmp)
#              
# =============================================================================
             
             
filenames=['topic18.txt']#include the training set file of the topics to find the real tweets
filtered_tweet_files=['clean_tweet18.txt']#the files containing the filtered tweets.
new_tweet_files=['topic18new.txt']#output: Will contain the tweets in the descending order of rank
ranked_tweet_files=['ranked_file_topic18.json']#output: Will contain the tweets along with rank in the descending order of rank
allfreq=[]#frequencies of all the top 30 words in all the files


#this will find the top 20 most frequent words in all the files and then find the associated word for each
#word and associate the frequency to it.
num=1
for name in filenames :
    f = open(name,"r")
    print("file----->",name)
    words1 = f.read()#.split()
    words1 = re.sub(r'[^\w]', ' ', words1)
    words1 = words1.lower()
    words = text_process(words1)
    words=remove_punc(words)
    wordfreq = {}
    for raw_word in words:
        word = raw_word
        if word not in wordfreq:
           wordfreq[word] = 0 
        wordfreq[word] += 1
    sorted_x = sorted(wordfreq.items(), key=operator.itemgetter(1))
    inv_map = list(reversed(sorted_x))
    i1 =1;
    freqmap ={}
    for tup in inv_map:
        
        if tup[0].lower()!='iowa' and tup[0].lower()!='rt' and tup[0].lower()!='bill' and tup[0]!='ialegis' and tup[0].lower()!='filed':
           freqmap[tup[0]]=tup[1]
           word = [tup[0]]
           
    
        associated_word = []
        print('---------',num)
        num=num+1
        for i in range(0, len(word)):
             if (word[i].lower() != 'iowa' and word[i].lower()!='rt' and word[i].lower()!='ialegis'):
                 try:
                   quote_page = 'https://wordassociations.net/en/words-associated-with/' + word[i] + '?button=Search'

                   page = urllib.request.urlopen(quote_page)
                   soup = BeautifulSoup(page, 'html.parser')
                   name_box = soup.find('div', attrs={'class': 'n-content-left'})
                   name = name_box.find('ul') # strip() is used to remove starting and trailing

            
                   try:
                     for li in name.findAll('li'):
                       associated_word.append(li.text.strip().lower())
                   except AttributeError:
                    pass
                 except UnicodeEncodeError:
                   pass
             for x in associated_word:
                 if x !='rt':
                  freqmap[x]=tup[1]
        if i1<30:
           i1=i1+1
        else:
          allfreq.append(freqmap)
          break;


rank=0
rnt =[]
rnt2=[]

# this will calculate the rank for each tweet and insert into the file.
for i in range(0,1):
          check_freq =allfreq[i] 
          newfile = open(filtered_tweet_files[i],"r")
          print("ranking",filenames[i])
          for line in newfile:
              newline = line.strip()
              rank=0
              nw=0
              matches=0
              if newline:
                  original_tweet = newline
       
                  newline = re.sub(r"http\S+", "", newline)
                  newline = re.sub(r'[^\w]', ' ', newline)
                  newline = re.sub(' +',' ',newline)
                  for wordinline in newline.split():
                      nw=nw+1
                      if wordinline.lower() in check_freq:
                         rank = rank + check_freq[wordinline.lower()]
                         matches = matches+1
               
                      else: 
                        if ps.stem(wordinline) in check_freq:
                             rank = rank+check_freq[ps.stem(wordinline)]
                             matches = matches+1
                   
        
                  if nw!=0 and matches!=0:
                    rnt.append((original_tweet,rank))
                    
          
                  else:
                     rnt.append((original_tweet,rank)) 
                     

          print(allfreq[0])    
          rnt = sorted(rnt,key=itemgetter(1),reverse=True)


          with open(new_tweet_files[i], 'w') as f1:
              for tup1 in rnt:
                  f1.write(tup1[0])
                  f1.write('\n')


          with open(ranked_tweet_files[i], 'w') as f:
              f.write(json.dumps(rnt, sort_keys=True, indent=4, separators=(',', ': ')))
   
    
    


