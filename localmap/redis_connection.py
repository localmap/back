import redis
from django.conf import settings

def get_redis_connection():
    redis_url = settings.CACHES['default']['LOCATION']
    return redis.StrictRedis.from_url(redis_url)