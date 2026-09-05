"""Tests for multi-recipient practice report email settings."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from practice_email.delivery import send_report
from practice_email.settings import EmailSettings, merge_recipients, parse_email_recipients


class TestPracticeEmailRecipients(unittest.TestCase):
    def test_parse_email_recipients_splits_and_dedupes(self) -> None:
        raw = "forceinteg@gmail.com, itsgeeth@gmail.com; forceinteg@gmail.com"
        self.assertEqual(
            parse_email_recipients(raw),
            ["forceinteg@gmail.com", "itsgeeth@gmail.com"],
        )

    def test_merge_recipients_combines_to_and_cc(self) -> None:
        merged = merge_recipients("a@example.com", "b@example.com, a@example.com")
        self.assertEqual(merged, ("a@example.com", "b@example.com"))

    @patch("practice_email.delivery._deliver_message")
    @patch("practice_email.delivery.delivery_ready", return_value=(True, "gmail_api", ""))
    @patch("practice_email.delivery.load_settings")
    def test_send_report_delivers_to_all_recipients(
        self,
        mock_load: unittest.mock.MagicMock,
        _mock_ready: unittest.mock.MagicMock,
        mock_deliver: unittest.mock.MagicMock,
    ) -> None:
        mock_load.return_value = EmailSettings(
            enabled=True,
            recipients=("forceinteg@gmail.com", "itsgeeth@gmail.com"),
            harshit_student_email="student@example.com",
            transport="auto",
            smtp_host="",
            smtp_port=587,
            smtp_user="",
            smtp_password="",
            smtp_from="",
            use_tls=True,
            gmail_client_id="id",
            gmail_client_secret="secret",
            gmail_refresh_token="token",
        )
        mock_deliver.side_effect = lambda settings, **kwargs: type(
            "R",
            (),
            {"ok": True, "recipient": kwargs["recipient"], "transport": "gmail_api", "error": ""},
        )()

        result = send_report(
            student_name="Arjun",
            unit_title="Unit 1",
            unit_subtitle="Test",
            report={"correct_count": 10, "total": 10, "score_pct": 100},
            time_spent_seconds=120,
        )

        self.assertTrue(result.ok)
        self.assertEqual(mock_deliver.call_count, 2)
        self.assertIn("forceinteg@gmail.com", result.recipient)
        self.assertIn("itsgeeth@gmail.com", result.recipient)


if __name__ == "__main__":
    unittest.main()
