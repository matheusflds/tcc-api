import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(os.path.join(os.path.dirname(__file__), '../.env')).resolve()
load_dotenv(dotenv_path=env_path)

class Config(object):
  CORS_HEADERS = 'Content-Type'
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False