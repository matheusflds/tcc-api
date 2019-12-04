from flask_restful import Resource, reqparse
from flask import jsonify, make_response

from ..terms.term_repository import TermRepository
from .topic_model import TopicDBModel

class Topics(Resource):
  def __init__(self):
    self.regparser_get_args = reqparse.RequestParser()

    self.regparser_get_args.add_argument('query', type=str, required=True, location='args')

  def get(self):
    req_data = self.regparser_get_args.parse_args()
    query = req_data['query']
    term = TermRepository.get(text=query)
    if not term:
      return make_response(jsonify({
        'message': 'Terms not found',
      }), 404)

    response = {
      'term': term.text,
      'tweetCount': term.tweet_count,
      'description': term.description,
      'overallResults': {
        'polarity': term.polarity,
        'joy': term.joy,
        'anger': term.anger,
        'fear': term.fear,
        'sadness': term.sadness
      },
      'topics': [{
          'words': list(zip(topic.words, topic.words_probability)),
          'polarity': topic.polarity,
          'joy': topic.joy_percentage,
          'anger': topic.anger_percentage,
          'fear': topic.fear_percentage,
          'sadness': topic.sad_percentage,
        } for topic in term.topics]
    }

    return jsonify(response)
