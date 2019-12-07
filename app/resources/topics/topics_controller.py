from flask_restful import Resource, reqparse
from flask import jsonify, make_response

from ..terms.term_repository import TermRepository
from .topic_model import TopicDBModel

class Topics(Resource):
  def __init__(self):
    self.regparser_get_args = reqparse.RequestParser()

    self.regparser_get_args.add_argument('id', type=int, required=True, location='args')

  def get(self):
    req_data = self.regparser_get_args.parse_args()
    id = req_data['id']
    term = TermRepository.get(id)
    if not term:
      return make_response(jsonify({
        'message': 'Terms not found',
      }), 404)

    response = {
      'term': term.text,
      'tweetCount': term.tweet_count,
      'description': term.description,
      'overallResults': {
        'polarity': self._to_percent(term.polarity),
        'joy': self._to_percent(term.joy),
        'anger': self._to_percent(term.anger),
        'fear': self._to_percent(term.fear),
        'sadness': self._to_percent(term.sadness)
      },
      'topics': [
        {
          'words': list(zip(topic.words, topic.words_probability)),
          'polarity': self._to_percent(topic.polarity),
          'joy': self._to_percent(topic.joy_percentage),
          'anger': self._to_percent(topic.anger_percentage),
          'fear': self._to_percent(topic.fear_percentage),
          'sadness': self._to_percent(topic.sad_percentage),
        } for topic in term.topics
      ]
    }

    return jsonify(response)

  def _to_percent(self, value):
    return round(value * 100)
