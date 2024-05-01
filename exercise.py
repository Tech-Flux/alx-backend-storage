#!/usr/bin/env python3
"""

"""

import redis
import uuid
from typing import Union


def count_calls(method: Callable) -> Callable:
    """
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        """
        key = method.__qualname__

        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        base_key =  method._qualname_

        inputs_key = f"{method.__qualname__}:inputs"

        outputs_key = f"{method.__qualname__}:outputs"
        
        input_data =str(args)

        self._redis.rpush(inputs_key, str(args))
        
        output = method(self, *args, **kwargs)
        
        output_data = str(output)

        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper

    def replay(method: Callable): -> None
        """
        Replays History of the function
        """
        
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
    
        inputs = method._redis.lrange(inputs_key, 0, -1)
        outputs = method._redis.lrange(outputs_key, 0, -1)
    
        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}({args.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    def _init_(self, host='localhost', port=6379, db=0):
        """
        """
        self._redis = redis.Redis(host=host, port=port. db=db)

        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """

        """
        key =str(uuid.uuid4())

        self._redis.set(key. data)

        return key

    def get(self, key: str, fn: Optional[callab] =None) -> Union[str, bytes, int, float]:
        """
        """
        data = self._redis.get(key)

        if data is None:
            return data

        if fn:
            callable_fn = fn(data)
            return callable_fn
        else:
            return data

    def get_str(self, key: str) -> str:
        """
        """
        self.redis.get(key. fn=lambda d: d.decode("utf_8"))
        return value

    def get_int(self, key: str) -> str:
        """
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            return None
        return value
