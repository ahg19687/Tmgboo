# telegram_bot/utils/rate_limiter.py
# simple token-bucket rate limiter

import time
from threading import Lock

class RateLimiter:
    def __init__(self, rate_per_minute=60):
        self.capacity = rate_per_minute
        self.tokens = rate_per_minute
        self.rate_per_second = rate_per_minute / 60.0
        self.lock = Lock()
        self.last = time.time()

    def allow(self, n=1):
        with self.lock:
            now = time.time()
            delta = now - self.last
            self.tokens = min(self.capacity, self.tokens + delta * self.rate_per_second)
            self.last = now
            if self.tokens >= n:
                self.tokens -= n
                return True
            return False

    def wait_for(self, n=1):
        while not self.allow(n):
            time.sleep(0.5)
