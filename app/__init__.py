from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import rq

from .config import Config

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.redis = Redis.from_url(app.config['REDIS_URL'])
  app.task_queue = rq.Queue('tcc-api', connection=app.redis, job_timeout='2h')
  db.init_app(app)
  CORS(app)

  return app
