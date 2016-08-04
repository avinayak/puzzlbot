import logging

from celery import Celery
from celery.task import periodic_task
from datetime import timedelta
from os import environ

REDIS_URL = environ.get('REDISTOGO_URL', 'redis://pub-redis-16210.us-east-1-2.5.ec2.garantiadata.com:16210')

celery = Celery('tasks', broker=REDIS_URL)


def fib(n):
    if n > 1:
        return fib(n - 1) + fib(n - 2)
    else:
        return 1


@periodic_task(run_every=timedelta(seconds=10))
def print_fib():
    logging.info(fib(30))