from search import search
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from sets import Set
from common_filter import CommonFilter
from MyFilter import MyFilter
from pycorenlp import StanfordCoreNLP
import CommonFunction as cf
# from Person_Filter import PersonFilter
import common_filter
import re
import math


symbol = "_"
N_GRAM = 4
INFINITY = 1000000
# def MyCompare1(a,b):
# 	if a[2][0]!=b[2][0]:
# 		# print(str(a)+"----"+str(b))
# 		return b[2][0]-a[2][0]
# 	else:
# 		return a[2][1]-b[2][1]
# def MyTokenize(sentence):
# 	rawTokens = word_tokenize(sentence)
# 	myTokens = [rawTokens[i].encode("ascii","ignore") for i in range(len(rawTokens))]
# 	return myTokens

# def SentencePOS(sentence):
# 	raw_pos = pos_tag(word_tokenize(sentence))
# 	pos = []
# 	for tup in raw_pos:
# 		pos.append([tup[0],tup[1]])
# 	return pos

# def QueryKeyword(query):
# 	stopWords = Set(stopwords.words('english'))
# 	pos = SentencePOS(query)
# 	pp = 0
# 	while pp<len(pos):
# 		if pos[pp][1][0]!="N" and pos[pp][1][0]!="V":
# 			pos.pop(pp)
# 		elif pos[pp][0] in stopWords:
# 			pos.pop(pp)
# 		else:
# 			pp += 1
# 	keyword = [pos[i][0] for i in range(len(pos))]
# 	return Set(keyword)

# def GramQueryDst(gram,qWordList,senTokens):
# 	gramWord = gram.split(symbol)
# 	idxs = [i for i in range(len(senTokens)) if senTokens[i]==gramWord[0]]
# 	if idxs == 0:
# 		return [0,0]
# 	position = []
# 	for idx in idxs:
# 		if idx+len(gramWord)-1>=len(senTokens):
# 			continue
# 		head = idx
# 		end = -1
# 		matchFlag = True
# 		for i in range(len(gramWord)):
# 			if matchFlag and gramWord[i] != senTokens[head+i]:
# 				matchFlag = False
# 		if matchFlag:
# 			end = head+len(gramWord)-1
# 			position.append([head,end])
# 	# print(gram+":"+str(senTokens))
# 	# print(position)

# 	qWordIdx = {}
# 	for word in qWordList:
# 		for i in range(len(senTokens)):
# 			if senTokens[i]==word:
# 				if word not in qWordIdx:
# 					qWordIdx[word] = []
# 				qWordIdx[word].append(i)
# 	# print(qWordIdx)

# 	minDst = INFINITY
# 	for onePos in position:
# 		tmpWholeMin = 0
# 		for qWord,idxs in qWordIdx.items():
# 			tmpMinDst = INFINITY
# 			for idx in idxs:
# 				if idx<onePos[0] and tmpMinDst>(onePos[0]-idx):
# 					tmpMinDst = onePos[0]-idx
# 				elif idx>onePos[1] and tmpMinDst>(idx-onePos[1]):
# 					tmpMinDst = idx-onePos[1]
# 			tmpWholeMin += tmpMinDst
# 		if minDst>tmpWholeMin:
# 			minDst = tmpWholeMin
# 	# print(minDst)
# 	if minDst==0:
# 		minDst = INFINITY	

# 	return [len(qWordIdx),minDst]








# def StanfordNERPOS(sentence):
# 	# print("Connect to the port: 53510")
# 	nlp = StanfordCoreNLP('http://localhost:9000')
# 	# print("Port connected: 53510")
# 	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,ner','outputFormat':'json'})
# 	ner = []
# 	pos = []
# 	for token in output['sentences'][0]['tokens']:
# 		ner.append([token['word'].encode('ascii', 'ignore'),token['ner'].encode('ascii', 'ignore')])
# 		pos.append([token['word'].encode('ascii', 'ignore'),token['pos'].encode('ascii', 'ignore')])
# 	return ner,pos

def WriteFile(data,path):
	file = open(path,"w+")
	for one in data:
		file.write(str(one)+"\n")
	file.close()
