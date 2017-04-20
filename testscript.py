from __future__ import print_function
import CommonFunction as cf
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from sets import Set
from pycorenlp import StanfordCoreNLP
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
import re

Q = "What can you do for solving this problem?"
# Q = "What did you do in this summer?"
# Q = "What have you done for the final exam?"
Q = "What is Machine Learning?"
Q = "What did he learning in the summer?"
Q = "What kind of drink would you like?"
# Q = "What time is it?"
Q = "What food would you like?"
Q = "How tall is Dempsey?"
Q = "How do you go to school?"
Q = "How do you finish the homework?"
# Q = "How is the weather today?"
Q = "How many goal did he make in 2017?"
Q = "How is the movie?"
Q = "When did he retired?"
Q = "I married Mary in 2012."
Q = "Who is Mountains?"
# print(stemmer.lemmatize("retired"))
# print(cf.StanfordStemmer(Q))
sentence = "He was active in the revolutionary movements of 1821 against the king of Sardinia "+\
"(who became ruler of Piedmont with Turin as his capital). "
Q = "How long was Lincoln's formal education?"
Q = "What is the smallest suborder of turtles?"
Q = "What did Jefferson call John Adams?"
Q = "What caused Calvin Jr.'s death?"
Q = "What do people commonly call cleptoparasitic bees?"
Q = "What kind of drink do you like?"
Q = "What animal can climb the trees?"
# Q = "What information do you have?"
sentence = "Dabbling ducks feed on the surface of water or on land, or as deep as they can reach by up-ending without completely submerging."
Q = "What kind of ducks feed on land?"
Q = "What Roman province was Liechtenstein part of?"
Q = "What do most recognizable international company and largest employer have in common?"
Q = "What years were Coolidge's two sons born in?"
Q = "What shares land borders with Papua New Guinea, East Timor and Malaysia?"
Q = "What district was Ford elected from?"
Q = "What is the nickname of Theodore Roosevelt's sister Anna?"
Q = "What is the largest ethnic minority in Romania?"
Q = "What is an otter's den called?."
Q = "Which nation invaded Singapore during World War II?"
Q = "What kind of animal do you like?"
Q = "Which spice originally attracted Europeans to Indonesia?"
Q = "Which temperature scale did Celsius propose?"
Q = "Which part of the strings does the left hand touch?"
Q = "Which country are you from?"
Q = "How long do most foxes live?"
Q = "How do you go to school?"
Q = "How would you go to school?"
Q = "How long does he live?"

sentence = "The place where we live is Earth."
sentence = "The collective noun for kangaroos is a mob, troop, or court."
sentence = "Celsius founded the Uppsala Astronomical Observatory in 1741, and "+\
"in 1742 he proposed the Celsius temperature scale in a paper to the Royal Swedish Academy of Sciences."
sentence = "The 1970 Bhola cyclone devastated much of the region, killing an estimated 500,000 people."

dep = cf.StanfordDependency(Q)
for sample in dep:
	print(sample)
print(cf.QueryClassification(Q))
print('Celsius'.isalpha())
ner,pos = cf.StanfordNERPOS(sentence)
print(pos)
# print("")
# sentence = "What did he finish?"
# dep = cf.StanfordDependency(sentence)
# for sample in dep:
# 	print(sample)
# print(nf.QueryClassification(Q))
# print(nf.StanfordNERPOS(Q))
# nlp = StanfordCoreNLP('http://localhost:9000')
# output = nlp.annotate(sentence,properties={'annotators':'tokenize,pos,parse','outputFormat':'json'})
# print(output)
# tree = output["sentences"][0]["parse"].encode("ascii","ignore")
# # print(tree.split(re"\n| \s"))
# tree = re.split("\s",tree)
# for node in tree:
# 	if node=="":
# 		continue
# 	print(node,end=" ")


# print(tree.split("\n"))
# print(tree[0:100])

# parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
# tree = list(parser.raw_parse(Q))[0][0]
# print(tree)

