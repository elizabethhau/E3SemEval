# create Features
# E3 Sem Eval
# Date Created: 12.12.15

import numpy as np
from __future__ import division
from afinn import Afinn
af = Afinn()

''' 
    - readFile reads in a file or a 2D array of shape [# tweets, # of tagged tuples]
    - tagged tuples: ('word', TAG)
'''
def readFile(filename):
    #with open(fileName, "r") as myfile:
    #    rawdata = myfile.readlines()
    #data = [i.replace('\n','').lower() for i in rawdata]
    #return data
    return np.load(filename)
        
''' given 1 tweet (an array of tuples), return an array of 3 feature values.
    features are: 
        - af_pos: afinn > 1 (2,3,4)
        - af_neu: afinn [-1,1] (-1,0,1)
        - af_neg: afinn  < -1 (-2,-3,-4)
'''
def afinn_ft(tweet):
    score = 0
    af_pos, af_neu, af_neg = 0
    for word in tweet:
        score += af.score(word)
    if score > 1:
        af_pos = 1
    elif score >= -1 and score <= 1:
        af_neu = 1
    else: 
        af_neg = 1
    return [af_big, af_med, af_neg]

