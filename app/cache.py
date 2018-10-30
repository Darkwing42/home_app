import redis
import os 

redis_URL = os.getenv('REDIS_URL').split('/')
redis_host = redis_URL[2][0:]
redis_port = redis_URL[2][10:14]

cache = redis.StrictRedis(host=redis_host, port=redis_port, db=1)

