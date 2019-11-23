import pandas as pd

from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from datetime import datetime
from math import log

from .term_repository import TermRepository
from .term_model import term_states
from data_fetch.get_tweet import get_tweets
from topic_modelling.topic_model import TopicModel
from sentiment_analysis.model import SAModel 
from emotion_recognition.model import LstmConvModel

class TermList(Resource):
  MAX_TIMESTAMP_DIFF = 2826090

  parser = reqparse.RequestParser()
  parser.add_argument('term_text', required=True, help='This field cannot be left empty')

  def get(self):
    terms = [[term.text, self._calculate_weight(term)] for term in TermRepository.get_all()]
    if terms:
      return jsonify({ 'terms': terms })

    return make_response(jsonify({
      'message': 'Terms not found',
    }), 404) 

  def post(self):
    dataset_dir = 'datasets'
    req_data = TermList.parser.parse_args()
    query = req_data['term_text']
    term = TermRepository.insert({ 'text': query })

    if term.processing_status is term_states[1]:
      return jsonify({ 
        'message': 'Term is being processed' 
      })
    elif term.processing_status is term_states[2]:
      return jsonify({ 
        'message': 'Term already processed' 
      })

    term.processing_status = term_states[1]
    TermRepository.save_changes(term)
    term_df = get_tweets(query, save_dir=dataset_dir, max_requests=100, count=100)
    if term_df is None:
      return make_response(jsonify({
        'message': 'Unable to find tweets'
      }), 500)
  
    topic_model = TopicModel(term_df, term=query)
    topics, term_df = topic_model.get_topics()

    # Ponto de atenção: o dataframe foi preprocessado com parametros diferentes se não me engano
    polarity_df = SAModel.predict(term_df.cleaned)
    emotions_df = LstmConvModel.predict(term_df.cleaned)
    term_df = pd.concat([term_df, polarity_df, emotions_df], axis=1)

    statistics_df = term_df.groupby('topic').agg({
      'polarity': 'mean',
      'joy': 'mean',
      'anger': 'mean',
      'fear': 'mean',
      'sadness': 'mean',
      'topic': 'count'
    })

    topics = [self._get_topic_detail(topic[1], statistics_df.loc[topic[0]]) for topic in topics]
    term = TermRepository.add_topics(term, topics)
    
    print(term_df.head())
    print(topics)
    print(statistics_df)

    term.processing_status = term_states[2]
    TermRepository.save_changes(term)

    return jsonify({ 
      'message': 'Succesfully processed tweets for specified term' 
    })


  def _calculate_weight(self, term):
    current = datetime.timestamp(datetime.now())
    term_updated_date = datetime.timestamp(term.updated_at)
    delta = current - term_updated_date

    if delta > self.MAX_TIMESTAMP_DIFF:
      return 0.5
    elif delta <= 1000:
      return 10
    return (-9.5 * delta / self.MAX_TIMESTAMP_DIFF) + 10

  def _get_topic_detail(self, topic, statistics):
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
