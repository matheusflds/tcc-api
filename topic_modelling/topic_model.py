import os
import re
import gensim
import pandas as pd
from pathlib import Path
from nlp.dataset import Dataset

class TopicModel:
  def __init__(self, save_path, num_workers=5):
    self.save_path = save_path
    self.num_workers = num_workers

  def get_topics(self, query, count=6):
    preprocessed_docs = self.get_preprocessed_docs(query);
    if preprocessed_docs is None:
      return None

    bow_corpus, dictionary = preprocessed_docs
    model = gensim.models.ldamulticore.LdaMulticore(bow_corpus, 
                                                    num_topics=count, 
                                                    id2word=dictionary,                                    
                                                    passes=10,
                                                    workers=self.num_workers,
                                                    chunksize=100,
                                                    iterations=400)
    topics_words = self.get_topics_words(model.print_topics())
    return topics_words

  def get_preprocessed_docs(self, query):
    FILES_DIR = Path(self.save_path).resolve()
    dir_list = os.listdir(FILES_DIR)
    filename = [filename for filename in dir_list if query in filename]
    if filename:
      dataset = Dataset('{}/{}'.format(self.save_path, filename[0]))
      dataset.load()
      dataset.preprocess_texts(lemmatization=True, no_emoji=True)
      tokenized_documents = [tweet.split() for tweet in dataset.dataframe.cleaned]
      dictionary = gensim.corpora.Dictionary(tokenized_documents)
      dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)
      bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized_documents]
      return (bow_corpus, dictionary)
    else:
      print('Unable to find dataset for "{}"'.format(query))
      return None

  def get_topics_words(self, topics):
    return [re.findall(r'(\d+\.?\d*)\*"(\w*)"', topic[1]) for topic in topics]
