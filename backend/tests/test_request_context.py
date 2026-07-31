import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.request_context import clear_request_id, get_request_id, set_request_id


class RequestContextTests(unittest.TestCase):
    def test_request_id_round_trip(self):
        clear_request_id()
        self.assertIsNone(get_request_id())

        request_id = set_request_id("trace-123")
        self.assertEqual(request_id, "trace-123")
        self.assertEqual(get_request_id(), "trace-123")

        clear_request_id()
        self.assertIsNone(get_request_id())


if __name__ == "__main__":
    unittest.main()