# query = query.lower()#Convert query to lower case
def GenerateNGram(n,doc,grampos,gramner):
	gram = {}
	pos = grampos
	gram_count = 0
	stemlist = []
	for line in doc:
		# print(line)
		# linepos = pos_tag(word_tokenize(line))
		linener,linepos = cf.StanfordNERPOS(line)
		linestem = cf.StanfordStemmer(line)
		stemlist += linestem
		# print(linener)
		# print("-----------"+str(linepos))
		line = [linepos[i][0] for i in range(len(linepos))]
		# print(line)
		for i in range(len(line)-n+1):
			tup = ""
			for j in range(n):
				tup += line[i+j]
				if j!=n-1:
					tup += symbol
			if tup not in gram:
				gram[tup] = 0
				posgram = ""
				nergram = ""
				for posi in range(n):
					posgram += linepos[i+posi][1]
					if posi != n-1:
						posgram += symbol
				pos[tup] = posgram

				for neri in range(n):
					nergram += linener[i+neri][1]
					if neri != n-1:
						nergram += symbol
				gramner[tup] = nergram
			gram[tup] += 1
			gram_count += 1
	return [gram,gram_count,stemlist]

def ProcessData(irresult):
	result = []
	# print(irresult)
	puntuation = Set([",",".",":"])
	for ss in irresult:
		ss = ss.encode('ascii', 'ignore').strip().split("\n")
		for onestring in ss:
			result.append(onestring)
		# ss = re.split(r'\s',ss)
		# tmps = []
		# for word in ss:
		# 	if word[len(word)-1] in puntuation:
		# 		# tmps.append(word[0:len(word)-1].lower())
		# 		tmps.append(word[0:len(word)-1])
		# 		tmps.append(word[len(word)-1])
		# 	else:
		# 		# tmps.append(word.lower())
		# 		tmps.append(word)
		# newss = " ".join(tmps)
		# newfile.write(newss+"\n")
		# result.append(newss)
	return result

def NGramTiling(query,answerlist):
	#IR Process
	# print("IR processing")
	# irresult = search(MY_SEARCH_FILE,QUERY)
	irresult = answerlist
	QUERY = query


	#Preprocess irresult
	pro_data = ProcessData(irresult)
	WriteFile(pro_data,"irresult.txt")
	# for onesample in pro_data:
	# 	print(ne_chunk(pos_tag(word_tokenize(onesample))))
	# 	print(pos_tag(word_tokenize(onesample)))


	# Genrate the ngram first
	# print("Generating N-gram")
	n = N_GRAM #The number of grams it will use, begin with unigram
	# file = open("processed_data.txt")
	# file = open("ptb.2-21.txt")
	# ss = file.readline().strip()
	# ss = file.readline().strip().lower()
	doc = []
	gram = []
	grampos = {}
	gramner = {}
	wordstem = {}
	for ss in pro_data:
		doc .append(ss)
		# ss = file.readline().strip()
		# ss = file.readline().strip().lower()
	for i in range(n):
		tmpgram,tmpcount,tmpstem = GenerateNGram(i+1,doc,grampos,gramner)
		# print(tmpstem)
		gram.append(tmpgram)
		for tup in tmpstem:
			wordstem[tup[0]] = tup[1]
	# print(grampos)
	# print(gram)

	#Get the stem for query
	qstem = cf.StanfordStemmer(query)
	for onestem in qstem:
		wordstem[onestem[0]] = onestem[1]
	# print(wordstem)

	# Voting: Calculate the score for every snippet
	# print("Voting.")
	score = []
	for i in range(n):
		for k,v in gram[i].items():
			score.append([k,v])
	score = sorted(score,key=lambda onescore:onescore[1], reverse = True)
	WriteFile(score,"voteresult.txt")
	# print(score)


	# General Filtering 
	# print("Filter process.")
	# score = CommonFilter(QUERY,score)
	myfilter = MyFilter()
	score = myfilter.Filter(score,QUERY,grampos,gramner)
	# print(score)

	#Combination
	# print("Combination.")
	combination = []
	for tup in score:
		word = tup[0]
		arr = word.split(symbol)
		tmpscore = tup[1]
		for i in range(len(arr)):
			tmpscore += gram[0][arr[i]]
		combination.append([word,tmpscore])
	combination = sorted(combination, key=lambda tup:tup[1],reverse = True)
	WriteFile(combination,"Combination.txt")


	#Measure the distance of between the ngram and the keyword of the query
	# qKeyWord = QueryKeyword(query)
	# # print(len(qKeyWord))
	# for oneCom in combination:
	# 	gram = oneCom[0]
	# 	keyWordNum,keyWordDst = 0,0
	# 	for sen in answerlist:
	# 		senTokens = MyTokenize(sen)
	# 		nn,dd = GramQueryDst(gram,qKeyWord,senTokens)
	# 		if nn>keyWordNum and dd!=INFINITY:
	# 			keyWordNum = nn
	# 			keyWordDst = dd
	# 		elif nn==keyWordNum and keyWordDst>dd:
	# 			keyWordNum = nn
	# 			keyWordDst = dd
	# 	oneCom.append([keyWordNum,keyWordDst])
	# candidateList = combination
	# candidateList = sorted(candidateList,cmp=MyCompare1)
	candidateList = combination
	queryType = cf.QueryClassification(QUERY)
	if queryType == "PERSON":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
		# None
	elif queryType == "PERSON_ENTITY":
		# candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query)
		None
	elif queryType == "TIME":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	WriteFile(candidateList,"CandidateList.txt")


	#Read Document Frequency
	# file = open("./doc_frequency.txt")
	# docmunet_count = int(file.readline().strip().split(" ")[1])
	# frequency = {}
	# ss = file.readline().strip()
	# word_in_corpus = 0
	# while ss!="":
	# 	arr = ss.split(" ")
	# 	frequency[arr[0]] = int(arr[1])
	# 	word_in_corpus += int(arr[1])
	# 	ss = file.readline().strip()

	# #Score
	# print("Rescore.")
	# for tup in combination:
	# 	arr = tup[0].split(symbol)
	# 	tmpsum = 0
	# 	for i in range(len(arr)):
	# 		df = 0
	# 		if arr[i] not in frequency:
	# 			df = 1
	# 		else:
	# 			df = frequency[arr[i]]
	# 		tmpsum += math.log(float(docmunet_count)/df)
	# 	tup[1] = tup[1]*1.0/len(arr)*tmpsum
	# combination = sorted(combination, key=lambda tup:tup[1],reverse = True)
	answer_phrase = candidateList[0][0].split(symbol)
	# print(combination[0:11])
	return answer_phrase
	# WriteFile(combination,"finalresult.txt")

