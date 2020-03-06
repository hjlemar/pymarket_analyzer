from textblob import TextBlob 
import re
from sentiment_analyzer.cache import sentiment_cache

def clean_str(string): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", string).split()) 


def get_sentiment(value): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_str(value)) 
    return analysis.sentiment.polarity

def get_max_sentiment(*strings):
  # need to get the most -1 or the most positive
  return max([get_sentiment(string) for string in strings])

def determine_store_sentiment(item):
  ticker, news_item = item
  ticker = ticker.lower()
  if sentiment_cache.has_been_processed(ticker,news_item['datetime']):
    print("Ticker has been seen with timestamp {} {}".format(ticker,news_item['datetime']))
    return

  sentiment = get_max_sentiment(news_item['headline'],news_item['summary'])
  sentiment_cache.save_series(sentiment=sentiment, ticker=ticker, timestamp=news_item['datetime'])

if __name__ == '__main__':
  print(get_max_sentiment("I am very sad today!","I am very happy today!"))
  print(get_max_sentiment("I am very happy today!"))
  print(get_max_sentiment("I am getting windows today"))