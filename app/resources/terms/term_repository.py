from .. import db
from .term_model import TermDBModel

class TermRepository:

  @staticmethod
  def get_all():
    return TermDBModel.query.all()

  @staticmethod
  def insert(data):
    term = TermDBModel.query.filter_by(text=data['text']).first()
    if term:
      return term

    new_term = TermDBModel(text=data['text'])
    TermRepository.save_changes(new_term)
    return new_term

  @staticmethod
  def save_changes(data):
    db.session.add(data)
    db.session.commit()