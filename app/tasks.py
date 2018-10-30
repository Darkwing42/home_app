from celery import Celery, current_task
from celery.result import AsyncResult
import os
from app.cache import cache



REDIS_URL = os.getenv('REDIS_URL') or 'redis://redis:6379/0'
BROKER_URL = os.getenv('BROKER_URL') or 'pyamqp://admin:mypass@rabbit//'

app = Celery('tasks',
		backend=REDIS_URL,
		broker=BROKER_URL)

	


