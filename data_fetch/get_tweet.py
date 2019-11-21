import os
import re

import pandas as pd
from pathlib import Path
from emoji import emojize
from tweepy import TweepError
from datetime import datetime

from .connection import Connection

def get_tweets(query, save_dir=None, max_requests=10, count=100):
  dataset_dir = 'datasets'
  DATASET_DIR = Path(dataset_dir).resolve()
  filenames = pd.Series([x for x in os.listdir(DATASET_DIR) if x.endswith('.csv')], 
                     name='files')
  if len(filenames) > 0:
    filenames = filenames[filenames.str.contains(query)]
    filename = filenames.iloc[0] if len(filenames) > 0 else None
    df = pd.read_csv(Path(os.path.join(DATASET_DIR, filename)).resolve()) if filename else None
    if df is not None:
      return df

  return fetch_tweets(query, save_dir=save_dir, max_requests=max_requests, count=count)


def fetch_tweets(query, save_dir=None, max_requests=10, count=100):
  connection = Connection()
  connection.load()
    
  q = emojize(query) + ' -filter:retweets'
  searched_tweets = []
  last_id = -1
  since_id = None
  request_count = 0
  while request_count < max_requests:
    try:
      new_tweets = connection.api.search(q=q,
                                         lang='en',
                                         count=count,
                                         max_id=str(last_id - 1),
                                         since_id=str(since_id),
                                         tweet_mode='extended')
      if not new_tweets:
          break
      searched_tweets.extend(new_tweets)
      last_id = new_tweets[-1].id
      request_count += 1
    except TweepError as e:
      print(e)
      break

  data = []
  for tweet in searched_tweets:
    data.append([tweet.id, tweet.created_at, tweet.user.screen_name, tweet.full_text])

  df = pd.DataFrame(data=data, columns=['id', 'date', 'user', 'text'])
  print(str(len(data)) + ' ' + query + ' tweets')

  if save_dir and data:
    PATH = Path(save_dir).resolve()
    query = '_'.join(query.split(' '))
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    filename = query + '-' + str(timestamp) + '.csv'
    df.to_csv(os.path.join(PATH, filename), index=None)
    print('Saved under: "' + PATH.as_posix() + '"')

  return df
