import nltk
from nltk.corpus import treebank
import matplotlib.pyplot as plt
sentence = "At eight o'clock on Thursday morning"
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
# print(tagged)
t = treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()