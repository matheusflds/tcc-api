from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.terms import Terms
from resources.topics import Topics

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
api.add_resource(Terms, '/terms')
api.add_resource(Topics, '/topics/<string:term>')

if __name__ == "__main__":
  app.run(debug=True)
