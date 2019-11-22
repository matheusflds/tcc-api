from flask_restful import Resource
from flask import jsonify

from .topic_model import TopicDBModel

class Topics(Resource):
  def get(self, term):
    # topics = TopicModel.query.filter_by(term_id=term)
    # query = request.args.get('query')
    # topic_model = TopicModel('datasets/topic_modelling')
    # topics = topic_model.get_topics(query)
    # response = [list(map(lambda x: [x[1], x[0]], topic)) for topic in topics]
    response = [
      [['apple', 0.05], ['banana', 0.01], ['grape', 0.04], ['strawberry', 0.03], ['lemon', 0.05], ['orange', 0.01], ['kiwi', 0.04], ['tree', 0.03]],
      [['car', 0.05], ['motor', 0.01], ['machine', 0.04], ['engine', 0.03], ['bicycle', 0.05]],
    ]
    if response:
      return jsonify({ 'topics': response })