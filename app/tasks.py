from celery import Celery, current_task
from celery.result import AsyncResult
import os


REDIS_URL = os.getenv('REDIS_URL') or 'redis://redis:6379/0'
BROKER_URL = os.getenv('BROKER_URL') or 'amqp://admin:mypass@rabbit//'

CELERY = Celery('tasks',
		backend=REDIS_URL,
		broker=BROKER_URL)


