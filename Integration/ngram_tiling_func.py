from search import search
from nltk import word_tokenize, pos_tag, ne_chunk
from sets import Set
from common_filter import CommonFilter
from MyFilter import MyFilter
from pycorenlp import StanfordCoreNLP
# from Person_Filter import PersonFilter
import common_filter
import re
import math


symbol = "_"
N_GRAM = 3

def StanfordNERPOS(sentence):
	nlp = StanfordCoreNLP('http://localhost:9000')
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,ner','outputFormat':'json'})
	ner = []
	pos = []
	for token in output['sentences'][0]['tokens']:
		ner.append([token['word'].encode('ascii', 'ignore'),token['ner'].encode('ascii', 'ignore')])
		pos.append([token['word'].encode('ascii', 'ignore'),token['pos'].encode('ascii', 'ignore')])
	return ner,pos

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
	for line in doc:
		# print(line)
		# linepos = pos_tag(word_tokenize(line))
		linener,linepos = StanfordNERPOS(line)
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
	return [gram,gram_count]

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
	print("IR processing")
	# irresult = search(MY_SEARCH_FILE,QUERY)
	irresult = answerlist
	QUERY = query


	#Preprocess irresult
	pro_data = ProcessData(irresult)
	# WriteFile(pro_data,"irresult.txt")
	# for onesample in pro_data:
	# 	print(ne_chunk(pos_tag(word_tokenize(onesample))))
	# 	print(pos_tag(word_tokenize(onesample)))


	# Genrate the ngram first
	print("Generating N-gram")
	n = N_GRAM #The number of grams it will use, begin with unigram
	# file = open("processed_data.txt")
	# file = open("ptb.2-21.txt")
	# ss = file.readline().strip()
	# ss = file.readline().strip().lower()
	doc = []
	gram = []
	grampos = {}
	gramner = {}
	for ss in pro_data:
		doc .append(ss)
		# ss = file.readline().strip()
		# ss = file.readline().strip().lower()
	for i in range(n):
		tmpgram,tmpcount = GenerateNGram(i+1,doc,grampos,gramner)
		gram.append(tmpgram)
	# print(grampos)
	# print(gram)


	# Voting: Calculate the score for every snippet
	print("Voting.")
	score = []
	for i in range(n):
		for k,v in gram[i].items():
			score.append([k,v])
	score = sorted(score,key=lambda onescore:onescore[1], reverse = True)
	# WriteFile(score,"voteresult.txt")
	# print(score)


	# General Filtering 
	print("Filter process.")
	score = CommonFilter(QUERY,score)
	myfilter = MyFilter()
	score = myfilter.Filter(score,QUERY,grampos,gramner)
	# print(score)

	#Combination
	print("Combination.")
	combination = []
	for tup in score:
		word = tup[0]
		arr = word.split(symbol)
		tmpscore = tup[1]
		for i in range(len(arr)):
			tmpscore += gram[0][arr[i]]
		combination.append([word,tmpscore])
	combination = sorted(combination, key=lambda tup:tup[1],reverse = True)
	# WriteFile(combination,"Combination.txt")

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
	answer_phrase = combination[0][0].split(symbol)
	# print(combination[0:11])
	return answer_phrase
	# WriteFile(combination,"finalresult.txt")

if __name__ == "__main__":
	QUERY = "Who is Dempsey ?"
	MY_SEARCH_FILE = "../data/set1/a1.txt"
	answerlist = search(MY_SEARCH_FILE,QUERY)
	print(NGramTiling(QUERY,answerlist))







