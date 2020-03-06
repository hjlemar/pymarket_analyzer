from flask import request, Response, jsonify

from sentiment_analyzer import api
import json
from flask_restx import Resource, fields

from sentiment_analyzer.work_queue import sentiment_wq
from sentiment_analyzer.cache import sentiment_cache


news_model = api.model('Resource', {
    'datetime': fields.Integer,
    'source': fields.String,
    'url': fields.String,
    'headline': fields.String,
    'summary': fields.String
})

sentiment = dict(
  sentiment=fields.Float,
  time=fields.Integer,
  ticker=fields.String
)
series_data = api.model('SentimentSeries',{
  'data': fields.List(fields.Nested(sentiment))
})

@api.route('/sentiment/<string:ticker>')
class SentimentAnalysis(Resource):

  @api.doc(body=news_model)
  def post(self, ticker):
    
      # queue job
      print(request)

      news = json.loads(request.data)
      if news is None:
        # errror somehow
        pass
      sentiment_wq.enqueue((ticker,news))
      
      return Response(status=201)
  
  #@api.doc(body=series_data)
  def get(self, ticker):
    return jsonify(sentiment_cache.get_series(ticker))


# @api.route('/global')
# class SentimentAnalysis(Resource):

#   @api.doc(body=news_model)
#   def post(self):
    
#       # queue job
#       print(request)

#       news = json.loads(request.data)
#       if news is None:
#         # errror somehow
#         pass
#       enqueue_sentiment_task(ticker,news)
#       return Response(status=201)
  
#   def get(self):
#     return jsonify(get_series(ticker))
      

      

