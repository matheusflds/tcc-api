from flask_restful import Resource, reqparse, inputs
from flask import current_app, jsonify, make_response
from datetime import datetime

from .statistics_repository import StatisticsRepository

class Statistics(Resource):
  def get(self):
    stats = StatisticsRepository.get()

    response = {
      "pendingTermCount": stats['pending_count'],
      "processingTermCount": stats['processing_count'],
      "processedTermCount": stats['completed_count'],
      "tweetCount": stats['tweet_count'],
      "topicCount": stats['topic_count']
    }
    return jsonify(response)
