'''
Authors: Elizabeth Hau, Emily Ahn, Emily Chen
Date created: 11/24/2015
Last modified: 12/12/2015
*************************************************************
This file contains all the data preprocessing
*************************************************************
'''

import readerAndWriter

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

print "\n********************* TRAIN GOLD **********************************"
trainGoldReadResult = readerAndWriter.readFile("trainC5gold.tsv")
trainGoldLen = len(trainGoldReadResult)
print "number of tweets in train gold before removing tweets that are 'not available':",trainGoldLen

trainGoldResult = deleteUnavailable(trainGoldReadResult)
trainGoldResultLen = len(trainGoldResult)
print "number of tweets in train gold after removing 'not available' tweets:",trainGoldResultLen

trainGoldNumUnAvail = (trainGoldLen-trainGoldResultLen)
print "Number of tweets unavailable in trainGold:", trainGoldNumUnAvail

print "\n********************* DEV GOLD **********************************"
devGoldReadResult = readerAndWriter.readFile("devC5gold.tsv")
devGoldLen = len(devGoldReadResult)
print "number of tweets in dev gold before removing tweets that are 'not available':",devGoldLen

devGoldResult = deleteUnavailable(devGoldReadResult)
devGoldResultLen = len(devGoldResult)
print "number of tweets in dev gold after removing 'not available' tweets:",devGoldResultLen

devGoldNumUnAvail = (devGoldLen-devGoldResultLen)
print "Number of tweets unavailable in devGold:", devGoldNumUnAvail

print "\n********************* DEVTEST GOLD **********************************"
devtestGoldReadResult = readerAndWriter.readFile("devtestC5gold.tsv")
devtestGoldLen = len(devtestGoldReadResult)
print "number of tweets in devtet gold before removing tweets that are 'not available':",devtestGoldLen

devtestGoldResult = deleteUnavailable(devtestGoldReadResult)
devtestGoldResultLen = len(devtestGoldResult)
print "number of tweets in devtest gold after removing 'not available' tweets:",devtestGoldResultLen

devtestGoldNumUnAvail = (devtestGoldLen-devtestGoldResultLen)
print "Number of tweets unavailable in devtestGold", devtestGoldNumUnAvail

print "\n*********************** TOTAL *****************************************"
print "Total tweets:",trainGoldResultLen+devGoldResultLen+devtestGoldResultLen
print "Total distinct ids:", len(totalValidIds)

print "\n********************* DEVTEST INPUT **********************************"
devtestInputReadResult = readerAndWriter.readFile("devtestC5input.tsv")
devtestInputLen = len(devtestInputReadResult)
print "number of tweets in devtest input before removing tweets that are 'not available':",devtestInputLen

devtestInputResult = deleteUnavailable(devtestInputReadResult)
devtestInputResultLen = len(devtestInputResult)
print "number of tweets in devtest input after removing 'not available' tweets:",devtestInputResultLen

devtestInputNumUnAvail = (devtestInputLen-devtestInputResultLen)
print "Number of tweets unavailable in devtest input:", devtestInputNumUnAvail


''' create new .tsv files to actually use for training, dev, and devtest '''

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
    as an array and changes '''
#lang_list = ['ar', 'cz', 'in']
#langs = {lang: read_csv(lang+'_formants.csv') for lang in lang_list}
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

originalFile = readerAndWriter.readFile("cleaned/allTopics.tsv")
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