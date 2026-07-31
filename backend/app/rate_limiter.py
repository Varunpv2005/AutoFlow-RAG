from collections import defaultdict, deque
import time
from typing import DefaultDict, Deque


class SimpleRateLimiter:
    """Simple in-memory rate limiter for auth endpoints."""

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: DefaultDict[str, Deque[float]] = defaultdict(deque)

    def _prune(self, key: str, now: float) -> None:
        bucket = self._requests[key]
        cutoff = now - self.window_seconds
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if not bucket:
            self._requests.pop(key, None)

    def allow_request(self, key: str) -> bool:
        now = time.time()
        self._prune(key, now)
        bucket = self._requests[key]
        if len(bucket) >= self.max_requests:
            return False
        bucket.append(now)
        return True
