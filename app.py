from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.terms import Terms

app = Flask(__name__)
api = Api(app)
api.add_resource(Terms, '/terms')

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route("/topics", methods=['GET'])
# def topics():
#   # query = request.args.get('query')
#   # topic_model = TopicModel('datasets/topic_modelling')
#   # topics = topic_model.get_topics(query)
#   # response = [list(map(lambda x: [x[1], x[0]], topic)) for topic in topics]
#   response = [
#     [['apple', 0.05], ['banana', 0.01], ['grape', 0.04], ['strawberry', 0.03], ['lemon', 0.05], ['orange', 0.01], ['kiwi', 0.04], ['tree', 0.03]],
#     [['car', 0.05], ['motor', 0.01], ['machine', 0.04], ['engine', 0.03], ['bicycle', 0.05]],
#   ]
#   print('done')
#   return jsonify({
#     'topics': response
#   })

if __name__ == "__main__":
  app.run(debug=True)
