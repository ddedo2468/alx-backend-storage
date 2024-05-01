#!/usr/bin/env python3

""" Module """
import redis
from typing import Union, Optional, Any, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count the calls """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrap it  """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ history decorator """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrap it """
        output = method(self, *args, **kwargs)
        method_name = method.__qualname__
        self._redis.rpush(f"{method_name}:inputs", str(args))
        self._redis.rpush(f"{method_name}:outputs", str(output))
        return output
    return wrapper


def replay(method: Callable) -> Callable:
    """  decorator for replay """
    r = redis.Redis()
    method_name = method.__qualname__
    count = r.get(method_name).decode("utf-8")
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)
    print(f"{method_name} was called {count} times:")
    for i, o in zip(inputs, outputs):
        print(f"{method_name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """ Cache """

    def __init__(self) -> None:
        """ constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    @staticmethod
    def get_int(value: bytes) -> int:
        """ byte to int """
        return int(value)

    @staticmethod
    def get_str(value: bytes) -> str:
        """ byte to str """
        return str(value)

    def get(self, key: str, fn: Optional[Any] = None) -> Any:
        """ getter method """
        val = self._redis.get(key)
        if fn:
            if fn == int:
                return self.get_int(val)
            elif fn == str:
                return self.get_str(val)
            else:
                return fn(val)
        return val
