from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from common_filter import CommonFilter
from sets import Set
import CommonFunction as cf
symbol = "_"
INFINITY = 1000000
class MyFilter:

	
		
	def Filter(self,candidate,query,grampos,gramner):
		queryclass = cf.QueryClassification(query)
		result = []
		if queryclass=="PERSON":
			candidate = CommonFilter(query,candidate)
			for gram in candidate:
				if self.IsName(gram[0],grampos,gramner) or self.IsPerson(gram[0],grampos,gramner):
						result.append(gram)
		elif queryclass=="PERSON_ENTITY":
			candidate = CommonFilter(query,candidate)
			for gram in candidate:
				if self.IsPerson(gram[0],grampos,gramner):
						result.append(gram)
		elif queryclass=="TIME":
			candidate = CommonFilter(query,candidate)
			# print(candidate)
			for gram in candidate:
				if self.IsTime(gram[0],grampos,gramner):
					result.append(gram)
		elif queryclass=="LOCATION":
			candidate = CommonFilter(query,candidate)
			for gram in candidate:
				if self.IsLocationOrganization(gram[0],grampos,gramner):
					result.append(gram)
		# elif queryclass=="LOCATION":
		# 	candidate = CommonFilter(query,candidate)
		# 	for 
		return result

	def IsLocationOrganization(self,gram,grampos,gramner):
		arr = gram.split(symbol)
		pos = grampos[gram].split(symbol)
		ner = gramner[gram].split(symbol)
		if ner[-1]=="LOCATION" or ner[-1]=="ORGANIZATION":
			return True
		else:
			return False
		





	def IsName(self,gram,grampos,gramner):
		arr = gram.split(symbol)
		pos = grampos[gram].split(symbol)
		ner = gramner[gram].split(symbol)
		for i in range(len(arr)):
			word = arr[i]
			if word=="":
				return False
			if not word[0].isupper() or ner[i]!="PERSON":
				return False
		return True

	def IsPerson(self,gram,grampos,gramner):
		arr = gram.split(symbol)
		pos = grampos[gram].split(symbol)
		if pos[-1][0]!="N":
			return False
		word = arr[-1]
		if word[0].isupper():
			return False
		syn = wn.synsets(word)
		# print(syn)
		if len(syn)==0:
			return False
		syn = syn[0]
		hyperpath = syn.hypernym_paths()
		# print(hyperpath)
		for onehyperpath in hyperpath:
			for onehyper in onehyperpath:
				obj = onehyper.name().split(".")[0]
				if obj=="person":
					return True
		return False

	def IsTime(self,gram,grampos,gramner):
		pos = grampos[gram].split(symbol)
		ner = gramner[gram].split(symbol)
		gram = gram.split(symbol)
		if ner[-1]=="TIME" or ner[-1]=="DATE":
			return True
		return False




	##Keyword distance measurement.
	
	def QueryKeyword(self,query):
		stopWords = Set(stopwords.words('english'))
		pos = cf.SentencePOS(query)
		pp = 0
		while pp<len(pos):
			if pos[pp][1][0]!="N" and pos[pp][1][0]!="V":
				pos.pop(pp)
			elif pos[pp][0] in stopWords:
				pos.pop(pp)
			else:
				pp += 1
		keyword = [pos[i][0] for i in range(len(pos))]
		return Set(keyword)

	def GramQueryDst(self,gram,qWordList,senTokens):
		gramWord = gram.split(symbol)
		idxs = [i for i in range(len(senTokens)) if senTokens[i]==gramWord[0]]
		if idxs == 0:
			return [0,0]
		position = []
		for idx in idxs:
			if idx+len(gramWord)-1>=len(senTokens):
				continue
			head = idx
			end = -1
			matchFlag = True
			for i in range(len(gramWord)):
				if matchFlag and gramWord[i] != senTokens[head+i]:
					matchFlag = False
			if matchFlag:
				end = head+len(gramWord)-1
				position.append([head,end])
		# print(gram+":"+str(senTokens))
		# print(position)

		qWordIdx = {}
		for word in qWordList:
			for i in range(len(senTokens)):
				if senTokens[i]==word:
					if word not in qWordIdx:
						qWordIdx[word] = []
					qWordIdx[word].append(i)
		# print(qWordIdx)

		minDst = INFINITY
		for onePos in position:
			tmpWholeMin = 0
			for qWord,idxs in qWordIdx.items():
				tmpMinDst = INFINITY
				for idx in idxs:
					if idx<onePos[0] and tmpMinDst>(onePos[0]-idx):
						tmpMinDst = onePos[0]-idx
					elif idx>onePos[1] and tmpMinDst>(idx-onePos[1]):
						tmpMinDst = idx-onePos[1]
				tmpWholeMin += tmpMinDst
			if minDst>tmpWholeMin:
				minDst = tmpWholeMin
		# print(minDst)
		if minDst==0:
			minDst = INFINITY	

		return [len(qWordIdx),minDst]

	def KeyWordDistance(self,candidateList,answerList, query,wordstem):
		qKeyWord = self.QueryKeyword(query)
		#Get the stem of qKeyWord
		qKeyWord = [wordstem[tmpw] for tmpw in qKeyWord]

		# print(len(qKeyWord))
		for oneCom in candidateList:
			gram = oneCom[0]
			keyWordNum,keyWordDst = 0,0
			for sen in answerList:
				senTokens = cf.MyTokenize(sen)
				#Get the stem for a candidate sentence
				senTokens = [wordstem[senTokens[i]] for i in range(len(senTokens)) if senTokens[i] in wordstem]

				nn,dd = self.GramQueryDst(gram,qKeyWord,senTokens)
				if nn>keyWordNum and dd!=INFINITY:
					keyWordNum = nn
					keyWordDst = dd
				elif nn==keyWordNum and keyWordDst>dd:
					keyWordNum = nn
					keyWordDst = dd
			oneCom.append([keyWordNum,keyWordDst])
		candidateList = candidateList
		candidateList = sorted(candidateList,cmp=cf.MyCompare1)
		return candidateList







	def TestIsPerson(self,gram):
		arr = gram.split(symbol)
		word = arr[-1]
		syn = wn.synsets(word)
		# print(syn)
		if len(syn)==0:
			return False
		syn = syn[0]
		hyperpath = syn.hypernym_paths()
		print(hyperpath)
		for onehyperpath in hyperpath:
			for onehyper in onehyperpath:
				obj = onehyper.name().split(".")[0]
				if obj=="person":
					return True
		return False

# myfilter = PersonFilter()
# print(myfilter.TestIsPerson('profile'))
# syn = wn.synsets('professor')[0]
# print(syn.name())
# print(syn.hypernym_paths())

