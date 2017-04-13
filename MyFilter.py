from nltk.corpus import wordnet as wn
symbol = "_"
class MyFilter:

	def QueryClassification(self,query):
		queryarr = query.split(" ")
		if queryarr[0].lower()=="who":
			return "PERSON"
		elif queryarr[0].lower()=="when":
			return "TIME"
		return None
		
	def Filter(self,candidate,query,grampos,gramner):
		queryclass = self.QueryClassification(query)
		result = []
		if queryclass=="PERSON":
			for gram in candidate:
				if self.IsName(gram[0],grampos,gramner) or self.IsPerson(gram[0],grampos,gramner):
						result.append(gram)
		elif queryclass=="TIME":
			for gram in candidate:
				if self.IsTime(gram[0],grampos,gramner):
					result.append(gram)
		return result

		





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

