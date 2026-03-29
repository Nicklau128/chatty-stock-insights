# integrations/rate_limiter.py

import time
from threading import Lock


class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self.interval = 60.0 / calls_per_minute
        self.last_called = 0.0
        self.lock = Lock()

    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_called

            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)

            self.last_called = time.time()
