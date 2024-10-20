from . import redis_

def update(key, score, member):
    return redis_.zadd(key, score, member)

def fetch_rank(key, member):
    rank = redis_.zrevrank(key, member)
    return rank

def fetch_top_ranking(key, num):
    return redis_.zrevrange(key, 0, num - 1, True)
