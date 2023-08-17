from django.conf import settings
from redis_connection import get_redis_connection

TOKEN_EXPIRY_TIME = getattr(settings, 'TOKEN_EXPIRY_TIME', 60 * 30)

# Redis 클라이언트 인스턴스를 가져옵니다.
redis_client = get_redis_connection()

def add_token_to_blacklist(token):
    redis_client.sadd('blacklisted', token)
    redis_client.expire('blacklisted', TOKEN_EXPIRY_TIME)

def is_token_blacklisted(token):
    return redis_client.sismember('blacklisted', token)
