#!/usr/bin/env python3
"""
tests/test_crm_sync_engine.py
=============================================================================
Unit Test Suite for Healing Touch Egypt CRM Dual-Layer Offline Sync Engine
=============================================================================
Validates:
  1. SQLite schema initialization and indexing
  2. Dual-layer persistence (SQLite DB + append-only JSONL journal)
  3. Egyptian phone normalization and validation
  4. Offline network failure handling and queue preservation (PENDING_SYNC)
  5. Successful live dispatch and status update (SYNCED_TO_SHEET)
  6. Batch queue sweeping
  7. Disaster Recovery from JSONL journal
  8. Storage statistics reporting
=============================================================================
"""

import os
import sys
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure UTF-8 output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.crm_sync_engine import CRMSyncEngine, record_and_sync


class TestCRMSyncEngine(unittest.TestCase):

    def setUp(self):
        # Create temporary isolated directory for tests
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)
        self.db_path = self.test_path / "test_leads.db"
        self.journal_path = self.test_path / "test_journal.jsonl"
        self.endpoint_url = "https://script.google.com/macros/s/TEST_ENDPOINT_ID/exec"

        self.engine = CRMSyncEngine(
            db_path=self.db_path,
            journal_path=self.journal_path,
            endpoint_url=self.endpoint_url
        )

    def tearDown(self):
        try:
            self.test_dir.cleanup()
        except Exception:
            pass

    def test_01_sqlite_initialization(self):
        """Verify SQLite DB and required indexes are created properly."""
        self.assertTrue(self.db_path.is_file(), "SQLite DB file must exist")
        with self.engine._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='consultation_leads';")
            self.assertIsNotNone(cursor.fetchone(), "consultation_leads table must exist")

            cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_leads_sync_status';")
            self.assertIsNotNone(cursor.fetchone(), "idx_leads_sync_status index must exist")

    def test_02_egyptian_phone_normalization(self):
        """Verify phone cleaning and normalization to 201XXXXXXXXX."""
        test_cases = [
            ("01155803307", "201155803307"),
            ("01012345678", "201012345678"),
            ("01298765432", "201298765432"),
            ("01555555555", "201555555555"),
            ("+201155803307", "201155803307"),
            ("00201155803307", "201155803307"),
            ("011-5580-3307", "201155803307"),
            (" 011 5580 3307 ", "201155803307"),
        ]
        for raw, expected in test_cases:
            norm = self.engine.normalize_egyptian_phone(raw)
            self.assertEqual(norm, expected, f"Failed normalizing {raw}")
            self.assertTrue(self.engine.is_valid_egyptian_phone(raw))

        # Invalid phone
        self.assertFalse(self.engine.is_valid_egyptian_phone("01912345678"))
        self.assertFalse(self.engine.is_valid_egyptian_phone("12345"))

    def test_03_dual_layer_recording(self):
        """Verify lead is stored in BOTH SQLite and JSONL journal."""
        payload = {
            "patient_name": "سارة أحمد",
            "patient_phone": "01155803307",
            "context_topic": "بروتوكول تعافي الولادة القيصرية",
            "promo_code": "HT10",
            "channel": "whatsapp",
            "source": "wa.html"
        }

        lead_id = self.engine.record_lead(payload)
        self.assertTrue(lead_id.startswith("HT-"))

        # Verify SQLite row
        lead = self.engine.get_lead(lead_id)
        self.assertIsNotNone(lead)
        self.assertEqual(lead["patient_name"], "سارة أحمد")
        self.assertEqual(lead["normalized_phone"], "201155803307")
        self.assertEqual(lead["sync_status"], "PENDING_SYNC")
        self.assertEqual(lead["sync_attempts"], 0)

        # Verify JSONL journal line
        self.assertTrue(self.journal_path.is_file(), "JSONL journal must exist")
        with open(self.journal_path, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["lead_id"], lead_id)
        self.assertEqual(lines[0]["patient_name"], "سارة أحمد")

    def test_04_offline_fallback_handling(self):
        """Verify that network failures keep lead safely in PENDING_SYNC status."""
        payload = {
            "patient_name": "نور الهدى",
            "patient_phone": "01099887766",
            "context_topic": "دعامات الأنف بعد التجميل"
        }
        lead_id = self.engine.record_lead(payload)

        # Mock network failure (ConnectionError)
        with patch("scripts.crm_sync_engine.requests.post", side_effect=Exception("Network unreachable / Offline")):
            success = self.engine.dispatch_lead(lead_id)
            self.assertFalse(success, "Dispatch should report False when offline")

        # Verify status is still PENDING_SYNC with incremented attempts
        lead = self.engine.get_lead(lead_id)
        self.assertEqual(lead["sync_status"], "PENDING_SYNC")
        self.assertEqual(lead["sync_attempts"], 1)
        self.assertIn("Network unreachable", lead["last_error"])

    def test_05_successful_sync(self):
        """Verify successful HTTP POST updates lead to SYNCED_TO_SHEET."""
        payload = {
            "patient_name": "مريم محمود",
            "patient_phone": "01233445566",
            "context_topic": "علاج ندبات استئصال الغدة الدرقية"
        }
        lead_id = self.engine.record_lead(payload)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "status": "success",
            "lead_id": lead_id,
            "message": "Lead recorded successfully"
        }

        with patch("scripts.crm_sync_engine.requests.post", return_value=mock_resp):
            success = self.engine.dispatch_lead(lead_id)
            self.assertTrue(success, "Dispatch should report True on HTTP 200 success")

        lead = self.engine.get_lead(lead_id)
        self.assertEqual(lead["sync_status"], "SYNCED_TO_SHEET")
        self.assertEqual(lead["sync_attempts"], 1)
        self.assertIsNotNone(lead["synced_at"])
        self.assertIsNone(lead["last_error"])

    def test_06_batch_queue_sweep(self):
        """Verify sweep of multiple pending leads."""
        leads = [
            {"patient_name": f"مريضة {i}", "patient_phone": f"0110000000{i}", "context_topic": "ندبات"}
            for i in range(3)
        ]
        for l in leads:
            self.engine.record_lead(l)

        self.assertEqual(len(self.engine.get_pending_leads()), 3)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "success"}

        with patch("scripts.crm_sync_engine.requests.post", return_value=mock_resp):
            report = self.engine.sync_pending_queue()
            self.assertEqual(report["processed"], 3)
            self.assertEqual(report["synced"], 3)
            self.assertEqual(report["failed"], 0)
            self.assertEqual(report["remaining_pending"], 0)

        # All leads should now be SYNCED_TO_SHEET
        self.assertEqual(len(self.engine.get_pending_leads()), 0)

    def test_07_disaster_recovery_from_journal(self):
        """Verify rebuilding SQLite from JSONL journal after total DB loss."""
        # 1. Record 3 leads
        lead_ids = []
        for i in range(3):
            lid = self.engine.record_lead({
                "patient_name": f"حالة مسترجعة {i}",
                "patient_phone": f"0120000000{i}",
                "context_topic": "جراحة تكميم المعدة"
            })
            lead_ids.append(lid)

        # 2. Simulate catastrophic SQLite deletion
        with self.engine._connect() as conn:
            conn.cursor().execute("DELETE FROM consultation_leads;")
            conn.commit()

        stats_empty = self.engine.get_stats()
        self.assertEqual(stats_empty["total_leads_in_sqlite"], 0)
        self.assertEqual(stats_empty["journal_entries_in_jsonl"], 3)

        # 3. Perform disaster recovery from journal
        restored = self.engine.recover_from_journal()
        self.assertEqual(restored, 3)

        # 4. Verify all leads restored with exact IDs
        stats_restored = self.engine.get_stats()
        self.assertEqual(stats_restored["total_leads_in_sqlite"], 3)
        for lid in lead_ids:
            lead = self.engine.get_lead(lid)
            self.assertIsNotNone(lead)
            self.assertTrue(lead["patient_name"].startswith("حالة مسترجعة"))

    def test_08_record_and_sync_helper(self):
        """Verify high-level record_and_sync convenience function."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "success"}

        with patch("scripts.crm_sync_engine.requests.post", return_value=mock_resp):
            lid, synced = record_and_sync({
                "patient_name": "ياسمين كمال",
                "patient_phone": "01511223344",
                "context_topic": "تضميد جروح السمنة"
            }, engine=self.engine)

            self.assertTrue(lid.startswith("HT-"))
            self.assertTrue(synced)
            lead = self.engine.get_lead(lid)
            self.assertEqual(lead["sync_status"], "SYNCED_TO_SHEET")


if __name__ == "__main__":
    unittest.main(verbosity=2)
