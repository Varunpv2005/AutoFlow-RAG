import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.analytics import analytics


class AnalyticsTests(unittest.TestCase):
    def test_analytics_snapshot_updates(self):
        snapshot = analytics
        snapshot.total_queries = 0
        snapshot.average_retrieval_latency = 0.0
        snapshot.average_llm_response_time = 0.0
        snapshot.uploaded_documents = 0
        snapshot.total_chunks = 0
        snapshot.embedding_generation_time = 0.0
        snapshot._retrieval_latencies = []
        snapshot._llm_response_times = []
        snapshot._embedding_times = []

        snapshot.record_query(0.4, 1.2)
        snapshot.record_query(0.6, 1.8)
        snapshot.record_upload(10, 0.5)

        data = snapshot.to_dict()
        self.assertEqual(data["total_queries"], 2)
        self.assertEqual(data["average_retrieval_latency"], 0.5)
        self.assertEqual(data["average_llm_response_time"], 1.5)
        self.assertEqual(data["uploaded_documents"], 1)
        self.assertEqual(data["total_chunks"], 10)
        self.assertEqual(data["embedding_generation_time"], 0.5)


if __name__ == "__main__":
    unittest.main()
