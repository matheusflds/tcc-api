from .. import db
from ..terms.term_model import TermDBModel, term_states
from ..topics.topic_model import TopicDBModel
from sqlalchemy.sql import func

class StatisticsRepository:

  @staticmethod
  def get():
    stats = {}
    stats['pending_count'] = TermDBModel.query.filter_by(processing_status=term_states[0]).count()
    stats['processing_count'] = TermDBModel.query.filter_by(processing_status=term_states[1]).count()
    stats['completed_count'] = TermDBModel.query.filter_by(processing_status=term_states[2]).count()
    stats['tweet_count'] = db.session \
      .query(func.sum(TermDBModel.tweet_count)) \
      .filter(TermDBModel.processing_status == term_states[2]) \
      .scalar()
    stats['topic_count'] = TopicDBModel.query.count()
    return stats