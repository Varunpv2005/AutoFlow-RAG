import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import parse_cors_origins


class CorsConfigTests(unittest.TestCase):
    def test_default_origins_are_used_when_not_configured(self):
        self.assertEqual(
            parse_cors_origins(None),
            [
                "http://localhost:3000",
                "http://localhost:5173",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:5173",
            ],
        )

    def test_comma_separated_origins_are_parsed(self):
        self.assertEqual(
            parse_cors_origins("https://app.example.com, https://admin.example.com"),
            ["https://app.example.com", "https://admin.example.com"],
        )

    def test_wildcard_origin_is_preserved(self):
        self.assertEqual(parse_cors_origins("*"), ["*"])


if __name__ == "__main__":
    unittest.main()
