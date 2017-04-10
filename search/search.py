# If on Python 2.X
from __future__ import print_function
import pysolr
import re
import sys
from nltk.tokenize import sent_tokenize,blankline_tokenize
import itertools


def search(file,query):
    # Setup a Solr instance. The timeout is optional.
    solr = pysolr.Solr('http://localhost:8983/solr/gettingstarted/', timeout=10)
    with open(file,"r") as f:
        text=f.read()
        paragraphs=blankline_tokenize(text.decode("utf8"))
        for i in range(len(paragraphs)):
            paragraphs[i]=sent_tokenize(paragraphs[i])
        sentences=list(itertools.chain(*paragraphs))
        del paragraphs
    # How you'd index data.
    for i in range(len(sentences)):
        index={'id':str(i),"_text_":sentences[i]}
        solr.add([index])
    # Note that the add method has commit=True by default, so this is
    # immediately committed to your index.

    # Later, searching is easy. In the simple case, just a plain Lucene-style
    # query is fine.
    results = solr.search(query)
    # The ``Results`` object stores total results found, by default the top
    # ten most relevant results and any additional data like
    # facets/highlighting/spelling/etc.
    print("Saw {0} result(s).".format(len(results)))
    # for result in results:
    #     print(result)

    searchresult = []
    # Just loop over it to access the results.
    for result in results:
        # print("The title is '{0}'.".format(result['id']))
        print(sentences[int(result['id'])])
        searchresult.append(sentences[int(result['id'])])
    return searchresult

if __name__=="__main__":
    # document=sys.argv[1]
    document = "text.txt"
    question="Who is an England soccer player?"
    search(document,question)