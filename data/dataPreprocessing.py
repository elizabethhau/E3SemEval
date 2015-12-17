'''
Authors: Elizabeth Hau, Emily Ahn, Emily Chen
Date created: 11/24/2015
Last modified: 12/17/2015
*************************************************************
This file contains all the data preprocessing
*************************************************************
'''
from __future__ import division
import readerAndWriter
from ttp import ttp
import numpy as np

import CMUTweetTagger
#import twokenize 

'''
*************************************************************
This section removes all the tweets that are 
'Not Available' at the time of download due to various reasons.
This removes unnecessary noise in the data we use to perform
sentiment analysis. All functions in this section assume that 
the files passed in are in the form (for gold files):
        id<TAB>topic<TAB>sentiment label<TAB>tweet
where the tweet will be in position 3 in the array if converted
to an array 
                    OR in the form (for input files):
                id<TAB>topic<TAB>tweet
where the tweet will be in position 2 in the array if converetd 
to an array
*************************************************************
'''
totalValidIds = [] # an array of all the valid tweet ids in the files

''' Given the array that contains all the lines in the file,
    deletes any file that contains 'Not Available' as the tweet
    and returns a new array with those tweets removed
'''
def deleteUnavailable(array):
    #counter = 0
    #global endData
    validIds = []
    global totalValidIds
    allIds = []
    endData = []
    # for each line, check if the tweet is 'Not Available'
    for element in array:
        line = element.split("\t")
        if line[0] not in allIds:
            allIds.append(line[0])
        # if the tweet is not "Not Available", append it to endData array
        if len(line) == 4 and line[3] != 'Not Available':
            endData.append(line)
            if line[0] not in validIds:
                validIds.append(line[0])
                totalValidIds.append(line[0])
        elif len(line) == 3 and line[2] != 'Not Available':
            endData.append(line)
            if line[0] not in validIds:
                validIds.append(line[0])
                totalValidIds.append(line[0])
        elif len(line) < 3 or len(line) > 4:
            print "error in data"
            break;
    print "# of all ids:",len(allIds)
    print "# of valid ids:",len(validIds)
    return endData
'''
print "\n********************* TRAIN GOLD **********************************"
trainGoldReadResult = readerAndWriter.readFile("trainC5gold.tsv")
trainGoldLen = len(trainGoldReadResult)
print "number of tweets in train gold before removing tweets that are 'not available':",trainGoldLen #6000

trainGoldResult = deleteUnavailable(trainGoldReadResult)
trainGoldResultLen = len(trainGoldResult)
print "number of tweets in train gold after removing 'not available' tweets:",trainGoldResultLen #5444

trainGoldNumUnAvail = (trainGoldLen-trainGoldResultLen)
print "Number of tweets unavailable in trainGold:", trainGoldNumUnAvail #544

print "\n********************* DEV GOLD **********************************"
devGoldReadResult = readerAndWriter.readFile("devC5gold.tsv")
devGoldLen = len(devGoldReadResult)
print "number of tweets in dev gold before removing tweets that are 'not available':",devGoldLen #2000

devGoldResult = deleteUnavailable(devGoldReadResult)
devGoldResultLen = len(devGoldResult)
print "number of tweets in dev gold after removing 'not available' tweets:",devGoldResultLen #1814

devGoldNumUnAvail = (devGoldLen-devGoldResultLen)
print "Number of tweets unavailable in devGold:", devGoldNumUnAvail #186

print "\n********************* DEVTEST GOLD **********************************"
devtestGoldReadResult = readerAndWriter.readFile("devtestC5gold.tsv")
devtestGoldLen = len(devtestGoldReadResult)
print "number of tweets in devtet gold before removing tweets that are 'not available':",devtestGoldLen #2000

devtestGoldResult = deleteUnavailable(devtestGoldReadResult)
devtestGoldResultLen = len(devtestGoldResult)
print "number of tweets in devtest gold after removing 'not available' tweets:",devtestGoldResultLen #1791

devtestGoldNumUnAvail = (devtestGoldLen-devtestGoldResultLen)
print "Number of tweets unavailable in devtestGold", devtestGoldNumUnAvail #209

print "\n*********************** TOTAL *****************************************"
print "Total tweets:",trainGoldResultLen+devGoldResultLen+devtestGoldResultLen #9049
print "Total distinct ids:", len(totalValidIds) #9020

print "\n********************* DEVTEST INPUT **********************************"
devtestInputReadResult = readerAndWriter.readFile("devtestC5input.tsv")
devtestInputLen = len(devtestInputReadResult)
print "number of tweets in devtest input before removing tweets that are 'not available':",devtestInputLen #2000

devtestInputResult = deleteUnavailable(devtestInputReadResult)
devtestInputResultLen = len(devtestInputResult)
print "number of tweets in devtest input after removing 'not available' tweets:",devtestInputResultLen #1794

devtestInputNumUnAvail = (devtestInputLen-devtestInputResultLen)
print "Number of tweets unavailable in devtest input:", devtestInputNumUnAvail #206
'''

