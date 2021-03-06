from celery import Celery, current_task
from celery.result import AsyncResult
import os
from celery.scheduled import crontab
import requests




REDIS_URL = os.getenv('REDIS_URL') or 'redis://redis:6379/0'
BROKER_URL = os.getenv('BROKER_URL') or 'amqp://home_user:test2345@rabbit//'

worker = Celery('tasks',
		backend=REDIS_URL,
		broker=BROKER_URL)



### periodical tasks

@worker.on_after_configure.connect
def setup_periodical_tasks(sender, **kwargs):
	sender.add_periodic_task(10.0, test.s('Hello'), name='add every 10')

	sender.add_periodic_task(
			crontab(hour=7, minute=30, day_of_week=1),
			test.s('Hello'),
	)

@worker.task
def test(arg):
	print(arg)
