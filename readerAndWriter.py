'''
Authors: Elizabeth Hau, Emily Ahn, Emily Chen
Date created: 12/10/2015
Last modified: 12/10/2015
*************************************************************
This file contains functions to read in a file, store it in
an array and write to a file given a file name and an array
containing the data.
*************************************************************
'''

''' 
    readFile reads in a file given the file name as a parameter and 
    returns the data as an array where each element in the array is 
    a String representation of each line read in file
'''
def readFile(fileName):
    with open(fileName, "r") as myfile:
        rawdata = myfile.readlines()
    data = [i.replace('\n','') for i in rawdata]
    return data

'''
    writeToFile takes in a fileName (to write to) and an 
    array containing the data to write to the file
    The data written to the file will be in tab-separated values
'''
def writeToFile(fileName, array):
    data = open(fileName, "w")
    for element in array:
        for e in element:
            data.write(e + '\t')
        data.write('\n')
    data.close()

def writeToFile2(fileName, array):
    data = open(fileName, "w")
    for element in array:
        data.write(element + '\n')
        #data.write('\n')
    data.close()
    
'''
    inFile takes in a fileName (to write to) and an 
    array containing the data that we want to match to the tweets
    If the tweet matches the input array data, we return the tweets in an array
'''

def inFile(fileName, array):
    fileArray = readFile(fileName)
    tweetArray = []
    for line in fileArray:
        tweetInfo = line.split("\t")
        topic = tweetInfo[1]
        tweet = tweetInfo[2]
        if topic in array:
            tweetArray.append(line)
    return tweetArray
    
# List of All Public Figures Topics
topicsArray = readFile('data/Public Figures Topics.txt')
print len(topicsArray)
topicsLower = [topic.lower() for topic in topicsArray]
train = topicsLower[:36]
print "train:\n", train
test = topicsLower[36:]
print "test:\n",test
# All Tweets Data Set
trainTweets = inFile('data/cleaned/allTopics3pt.tsv', train)
testTweets = inFile('data/cleaned/allTopics3pt.tsv', test)
writeToFile2('data/cleaned/PFTweetsTrain.txt', trainTweets)  
writeToFile2('data/cleaned/PFTweetsTest.txt', testTweets)  

# List of just Politicians Topics
#topicsArray = readFile('Politicians Topics.txt')
## All Tweets Data Set
#topicsTweetsArray = inFile('data/cleaned/allTopics3pt.tsv', topicsArray)
#writeToFile2('data/cleaned/PoliTweets.txt', topicsTweetsArray)  

# List of just Entertainers Topics
#topicsArray = readFile('Entertainers Topics.txt')
## All Tweets Data Set
#topicsTweetsArray = inFile('data/cleaned/allTopics3pt.tsv', topicsArray)
#writeToFile2('data/cleaned/EntTweets.txt', topicsTweetsArray)  

# List of just Athletes Topics
#topicsArray = readFile('Athletes Topics.txt')
## All Tweets Data Set
#topicsTweetsArray = inFile('data/cleaned/allTopics3pt.tsv', topicsArray)
#writeToFile2('data/cleaned/AthTweets.txt', topicsTweetsArray)  