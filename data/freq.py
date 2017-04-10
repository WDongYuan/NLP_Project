from sets import Set
import re


dic = {}
punctuation = Set([",",".",":","\"","(",")","[","]",";","\'"])
count = 0
sentence = []
alldata = open("alldata.txt","w+")
for i in range(1,5):
	for j in range(1,11):
		file = open("./set"+str(i)+"/a"+str(j)+".txt")
		# file = open("ptb.2-21.txt")
		doc = ""
		ss = file.readline()
		alldata.write(ss+"\n")
		while ss!="":
			ss = ss.strip()
			doc = doc+"."+ss
			ss = file.readline()
			alldata.write(ss+"\n")
		sentence.append(doc)
		file.close()
alldata.close()

for i in range(1000):
	path = "./nyt/file"+str(i)+".txt"
	file = open(path)
	sentence.append(file.readline().strip())
	file.close()


for ss in sentence:
	wordset = Set([])
	ss = re.split(r'\s',ss)
	tmps = []
	for word in ss:
		if word=="":
			continue
		while len(word)!=1 and word[len(word)-1] in punctuation:
			count += 1
			pun = word[len(word)-1]
			# if pun not in dic:
			# 	dic[pun] = 0
			# dic[pun] += 1
			wordset.add(pun)
			word = word[0:len(word)-1]
		while len(word)!=1 and word[0] in punctuation:
			count += 1
			pun = word[0]
			# if pun not in dic:
			# 	dic[pun] = 0
			# dic[pun] += 1
			wordset.add(pun)
			word = word[1:len(word)] 
		count += 1
		# if word not in dic:
		# 	dic[word] = 0
		# dic[word] += 1
		wordset.add(word)
	for w in wordset:
		if w not in dic:
			dic[w] = 0
		dic[w] += 1

# Smoothing
for k,v in dic.items():
	dic[k] += 1
dic["UNKNOWN_WORD"] = 1

file = open("doc_frequency.txt","w+")
file.write("Document_count "+str(len(sentence))+"\n")
for k,v in dic.items():
	file.write(k+" "+str(v)+"\n")
print(count)