from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from resources.terms import Terms
from resources.topics import Topics
api = Api(app)
api.add_resource(Terms, '/terms')
api.add_resource(Topics, '/topics/<string:term>')

if __name__ == "__main__":
  app.run(debug=True)
