from .. import db
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ARRAY

class TopicDBModel(db.Model):
  __tablename__ = 'topics'

  id = db.Column(db.Integer, primary_key=True)
  term_id = db.Column(db.Integer, db.ForeignKey('terms.id'))
  words = db.Column(ARRAY(db.String(32)))
  words_probability = db.Column(ARRAY(db.Integer))
  polarity = db.Column(db.Float)
  anger_percentage = db.Column(db.Float)
  fear_percentage = db.Column(db.Float)
  joy_percentage = db.Column(db.Float)
  sad_percentage = db.Column(db.Float)
  created_at = db.Column(DateTime, default=datetime.now)
  updated_at = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)

  def __init__(self, words, words_probability, term_id, polarity, anger_percentage, fear_percentage, joy_percentage, sad_percentage):
    self.words = words
    self.words_probability = words_probability
    self.term_id = term_id
    self.polarity = polarity
    self.anger_percentage = anger_percentage
    self.fear_percentage = fear_percentage
    self.joy_percentage = joy_percentage
    self.sad_percentage = sad_percentage

  def __repr__(self):
    return '<id {}>'.format(self.id)
