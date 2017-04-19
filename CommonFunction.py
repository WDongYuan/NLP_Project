from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from sets import Set
from pycorenlp import StanfordCoreNLP
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

def StanfordNERPOS(sentence):
	# print("Connect to the port: 53510")
	nlp = StanfordCoreNLP('http://localhost:9000')
	# print("Port connected: 53510")
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,ner','outputFormat':'json'})
	# print(output)
	ner = []
	pos = []
	for token in output['sentences'][0]['tokens']:
		ner.append([token['word'].encode('ascii', 'ignore'),token['ner'].encode('ascii', 'ignore')])
		pos.append([token['word'].encode('ascii', 'ignore'),token['pos'].encode('ascii', 'ignore')])
	return ner,pos

def QueryClassification(query):
		queryarr = MyTokenize(query)
		ner,pos = StanfordNERPOS(query)
		if queryarr[0].lower()=="who":
			beV = Set(["is","are","was","were"])
			if queryarr[1] in beV and ner[2][1]=="PERSON":
				return "PERSON_ENTITY"
			else:
				return "PERSON"
		elif queryarr[0].lower()=="when":
			return "TIME"
		elif queryarr[0].lower()=="where":
			return "LOCATION"
		elif queryarr[0].lower()=="what":
			dep = StanfordDependency(query)
			for onedep in dep:
				do = ["do","did","done"]
				if onedep["dep"]=="dobj" and onedep["dependentGloss"].lower()=="what":
					if onedep["governorGloss"].lower() in do:
						return "DO_VP"
					return "DO_NP"
				elif onedep["dep"]=="det" and onedep["dependentGloss"].lower()=="what":
					if onedep["governorGloss"].lower()=="time":
						return "TIME"
					else:
						return "DO_NP"
		elif queryarr[0].lower()=="why":
			return "REASON"
		elif queryarr[0].lower()=="how":
			dep = StanfordDependency(query)
			ner,pos = StanfordNERPOS(query)
			bev = ["is","was","are","were"]
			if pos[1][0] in bev:
				return "HOW_JJ"
			howprase = ""
			for onedep in dep:
				if onedep['dep']=="advmod" and onedep["dependentGloss"].lower()=="how":
					howprase = onedep["governorGloss"]
			for onepos in pos:
				if onepos[0]==howprase and onepos[1][0]=="V":
					return "HOW_ADV"
				elif onepos[0]==howprase and onepos[1]=="JJ":
					return "HOW_DEGREE"


		# elif queryarr[0].lower()=="how":

		return None
def StanfordDependency(sentence):
	nlp = StanfordCoreNLP('http://localhost:9000')
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,depparse','outputFormat':'json'})
	dep = output['sentences'][0]["basicDependencies"]
	# for tmpdep in dep:
	# 	print(tmpdep)
	return dep

def StanfordStemmer(sentence):
	nlp = StanfordCoreNLP('http://localhost:9000')
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,lemma','outputFormat':'json'})
	stem = []
	for token in output['sentences'][0]['tokens']:
		stem.append([token['word'].encode('ascii', 'ignore'),token['lemma'].encode('ascii', 'ignore')])
	return stem