from app import db
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ENUM

term_states = ('pending', 'processing', 'done')
processing_status_enum = ENUM(*term_states, name='processing_status')

class TermDBModel(db.Model):
  __tablename__ = 'terms'

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(64))
  description = db.Column(db.String(256))
  tweet_count = db.Column(db.Integer)
  processing_status = db.Column(processing_status_enum, nullable=False, server_default='pending')
  topics = db.relationship('TopicDBModel', backref='term', lazy='dynamic')
  polarity = db.Column(db.Float)
  joy = db.Column(db.Float)
  anger = db.Column(db.Float)
  fear = db.Column(db.Float)
  sadness = db.Column(db.Float)
  created_at = db.Column(DateTime, default=datetime.now)
  updated_at = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)

  def __init__(self, text):
    self.text = text

  def __repr__(self):
    return '<id {} Text {}>'.format(self.id, self.text)
