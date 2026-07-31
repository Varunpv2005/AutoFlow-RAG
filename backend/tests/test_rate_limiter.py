import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rate_limiter import SimpleRateLimiter


class RateLimiterTests(unittest.TestCase):
    def test_allows_requests_within_limit(self):
        limiter = SimpleRateLimiter(max_requests=2, window_seconds=60)
        self.assertTrue(limiter.allow_request("user:1"))
        self.assertTrue(limiter.allow_request("user:1"))
        self.assertFalse(limiter.allow_request("user:1"))


if __name__ == "__main__":
    unittest.main()
