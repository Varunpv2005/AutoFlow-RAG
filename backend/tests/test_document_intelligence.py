import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.document_intelligence import enrich_file_metadata


class DocumentIntelligenceTests(unittest.TestCase):
    def test_enrich_file_metadata_returns_expected_shape(self):
        payload = {
            "summary": "A summary",
            "keywords": ["ai", "rag"],
            "suggested_questions": ["What is this?"],
        }
        with patch("app.document_intelligence.gemini_service.invoke", return_value=json.dumps(payload)):
            self.assertEqual(enrich_file_metadata("some text"), payload)

    def test_enrich_file_metadata_handles_empty_text(self):
        self.assertEqual(
            enrich_file_metadata(""),
            {"summary": "", "keywords": [], "suggested_questions": []},
        )


if __name__ == "__main__":
    unittest.main()