''' create new .tsv files to actually use for training, dev, and devtest '''
'''
print "\n************************* CHECK LENGTH OF NEW FILES *********************"

# train
readerAndWriter.writeToFile("trainGold.tsv",trainGoldResult)
trainGold = readerAndWriter.readFile("trainGold.tsv")
print "length of new train file(5444):",len(trainGold)

# dev
readerAndWriter.writeToFile("devGold.tsv",devGoldResult)
devGold = readerAndWriter.readFile("devGold.tsv")
print "length of new dev file(1814):",len(devGold)

# devtest
readerAndWriter.writeToFile("devtestGold.tsv",devtestGoldResult)
devtestGold = readerAndWriter.readFile("devtestGold.tsv")
print "length of new devtest file(1791):",len(devtestGold)

# devtest input
readerAndWriter.writeToFile("devtestInput.tsv",devtestInputResult)
devtestInput = readerAndWriter.readFile("devtestInput.tsv")
print "length of new devtest input file(1794):",len(devtestInput)

# file with all topics and tweets
result = trainGoldResult + devGoldResult + devtestGoldResult
'''
''' 
    The below writeToFile call to 'allTopics.tsv' was meant to only be called once
    Don't uncomment!
'''
#print "result length", len(result)
#writeToFile("allTopics.tsv",result)


'''
*************************************************************
This part of the file collapses the data we have that are on
a 5 point scale (-2, -1, 0, 1, 2) to a 3 point scale (-1, 0, 1)
The files on a 3 point scale will be named as: <fileName>3pt.tsv
*************************************************************
'''

'''
    This function takes in the original data on a 5 point scale
    as an array and changes 
'''
def collapseScales(originalData):
    # newFile is an array of arrays where each element in newFile 
    # is a line (as an array)
    newFile = [] 
    for e in originalData:
        line = e.split("\t")
        if (int(line[2]) == -2):
            line[2] = str(-1)
        elif (int(line[2]) == 2):
            line[2] = str(1)
        newFile.append(line)
    return newFile 

''' ******************* COLLAPSE SCALES ***************************'''
originalFile = readerAndWriter.readFile("cleaned/allTopics.tsv")

# find the distribution of the labels before collapsing the scales
dist_count = [0]*5
for element in originalFile:
    line = element.split("\t")
    dist_count[int(line[2])+2] += 1

print "Distribution count of numbers [-2, -1, 0, 1, 2]:",dist_count #[139, 1086, 2667, 4608, 549]
print "Total number of tweets",np.sum(dist_count) #9049
distribution = [0]*5
for num in range(len(dist_count)):
    print "num is", num
    print dist_count[num]
    distribution[num] = dist_count[num]/np.sum(dist_count)
    
print "Distribution of numbers [-2, -1, 0, 1, 2] (in %):", distribution 
#[0.015360813349541386, 0.12001326113382695, 0.29472869930379048, 0.50922753895458062, 0.06066968725826058]

    
'''
result = collapseScales(originalFile)
readerAndWriter.writeToFile("cleaned/allTopics3pt.tsv",result)

originalTraining = readerAndWriter.readFile("cleaned/trainGold.tsv")
trainReadResult = collapseScales(originalTraining)
readerAndWriter.writeToFile("cleaned/trainGold3pt.tsv",trainReadResult)

originalDev = readerAndWriter.readFile("cleaned/devGold.tsv")
devReadResult = collapseScales(originalDev)
readerAndWriter.writeToFile("cleaned/devGold3pt.tsv", devReadResult)

originalDevtest = readerAndWriter.readFile("cleaned/devtestGold.tsv")
devtestReadResult = collapseScales(originalDevtest)
readerAndWriter.writeToFile("cleaned/devtestGold3pt.tsv", devtestReadResult)
'''

