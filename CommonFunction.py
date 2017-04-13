from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from sets import Set
def MyCompare1(a,b):
	if a[2][0]!=b[2][0]:
		# print(str(a)+"----"+str(b))
		return b[2][0]-a[2][0]
	else:
		return a[2][1]-b[2][1]
def MyTokenize(sentence):
	rawTokens = word_tokenize(sentence)
	myTokens = [rawTokens[i].encode("ascii","ignore") for i in range(len(rawTokens))]
	return myTokens
def SentencePOS(sentence):
	raw_pos = pos_tag(word_tokenize(sentence))
	pos = []
	for tup in raw_pos:
		pos.append([tup[0],tup[1]])
	return pos
def QueryClassification(query):
		queryarr = query.split(" ")
		if queryarr[0].lower()=="who":
			return "PERSON"
		elif queryarr[0].lower()=="when":
			return "TIME"
		return None