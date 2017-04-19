from nltk import word_tokenize, pos_tag, ne_chunk
from pycorenlp import StanfordCoreNLP
def StanfordNERPOS(sentence):
	nlp = StanfordCoreNLP('http://localhost:9000')
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,ner,depparse','outputFormat':'json'})
	dep = output['sentences'][0]["basicDependencies"]
	for tmpdep in dep:
		print(tmpdep)

	ner = []
	pos = []
	for token in output['sentences'][0]['tokens']:
		ner.append([token['word'].encode('ascii', 'ignore'),token['ner'].encode('ascii', 'ignore')])
		pos.append([token['word'].encode('ascii', 'ignore'),token['pos'].encode('ascii', 'ignore')])
	return ner,pos

def QuestionType(query):
	nlp = StanfordCoreNLP('http://localhost:9000')
	# qpos = pos_tag(word_tokenize(query))
	# print(ne_chunk(qpos))
	#Question about person
	# if qpos[0][0].lower()=="who":
	# print(qpos)
	text = (query)
	output = nlp.annotate(text,properties={'annotators':'tokenize,pos,ner','outputFormat':'json'})
	# print(output['sentences'][0]['ner'])
	# print(output)
	for one in output['sentences'][0]['tokens']:
		print(one['ner'])
# QuestionType("Who did this to make the teacher happy?")
sentence = "Clinton Drew \"Clint\" Dempsey (born March 9, 1983) is an American "+\
			"professional soccer player who plays for Seattle Sounders FC in Major "+\
			"League Soccer and has served as the captain of the United States national team."
sentence = "He won the highest individual honor in football in America when he was named"+\
			" Honda Player of the Year for 2006, beating Fulham teammates Kasey Keller and"+\
			" Brian McBride in a poll of sportswriters."
sentence = "What did he play in England on Sunday?"
# sentence = "What is Linear Regression?"
sentence = "What course do you like to take?"
sentence = "What is the weather like in Beijing?"
sentence = "What do you want to buy?"
sentence = "What did you do in England"
result = StanfordNERPOS(sentence)
for row in result:
	for word in row:
		print(word[0]+"("+word[1]+")"),
	print("")