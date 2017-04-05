import common_filter
import math
symbol = "_"
query = "Who is an England soccer player ?"
# query = query.lower()#Convert query to lower case
def GenerateNGram(n,doc):
	gram = {}
	gram_count = 0
	for line in doc:
		for i in range(len(line)-n+1):
			tup = ""
			for j in range(n):
				tup += line[i+j]
				if j!=n-1:
					tup += symbol
			if tup not in gram:
				gram[tup] = 0
			gram[tup] += 1
			gram_count += 1
	return [gram,gram_count]

# Genrate the ngram first
n = 2 #The number of grams it will use, begin with unigram
file = open("processed_data.txt")
# file = open("ptb.2-21.txt")
ss = file.readline().strip()
# ss = file.readline().strip().lower()
doc = []
gram = []
while ss!="":
	doc .append(ss.split(" "))
	ss = file.readline().strip()
	# ss = file.readline().strip().lower()
for i in range(n):
	gram.append(GenerateNGram(i+1,doc)[0])
# print(gram)

# Voting: Calculate the score for every snippet
score = []
for i in range(n):
	for k,v in gram[i].items():
		score.append([k,v])
score = sorted(score,key=lambda onescore:onescore[1], reverse = True)
# print(score)

# General Filtering 
score = common_filter.RemoveStopWord(query,score)
score = common_filter.RemoveQueryWord(query,score)
# print(score)

#Combination
combination = []
for tup in score:
	word = tup[0]
	arr = word.split(symbol)
	tmpscore = tup[1]
	for i in range(len(arr)):
		tmpscore += gram[0][arr[i]]
	combination.append([word,tmpscore])
combination = sorted(combination, key=lambda tup:tup[1],reverse = True)
# print(combination)

#Read Document Frequency
file = open("./data/doc_frequency.txt")
docmunet_count = int(file.readline().strip().split(" ")[1])
frequency = {}
ss = file.readline().strip()
word_in_corpus = 0
while ss!="":
	arr = ss.split(" ")
	frequency[arr[0]] = int(arr[1])
	word_in_corpus += int(arr[1])
	ss = file.readline().strip()

#Score
for tup in combination:
	arr = tup[0].split(symbol)
	tmpsum = 0
	for i in range(len(arr)):
		df = 0
		if arr[i] not in frequency:
			df = 1
		else:
			df = frequency[arr[i]]
		tmpsum += math.log(float(docmunet_count)/df)
	tup[1] = tup[1]*1.0/len(arr)*tmpsum
combination = sorted(combination, key=lambda tup:tup[1],reverse = True)
print(combination)






