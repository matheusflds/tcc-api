from flask_restful import Resource
from flask import jsonify
from datetime import datetime
from math import log

from models import TermModel

class Terms(Resource):
  MAX_TIMESTAMP_DIFF = 2826090

  def get(self):
    terms = [[term.text, self._calculate_weight(term)] for term in TermModel.query.all()]
    if terms:
      return jsonify({ 'terms': terms })
    return {
      'message': 'Terms not found',
      'code': '404'
    }

  def _calculate_weight(self, term):
    current = datetime.timestamp(datetime.now())
    term_updated_date = datetime.timestamp(term.updated_at)
    delta = current - term_updated_date

    if delta > self.MAX_TIMESTAMP_DIFF:
      return 0.5
    elif delta <= 1000:
      return 10
    return (-9.5 * delta / self.MAX_TIMESTAMP_DIFF) + 10
