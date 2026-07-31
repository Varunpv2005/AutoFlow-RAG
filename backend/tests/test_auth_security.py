import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.auth import DEFAULT_SECRET_KEY, validate_secret_key


class AuthSecurityTests(unittest.TestCase):
    def test_allows_non_default_secret(self):
        self.assertEqual(validate_secret_key("super-secure-secret"), "super-secure-secret")

    def test_rejects_default_secret_in_production(self):
        with self.assertRaises(RuntimeError):
            validate_secret_key(DEFAULT_SECRET_KEY, environment="production")


if __name__ == "__main__":
    unittest.main()
