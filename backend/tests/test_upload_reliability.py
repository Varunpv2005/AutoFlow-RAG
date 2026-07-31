import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi import UploadFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.file_service import upload_file


class UploadReliabilityTests(unittest.TestCase):
    def test_upload_rolls_back_and_cleans_up_on_db_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_dir = os.path.join(temp_dir, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            db = MagicMock()
            db.commit.side_effect = RuntimeError("db unavailable")

            upload = UploadFile(filename="sample.txt", file=io.BytesIO(b"hello"))

            with patch("app.services.file_service.UPLOAD_DIR", upload_dir):
                with self.assertRaises(RuntimeError):
                    upload_file(file=upload, db=db, user_id=1)

            self.assertEqual(os.listdir(upload_dir), [])
            db.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
