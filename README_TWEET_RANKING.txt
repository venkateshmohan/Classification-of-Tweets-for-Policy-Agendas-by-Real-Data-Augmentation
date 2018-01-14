Add all the topic file names in the code in


filenames=['topic18.txt,'......]     /*files present in tweet files folder*/     #add the training set file of the topics to find the real tweets

filtered_tweet_files=['clean_tweet18.txt',.....]  /*files present in tweet files folder*/           #the files containing the filtered tweets.

new_tweet_files=['topic18new.txt',.....]  /*files present in tweet files folder*/                   #(This files are initially empty after completion of code they Will contain the tweets in 
                                                        the descending order of rank


ranked_tweet_files=['ranked_file_topic18.json',......] /*files present in tweet files folder*/    #(These json files are initially empty after the code completes these files
                                                         Will contain the tweets along with rank.
														 
														 
The classifier code is svm1.py(provided to us by professor).
Same svm code is used for testing the accuracy after augmenting tweets.														 