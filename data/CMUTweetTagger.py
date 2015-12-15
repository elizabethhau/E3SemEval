#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Python wrapper for runTagger.sh script for CMU's Tweet Tokeniser and Part of Speech tagger: http://www.ark.cs.cmu.edu/TweetNLP/

Usage:
results=runtagger_parse(['example tweet 1', 'example tweet 2'])
results will contain a list of lists (one per tweet) of triples, each triple represents (term, type, confidence)
"""
import subprocess
import shlex
import readerAndWriter
import numpy as np

# The only relavent source I've found is here:
# http://m1ked.com/post/12304626776/pos-tagger-for-twitter-successfully-implemented-in
# which is a very simple implementation, my implementation is a bit more
# useful (but not much).

# NOTE this command is directly lifted from runTagger.sh
RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar ../ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar"


def _split_results(rows):
    """Parse the tab-delimited returned lines, modified from: https://github.com/brendano/ark-tweet-nlp/blob/master/scripts/show.py"""
    for line in rows:
        line = line.strip()  # remove '\n'
        if len(line) > 0:
            if line.count('\t') == 2:
                parts = line.split('\t')
                tokens = parts[0]
                tags = parts[1]
                confidence = float(parts[2])
                yield tokens, tags, confidence


def _call_runtagger(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh using a named input file"""

    # remove carriage returns as they are tweet separators for the stdin
    # interface
    tweets_cleaned = [tw.replace('\n', ' ') for tw in tweets]
    message = "\n".join(tweets_cleaned)

    # force UTF-8 encoding (from internal unicode type) to avoid .communicate encoding error as per:
    # http://stackoverflow.com/questions/3040101/python-encoding-for-pipe-communicate
    message = message.encode('utf-8')

    # build a list of args
    args = shlex.split(run_tagger_cmd)
    args.append('--output-format')
    args.append('conll')
    po = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # old call - made a direct call to runTagger.sh (not Windows friendly)
    #po = subprocess.Popen([run_tagger_cmd, '--output-format', 'conll'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = po.communicate(message)
    # expect a tuple of 2 items like:
    # ('hello\t!\t0.9858\nthere\tR\t0.4168\n\n',
    # 'Listening on stdin for input.  (-h for help)\nDetected text input format\nTokenized and tagged 1 tweets (2 tokens) in 7.5 seconds: 0.1 tweets/sec, 0.3 tokens/sec\n')

    pos_result = result[0].strip('\n\n')  # get first line, remove final double carriage return
    pos_result = pos_result.split('\n\n')  # split messages by double carriage returns
    pos_results = [pr.split('\n') for pr in pos_result]  # split parts of message by each carriage return
    return pos_results


def runtagger_parse(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh on a list of tweets, parse the result, return lists of tuples of (term, type, confidence)"""
    pos_raw_results = _call_runtagger(tweets, run_tagger_cmd)
    pos_result = []
    for pos_raw_result in pos_raw_results:
        pos_result.append([x for x in _split_results(pos_raw_result)])
    return pos_result


def check_script_is_present(run_tagger_cmd=RUN_TAGGER_CMD):
    """Simple test to make sure we can see the script"""
    success = False
    try:
        args = shlex.split(run_tagger_cmd)
        args.append("--help")
        po = subprocess.Popen(args, stdout=subprocess.PIPE)
        # old call - made a direct call to runTagger.sh (not Windows friendly)
        #po = subprocess.Popen([run_tagger_cmd, '--help'], stdout=subprocess.PIPE)
        while not po.poll():
            lines = [l for l in po.stdout]
            #print lines
        # we expected the first line of --help to look like the following:
        assert "RunTagger [options]" in lines[0]
        success = True
    except OSError as err:
        print "Caught an OSError, have you specified the correct path to runTagger.sh? We are using \"%s\". Exception: %r" % (run_tagger_cmd, repr(err))
    return success

''' ****************************************************************************
    We added this section
    ****************************************************************************
'''
#tweets = list of tweets
def cleanTweet(tweets):
    tagResults = runtagger_parse(tweets)
    result = []
    #print "tag results\t",tagResults
    for tweet in tagResults: #w = word, t = tag, c = confidence level
        #cleanTweet = ""
        tuplesList = []
        for triple in tweet:
            #print triple
            (w, t, c) = triple
            #removing urls, user mentions, numbers, and hashtags from the tweet
            if t != 'U' and t != '@' and t!= '$' and t != '#':
                tuplesList.append((w,t))
                #print 'got here'
                #cleanTweet+=str(w) + " "
        #print tuplesList
        #print "clean tweet is:\t", tuplesList
        #result.append(cleanTweet)
        result.append(tuplesList)
        
    #print result
    return result

def replaceTaggedTweet(data):
    #print "data is\n",data
    result = []
    for element in data:
        line = element.split("\t")
        #result.append(line[0])
        #result.append(line[1])
        #result.append(line[2])
        #print "\nline is",line
        #break;
        tweet = [line[3]]
        #print "tweet is\t", tweet
        cleaned = cleanTweet(tweet)
        #print "cleaned tweet\t",cleaned
        line[3] = cleaned
        result.append(line[3][0])
        #print "\nline[3]\t",line[3][0]
        #print len(line)
        #print len(result)
        #print "\nresult is\t",result
    return result
        
def toFile(fileName, data):
    result = open(fileName, "w")
    for element in data:
        #print "ELEMENT IS:\t",element
        result.write(str(element))
        result.write('\n')
        #data.write('\n')
    result.close()

if __name__ == "__main__":
    print "Checking that we can see \"%s\", this will crash if we can't" % (RUN_TAGGER_CMD)
    success = check_script_is_present()
    if success:
        print "Success."
        print "Now pass in two messages, get a list of tuples back:"
        tweets = ["dear @Microsoft the newOoffice for Mac is great and all, but no Lync update? C'mon.	", 
            "Innovation for jobs is just around the corner - to be exact next Wednesday 8/19 at @Microsoft http://t.co/3DK6ToZeA8 http://t.co/L2wOZcwgRb",
            "For the 1st time @Skype has a 'High Startup impact'   Does anyone at @Microsoft have a clue? #Windows10Fail http://t.co/loO3yd5rwe"]
        
        #tagResults = runtagger_parse(tweets)
        #result = []
        #for tweet in tagResults: #w = word, t = tag, c = confidence level
        #    cleanTweet = ""
        #    for triple in tweet:
        #        print triple
        #        (w, t, c) = triple
        #        #removing urls, user mentions, numbers, and hashtags from the tweet
        #        if t != 'U' and t != '@' and t!= '$' and t != '#':
        #            cleanTweet+=str(w) + " "
        #            #print "cleantweet is:",cleanTweet
        #            #print w
        #    print cleanTweet
        #    result.append(cleanTweet)
        #print result
        #readResults = readerAndWriter.readFile("cleaned/PFTweets.txt")
        readTrain = readerAndWriter.readFile("cleaned/PFTweetsTrain.txt")
        readTest = readerAndWriter.readFile("cleaned/PFTweetsTest.txt")
        #print "read results\n",readResults
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
            
