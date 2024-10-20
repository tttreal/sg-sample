import redis

from django.conf import settings

def get_client():
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,  # 文字列を扱う場合は True
    )

def set(k, v):
    return get_client().set(k, v)

def zadd(key, score, member):
    return get_client().zadd(key, {member: score})

def zrevrank(key, member):
    return get_client().zrevrank(key, member, True)

def zrevrange(key, start, end, withscores=True):
    return get_client().zrevrange(key, start, end, withscores)
