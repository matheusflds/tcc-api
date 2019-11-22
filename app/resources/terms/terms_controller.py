from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from datetime import datetime
from math import log

from .term_model import TermDBModel
from data_fetch.get_tweet import get_tweets
from topic_modelling.topic_model import TopicModel

class TermList(Resource):
  MAX_TIMESTAMP_DIFF = 2826090

  parser = reqparse.RequestParser()
  parser.add_argument('term_text', required=True, help='This field cannot be left empty')

  def get(self):
    terms = [[term.text, self._calculate_weight(term)] for term in TermDBModel.query.all()]
    if terms:
      return jsonify({ 'terms': terms })

    return make_response(jsonify({
      'message': 'Terms not found',
    }), 404) 

  def post(self):
    dataset_dir = 'datasets'
    req_data = TermList.parser.parse_args()
    query = req_data['term_text']

    term_df = get_tweets(query, save_dir=dataset_dir, max_requests=100, count=100)
    if term_df is None:
      return make_response(jsonify({
        'message': 'Unable to find tweets'
      }), 500)
  
    topic_model = TopicModel(term_df, term=query)
    topics, term_df = topic_model.get_topics()

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
