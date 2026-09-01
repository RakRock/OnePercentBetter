"""Tests for unit test work photo uploads."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import harshit_class10_unit_test_uploads as h10utu


class _FakeUpload:
    def __init__(self, name: str, data: bytes) -> None:
        self.name = name
        self._data = data

    def getvalue(self) -> bytes:
        return self._data


class TestUnitTestUploads(unittest.TestCase):
    def test_work_upload_required_for_written_only(self) -> None:
        self.assertTrue(h10utu.work_upload_required({"type": "written", "marks": 2}))
        self.assertFalse(h10utu.work_upload_required({"type": "mcq", "marks": 1}))

    def test_test_requires_work_photo(self) -> None:
        self.assertTrue(
            h10utu.test_requires_work_photo([{"type": "mcq"}, {"type": "written"}])
        )
        self.assertFalse(h10utu.test_requires_work_photo([{"type": "mcq"}]))

    def test_has_work_upload(self) -> None:
        self.assertFalse(h10utu.has_work_upload({}))
        self.assertTrue(h10utu.has_work_upload({"work_images": [{"path": "/x.jpg"}]}))
        self.assertFalse(h10utu.has_session_work_upload([]))
        self.assertTrue(h10utu.has_session_work_upload([{"path": "/x.jpg"}]))

    def test_save_session_work_images_jpg(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(h10utu, "WORK_ROOT", Path(tmp)):
                data = b"\xff\xd8\xff fake jpeg"
                merged, err = h10utu.save_session_work_images(
                    session_id="sess-1",
                    student_name="Harshit",
                    unit_id=1,
                    uploaded_files=_FakeUpload("paper.jpg", data),
                )
                self.assertIsNone(err)
                self.assertEqual(len(merged), 1)
                path = Path(merged[0]["path"])
                self.assertTrue(path.is_file())
                self.assertEqual(path.read_bytes(), data)
                self.assertIn("paper", str(path))

    def test_save_work_images_jpg(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(h10utu, "WORK_ROOT", Path(tmp)):
                data = b"\xff\xd8\xff fake jpeg"
                merged, err = h10utu.save_work_images(
                    session_id="sess-1",
                    student_name="Harshit",
                    unit_id=1,
                    q_num=6,
                    uploaded_files=[_FakeUpload("page1.jpg", data)],
                )
                self.assertIsNone(err)
                self.assertEqual(len(merged), 1)
                path = Path(merged[0]["path"])
                self.assertTrue(path.is_file())
                self.assertEqual(path.read_bytes(), data)

    def test_replace_keeps_one_photo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(h10utu, "WORK_ROOT", Path(tmp)):
                first, err1 = h10utu.save_session_work_images(
                    session_id="sess-3",
                    student_name="Harshit",
                    unit_id=3,
                    uploaded_files=_FakeUpload("first.jpg", b"\xff\xd8\xff a"),
                )
                self.assertIsNone(err1)
                second, err2 = h10utu.save_session_work_images(
                    session_id="sess-3",
                    student_name="Harshit",
                    unit_id=3,
                    uploaded_files=_FakeUpload("second.jpg", b"\xff\xd8\xff b"),
                    existing=first,
                )
                self.assertIsNone(err2)
                self.assertEqual(len(second), 1)
                self.assertEqual(second[0]["filename"], "second.jpg")

    def test_rejects_non_image_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(h10utu, "WORK_ROOT", Path(tmp)):
                merged, err = h10utu.save_work_images(
                    session_id="sess-2",
                    student_name="Harshit",
                    unit_id=1,
                    q_num=7,
                    uploaded_files=[_FakeUpload("notes.pdf", b"%PDF")],
                )
                self.assertEqual(merged, [])
                self.assertIn("JPG", err or "")

    def test_work_upload_label_for_paper(self) -> None:
        label = h10utu.work_upload_label({"section": "D", "marks": 5})
        self.assertIn("one photo", label)
        self.assertIn("submit", label)


if __name__ == "__main__":
    unittest.main()
