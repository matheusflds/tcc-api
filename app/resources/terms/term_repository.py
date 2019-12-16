from .. import db
from .term_model import TermDBModel, term_states
from ..topics.topic_model import TopicDBModel

class TermRepository:

  @staticmethod
  def get_all(completed=None, quantity=None):
    query = TermDBModel.query
    if completed:
      query = query.filter_by(processing_status=term_states[2]).order_by(TermDBModel.created_at.asc())
    if quantity:
      query = query.order_by(TermDBModel.updated_at.desc()).limit(quantity)
    return query.all()

  @staticmethod
  def get(id):
    return TermDBModel.query.get(id)

  @staticmethod
  def insert(data):
    term = TermDBModel.query.filter(TermDBModel.text.ilike(data['text'])).first()
    if term:
      return term

    new_term = TermDBModel(text=data['text'])
    TermRepository.save_changes(new_term)
    return new_term

  @staticmethod
  def add_topics(term, topics_data):
    topics = []
    for data in topics_data:
      topic = TopicDBModel(
        words=data['words'],
        words_probability=data['words_probability'],
        term_id=term.id,
        polarity=data['polarity'],
        anger_percentage=data['anger'],
        fear_percentage=data['fear'],
        joy_percentage=data['joy'],
        sad_percentage=data['sadness']
      )
      topics.append(topic)
    term.topics = topics
    TermRepository.save_changes(term)
    return term

  @staticmethod
  def save_changes(data):
    db.session.add(data)
    db.session.commit()
