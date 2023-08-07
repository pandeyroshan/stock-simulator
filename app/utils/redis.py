import json
from typing import Any

import redis

from app.config import redis_url

redis = redis.from_url(redis_url)



def set_cache(key: str, value: str):
    """
    Set the value for the given key in Redis.
    """
    return redis.set(key, value)

def get_cache(key: str):
    """
    Get the value for the given key in Redis.
    """
    serialized_value = redis.get(key)
    return serialized_value and json.loads(serialized_value)