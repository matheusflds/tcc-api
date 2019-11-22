from flask_restful import Api

from .resources.terms import TermList
from .resources.topics import Topics

def setup_routes(app):
  api = Api(app)
  api.add_resource(TermList, '/terms')
  api.add_resource(Topics, '/topics/<string:term>')
