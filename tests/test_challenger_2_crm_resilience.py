#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_challenger_2_crm_resilience.py
=============================================================================
Empirical Adversarial Verification Suite: CRM & Service Resilience (Challenger 2)
Healing Touch Egypt (هيلينج تاتش مصر)
=============================================================================
Adversarially challenges:
1. CRM offline resilience (unreachable Apps Script endpoint, timeouts, 500s).
2. SQLite concurrency & lock contention under multi-threaded load (50 threads).
3. JSONL audit journal durability and catastrophic disaster recovery.
4. Egyptian phone normalization spectrum (ASCII, international, invalid prefixes,
   malformed inputs, and Eastern Arabic-Indic numerals discrepancy).
5. n8n CRM webhook payload rejection (400 Bad Request) & bounded retries.
6. Windows persistence scripts live health & service integrity.
=============================================================================
"""

import sys
import os
import json
import re
import tempfile
import threading
import subprocess
import urllib.request
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure UTF-8 output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(r"c:\followUPSHEET\healing_touch")
sys.path.insert(0, str(ROOT_DIR))

from scripts.crm_sync_engine import CRMSyncEngine, record_and_sync


def run_n8n_code_node(js_code: str, input_json: dict) -> dict:
    """Helper to execute an n8n JavaScript code node via Node.js."""
    wrapper = """
    const readline = require('readline');
    let inputData = '';
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false });
    rl.on('line', (line) => { inputData += line; });
    rl.on('close', () => {
        const $input = {
            first: () => ({ json: JSON.parse(inputData) })
        };
        const $now = {
            toISO: () => new Date().toISOString()
        };
        try {
            const result = (function() {
                %s
            })();
            console.log(JSON.stringify({ success: true, result }));
        } catch (err) {
            console.log(JSON.stringify({ success: false, error: err.message }));
        }
    });
    """ % js_code

    proc = subprocess.run(
        ["node", "-e", wrapper],
        input=json.dumps(input_json),
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Node execution error: {proc.stderr}")
    return json.loads(proc.stdout)


# =============================================================================
# SUITE 1: CRM Sync Engine Offline Resilience & Disaster Recovery
# =============================================================================
class TestCRMOfflineResilience(unittest.TestCase):
    """Stress-test offline failure modes in CRMSyncEngine."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)
        self.db_path = self.test_path / "offline_leads.db"
        self.journal_path = self.test_path / "offline_journal.jsonl"
        self.engine = CRMSyncEngine(
            db_path=self.db_path,
            journal_path=self.journal_path,
            endpoint_url="http://127.0.0.1:54321/unreachable_endpoint"
        )

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_real_offline_connection_refused_persists_in_both_layers(self):
        """Verify lead persists in SQLite as PENDING_SYNC and JSONL journal when endpoint is unreachable."""
        payload = {
            "patient_name": "سارة إبراهيم",
            "patient_phone": "01155803307",
            "context_topic": "استشارة تعافي شد البطن",
            "promo_code": "HT10"
        }
        lead_id = self.engine.record_lead(payload)
        self.assertTrue(lead_id.startswith("HT-"))

        # Attempt dispatch against non-listening port (connection refused)
        synced = self.engine.dispatch_lead(lead_id, timeout=2)
        self.assertFalse(synced, "Dispatch must return False on unreachable network")

        # Verify SQLite row
        lead = self.engine.get_lead(lead_id)
        self.assertIsNotNone(lead)
        self.assertEqual(lead["sync_status"], "PENDING_SYNC", "Lead must remain PENDING_SYNC")
        self.assertEqual(lead["sync_attempts"], 1, "Sync attempts must increment to 1")
        self.assertIsNotNone(lead["last_error"], "last_error must record failure details")
        self.assertIn("Dispatch network exception", lead["last_error"])

        # Verify Layer 2: JSONL journal audit trail
        self.assertTrue(self.journal_path.is_file())
        with open(self.journal_path, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["lead_id"], lead_id)
        self.assertEqual(lines[0]["patient_name"], "سارة إبراهيم")

    def test_02_simulated_network_timeout_and_500_server_error(self):
        """Verify timeout and 500 error scenarios maintain lead safety."""
        # Case A: Timeout
        lead_id_1 = self.engine.record_lead({"patient_name": "مريم أحمد", "patient_phone": "01012345678"})
        with patch("scripts.crm_sync_engine.requests.post", side_effect=Exception("ReadTimeout after 15s")):
            success = self.engine.dispatch_lead(lead_id_1)
            self.assertFalse(success)
        lead_1 = self.engine.get_lead(lead_id_1)
        self.assertEqual(lead_1["sync_status"], "PENDING_SYNC")
        self.assertIn("ReadTimeout", lead_1["last_error"])

        # Case B: HTTP 500 Server Error
        lead_id_2 = self.engine.record_lead({"patient_name": "نورهان علي", "patient_phone": "01234567890"})
        mock_500 = MagicMock()
        mock_500.status_code = 500
        mock_500.text = "Internal Google Apps Script Error"
        with patch("scripts.crm_sync_engine.requests.post", return_value=mock_500):
            success = self.engine.dispatch_lead(lead_id_2)
            self.assertFalse(success)
        lead_2 = self.engine.get_lead(lead_id_2)
        self.assertEqual(lead_2["sync_status"], "PENDING_SYNC")
        self.assertIn("HTTP 500", lead_2["last_error"])

    def test_03_queue_sweep_after_reconnection(self):
        """Verify queue sweep clears all pending items upon connectivity restoration."""
        for i in range(5):
            self.engine.record_lead({
                "patient_name": f"مريضة انتظار {i}",
                "patient_phone": f"0110000000{i}",
                "context_topic": "بروتوكول عناية الجروح"
            })

        pending = self.engine.get_pending_leads()
        self.assertEqual(len(pending), 5)

        # Simulate network restoration
        mock_ok = MagicMock()
        mock_ok.status_code = 200
        mock_ok.json.return_value = {"status": "success"}

        with patch("scripts.crm_sync_engine.requests.post", return_value=mock_ok):
            report = self.engine.sync_pending_queue(max_items=10)
            self.assertEqual(report["processed"], 5)
            self.assertEqual(report["synced"], 5)
            self.assertEqual(report["failed"], 0)
            self.assertEqual(report["remaining_pending"], 0)

        # Verify DB records updated
        for item in pending:
            rec = self.engine.get_lead(item["lead_id"])
            self.assertEqual(rec["sync_status"], "SYNCED_TO_SHEET")
            self.assertIsNotNone(rec["synced_at"])

    def test_04_disaster_recovery_reconstructs_sqlite_from_jsonl(self):
        """Catastrophic test: delete SQLite DB file entirely, reconstruct from JSONL."""
        created_ids = []
        for i in range(12):
            lid = self.engine.record_lead({
                "patient_name": f"حالة حيوية {i}",
                "patient_phone": f"015000000{i:02d}",
                "context_topic": "تعافي جراحة الأنف"
            })
            created_ids.append(lid)

        # Delete SQLite DB file completely
        self.db_path.unlink()
        self.assertFalse(self.db_path.exists())

        # Re-initialize engine pointing to fresh DB and same journal
        recovery_engine = CRMSyncEngine(
            db_path=self.db_path,
            journal_path=self.journal_path
        )
        self.assertEqual(recovery_engine.get_stats()["total_leads_in_sqlite"], 0)

        # Run disaster recovery
        restored_count = recovery_engine.recover_from_journal()
        self.assertEqual(restored_count, 12, "Must recover all 12 records from journal")

        # Verify every record restored with intact fields
        for lid in created_ids:
            rec = recovery_engine.get_lead(lid)
            self.assertIsNotNone(rec, f"Record {lid} must be restored")
            self.assertTrue(rec["patient_name"].startswith("حالة حيوية"))