'''
*************************************************************
This section of the file tags the raw tweet
*************************************************************
'''

''' This function takes in a list of tweets, tags each word in
    the tweet as a triple in the form of (word, tag, confidence level)
    and returns a list of tuples in the form of (word, tag) 
    with URLs, user mentions, numbers, and hashtags removed
'''
def tag_tweets(tweets):
    tagResults = CMUTweetTagger.runtagger_parse(tweets)
    result = []
    for tweet in tagResults: #w = word, t = tag, c = confidence level
        tuplesList = []
        for triple in tweet:
            (w, t, c) = triple
            #removing urls, user mentions, numbers, and hashtags from the tweet
            if t != 'U' and t != '@' and t!= '$' and t != '#':
                tuplesList.append((w,t))
        result.append(tuplesList)
        
    return result

''' This function takes in an array with tweet IDs, topics, sentiment
    labels, tweets and returns an array of tagged tweets with URLs, 
    user mentions, numbers, and hashtags removed
'''
def replaceTaggedTweet(data):
    result = []
    for element in data:
        line = element.split("\t")
        tweet = [line[3]]
        cleaned = tag_tweets(tweet)
        line[3] = cleaned
        result.append(line[3][0])
    return result
        
''' This function takes in a file name to write to and an array containing
    the data to write to the file (for example, an array of tagged tweets)
    and writes to the file
'''
def toFile(fileName, data):
    result = open(fileName, "w")
    for element in data:
        result.write(str(element))
        result.write('\n')
    result.close()


# Testing ttp parser       
'''        
p = ttp.Parser()
result = p.parse("@Microsoft 2nd computer with same error!!! #Windows10fail Guess we will shelve this until SP1! http://t.co/QCcHlKuy8Q")
print result.reply
#print result
print result.users
print result.tags
print result.urls
#print result.html
print result.lists
#p = ttp.Parser(include_spans=True)
#result = p.parse("@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edburnett/")
#print result.urls
#print result.lists
#print result.tags

#twokenize.simpleTokenize("@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edburnett/ @butthead"))
'''

''' ************************* Using CMUTweetTagger ***************************
    The script that we actually ran to generate the tagged tweet files was 
    CMUTweetTagger.py because this script was not working, but it works now.
'''
'''
print "check is present",CMUTweetTagger.check_script_is_present()
print CMUTweetTagger.runtagger_parse(['example tweet 1', 'example tweet 2'])
#print CMUTweetTagger.check_script_is_present(['example tweet 1', 'example tweet 2'])
#print CMUTweetTagger.runtagger_parse(['example tweet 1', 'example tweet 2'], run_tagger_cmd="java -XX:ParallelGCThreads=2 -Xmx500m -jar ../../ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar")

#readResults = readerAndWriter.readFile("cleaned/PFTweets.txt")
readResults = np.loadtxt(fname="cleaned/PFTweets.txt", dtype=str, delimiter = '\n')

print "read results\n",readResults
print "\n DONE READING \n"
#print "\nclean tweet\n",cleanTweet(tweets)
#replacedResults = replaceTaggedTweet(readResults)
taggedTrain = replaceTaggedTweet(readTrain)
taggedTest = replaceTaggedTweet(readTest)
print "\n DONE REPLACING \n"
#print "\nreplace tagged tweet\t",replacedResults
#np.savetxt("cleaned/testCleaned.txt",replacedResults)
#toFile("cleaned/PFTweetsCleaned.txt",replacedResults)
toFile("cleaned/PFTrainTag.txt", taggedTrain)
toFile("cleaned/PFTestTag.txt", taggedTest)
print "\n DONE WRITING \n"
'''      
        