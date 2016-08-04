import logging
import tweepy
from celery import Celery
from celery.task import periodic_task
from datetime import timedelta
from os import environ
from puzzls import word_grid

REDISCLOUD_URL = environ.get('REDISCLOUD_URL', 'redis://localhost')
TWITTER_CONSUMER_KEY = environ.get('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = environ.get('TWITTER_CONSUMER_SECRET', '')
TWITTER_ACCESS_TOKEN = environ.get('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')
celery = Celery('tasks', broker=REDISCLOUD_URL)

@periodic_task(run_every=timedelta(seconds=600))
def print_fib():
    puzzl = word_grid.get_puzzl()
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_with_media(puzzl['tweet_image'], status=puzzl['tweet_text'])