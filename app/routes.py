from flask_restful import Api

from .resources.terms.terms_controller import TermList
from .resources.topics.topics_controller import Topics
from .resources.statistics.statistics_controller import Statistics

def setup_routes(app):
  api = Api(app)
  api.add_resource(TermList, '/terms')
  api.add_resource(Topics, '/topics')
  api.add_resource(Statistics, '/statistics')
