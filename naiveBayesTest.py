'''
Authors: Emily Ahn, Emily Chen, Elizabeth Hau
Date created: 12/5/2015
Last modified: 12/10/2015
****************************************************
This is an initial run of using the Naive Bayes
Classifier on the training gold dataset for training
and dev gold dataset for testing. 
The first run-through achieved an accuracy of 7.3%
*****************************************************
'''
import nltk
import readerAndWriter
    
''' reads in each tweet, stores and returns it in a list of
    tuples as (list of words, sentiment (score))
    and a counter dictionary that counts the frequency 
    of each score
'''
def readTweets(array):
    counter = {'-2':0,'-1':0,'0':0,'1':0,'2':0}
    tweets = []
    for element in array:
        line = element.split("\t")
        topic = line[1]
        score = int(line[2])
        if score == -2:
            counter['-2'] +=1
        elif score == -1:
            counter['-1'] +=1
        elif score == 0:
            counter['0'] += 1
        elif score == 1:
            counter['1'] += 1
        elif score == 2:
            counter['2'] += 1
        #scoreString = "" + score
        #counter[scoreString] += 1
        words = [e.lower() for e in line[3].split(" ") if len(e)>=2]
        tweets.append((words, score))
    print "COUNTER IS:",counter
    return tweets

#print readTweets(read)

''' Given an array of tuples (for each tweet),
    Returns an array of all words in the entire training dataset
'''
def get_words_in_tweets(tweets):
    all_words = [] 
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

''' Makes each word a feature'''
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

''' Returns features (whether each word was present or not) for 1 tweet'''
def extract_features(tweet):
    word_features = get_word_features(tweet)
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


''' Train on file "trainGold.tsv"
    Test on file "devGold.tsv"
    (attempted to view confusion matrix. bugs...)
'''

# TRAIN
read = readerAndWriter.readFile("data/cleaned/trainGold.tsv")
dataForTweets = readTweets(read)
training_set = nltk.classify.apply_features(extract_features, dataForTweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

# TEST
testFile = readerAndWriter.readFile("data/cleaned/devGold.tsv")
dataForTest = readTweets(testFile)
test_set = nltk.classify.apply_features(extract_features, dataForTest)
print "CLASSIFYING: ", nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(10)

'''
cm = nltk.ConfusionMatrix(training_set, training_set)
print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))
'''
