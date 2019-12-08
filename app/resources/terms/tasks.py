import time
import pandas as pd
import wikipedia 

from flask import jsonify, make_response

from app import create_app
from .term_repository import TermRepository
from .term_model import term_states
from data_fetch.get_tweet import get_tweets
from topic_modelling.topic_model import TopicModel
from machine_learning.sentiment_analysis import SentimentAnalysis

app = create_app()
app.app_context().push()

def process_term(query, id):
  print('Starting Task: Processing term "{}"'.format(query))

  dataset_dir = 'datasets'
  term = TermRepository.get(id)
  term.processing_status = term_states[1]
  TermRepository.save_changes(term)
  term_df = get_tweets(query, save_dir=dataset_dir, max_requests=100, count=100)
  if term_df is None:
    print('Unable to find tweets')
    return

  topic_model = TopicModel(term_df, term=query)
  topics, term_df = topic_model.get_topics()

  term_df = term_df[~term_df.text.str.contains('http')]
  sentiment_df = SentimentAnalysis.process(term_df.text)
  term_df = pd.concat([term_df, sentiment_df], axis=1)

  statistics_df = term_df.groupby('topic').agg({
    'polarity': 'mean',
    'joy': 'mean',
    'anger': 'mean',
    'fear': 'mean',
    'sadness': 'mean',
    'topic': 'count'
  })
  overview_df = statistics_df.mean()
  topics = [_get_topic_detail(topic[1], statistics_df.loc[topic[0]]) for topic in topics]

  term.polarity = overview_df['polarity']
  term.joy = overview_df['joy']
  term.anger = overview_df['anger']
  term.fear = overview_df['fear']
  term.sadness = overview_df['sadness']

  term.tweet_count = int(statistics_df.agg({ 'topic': ['sum'] }).iloc[0,0])
  term.description = _get_term_definition(query)
  term.processing_status = term_states[2]
  TermRepository.add_topics(term, topics)

  print('Task completed')

def _get_topic_detail(topic, statistics):
  probabilities, words = zip(*topic)
  return {
    'words': words,
    'words_probability': probabilities,
    'polarity': statistics.polarity,
    'joy': statistics.joy,
    'anger': statistics.anger,
    'fear': statistics.fear,
    'sadness': statistics.sadness
  }

def _get_term_definition(term):
  try:
    definition = wikipedia.summary(term, sentences=1)
    return definition
  except wikipedia.exceptions.DisambiguationError as e:
    return wikipedia.summary(e.options[0], sentences=1)
  except wikipedia.exceptions.PageError:
    return 'No description available'