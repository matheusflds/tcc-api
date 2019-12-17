import os
import re
import gensim
import pandas as pd

from pathlib import Path
from nlp.utils import preprocess
from operator import itemgetter

class TopicModel:
  def __init__(self, dataframe, term, num_workers=3):
    self.dataframe = dataframe
    self.term = term
    self.num_workers = num_workers

  def get_topics(self, count=5):
    self.dataframe['cleaned'] = preprocess(self.dataframe.text, lemmatization=True, no_emoji=True, no_special_words=True)
    self.num_topics = count

    tokenized_documents = [tweet.split() for tweet in self.dataframe.cleaned]
    bigram = gensim.models.Phrases(tokenized_documents, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    bigrams = [bigram_mod[doc] for doc in tokenized_documents]

    dictionary = gensim.corpora.Dictionary(bigrams)
    dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in bigrams]

    self.model = gensim.models.ldamulticore.LdaMulticore(bow_corpus, 
                                                         num_topics=self.num_topics, 
                                                         id2word=dictionary,                                    
                                                         passes=10,
                                                         workers=self.num_workers,
                                                         chunksize=100,
                                                         iterations=400)
    topics = [(topic[0], re.findall(r'(\d\.\d+)\*"(.*?)"', topic[1])) for topic in self.model.print_topics()]
    topics = [(topic[0], list(map(lambda x: (round(1000 * float(x[0])), x[1]), topic[1]))) for topic in topics]
    document_topics = [self._get_document_topic(doc) for doc in bow_corpus]
    self.dataframe['topic'] = document_topics

    return (topics, self.dataframe)

  def _get_document_topic(self, document):
    topics = self.model.get_document_topics(document)
    topic = max(topics, key=itemgetter(1))
    return topic[0]
