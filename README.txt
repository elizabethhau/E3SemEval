******************************************************
* E3 SemEval 2016: Sentiment Analysis on Twitter     *
*                                                    *
* CS 232 Artificial Intelligence Final Project       *
*                                                    *
*		         Fall 2015			                         *
*							                                       *
* 	Emily Ahn, Emily Chen, Elizabeth Hau		         *   
*							                                       *
*   https://github.com/elizabethhau/E3SemEval/       *
*                       				                     *
*                                                    *
******************************************************

DIRECTORIES:

ark-tweet-nlp-0.3.2 —> directory that contains the code for the tweet tagger and the jar file that we needed to tag the tweets

data —> directory that contains all the data (specific files in data directory explained below)

data/cleaned—> directory that contains data with tweets that were not available at the time of download removed

FILES: 

create_features.py —> reads in training and testing files, creates feature arrays, and trains an SVM classifier to predict test tweets.

naiveBayesTest.py —> an initial run of using the Naive Bayes Classifier on the training gold dataset for training and dev gold dataset for testing, both of which are on a 5-point scale. The first run-through achieved an accuracy of 7.3%. 

readerAndWriter.py —> This file contains functions to read in a file, store it in
an array and write to a file given a file name and an array
containing the data.

data/CMUTweetTagger.py —> Simple Python wrapper for runTagger.sh script for CMU's Tweet Tokeniser and Part of Speech tagger: http://www.ark.cs.cmu.edu/TweetNLP/

data/Public\ Figures\ Topics.txt —> the 49 topics that fell into the ‘public figures’ category.

data/dataPreprocessing.py —> This file contains all the data preprocessing steps 

data/cleaned/PFTestTag.txt —> This file contains all the tagged tweets used for testing (public figures only)

data/cleaned/PFTrainTag.txt —> This file contains all the tagged tweets used for training (public figures only)

data/cleaned/PFTweets.txt —> This file contains the tweetIds, topics, labels, and tweets for all of the 49 public figures

data/cleaned/PFTweetsCleaned.txt —> This file contains all the tweets (no ids, topics, or labels) of the 49 public figures

data/cleaned/allTopics.tsv —> This file contains the tweetIds, topics, labels, and tweets for all 100 topics provided (on a 5-point scale)

data/cleaned/allTopics3pt.tsv —> This file contains the tweetIds, topics, labels, and tweets for all 100 topics provided converted to a 3-point scale from the ‘allTopics.tsv’ file that was on a 5-point scale

