# store in influxdb
from influxdb import InfluxDBClient
from datetime import datetime

USER='analyser_service'
PASS='Say$omethingN!ce'
ANALYSIS_DB='analyser_data'
GLOBAL_DB = 'analyser_global_data'

SENTIMENT='sentiment'
GSENTIMENT='global_sentiment'

def setup_influx():
  client = InfluxDBClient('localhost', 8086)

  client.create_database(ANALYSIS_DB)
  client.create_database(GLOBAL_DB)
  
  for user in client.get_list_users():
    if user['user'] == USER:
      return
  
  client.create_user(USER,PASS)
  client.grant_privilege('all',ANALYSIS_DB,USER)
  client.grant_privilege('all',GLOBAL_DB,USER)

  client.create_retention_policy(SENTIMENT, '30d', 1, default=True,database=ANALYSIS_DB)
  client.create_retention_policy(GSENTIMENT, '180d', 1, default=True, database=GLOBAL_DB)



class SentimentCache:

  def __init__(self):
    self.client = InfluxDBClient('localhost', 8086, USER,PASS,ANALYSIS_DB)

  def save_series(self,sentiment, ticker, timestamp):
    point = dict(
      measurement=SENTIMENT,
      tags=dict(),
      time=timestamp,
      fields=dict(
        ticker=ticker.lower(),
        value=sentiment
      )
    )
    self.client.write_points([point],time_precision='ms')

  def get_series(self,ticker):
    query = "select * from sentiment where ticker = $ticker"
    result = self.client.query(query,bind_params=dict(ticker=ticker.lower()),database=ANALYSIS_DB)
    
    return dict(data=list(result.get_points(measurement=SENTIMENT)))    

  def has_been_processed(self, ticker, timestamp):
    query = "select * from sentiment where ticker = $ticker and time = $timestamp"
    params = dict(ticker=ticker.lower(),timestamp=timestamp)
    result = self.client.query(query,bind_params=params)
    points = list(result.get_points(measurement=SENTIMENT))

    return len(points) > 0
  

class GlobalNewsSentimentCache:

  def __init__(self):
    self.client = InfluxDBClient('localhost', 8086, USER,PASS, GLOBAL_DB)
    

  def save_series(self,sentiment,timestamp):
    print("saving global data")
    point = dict(
      measurement=GSENTIMENT,
      tags=dict(),
      time=timestamp,
      fields=dict(
        value=sentiment
      )
    )
    self.client.write_points([point],time_precision='ms')

  def get_series(self):
    query = "select * from global_sentiment"
    result = self.client.query(query)
    
    return dict(data=list(result.get_points(measurement=GSENTIMENT)))    

  def has_been_processed(self, timestamp):
    query = "select * from global_sentiment where time = $timestamp"
    params = dict(timestamp=timestamp)
    result = self.client.query(query,bind_params=params)    
    points = list(result.get_points(measurement=GSENTIMENT))

    return len(points) > 0  
