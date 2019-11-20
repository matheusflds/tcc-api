from flask_restful import Resource, reqparse
from flask import jsonify
from datetime import datetime
from math import log

from models import TermModel
from data_fetch.get_tweet import get_tweets

class Terms(Resource):
  MAX_TIMESTAMP_DIFF = 2826090

  parser = reqparse.RequestParser()
  parser.add_argument('term_text', required=True, help='This field cannot be left empty')

  def get(self):
    terms = [[term.text, self._calculate_weight(term)] for term in TermModel.query.all()]
    if terms:
      return jsonify({ 'terms': terms })
    return {
      'message': 'Terms not found',
      'code': '404'
    }

  def post(self):
    req_data = Terms.parser.parse_args()
    query = req_data['term_text']
    # term_df = get_tweets(query, save_dir='datasets', max_requests=100, count=100)
    term_df = get_tweets(query, save_dir='datasets', max_requests=1, count=10)
    if term_df is not None:
      print(term_df.head())
    else:
      print('aaaaaa')
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
