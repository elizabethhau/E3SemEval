# create Features
# E3 Sem Eval
# Date Created: 12.12.15

from __future__ import division
import numpy as np
from afinn import Afinn
import ast
from sklearn import svm
from sklearn.metrics import accuracy_score


''' 
    - readFile reads in a file or a 2D array of shape [# tweets, # of tagged tuples]
    - tagged tuples: ('word', TAG)
'''
def readfile(filename):
    with open(filename, "r") as myfile:
        rawdata = myfile.readlines()
    data = [i.replace('\n','') for i in rawdata]
    return data
    #return np.loadtxt(filename)

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
        full_ft.append(afinn_ft(tweet))
    return full_ft
            
''' given 1 tweet (an array of tuples), return an array of 3 feature values.
    takes sum of sentiment scores within entire tweet.
    features are: 
        - af_pos: afinn > 1 (2,3,4)
        - af_neu: afinn [-1,1] (-1,0,1)
        - af_neg: afinn  < -1 (-2,-3,-4)
'''
def afinn_ft(tweet):
    score = 0
    ft = [0]*21
    #af_pos = 0
    #af_neu = 0
    #af_neg = 0
    for (word,tag) in tweet:
        score += af.score(word)
    #print "SCORE:", score
    
    if score < -10:
        score = -10
    elif score > 10:
        score = 10
    
    ft[int(score+10)] = 1
    
    #if score > 1:
    #    af_pos = 1
    #elif score >= -1 and score <= 1:
    #    af_neu = 1
    #else: 
    #    af_neg = 1
    return ft

def get_labels(filename):
    return np.loadtxt(filename, delimiter="\t", usecols=(2,))
    
#def label_distribution(labels):
    
#def svm_fit(ft_array):
#    classifier = svm.SVC(kernel='rbf', C=0.75) #gamma=0.7
#    classifier.fit(sample_ft, sample_labels)
#    #predict = classifier.predict(sample_ft)

if __name__ == "__main__":
    af = Afinn(emoticons=True)
    all_tweets = full_array(readfile('data/cleaned/PFTweetsCleaned.txt'))
    #print apply_ft(all_tweets[0])
    all_ft = apply_ft(all_tweets)
    print all_ft
    all_labels = get_labels('data/cleaned/PFTweets.txt')
    count = [0,0,0]
    for label in all_labels:
        count[int(label+1)] += 1
    print "distribution [-1,0,1]:",count
    
    #print "ALL LABELS:", all_labels
    classifier = svm.SVC(kernel='rbf', C=0.75) #gamma=0.7
    classifier.fit(all_ft, all_labels)
    predict = classifier.predict(all_ft)
    #print "PREDICT:", predict
    print accuracy_score(all_labels, predict) #get accuracy
    