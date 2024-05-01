#!/usr/bin/env python3
""" Main file """
import requests
import redis
import functools
import time
from typing import Callable

def track_url_access_count(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(url):
        key = f"count:{url}"
        method._redis.incr(key)
        return method(url)
    return wrapper

def cache_with_expiry(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(url):
        key = f"cache:{url}"
        cached_result = method._redis.get(key)
        if cached_result:
            return cached_result.decode("utf-8")
        else:
            result = method(url)
            method._redis.setex(key, 10, result)  # Cache result with 10 seconds expiry
            return result
    return wrapper

class Web:
    def __init__(self):
        self._redis = redis.Redis()

    @track_url_access_count
    @cache_with_expiry
    def get_page(self, url: str) -> str:
        response = requests.get(url)
        return response.text

# Example usage:
web = Web()

# Simulate accessing a slow website multiple times
for _ in range(5):
    print(web.get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"))

# Wait for cached result to expire
time.sleep(15)

# Access the same URL again to trigger fetching and caching
print(web.get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"))

