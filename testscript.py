import CommonFunction as cf
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from sets import Set
from pycorenlp import StanfordCoreNLP
from nltk.stem.wordnet import WordNetLemmatizer
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
print(cf.StanfordStemmer(Q))
# print(nf.StanfordDependency(Q))
# print(nf.QueryClassification(Q))
# print(nf.StanfordNERPOS(Q))