import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rate_limiter import SimpleRateLimiter

PUBLIC_ENDPOINTS = {"/api/health", "/api/auth/signup", "/api/auth/login", "/api/chat/stream", "/api/chat"}


class PublicRateLimitingTests(unittest.TestCase):
    def test_rate_limiter_blocks_excess_requests(self):
        limiter = SimpleRateLimiter(max_requests=2, window_seconds=60)
        self.assertTrue(limiter.allow_request("public:/api/health:127.0.0.1"))
        self.assertTrue(limiter.allow_request("public:/api/health:127.0.0.1"))
        self.assertFalse(limiter.allow_request("public:/api/health:127.0.0.1"))

    def test_public_endpoints_include_chat_routes(self):
        self.assertIn("/api/chat", PUBLIC_ENDPOINTS)
        self.assertIn("/api/chat/stream", PUBLIC_ENDPOINTS)


if __name__ == "__main__":
    unittest.main()
