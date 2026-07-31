import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi import UploadFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.file_service import upload_file, get_file_preview


class FileUploadCleanupTests(unittest.TestCase):
    def test_upload_removes_saved_file_when_commit_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_dir = os.path.join(temp_dir, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            db = MagicMock()
            db.commit.side_effect = RuntimeError("db failed")

            upload = UploadFile(filename="sample.txt", file=io.BytesIO(b"hello world"))

            with patch("app.services.file_service.UPLOAD_DIR", upload_dir):
                with self.assertRaises(RuntimeError):
                    upload_file(file=upload, db=db, user_id=1)

            self.assertEqual(os.listdir(upload_dir), [])
            db.rollback.assert_called_once()

    def test_upload_records_file_size_and_indexing_defaults(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_dir = os.path.join(temp_dir, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            db = MagicMock()
            upload = UploadFile(filename="sample.txt", file=io.BytesIO(b"hello world"))

            with patch("app.services.file_service.UPLOAD_DIR", upload_dir):
                saved_file = upload_file(file=upload, db=db, user_id=1)

            self.assertEqual(saved_file.file_size_bytes, 11)
            self.assertEqual(saved_file.chunk_count, 0)
            self.assertEqual(saved_file.is_indexed, 0)

    def test_get_file_preview_returns_text_for_txt_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "sample.txt")
            with open(file_path, "w", encoding="utf-8") as handle:
                handle.write("Hello preview")

            preview = get_file_preview(file_path)

            self.assertEqual(preview["type"], "text")
            self.assertIn("Hello preview", preview["content"])


if __name__ == "__main__":
    unittest.main()
