import re
from nltk.corpus import stopwords
import string
from collections import Counter
import urllib.request
from bs4 import BeautifulSoup
import json

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def readFile(path):
    tweet = []

    with open(path, 'r') as f:
        myNames = f.readlines()

    for i in range(0, len(myNames)):
        tweet.append(myNames[i].lower())
    return tweet

# removing stop word
def removeStopword(path):
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']

    gen_docs = []
    count_all = Counter()
    #
    for i in range(0, len(readFile(path))):
        term_stop = [term for term in preprocess(readFile(path)[i]) if term not in stop]
        gen_docs.append(term_stop)
        count_all.update(term_stop)
    return count_all

#read input file
topicPath = "train_data\\topic9.txt"
word = []
for key, value in removeStopword(topicPath).items():
    word.append(key)
threshold = int(0.05 * len(word))#Threshold for ranking word

#crawl associated word
def dictionary(keyword):
    associatedWordList = []
    if (keyword != 'iowa'):
        try:
            try:
                quote_page = 'https://wordassociations.net/en/words-associated-with/' + keyword + '?button=Search'

                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, 'html.parser')
                name_box = soup.find('div', attrs={'class': 'n-content-left'})
                name = name_box.find('ul')  # strip() is used to remove starting and trailing
                try:
                    for li in name.findAll('li'):
                        associatedWordList.append(li.text.strip().lower())
                except AttributeError:
                    pass
            except TimeoutError:
                pass
        except UnicodeEncodeError:
            pass
    return associatedWordList

#find topic-associated word list
def associatedWord(word):
    frequency = 0
    frequencyArray = []
    wordArray = []
    topicAssociatedWordList = []


    ##########################find intersected word#############################
    for i in range(0, len(word)):
        if (word[i] != 'iowa'):
            try:
                try:
                    # print(associated_word)
                    if (len(list(set(dictionary(word[i])) & set(word))) > 3):
                        # print(word[i])
                        # print(list(set(associated_word) & set(word)))
                        for j in range(0, len(list(set(dictionary(word[i])) & set(word)))):
                            frequency += removeStopword(topicPath)[list(set(dictionary(word[i])) & set(word))[j]]
                        if word[i].lower() not in dictionary(word[i]):
                            frequency += removeStopword(topicPath)[word[i]]
                        frequencyArray.append(frequency)
                        wordArray.append(word[i])
                        # if count >= 7:
                        print(word[i])
                        print(list(set(dictionary(word[i])) & set(word)))
                        print(frequency)
                        # threshold.append(count)
                        frequency = 0
                except AttributeError:
                    pass
            except UnicodeEncodeError:
                pass

    #######################order word in term of frequency##################################
    print("------------------------------------------------------------------------------")
    for i in range(0, len(wordArray)):
        for j in range(0, len(wordArray) - i - 1):
            if frequencyArray[j] > frequencyArray[j + 1]:
                frequencyArray[j], frequencyArray[j + 1] = frequencyArray[j + 1], frequencyArray[j]
                wordArray[j], wordArray[j + 1] = wordArray[j + 1], wordArray[j]
    for i in range(len(wordArray) - 1, len(wordArray) - threshold, -1):
        topicAssociatedWordList.append(wordArray[i])


    ###########################remove incorect word#####################################
    finalList = []
    removed_word = []

    for i in range(0, len(topicAssociatedWordList)):
        finalList.append(topicAssociatedWordList[i].lower().strip('\n'))
    for i in range(0, len(finalList)):
        if i > len(finalList) - 1:
            break
        for j in range(0, len(finalList)):
            if j > len(finalList) - 1:
                break
            if finalList[i] == finalList[j] and i != j:
                del finalList[i]
    i = 0
    while i <= len(finalList):
        if i > len(finalList) - 1:
            break

        #print(finalList[i])
        #print(list(set(dictionary(finalList[i])) & set(finalList)))
        if len(list(set(dictionary(finalList[i])) & set(finalList))) <= 2:
            print(finalList[i])
            removed_word.append(finalList[i])
        i = i + 1
    print('----------------------------------------')
    for i in range(0, len(removed_word)):
        finalList.remove(removed_word[i])
        # for i in range(0, len(finalList)):
        # print(finalList[i])
    print(finalList)
    return finalList

def tweet():
    finalListCopy = associatedWord(word).copy()
    data = []
    #read senator's tweets
    with open('data\data.json', 'r') as f:
        for line in f:
            if line[0] == "{":
                tweet = json.loads(line)  # load it as Python dict
                try:
                    data.append(tweet["text"])
                except KeyError:
                    pass

    text = []
    for i in range(0, len(data) - 1):
        text.append(preprocess(data[i].lower()))

    #write filter tweet
    filteredTweet = open("filterTweet\clean_tweet9.txt", "w")
    for i in range(0, len(text)):
        if len(list(set(text[i]) & set(finalListCopy))) > 0:
            try:
                filteredTweet.write(data[i])
                filteredTweet.write('\n')
                filteredTweet.write('-------------------\n')
            except UnicodeEncodeError:
                pass

if __name__ == '__main__':
    tweet()
