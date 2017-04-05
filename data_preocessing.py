from sets import Set
import re
file = open("data.txt")
# file = open("ptb.2-21.txt")
ss = file.readline().strip()
newfile = open("processed_data.txt","w+")
puntuation = Set([",",".",":"])
while ss!="":
	ss = re.split(r'\s',ss)
	tmps = []
	for word in ss:
		if word[len(word)-1] in puntuation:
			# tmps.append(word[0:len(word)-1].lower())
			tmps.append(word[0:len(word)-1])
			tmps.append(word[len(word)-1])
		else:
			# tmps.append(word.lower())
			tmps.append(word)
	newss = " ".join(tmps)
	newfile.write(newss+"\n")
	ss = file.readline().strip()

