from flask_restful import Resource, reqparse, inputs
from flask import current_app, jsonify, make_response
from datetime import datetime

from .term_repository import TermRepository
from .term_model import term_states

class TermList(Resource):
  def __init__(self):
    self.MAX_TIMESTAMP_DIFF = 2826090

    self.regparser_get_args = reqparse.RequestParser()
    self.regparser_get_args.add_argument('completed', type=inputs.boolean, location='args')
    self.regparser_get_args.add_argument('quantity', type=int, location='args')

    self.regparser_post_args = reqparse.RequestParser()
    self.regparser_post_args.add_argument('term_text', required=True, help='This field cannot be left empty')

  def get(self):
    req_data = self.regparser_get_args.parse_args()
    filter_by_completed = req_data['completed']
    quantity = req_data['quantity']

    terms_response = []
    for term in TermRepository.get_all(completed=filter_by_completed, quantity=quantity):
      term_response = {
        'term': term.text,
        'status': term_states.index(term.processing_status),
        'description': term.description,
        'weigth': self._calculate_weight(term)
      }
      terms_response.append(term_response)
    if terms_response:
      return jsonify({ 'terms': terms_response })

    return make_response(jsonify({
      'message': 'Terms not found',
    }), 404)

  def post(self):
    req_data = self.regparser_post_args.parse_args()
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

    current_app.task_queue.enqueue('app.resources.terms.tasks.process_term', query)

    return jsonify({
      'message': 'Succesfully added term {} to queue'.format(query)
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
