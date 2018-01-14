
# -*- coding: utf-8 -*-
import os, sys
from sklearn.svm import *
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.metrics import precision_recall_fscore_support



import warnings
from sklearn.metrics import classification_report
warnings.filterwarnings("ignore")



def isAnscii(word):
    for elem in word:
        if ord(elem) >= 128 or ord(elem) < 48:
            return True
    return False
    
def deleteUnAnscii(sentence):
	tempList = []
	for elem in sentence.split():
		if not isAnscii(elem):
			tempList.append(elem)
	return " ".join(tempList)


def getFileNames(dir_path):        
    files = getFilesPath(dir_path)
    fileNames = []    
    for file in files:        
        file = os.path.split(file)[1]
        fileNames.append(file)
    return fileNames

def getFilesPath(dir_path):
    filesPath = []
    for parent, dirnames, filenames in os.walk(dir_path):    
        for filename in filenames[:]:                        
            full_filename =  os.path.join(parent, filename)
            filesPath.append(full_filename)
    return filesPath

def exit():
    sys.exit()


def getContent(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines    

def load_data(data_path):
    data_set = []
    label_set = []
    
    filenames = getFileNames(data_path)
        
    for filename in filenames:
        # print filename
        lines = getContent(os.path.join(data_path, filename))
        
        data_set += lines
        label_set += [filename[:-4]] * len(lines)
    
        
    data_set = [line.replace("\n", "") for line in data_set]      
    shortestword = 3
    longestword = 1200
    temp = []
    for line in data_set:
        line = deleteUnAnscii(line)
        line = " ".join([word for word in line.split() if longestword >= len(word) >= shortestword])
        temp.append(line)
    
    data_set[:] = temp[:]
    
    return data_set, label_set


def simple_svm():     
    # following two lines are for data set directory
    # you need adapt them to your data set directory
    train_path = 'train_data'    
    test_path = 'test_data'       
    
    
    train_set, train_label_set = load_data(train_path)    
    test_set, test_label_set = load_data(test_path)
    
    # print len(train_orgin_set)
    # print len(train_new_set)    
    
    
    X_train = train_set
    y_train = train_label_set
    
    X_test = test_set
    y_test = test_label_set
    
            
    ###########################################################################################################
    # following line is for mapping text to vector 
    # you can choose different value for each parameters
    # by choosing different parameters, you can do different gram, stop_words and so on...
    # please see the meaning for each parameters in details uisng following link
    # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
    
    vectorizer = TfidfVectorizer(stop_words='english', analyzer='word', ngram_range=(1,1), max_df=1.0, )
    train_text_matrix = vectorizer.fit_transform(X_train)
    train_text_target = y_train # just give label set a different name for my understanding 
    test_text_matrix = vectorizer.transform(X_test)
    test_text_target = y_test
    
    # print train_text_matrix.shape
    # print test_text_matrix.shape
    
    from sklearn.svm import SVC
    clf = SVC() # here you can choose different classifier in sklearn
    
    # here I just give an example to these parameters. It has infinite combinations. You can list more.
    param_grid = {                                                 
                    'C': [ 1, 10, 100, 1000],
                    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                    'gamma': [0.001, 0.01, 0.1, 1.0, 10],                        
                 }
    
    # for grid search, please check the online document for details
    grid_search = GridSearchCV(clf, param_grid, cv=10, n_jobs=-1, verbose=1, scoring='f1_weighted')#)
    
    grid_search.fit(train_text_matrix, train_text_target)          
    
    # print grid_search.best_params_    

    
    # up to now, get the best parameters
    best_gamma = grid_search.best_params_['gamma']
    best_C = grid_search.best_params_['C']
    best_kernel = grid_search.best_params_['kernel']

    
    # re build the model using best parameters
    
    clf = SVC(C = best_C, kernel = best_kernel, gamma = best_gamma,)
    clf.fit(train_text_matrix, train_text_target)
    result = clf.predict(test_text_matrix)
    
    
    # get accuracy
    accuracy = accuracy_score(test_text_target, result)
    print (accuracy)
    
    report = classification_report(test_text_target, result)
    print (report) 
    plt.classification_report(report)
    plt.savefig('test_plot_classif_report.png', dpi=200, format='png', bbox_inches='tight')
    plt.close()
    



    
if __name__ == '__main__':
	
    simple_svm()
    print ("\n\ndone...\n\n")
    
    
    

