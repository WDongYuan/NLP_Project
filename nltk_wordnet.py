from __future__ import print_function
from nltk.corpus import wordnet as wn
from sets import Set
import nltk
# syn = wn.synsets("Shanghai")
# print(syn)
# for lemma in syn[0].lemmas():
# 	print(lemma.name())
# # for synset in syn:
# # 	print(synset)
# nltk.help.upenn_tagset('RB')
# tokens = nltk.word_tokenize("He takes off his coat.")
# pos = nltk.pos_tag(tokens)
# print(pos)
# sent = "The Washington Monument is the most prominent structure "+\
#  "in Washington, D.C. and one of the city's early attractions. "+\
#  "It was built in honor of George Washington, who led the country "+\
#  "to independence and then became its first President."
# sent = "What is the location of Police Station?"
# sent = "Where is your children's high school?"
sent =  "When did you begin to study in Paris?"
# print(nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)),binary=True))
pos = nltk.pos_tag(nltk.word_tokenize(sent))
# print(pos)
# print(wn.synsets("high"))
query = ""
for onetag in pos:
	if onetag[1][0] == "N" or onetag[1][0] == "J":
		noun = onetag[0]
		syn = wn.synsets(noun)
		synset = Set([onetag[0].lower()])
		for i in range(len(syn)):
			if (syn[i].name().split(".")[1]=="n" and onetag[1][0] == "N") or \
			(syn[i].name().split(".")[1]=="a" or syn[i].name().split(".")[1]=="s" and onetag[1][0] == "J"):
				word = syn[i].name().split(".")[0].lower()
				if word not in synset:
					synset.add(word)
			# if syn[i].name().split(".")[1]=="s":
			# 	print(syn[i].definition())
		synset = list(synset)
		for i in range(len(synset)):
			if i==0:
				query += "("
			query += synset[i]
			if i!=len(synset)-1:
				query += "|"
			else:
				query += ") "
	else:
		query += (onetag[0]+" ")
print(query)
