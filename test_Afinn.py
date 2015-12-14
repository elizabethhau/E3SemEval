# test AFINN

from afinn import Afinn
af = Afinn()
af_emoticon = Afinn(emoticons=True)
text1 = 'This is utterly excellent!'
text2 = ':/'
text3 = 'This is hardly excellent'
print text1, ":", af.score(text1) #score = 3.0
print "find_all:", af.find_all(text1) #['excellent']
print text2, ":", af_emoticon.score(text2) #score = -2.0
print text3, ":", af.score(text3)
print "find_all:", af.find_all(text3) #['excellent']
print "the", af.score("the")