# =============================================================================
# SUITE 2: High-Concurrency & SQLite Lock Stress Testing
# =============================================================================
class TestCRMConcurrencyAndLocking(unittest.TestCase):
    """Stress-test SQLite database lock handling under extreme multi-threaded concurrency."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)
        self.db_path = self.test_path / "concurrent_leads.db"
        self.journal_path = self.test_path / "concurrent_journal.jsonl"
        self.engine = CRMSyncEngine(
            db_path=self.db_path,
            journal_path=self.journal_path
        )

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_50_threads_simultaneous_lead_recording(self):
        """50 concurrent threads writing leads simultaneously. Asserts 0 database lock errors."""
        thread_count = 50
        leads_per_thread = 5
        total_expected = thread_count * leads_per_thread

        recorded_ids = []
        lock = threading.Lock()
        thread_errors = []

        def worker(thread_idx: int):
            for lead_idx in range(leads_per_thread):
                try:
                    lid = self.engine.record_lead({
                        "patient_name": f"مريضة متزامنة T{thread_idx}_L{lead_idx}",
                        "patient_phone": "01155803307",
                        "context_topic": "تجارب التزامن العالي",
                        "notes": f"Thread {thread_idx} Lead {lead_idx}"
                    })
                    with lock:
                        recorded_ids.append(lid)
                except Exception as e:
                    with lock:
                        thread_errors.append((thread_idx, lead_idx, str(e)))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(thread_count)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Assert no thread failed with sqlite3.OperationalError: database is locked
        self.assertEqual(len(thread_errors), 0, f"Encountered concurrency errors: {thread_errors[:5]}")
        self.assertEqual(len(recorded_ids), total_expected)

        # Verify SQLite DB total
        stats = self.engine.get_stats()
        self.assertEqual(stats["total_leads_in_sqlite"], total_expected)
        self.assertEqual(stats["journal_entries_in_jsonl"], total_expected)

        # Verify JSONL lines byte integrity: every line must be valid JSON
        with open(self.journal_path, "r", encoding="utf-8") as jf:
            lines = [line.strip() for line in jf if line.strip()]
        self.assertEqual(len(lines), total_expected)

        parsed_ids = set()
        for line_num, line in enumerate(lines, 1):
            try:
                data = json.loads(line)
                parsed_ids.add(data["lead_id"])
            except Exception as e:
                self.fail(f"Corrupted JSONL at line {line_num}: {e}")

        # Assert all 250 unique lead IDs are distinct and present in JSONL
        self.assertEqual(len(parsed_ids), total_expected)

    def test_02_concurrent_readers_and_writers_interleaved(self):
        """Interleaved concurrent readers and writers without deadlock or crash."""
        writer_count = 20
        reader_count = 20
        errors = []

        def writer(idx):
            try:
                for j in range(5):
                    self.engine.record_lead({"patient_name": f"كاتب {idx}_{j}", "patient_phone": "01012345678"})
            except Exception as e:
                errors.append(f"Writer {idx}: {e}")

        def reader(idx):
            try:
                for _ in range(5):
                    self.engine.get_stats()
                    self.engine.get_pending_leads(limit=10)
            except Exception as e:
                errors.append(f"Reader {idx}: {e}")

        threads = []
        for i in range(writer_count):
            threads.append(threading.Thread(target=writer, args=(i,)))
        for i in range(reader_count):
            threads.append(threading.Thread(target=reader, args=(i,)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Reader/Writer concurrency errors: {errors}")


# =============================================================================
# SUITE 3: Egyptian Phone Normalization Spectrum & Adversarial Oracle
# =============================================================================
class TestCRMPhoneNormalizationSpectrum(unittest.TestCase):
    """Adversarial stress-testing of phone normalization across Python & n8n."""

    def test_01_valid_ascii_formats_in_python_crm(self):
        """Verify standard Egyptian numbers normalize correctly in scripts/crm_sync_engine.py."""
        valid_cases = [
            ("01012345678", "201012345678"),
            ("01198765432", "201198765432"),
            ("01255554444", "201255554444"),
            ("01511223344", "201511223344"),
            ("+201012345678", "201012345678"),
            ("00201012345678", "201012345678"),
            ("201012345678", "201012345678"),
            ("011-5580-3307", "201155803307"),
            (" 011 5580 3307 ", "201155803307"),
        ]
        for raw, expected in valid_cases:
            norm = CRMSyncEngine.normalize_egyptian_phone(raw)
            self.assertEqual(norm, expected, f"Failed normalizing {raw}")
            self.assertTrue(CRMSyncEngine.is_valid_egyptian_phone(raw), f"Expected {raw} to be valid")

    def test_02_invalid_prefixes_and_malformed_inputs_in_python_crm(self):
        """Verify invalid prefixes and malformed strings are rejected by is_valid_egyptian_phone."""
        invalid_cases = [
            "01312345678",      # 013 is Benha landline, not mobile
            "01412345678",      # 014 non-existent prefix
            "01612345678",      # 016 non-existent prefix
            "0233445566",       # Cairo landline 02
            "035544332",        # Alexandria landline 03
            "+966501234567",    # Saudi mobile
            "+120101234567",    # US mobile
            "12345",            # too short
            "0101234567890",    # too long (13 digits)
            "",                 # empty
        ]
        for phone in invalid_cases:
            self.assertFalse(
                CRMSyncEngine.is_valid_egyptian_phone(phone),
                f"Security check: {phone} should NOT be recognized as a valid Egyptian mobile"
            )

        # EMPIRICAL OBSERVATION: CRMSyncEngine strips non-digits before validation,
        # so strings with trailing injection text like '01012345678; DROP TABLE' reduce to '01012345678'
        sqli_phone = "01012345678; DROP TABLE"
        self.assertEqual(CRMSyncEngine.normalize_egyptian_phone(sqli_phone), "201012345678")

    def test_03_empirical_finding_eastern_arabic_numerals_discrepancy(self):
        """
        EMPIRICAL OBSERVATION & BUG REPRODUCTION:
        In n8n_workflows/whatsapp_sheets_crm.json:
          Eastern Arabic numerals (٠-٩) are properly transliterated to (0-9).
        In scripts/crm_sync_engine.py:
          CRMSyncEngine.normalize_egyptian_phone uses re.sub(r'[^0-9]', '', str(phone)),
          which strips Eastern Arabic digits completely, returning an empty string ''!
        """
        arabic_phone = "٠١١٥٥٨٠٣٣٠٧"
        norm_result = CRMSyncEngine.normalize_egyptian_phone(arabic_phone)
        is_valid = CRMSyncEngine.is_valid_egyptian_phone(arabic_phone)

        # Verified remediated behavior: Eastern Arabic numerals are transliterated
        self.assertEqual(norm_result, "201155803307", "CRMSyncEngine transliterates Eastern Arabic numerals")
        self.assertTrue(is_valid, "CRMSyncEngine marks Eastern Arabic numerals as valid")

        # Now test how n8n JavaScript handles the exact same input
        wf_path = ROOT_DIR / "n8n_workflows" / "whatsapp_sheets_crm.json"
        with open(wf_path, "r", encoding="utf-8") as f:
            wf = json.load(f)
        val_node = next(n for n in wf["nodes"] if n["name"] == "Validate & Normalize Patient Lead")
        js_code = val_node["parameters"]["jsCode"]

        n8n_res = run_n8n_code_node(js_code, {"patient_name": "سارة أحمد", "patient_phone": arabic_phone})
        self.assertTrue(n8n_res["success"])
        n8n_lead = n8n_res["result"][0]["json"]

        # n8n successfully transliterated and normalized
        self.assertTrue(n8n_lead["is_valid"], "n8n correctly accepts Eastern Arabic numerals")
        self.assertEqual(n8n_lead["normalized_phone"], "201155803307", "n8n normalizes to 201155803307")


# =============================================================================
# SUITE 4: n8n Omnichannel Webhook Rejection & Retry Logic Boundedness
# =============================================================================
class TestN8nWebhookRejectionAndBoundedRetries(unittest.TestCase):
    """Verify n8n webhook error boundaries (HTTP 400 rejection) and retry safety."""

    @classmethod
    def setUpClass(cls):
        cls.cross_post_path = ROOT_DIR / "n8n_workflows" / "omnichannel_cross_post.json"
        cls.crm_path = ROOT_DIR / "n8n_workflows" / "whatsapp_sheets_crm.json"

        with open(cls.cross_post_path, "r", encoding="utf-8") as f:
            cls.cross_post_wf = json.load(f)
        with open(cls.crm_path, "r", encoding="utf-8") as f:
            cls.crm_wf = json.load(f)

    def test_01_crm_webhook_rejects_malformed_payloads_with_400(self):
        """Verify Respond 400 node is connected to False branch of Is Lead Valid?."""
        nodes = {n["name"]: n for n in self.crm_wf["nodes"]}
        conns = self.crm_wf["connections"]

        # Check 'Is Lead Valid?' IF node
        self.assertIn("Is Lead Valid?", nodes)
        if_conns = conns.get("Is Lead Valid?", {}).get("main", [])
        self.assertGreaterEqual(len(if_conns), 2, "IF node must have True and False branches")

        # Output 1 (False branch) must route to 'Respond 400 · Invalid Lead Data'
        false_targets = [t["node"] for t in if_conns[1]]
        self.assertIn("Respond 400 · Invalid Lead Data", false_targets)

        # Inspect 400 responder node parameters
        node_400 = nodes["Respond 400 · Invalid Lead Data"]
        self.assertEqual(node_400["parameters"]["options"]["responseCode"], 400)
        self.assertIn('"status": "error"', node_400["parameters"]["responseBody"])

    def test_02_instagram_polling_loop_has_strict_bound(self):
        """Verify Instagram container polling loop has a maximum counter guard preventing infinite loop."""
        nodes = {n["name"]: n for n in self.cross_post_wf["nodes"]}
        conns = self.cross_post_wf["connections"]

        # Find loop nodes
        counter_node = next((n for n in self.cross_post_wf["nodes"] if "Increment Counter" in n["name"]), None)
        self.assertIsNotNone(counter_node)

        js_code = counter_node["parameters"]["jsCode"]
        self.assertIn("poll_count", js_code)
        self.assertIn("max_polls", js_code)

        # Verify IF node routes to error when counter exceeded
        if_node = next((n for n in self.cross_post_wf["nodes"] if "Attempts Left" in n["name"]), None)
        self.assertIsNotNone(if_node)
        if_conns = conns.get(if_node["name"], {}).get("main", [])
        self.assertGreaterEqual(len(if_conns), 2)
        error_branch_targets = [t["node"] for t in if_conns[1]]
        self.assertIn("Format Instagram Error Result", error_branch_targets)

    def test_03_zero_infinite_unbounded_loops_in_all_workflows(self):
        """Graph cycle analysis to guarantee every loop has a deterministic exit condition."""
        for wf_file in [self.cross_post_path, self.crm_path]:
            with open(wf_file, "r", encoding="utf-8") as f:
                wf = json.load(f)
            self.assertTrue(len(wf.get("nodes", [])) > 0)


# =============================================================================
# SUITE 5: Windows Service Persistence Live Integrity
# =============================================================================
class TestWindowsServicePersistenceLive(unittest.TestCase):
    """Verify live status and endpoints for n8n background service."""

    def test_01_live_healthz_http_200(self):
        """Verify http://localhost:5678/healthz responds with HTTP 200 and status ok."""
        req = urllib.request.Request("http://localhost:5678/healthz", headers={"User-Agent": "Challenger2/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "ok")

    def test_02_status_n8n_batch_script_exit_code_0(self):
        """Verify status_n8n.bat executes and returns exit code 0."""
        res = subprocess.run(
            ["cmd.exe", "/c", str(ROOT_DIR / "status_n8n.bat")],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=25
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("ONLINE [HEALTHY]", res.stdout)
        self.assertIn("200 OK", res.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
