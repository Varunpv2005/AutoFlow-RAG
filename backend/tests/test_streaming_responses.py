import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.chat_service import iter_response_tokens


class StreamingResponseTests(unittest.TestCase):
    def test_iter_response_tokens_breaks_text_into_small_stream_chunks(self):
        tokens = list(iter_response_tokens("Hello, world!"))
        self.assertEqual(tokens, ["Hello,", " ", "world!"])

    def test_iter_response_tokens_preserves_whitespace(self):
        tokens = list(iter_response_tokens("The document describes..."))
        self.assertEqual(tokens, ["The", " ", "document", " ", "describes..."])


if __name__ == "__main__":
    unittest.main()
