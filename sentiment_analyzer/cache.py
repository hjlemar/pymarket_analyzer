# store in influxdb
from influxdb import InfluxDBClient
from datetime import datetime


SENTIMENT='sentiment'
client = InfluxDBClient('localhost', 8086, 'analyser_service', 'Say$omethingN!ce', 'analyser_data')
client.create_retention_policy(SENTIMENT, '30d', 1, default=True)

def save_series(sentiment, ticker, timestamp):
  point = dict(
    measurement=SENTIMENT,
    tags=dict(),
    time=timestamp,
    fields=dict(
      ticker=ticker.lower(),
      value=sentiment
    )
  )
  client.write_points([point],time_precision='ms')

def get_series(ticker):
  query = "select * from sentiment where ticker = $ticker"
  result = client.query(query,bind_params=dict(ticker=ticker.lower()),database='analyser_data')
  
  return dict(data=list(result.get_points(measurement=SENTIMENT)))
  


def has_been_processed(ticker, timestamp):
  query = "select * from sentiment where ticker = $ticker and time = $timestamp"
  params = dict(ticker=ticker.lower(),timestamp=timestamp)
  result = client.query(query,bind_params=params)
  points = list(result.get_points(measurement=SENTIMENT))

  return len(points) > 0
  