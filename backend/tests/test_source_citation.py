import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.chat_service import build_source_citations


class SourceCitationTests(unittest.TestCase):
    def test_build_source_citations_uses_retrieved_chunk_metadata(self):
        docs = [
            SimpleNamespace(
                page_content="content-a",
                metadata={"filename": "report.pdf", "page": 3, "chunk_index": 7, "score": 0.91},
            ),
            SimpleNamespace(
                page_content="content-b",
                metadata={"file_name": "notes.txt", "page_number": 2, "chunk_id": 4, "similarity_score": 0.77},
            ),
        ]

        citations = build_source_citations(docs)

        self.assertEqual(citations[0]["document_name"], "report.pdf")
        self.assertEqual(citations[0]["page_number"], 3)
        self.assertEqual(citations[0]["chunk_id"], 7)
        self.assertEqual(citations[0]["similarity_score"], 0.91)
        self.assertEqual(citations[1]["document_name"], "notes.txt")
        self.assertEqual(citations[1]["page_number"], 2)
        self.assertEqual(citations[1]["chunk_id"], 4)
        self.assertEqual(citations[1]["similarity_score"], 0.77)


if __name__ == "__main__":
    unittest.main()
