'''
Authors: Elizabeth Hau, Emily Ahn, Emily Chen
Date created: 11/24/2015
Last modified: 11/29/2015
*************************************************************
The funtion of this file is to remove all tweets that are 
'Not Available' at the time of download due to various reasons
to remove unnecessary noise in the data we use to perform
sentiment analysis. All functions in this file assume that 
the files passed in are in the form:
        id<TAB>topic<TAB>sentiment label<TAB>tweet
where the tweet will be in position 3 in the array if converted
to an array 
                    OR in the form:
                id<TAB>topic<TAB>tweet
where the tweet will be in position 2 in the array if converetd 
to an array
*************************************************************
'''


''' reads in a file given the file name as a parameter and 
    returns the data as an array, where each line in the file
    is an element in the array
'''
def readFile(fileName):
    with open(fileName, "r") as myfile:
        rawdata = myfile.readlines()
        #print "rawdata",rawdata
    data = [i.replace('\n','') for i in rawdata]
    return data

totalValidIds = []
''' given the array that contains all the lines in the file,
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
            #if line[3] != 'Not Available':
                #print line
            endData.append(line)
            if line[0] not in validIds:
                validIds.append(line[0])
                totalValidIds.append(line[0])
            #counter+=1
        elif len(line) == 3 and line[2] != 'Not Available':
            endData.append(line)
            if line[0] not in validIds:
                validIds.append(line[0])
                totalValidIds.append(line[0])
        elif len(line) < 3 or len(line) > 4:
            print "error in data"
            break;
    #print "all ids:",allIds
    print "# of all ids:",len(allIds)
    print "# of valid ids:",len(validIds)
        #else:
         #   print '********************',line[3]
            #break;
    #print "counter is",counter
    #print "end data is:",endData
    #print "length of end data is:", len(endData)
    return endData

'''function that takes in a fileName (to write to) and an 
   array containing the data to write to the file
'''
def writeToFile(fileName, array):
    data = open(fileName, "w")
    for element in array:
        for e in element:
            data.write(e + '\t')
        data.write('\n')
    data.close()
        

#read = readFile("test.txt")
#print "read has:",read
#array = deleteUnavailable(read)
#writeToFile("test1.txt",read)

print "\n********************* TRAIN GOLD **********************************"
trainGoldReadResult = readFile("trainC5gold.tsv")
trainGoldLen = len(trainGoldReadResult)
print "number of tweets in train gold before removing tweets that are 'not available':",trainGoldLen

trainGoldResult = deleteUnavailable(trainGoldReadResult)
trainGoldResultLen = len(trainGoldResult)
print "number of tweets in train gold after removing 'not available' tweets:",trainGoldResultLen

trainGoldNumUnAvail = (trainGoldLen-trainGoldResultLen)
print "Number of tweets unavailable in trainGold:", trainGoldNumUnAvail

print "\n********************* DEV GOLD **********************************"
devGoldReadResult = readFile("devC5gold.tsv")
devGoldLen = len(devGoldReadResult)
print "number of tweets in dev gold before removing tweets that are 'not available':",devGoldLen

devGoldResult = deleteUnavailable(devGoldReadResult)
devGoldResultLen = len(devGoldResult)
print "number of tweets in dev gold after removing 'not available' tweets:",devGoldResultLen

devGoldNumUnAvail = (devGoldLen-devGoldResultLen)
print "Number of tweets unavailable in devGold:", devGoldNumUnAvail

print "\n********************* DEVTEST GOLD **********************************"
devtestGoldReadResult = readFile("devtestC5gold.tsv")
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
devtestInputReadResult = readFile("devtestC5input.tsv")
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
writeToFile("trainGold.tsv",trainGoldResult)
trainGold = readFile("trainGold.tsv")
print "length of new train file(5444):",len(trainGold)

# dev
writeToFile("devGold.tsv",devGoldResult)
devGold = readFile("devGold.tsv")
print "length of new dev file(1814):",len(devGold)

# devtest
writeToFile("devtestGold.tsv",devtestGoldResult)
devtestGold = readFile("devtestGold.tsv")
print "length of new devtest file(1791):",len(devtestGold)

# devtest input
writeToFile("devtestInput.tsv",devtestInputResult)
devtestInput = readFile("devtestInput.tsv")
print "length of new devtest input file(1794):",len(devtestInput)