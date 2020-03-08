from textblob import TextBlob 
import re
from sentiment_analyzer.cache import SentimentCache, GlobalNewsSentimentCache
from abc import ABC, abstractmethod

class Sentiment(ABC):

  def __init__(self, cache):
    self.cache = cache

  def clean_str(self, string): 
      ''' 
      Utility function to clean tweet text by removing links, special characters 
      using simple regex statements. 
      '''
      return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", string).split()) 


  def get_sentiment(self, value): 
      ''' 
      Utility function to classify sentiment of passed tweet 
      using textblob's sentiment method 
      '''
      # create TextBlob object of passed tweet text 
      analysis = TextBlob(self.clean_str(value)) 
      return analysis.sentiment.polarity

  def get_max_sentiment(self, *strings):
    # need to get the most -1 or the most positive
    return max([self.get_sentiment(string) for string in strings])

class TickerSentiment(Sentiment):

  def __init__(self):
    super().__init__(SentimentCache())

  def __call__(self, item):
    ticker, news_item = item
    ticker = ticker.lower()
    if self.cache.has_been_processed(ticker,news_item['datetime']):
      print("Ticker has been seen with timestamp {} {}".format(ticker,news_item['datetime']))
      return

    sentiment = self.get_max_sentiment(news_item['headline'],news_item['summary'])
    self.cache.save_series(sentiment=sentiment, ticker=ticker, timestamp=news_item['datetime'])

class GlobalNewsSentiment(Sentiment):
  def __init__(self):
    super().__init__(GlobalNewsSentimentCache())

  def __call__(self, item):
    dtime = item['datetime']
    if self.cache.has_been_processed(dtime):
      print("News has been processed with timestamp {}".format(dtime))
      return

    sentiment = self.get_max_sentiment(item['headline'],item['summary'])
    self.cache.save_series(sentiment=sentiment, timestamp=dtime)



