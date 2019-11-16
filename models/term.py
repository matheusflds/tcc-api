from app import db
from datetime import datetime
from sqlalchemy import DateTime

class TermModel(db.Model):
  __tablename__ = 'terms'

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(64))
  created_at = db.Column(DateTime, default=datetime.now)
  updated_at = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)

  def __repr__(self):
    return '<id {} Text {}>'.format(self.id, self.text)
