from nltk.corpus import stopwords
from sets import Set
import CommonFunction as cf
symbol = "_"
punctuation = [",",":",".",""]
def CommonFilter(query,score,wordstem):
	score = RemoveStopWord(query,score)
	score = RemoveQueryWord(query,score,wordstem)
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

def RemoveQueryWord(query,score,wordstem,notremoved=[]):
	# queryWord = Set(cf.MyTokenize(query))
	queryWord = Set(cf.StanfordTokenize(query))
	queryWord = Set([wordstem[tmpw] for tmpw in queryWord])
	i=0
	while i<len(score):
		arr = score[i][0].split(symbol)
		if len(arr)==1 and wordstem[arr[0]] in queryWord:
			score.pop(i)
			i -= 1
		else:
			for j in range(len(arr)):
				if wordstem[arr[j]] in queryWord and wordstem[arr[j]] not in notremoved:
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
def RemoveNotWordWithNumber(score,grampos):
	i = 0
	while i<len(score):
		arr = score[i][0].split(symbol)
		arrpos = grampos[score[i][0]].split(symbol)
		for j in range(len(arr)):
			if not arr[j].isalpha() and not (arr[j].isdigit() or arrpos[j]=="CD"):
				score.pop(i)
				i -= 1
				break
		i += 1
	return score