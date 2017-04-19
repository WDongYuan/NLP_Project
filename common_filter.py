from nltk.corpus import stopwords
from sets import Set
import CommonFunction as cf
symbol = "_"
punctuation = [",",":",".",""]
def CommonFilter(query,score):
	score = RemoveStopWord(query,score)
	score = RemoveQueryWord(query,score)
	score = RemoveNotWord(score)
	return score

def RemoveStopWord(query,score):
	stopWords = Set(stopwords.words('english'))
	for pun in punctuation:
		stopWords.add(pun)
	i=0
	while i<len(score):
		arr = score[i][0].split(symbol)
		for j in range(len(arr)):
			if arr[j] in stopWords and not arr[j].isdigit():
				score.pop(i)
				i -= 1
				break
		i += 1
	return score

def RemoveQueryWord(query,score):
	queryWord = Set(cf.MyTokenize(query))
	i=0
	while i<len(score):
		arr = score[i][0].split(symbol)
		for j in range(len(arr)):
			if arr[j] in queryWord:
				score.pop(i)
				i -= 1
				break
		i += 1
	return score
def RemoveNotWord(score):
	i = 0
	while i<len(score):
		arr = score[i][0].split(symbol)
		for j in range(len(arr)):
			if not arr[j].isalpha() and not arr[j].isdigit():
				score.pop(i)
				i -= 1
				break
		i += 1
	return score