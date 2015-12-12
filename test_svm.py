# test SVM
# E3 Sem Eval
# Date Created: 12.12.15


from sklearn import svm
#import numpy as np
#from sklearn.cross_validation import StratifiedKFold
#from __future__ import division
#import os
#import sys

''' given 1 tweet, posssible features (binary)
    - sentiment score (sum/max/min...?) of tweet (binary values, scale [-10,10]
        - score_10
        - score_9
        - score_8
        ...
        - score_-9
        - score_-10
    - emoticon score (binary values, # of features = # of emoticons)
        - emo_:)
        - emo_:/
        ...
    - contains word with all caps (indicate 1 or -1, not 0)

'''

sample_text = ['i hate everyone', 'butterflies are beautiful and lovely', 'nothing to say']
sample_ft = [[-2,-5],[3,2],[0,0.5]] # X_train
sample_labels = [-1,1,0] # Y_train

# svm, rbf kernel, C=0.75 (acc. to Dalmia et al.)
# X_train = array of shape (# samples x # features)
# Y_train = array of correct labels
classifier = svm.SVC(kernel='rbf', C=0.75) #gamma=0.7
classifier.fit(sample_ft, sample_labels)
predict = classifier.predict(sample_ft)
print "PREDICT:", predict #[-1 1 0] 
#success!







