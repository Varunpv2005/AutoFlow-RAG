import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.log_utils import build_log_entry, emit_observability_event, safe_log_gotcha
from app.request_context import clear_request_id, set_request_id


class ObservabilityTests(unittest.TestCase):
    def test_build_log_entry_includes_request_id(self):
        entry = build_log_entry("chat", request_id="req-1", latency_ms=42.0)
        self.assertIn("request_id=req-1", entry)
        self.assertIn("latency_ms=42.0", entry)

    def test_emit_observability_event_returns_payload(self):
        payload = emit_observability_event("error", request_id="req-2", message="boom")
        self.assertEqual(payload["event"], "error")
        self.assertEqual(payload["request_id"], "req-2")

    def test_safe_log_gotcha_uses_request_context(self):
        set_request_id("req-3")
        try:
            payload = safe_log_gotcha("contextual_event", message="boom")
        finally:
            clear_request_id()
        self.assertEqual(payload["request_id"], "req-3")


if __name__ == "__main__":
    unittest.main()
