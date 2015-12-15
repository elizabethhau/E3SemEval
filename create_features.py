'''
Authors: Elizabeth Hau, Emily Ahn, Emily Chen
Date created: 12/12/2015
Last modified: 12/14/2015
*************************************************************
This file reads in training and testing files, creates feature arrays, and 
trains an SVM classifier to predict test tweets.

TODO:
    # create tagged files for PFTrainTag and PFTestTag
    # find limit to utility of ALL CAPS feature
    - new FT: presence of emoticons (use tagger an AFinn)
    # confusion matrices
    - documentation
    - write-up
*************************************************************
'''

from __future__ import division
import numpy as np
from afinn import Afinn
import ast
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

''' 
    - reads in a file or a 2D array of shape [# tweets, # of tagged tuples]
    - tagged tuples: ('word', TAG)
'''
def readfile(filename):
    with open(filename, "r") as myfile:
        rawdata = myfile.readlines()
    data = [i.replace('\n','') for i in rawdata]
    return data

''' This function takes in string versions of tagged tweets and returns them
    as a list of arrays of tuples
'''
def full_array(string_array):
    full_list = []
    for tweet in string_array:
        full_list.append(ast.literal_eval(tweet))
    return full_list
   
''' This function takes in a list of arrays of tuples and
    returns sample_features in the form [[f1, f2, f3], [f1, f2, f3],...]
''' 
def apply_ft(array):
    full_ft = []
    for tweet in array:
        full_ft.append(create_ft(tweet))
    return full_ft
            
''' given 1 tweet (an array of tuples), return an array of 21 feature values.
    takes sum of sentiment scores within entire tweet, and array at that sum 
    index + 10 gets a feature of 1.
    features are: 
        - array[0] --> -10
        - array[1] --> -9
        ...
        - array[20] --> 10
'''
def create_ft(tweet):
    score = 0
    afinn_ft = [0]*21 # initialize array of 0's
    
    num_all_caps = 0
    caps_ft = [0]*6
    
    for (word,tag) in tweet:
        score += af.score(word) #using the afinn score function
        if is_all_caps(word):
            num_all_caps += 1
            
    #if scores are beyond -10 or 10 on either extreme, make them -10 or 10 respectively
    if score < -10:
        score = -10
    elif score > 10:
        score = 10
    afinn_ft[int(score+10)] = 1

    if num_all_caps > 5:
        num_all_caps = 5
    caps_ft[int(num_all_caps)] = 1
    #print "CAPS FT:\n",caps_ft
    return afinn_ft+caps_ft

def is_all_caps(word):
    def isCap(x) : return x.isupper()
    result = filter(isCap, word)
    #if len(result) == len(word):
    #    print "ALL CAPS"
    #    return
    return len(result) == len(word)
    
''' read file of full tweets and grab the column of correct labels only '''
def get_labels(filename):
    return np.loadtxt(filename, delimiter="\t", usecols=(2,))

if __name__ == "__main__":
    af = Afinn(emoticons=True)
    
    train_tweets = full_array(readfile('data/cleaned/PFTrainTag.txt'))
    train_ft = apply_ft(train_tweets)
    train_labels = get_labels('data/cleaned/PFTweetsTrain.txt')
    
    test_tweets = full_array(readfile('data/cleaned/PFTestTag.txt'))
    test_ft = apply_ft(test_tweets)
    test_labels = get_labels('data/cleaned/PFTweetsTest.txt')
    
    # count frequencies of test labels
    count = [0,0,0]
    for label in test_labels:
        count[int(label+1)] += 1
    print "distribution in test[-1,0,1] :",count
    total = np.sum(count)
    print "% of 1s in test:",count[2]/total #0.458218549128
    print "% of 0s in test:",count[1]/total #0.341597796143
    print "% of -1s in test:",count[0]/total #0.200183654729
    
    #print "ALL LABELS:", all_labels
    classifier = svm.SVC(kernel='rbf', C=0.75) #gamma=0.7
    classifier.fit(train_ft, train_labels) # fit SVM on train data
    predict = classifier.predict(test_ft)
    print "PREDICT:", predict
    
    # count frequencies of predicted labels
    count2 = [0,0,0]
    for label in predict:
        count2[int(label+1)] += 1
    print "distribution in test[-1,0,1] :",count2
    total2 = np.sum(count2)
    print "% of 1s in predict:",count2[2]/total2 #0.904499540863
    print "% of 0s in predict:",count2[1]/total2 #0.0955004591368
    print "% of -1s in predict:",count2[0]/total2 #0.0
    
    print "accuracy score of our predictions:",accuracy_score(test_labels, predict) #get accuracy: 0.474747474747
    
    # Compute confusion matrix
    cm = confusion_matrix(test_labels, predict)
    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization')
    print(cm)
    # [[  0  40 178]
    #  [  0  41 331]
    #  [  0  23 476]]


    