if __name__ == "__main__":
	# print(pos_tag(word_tokenize("Welcome to Carnegie Mellon University.")))
	# Q = "When was Dempsey born ?"
	# Q = "Who is John Terry ?"
	# Q = "Who is the Chelsea Captain ?"
	# Q = "When did Dempsey join Seattle Sounders ?"
	# Q = "When was Donovan born ?"
	# Q = "When Terry became the captain ?"
	# Q = "Who is Chelsea Captain ?"
	# Q = "Where does Terry play football?"
	# # print(QueryKeyword(QUERY))
	# Q = "Where was Solo born ?"
	# Q = "Who did Alessandro Volta marry?"
	Q = "Who made Volta a count?"
	# Q = "When did Volta retire?"
	# Q = "Where was Volta born?"
	Q = "Who showed that Avogadro's theory held in dilute solutions?"
	Q = "Who wrote about ants in A Tramp Abroad?"
	Q = "Where are bullet ants located?"
	Q = "Where is the city of Antwerp?"
	Q = "When was the first photgraph of lincoln taken?"
	Q = "When did he publish another memoria?"
	Q = "When did he become a professor?"
	print(Q)
	# MY_SEARCH_FILE = "./data/set4/a8.txt"
	MY_SEARCH_FILE = "/Users/weidong/Downloads/Question_Answer_Dataset_v1.2/S08/data/set4/a8.txt"
	answerlist = search(MY_SEARCH_FILE,Q)
	answer = NGramTiling(Q,answerlist)
	for word in answer:
		print(word),

	# print(cf.StanfordNERPOS("In 2007, he became the first captain to lift the FA Cup "+\
	# 	"at the new Wembley Stadium in Chelsea\'s 10 win over Manchester United, and "+\
	# 	"also the first player to score an international goal there, scoring a header "+\
	# 	"in England\'s 11 draw with Brazil."))







