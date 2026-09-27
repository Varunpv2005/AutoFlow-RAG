import sys
import os
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app, rag_pipeline
from app.config import settings


class UserIsolationAndSecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check_status_configured(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("llm", data)
        self.assertIn(data["llm"]["msg"], ["Configured", "Unconfigured"])

    def test_analytics_user_scoping(self):
        username = "isolation_test_user_val"
        signup_res = self.client.post("/api/auth/signup", json={"username": username, "password": "Password123!"})
        if signup_res.status_code == 409:
            login_res = self.client.post("/api/auth/login", json={"username": username, "password": "Password123!"})
            token = login_res.json()["access_token"]
        else:
            token = signup_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        res = self.client.get("/api/analytics", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["users"], 1)
        self.assertIn("user_documents", data)
        self.assertIn("user_chats", data)

    def test_user_isolation_rag_retrieval_candidate_filtering(self):
        # Create documents for User A (ID 101) and User B (ID 202)
        # Add multiple identical high-similarity chunks for User B to dominate initial candidates
        user_b_docs = [
            Document(page_content=f"Secret financial report candidate {i} for User B", metadata={"user_id": 202, "file_id": 200})
            for i in range(15)
        ]
        user_a_docs = [
            Document(page_content="Secret financial report for User A unique query context", metadata={"user_id": 101, "file_id": 100})
        ]

        from langchain_community.vectorstores import FAISS
        test_vectorstore = FAISS.from_documents(user_b_docs + user_a_docs, rag_pipeline.embeddings)

        original_vectorstore = rag_pipeline.vectorstore
        try:
            rag_pipeline.vectorstore = test_vectorstore

            # Query for User A — must filter candidates against User A's identity and return ONLY User A's chunk
            res_a = rag_pipeline.retrieve("financial report", k=4, metadata_filter={"user_id": 101})
            self.assertTrue(len(res_a) > 0)
            for doc in res_a:
                self.assertEqual(doc.metadata.get("user_id"), 101)
                self.assertNotIn("User B", doc.page_content)

            # Query for User B — must return ONLY User B's chunks
            res_b = rag_pipeline.retrieve("financial report", k=4, metadata_filter={"user_id": 202})
            self.assertTrue(len(res_b) > 0)
            for doc in res_b:
                self.assertEqual(doc.metadata.get("user_id"), 202)
                self.assertNotIn("User A", doc.page_content)

        finally:
            rag_pipeline.vectorstore = original_vectorstore


if __name__ == "__main__":
    unittest.main()
