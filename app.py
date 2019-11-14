from flask import Flask, jsonify, request
from topic_modelling.topic_model import TopicModel
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/topics", methods=['GET'])
@cross_origin()
def topics():
  # query = request.args.get('query')
  # topic_model = TopicModel('datasets/topic_modelling')
  # topics = topic_model.get_topics(query)
  # response = [list(map(lambda x: [x[1], x[0]], topic)) for topic in topics]
  response = [
    [['apple', 0.05], ['banana', 0.01], ['grape', 0.04], ['strawberry', 0.03], ['lemon', 0.05], ['orange', 0.01], ['kiwi', 0.04], ['tree', 0.03]],
    [['car', 0.05], ['motor', 0.01], ['machine', 0.04], ['engine', 0.03], ['bicycle', 0.05]],
  ]
  print('done')
  return jsonify({
    'topics': response
  })

@app.route("/terms")
@cross_origin()
def terms():
  terms = [
    ['nobel', 0.5],
    ['blizzard', 0.3],
    ['trump', 0.4],
    ['brazil', 0.1],
  ]
  return jsonify({
    'terms': terms
  })

if __name__ == "__main__":
  app.run()
