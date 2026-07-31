import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.chat_service import chat_service


class ChatServicePerformanceTests(unittest.TestCase):
    def test_chat_service_uses_cached_user_file_ids(self):
        class DummyDB:
            def __init__(self):
                self.added = []
                self.committed = False
                self.refreshed = []

            def query(self, model):
                class Query:
                    def __init__(self, owner):
                        self.owner = owner

                    def filter(self, *args, **kwargs):
                        return self

                    def all(self):
                        return [SimpleNamespace(id=1, user_id=1)]

                return Query(self)

            def add(self, obj):
                self.added.append(obj)

            def commit(self):
                self.committed = True

            def refresh(self, obj):
                self.refreshed.append(obj)

        class DummyPipeline:
            def retrieve(self, question, k=None, keywords=None, metadata_filter=None):
                return [SimpleNamespace(page_content="content", metadata={"file_id": "1"})]

        class DummyLLM:
            def invoke(self, prompt):
                return "answer"

        db = DummyDB()
        result = chat_service(
            question="hello",
            file_id=1,
            db=db,
            rag_pipeline=DummyPipeline(),
            llm=DummyLLM(),
            user_id=1,
        )

        self.assertEqual(result["answer"], "answer")
        self.assertTrue(db.committed)


if __name__ == "__main__":
    unittest.main()
