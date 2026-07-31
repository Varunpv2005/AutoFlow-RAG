import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.file_service import upload_file


class DocumentVersioningTests(unittest.TestCase):
    def test_upload_creates_new_version_for_existing_filename(self):
        class DummyDB:
            def __init__(self):
                self.added = []
                self.committed = False
                self.refreshed = []
                self.query_results = []

            def query(self, model):
                class Query:
                    def filter(self, *args, **kwargs):
                        return self

                    def all(self):
                        return self.owner.query_results

                query = Query()
                query.owner = self
                return query

            def add(self, obj):
                self.added.append(obj)

            def commit(self):
                self.committed = True

            def refresh(self, obj):
                self.refreshed.append(obj)

        class DummyFile:
            pass

        db = DummyDB()
        db.query_results = [SimpleNamespace(id=1, filename="report.pdf", user_id=1)]
        import io
        import os
        import tempfile
        from fastapi import UploadFile
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("app.services.file_service.UPLOAD_DIR", temp_dir):
                upload = UploadFile(filename="report.pdf", file=io.BytesIO(b"hello"))
                result = upload_file(file=upload, db=db, user_id=1)
                self.assertEqual(result.filename, "report.pdf")
                self.assertEqual(result.version, 2)


if __name__ == "__main__":
    unittest.main()
