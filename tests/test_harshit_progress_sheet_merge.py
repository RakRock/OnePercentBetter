"""Tests for Harshit Physics/Chemistry progress merge from Google Sheets."""

import os
import tempfile
import unittest

import database as db


class HarshitProgressSheetMergeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._db_fd, cls._db_path = tempfile.mkstemp(suffix=".db")
        os.close(cls._db_fd)
        cls._prev_db = os.environ.get("ONEPERCENT_DB")
        os.environ["ONEPERCENT_DB"] = cls._db_path
        db.init_db()
        user = db.get_user("Harshit Sai")
        if not user:
            raise RuntimeError("seed user missing")
        cls.user_id = user["id"]

    @classmethod
    def tearDownClass(cls):
        if cls._prev_db is None:
            os.environ.pop("ONEPERCENT_DB", None)
        else:
            os.environ["ONEPERCENT_DB"] = cls._prev_db
        os.unlink(cls._db_path)

    def test_merge_concept_progress_keeps_viewed(self):
        db.merge_harshit_concept_progress_from_sheet(
            self.user_id,
            module="physics",
            unit_id=1,
            concept_id="u1_d1_c1",
            viewed=1,
            marked_review=0,
            simpler_requests=0,
            example_requests=0,
        )
        db.merge_harshit_concept_progress_from_sheet(
            self.user_id,
            module="physics",
            unit_id=1,
            concept_id="u1_d1_c1",
            viewed=0,
            marked_review=1,
            simpler_requests=2,
            example_requests=1,
        )
        viewed = db.get_harshit_physics_viewed_concepts(self.user_id, unit_id=1)
        review = db.get_harshit_physics_review_concepts(self.user_id, unit_id=1)
        self.assertIn("u1_d1_c1", viewed)
        self.assertIn("u1_d1_c1", review)

    def test_merge_day_progress_prefers_complete(self):
        db.merge_harshit_day_progress_from_sheet(
            self.user_id,
            module="physics",
            unit_id=1,
            day_id=1,
            status="in_progress",
            concepts_viewed=3,
            concepts_total=10,
        )
        db.merge_harshit_day_progress_from_sheet(
            self.user_id,
            module="physics",
            unit_id=1,
            day_id=1,
            status="complete",
            concepts_viewed=10,
            concepts_total=10,
        )
        with db.get_connection() as conn:
            row = conn.execute(
                """SELECT status, concepts_viewed FROM harshit_physics_day_status
                   WHERE user_id = ? AND unit_id = ? AND day_id = ?""",
                (self.user_id, 1, 1),
            ).fetchone()
        self.assertEqual(row["status"], "complete")
        self.assertEqual(int(row["concepts_viewed"]), 10)


if __name__ == "__main__":
    unittest.main()
