'''
Authors: Elizabeth Hau, Emily Ahn, Emily Chen
Date created: 12/12/2015
Last modified: 12/17/2015
*************************************************************
This file reads in training and testing files, creates feature arrays, and 
trains an SVM classifier to predict test tweets.
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
            
''' This function creates all the features for a given tweet.
    Given 1 tweet (an array of tuples), return an array of all feature values.
    Features are:
        - sentiment score (AFinn lexicon): 7 binary values
        - number of words in ALL CAPS: 6 binary values
        - emoticon score (AFinn Emoticon lexicon): 5 binary values
'''
def create_ft(tweet):
    # afinn score for each word
    score = 0
    afinn_ft = [0]*7 # initialize array of 0's
    
    # number of words in all caps
    num_all_caps = 0
    caps_ft = [0]*6
    
    # afinn emoticon scores
    emo_score = 0
    emo_ft = [0]*5 
    
    for (word,tag) in tweet:
        # word sentiments feature
        score += af_emo.score(word) #using the afinn score function
        
        # all caps feature
        if is_all_caps(word):
            num_all_caps += 1
        
        # emoticon feature
        if tag == 'E':
            emo_score += af_emo.score(word)
            
    #if sum of the afinn scores for the tweet is beyond -3 or 3 on either extreme, 
    # make them -3 or 3 respectively
    if score < -3:
        score = -3
    elif score > 3:
        score = 3
    afinn_ft[int(score+3)] = 1

    # if the number of words in all caps is more than 5, set it to 5
    if num_all_caps > 5:
        num_all_caps = 5
    caps_ft[int(num_all_caps)] = 1
    
    #if sum of the afinn emoticon scores are beyond -2 or 2 on either extreme, 
    # make them -2 or 2 respectively
    if emo_score < -2:
        emo_score = -2
    elif emo_score > 2:
        emo_score = 2
    emo_ft[int(emo_score+2)] = 1

    return afinn_ft + caps_ft + emo_ft

''' This function checks if a given word is in all caps
'''
def is_all_caps(word):
    def isCap(x) : return x.isupper()
    result = filter(isCap, word)
    return len(result) == len(word)
    
''' This function reads a file of tweets and returns the column of 
    correct labels as an array '''
def get_labels(filename):
    return np.loadtxt(filename, delimiter="\t", usecols=(2,))

if __name__ == "__main__":
    af = Afinn()
    af_emo = Afinn(emoticons=True)
    
    train_tweets = full_array(readfile('data/cleaned/PFTrainTag.txt'))
    train_ft = apply_ft(train_tweets)
    train_labels = get_labels('data/cleaned/PFTweetsTrain.txt')
    
    test_tweets = full_array(readfile('data/cleaned/PFTestTag.txt'))
    test_ft = apply_ft(test_tweets)
    test_labels = get_labels('data/cleaned/PFTweetsTest.txt')
    
    # count frequencies of train labels
    count0 = [0,0,0]
    for label in train_labels:
        count0[int(label+1)] += 1
    print "distribution in train[-1,0,1] :",count0
    total = np.sum(count0)
    print "% of 1s in train:",count0[2]/total #0.53053083768
    print "% of 0s in train:",count0[1]/total #0.305922061982
    print "% of -1s in train:",count0[0]/total #0.163547100338
    
    # count frequencies of test labels
    count = [0,0,0]
    for label in test_labels:
        count[int(label+1)] += 1
    print "\ndistribution in test[-1,0,1] :",count
    total = np.sum(count)
    print "% of 1s in test:",count[2]/total #0.458218549128
    print "% of 0s in test:",count[1]/total #0.341597796143
    print "% of -1s in test:",count[0]/total #0.200183654729

    classifier = svm.SVC(kernel='rbf', C=0.758) #gamma=0.7
    classifier.fit(train_ft, train_labels) # fit SVM on train data
    predict = classifier.predict(test_ft)
    print "\nPREDICT:", predict
    
    # count frequencies of predicted labels
    count2 = [0,0,0]
    for label in predict:
        count2[int(label+1)] += 1
    print "distribution in predicted[-1,0,1] :",count2
    total2 = np.sum(count2)
    print "% of 1s in predict:",count2[2]/total2 #0.904499540863
    print "% of 0s in predict:",count2[1]/total2 #0.0955004591368
    print "% of -1s in predict:",count2[0]/total2 #0.0
    
    # Baseline: 0.458218549128 (proportion of label = 1)
    # Accuracy with af score range [-10,10], all caps counting up to 6 words in all caps, no separate emo_ft: 0.474747474747
    # Accuracy with af score range [-5,5], same all caps, emo_ft range [-2, 2] using afinn emoticon scores: 0.481175390266
    # Accuracy with af score range [-3,3], same all caps, emo_ft range [-2, 2] using afinn emoticon scores: 0.483011937557
    print "\naccuracy score of our predictions:",accuracy_score(test_labels, predict) 
    
    # Compute confusion matrix
    cm = confusion_matrix(test_labels, predict)
    np.set_printoptions(precision=2)
    print('\nConfusion matrix, without normalization')
    print(cm)
    
    #[[  0  67 151]
    # [  0  60 312]
    # [  0  33 466]]

    percent_neg1_as_0 = cm[0][1]/np.sum(cm[0])
    print "Among all the -1 labels, % incorrectly classified as 0:",percent_neg1_as_0
    percent_neg1_as_1 = cm[0][2]/np.sum(cm[0])
    print "Among all the -1 labels, % incorrectly classified as 1:",percent_neg1_as_1
    percent_0_correct = cm[1][1]/np.sum(cm[1])
    print "Among all the 0 labels, % classified correctly:", percent_0_correct 
    percent_1_correct = cm[2][2]/np.sum(cm[2])
    print "Among all the 1 labels, % classified correctly:", percent_1_correct
    
    # Compute normalized confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print('\nNormalized confusion matrix')
    print(cm_normalized)
    # [[ 0.    0.31  0.69]
    #  [ 0.    0.16  0.84]
    #  [ 0.    0.07  0.93]]
