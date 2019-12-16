from flask_restful import Resource, reqparse, inputs
from flask import current_app, jsonify, make_response
from datetime import datetime

from .term_repository import TermRepository
from .term_model import term_states

class TermList(Resource):
  def __init__(self):
    self.regparser_get_args = reqparse.RequestParser()
    self.regparser_get_args.add_argument('completed', type=inputs.boolean, location='args')
    self.regparser_get_args.add_argument('quantity', type=int, location='args')

    self.regparser_post_args = reqparse.RequestParser()
    self.regparser_post_args.add_argument('term_text', required=True, help='This field cannot be left empty')

  def get(self):
    req_data = self.regparser_get_args.parse_args()
    filter_by_completed = req_data['completed']
    quantity = req_data['quantity']

    terms_data = TermRepository.get_all(completed=filter_by_completed, quantity=quantity)
    oldest_date = terms_data[0].created_at
    terms_response = []
    for term in terms_data:
      term_response = {
        'id': term.id,
        'term': term.text,
        'status': term_states.index(term.processing_status),
        'description': term.description,
        'weigth': self._calculate_weight(term, oldest_date) / 10
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
        'message': '"{}" is being processed'.format(query)
      })
    elif term.processing_status is term_states[2]:
      return jsonify({
        'message': '"{}" already processed'.format(query),
        'id': term.id
      })

    current_app.task_queue.enqueue('app.resources.terms.tasks.process_term',
                                   query,
                                   term.id,
                                   job_timeout='2h')

    return jsonify({
      'message': '"{}" will be processed in a few minutes'.format(query)
    })


  def _calculate_weight(self, term, oldest_date):
    min_timestamp = datetime.timestamp(oldest_date)
    current = datetime.timestamp(datetime.now())
    min_weight = 4
    max_weight = 10
    inclination = (max_weight - min_weight) / (current - min_timestamp)
    
    term_timestamp = datetime.timestamp(term.updated_at)
    return inclination * (term_timestamp - min_timestamp) + min_weight

