from flask_restful import Resource
from flask import jsonify

class Terms(Resource):
  def get(self):
    terms = [
      ['nobel', 0.5],
      ['blizzard', 0.3],
      ['trump', 0.4],
      ['brazil', 0.1],
    ]
    if terms:
      return jsonify({ 'terms': terms })
    return {
      'message': 'Terms not found',
      'code': '404'
    }