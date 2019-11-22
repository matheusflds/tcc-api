import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(os.path.join(os.path.dirname(__file__), '../.env')).resolve()
load_dotenv(dotenv_path=env_path)

db_uri = 'postgresql://{user}:{password}@{uri}/{db}'.format(
  user=os.getenv('DATABASE_USER'),
  password=os.getenv('DATABASE_PASSWORD'),
  uri=os.getenv('DATABASE_URI'),
  db=os.getenv('DATABASE_NAME')
)

class Config(object):
  CORS_HEADERS = 'Content-Type'
  SQLALCHEMY_DATABASE_URI = db_uri
  SQLALCHEMY_TRACK_MODIFICATIONS = False