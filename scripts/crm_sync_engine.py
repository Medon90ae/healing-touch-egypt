#!/usr/bin/env python3
"""
scripts/crm_sync_engine.py
=============================================================================
Healing Touch Egypt — Production CRM Dual-Layer Offline Sync Engine (Zero-GCP)
=============================================================================

This module provides a fail-safe, 100% free CRM persistence and synchronization
engine that bridges patient consultation requests to Google Sheets via Google
Apps Script Web App without any dependency on Google Cloud Platform (GCP)
Console, OAuth credentials, or billing cards.

Architecture:
  Dual-Layer Local Offline Storage:
    1. Layer 1 (Relational / Queue): SQLite database (leads_fallback.db)
       - Tracks state: PENDING_SYNC, SYNCED_TO_SHEET, FAILED_FATAL
       - Records retry counts, error timestamps, and sync dates.
    2. Layer 2 (Audit / Disaster Recovery): Append-only JSONL (leads_journal.jsonl)
       - Immutable stream of raw events for audit and catastrophic DB recovery.

  Sync Queue & Retry Mechanism:
    - Attempts immediate HTTP POST to Apps Script Web App endpoint.
    - Follows HTTP 302 redirects automatically (Apps Script echo redirect).
    - If network is unavailable or endpoint times out, lead remains safely
      persisted in PENDING_SYNC status for automatic batch sweeping.
=============================================================================
"""

import os
import sys
import json
import re
import sqlite3
import datetime
import time
import threading
import argparse
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# Ensure stdout and stderr handle UTF-8 cleanly on Windows
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

try:
    import requests
except ImportError:
    requests = None

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = BASE_DIR / "media_assets" / "crm_leads"
DEFAULT_DB_PATH = DEFAULT_DATA_DIR / "leads_fallback.db"
DEFAULT_JOURNAL_PATH = DEFAULT_DATA_DIR / "leads_journal.jsonl"
PROMO_CONFIG_PATH = BASE_DIR / "promo_config.json"

DEFAULT_ENDPOINT = (
    "https://script.google.com/macros/s/AKfycbwDYeWbB9SjUqX1RXH7DaZ8yqG6V5Ay7yAiJ9L27Du1pJ8zb-NVgXzw6oz_0wJVp8Fr/exec"
)

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [CRMSyncEngine] %(message)s"
)
logger = logging.getLogger("CRMSyncEngine")


class CRMSyncEngine:
    """
    Dual-layer offline fallback & queue sync engine for Healing Touch Egypt CRM.
    """

    def __init__(
        self,
        db_path: Optional[Path] = None,
        journal_path: Optional[Path] = None,
        endpoint_url: Optional[str] = None
    ):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.journal_path = Path(journal_path) if journal_path else DEFAULT_JOURNAL_PATH
        self.endpoint_url = endpoint_url or self._load_endpoint_url()

        # Ensure parent directories exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        self._journal_lock = threading.Lock()

        # Initialize SQLite storage
        self._init_sqlite()

    def _load_endpoint_url(self) -> str:
        """Loads tracking_endpoint from promo_config.json if available."""
        if PROMO_CONFIG_PATH.is_file():
            try:
                with open(PROMO_CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    endpoint = data.get("tracking_endpoint")
                    if endpoint and endpoint.startswith("https://script.google.com"):
                        return endpoint
            except Exception as e:
                logger.warning(f"Could not read promo_config.json: {e}")
        return DEFAULT_ENDPOINT

    @contextmanager
    def _connect(self, row_factory: bool = False):
        """Thread-safe and process-safe SQLite connection manager with guaranteed closure."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        if row_factory:
            conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_sqlite(self) -> None:
        """Initializes the SQLite schema and indexes."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA busy_timeout=30000;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consultation_leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL,
                    patient_name TEXT NOT NULL,
                    patient_phone TEXT NOT NULL,
                    normalized_phone TEXT NOT NULL,
                    context_topic TEXT NOT NULL,
                    promo_code TEXT DEFAULT 'HT10',
                    channel TEXT DEFAULT 'whatsapp',
                    source TEXT,
                    page_url TEXT,
                    notes TEXT,
                    sync_status TEXT DEFAULT 'PENDING_SYNC',
                    sync_attempts INTEGER DEFAULT 0,
                    synced_at TEXT,
                    last_error TEXT,
                    raw_payload TEXT
                );
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_leads_sync_status 
                ON consultation_leads(sync_status);
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_leads_created_at 
                ON consultation_leads(created_at);
            """)
            conn.commit()

    @classmethod
    def normalize_egyptian_phone(cls, phone: str) -> str:
        """
        Cleans and normalizes an Egyptian phone number to 201XXXXXXXXX format.
        Valid formats:
          - 01XXXXXXXXX (11 digits) -> 201XXXXXXXXX
          - 201XXXXXXXXX (12 digits) -> 201XXXXXXXXX
          - +201XXXXXXXXX -> 201XXXXXXXXX
          - 00201XXXXXXXXX -> 201XXXXXXXXX
        """
        if not phone:
            return ""

        # Transliterate Eastern Arabic-Indic numerals (٠-٩) to ASCII (0-9)
        arabic_digits = "٠١٢٣٤٥٦٧٨٩"
        phone_str = str(phone)
        for idx, d in enumerate(arabic_digits):
            phone_str = phone_str.replace(d, str(idx))

        clean = re.sub(r"[^0-9]", "", phone_str)

        if clean.startswith("00201") and len(clean) == 14:
            clean = clean[2:]
        if re.match(r"^01[0125][0-9]{8}$", clean):
            return "2" + clean
        elif re.match(r"^201[0125][0-9]{8}$", clean):
            return clean
        return clean

    @classmethod
    def is_valid_egyptian_phone(cls, phone: str) -> bool:
        """Validates Egyptian mobile phone pattern."""
        normalized = cls.normalize_egyptian_phone(phone)
        return bool(re.match(r"^201[0125][0-9]{8}$", normalized))

    def record_lead(self, payload: Dict[str, Any]) -> str:
        """
        Persists a lead into the dual-layer offline fallback (SQLite DB + JSONL journal).
        Returns the unique lead_id.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        created_at = payload.get("timestamp") or now.isoformat()
        
        # Patient fields
        patient_name = (payload.get("patient_name") or payload.get("name") or "مريضة هيلينج تاتش").strip()
        patient_phone = str(payload.get("patient_phone") or payload.get("phone") or "").strip()
        normalized_phone = payload.get("normalized_phone") or self.normalize_egyptian_phone(patient_phone)
        context_topic = (payload.get("context_topic") or payload.get("topic") or "استشارة عامة لتعافي الجروح").strip()
        promo_code = (payload.get("promo_code") or "HT10").strip()
        channel = (payload.get("channel") or "whatsapp").strip()
        source = (payload.get("source") or "consultation_lead_modal").strip()
        page_url = (payload.get("page_url") or "").strip()
        notes = (payload.get("notes") or "مسجل عبر CRM Sync Engine").strip()

        # Generate unique ID if not present
        lead_id = payload.get("lead_id")
        if not lead_id:
            rand_suffix = os.urandom(3).hex().upper()
            lead_id = f"HT-{now.strftime('%Y%m%d-%H%M%S')}-{rand_suffix}"

        lead_record = {
            "lead_id": lead_id,
            "created_at": created_at,
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "normalized_phone": normalized_phone,
            "context_topic": context_topic,
            "promo_code": promo_code,
            "channel": channel,
            "source": source,
            "page_url": page_url,
            "notes": notes,
            "sync_status": "PENDING_SYNC",
            "sync_attempts": 0,
            "raw_payload": json.dumps(payload, ensure_ascii=False)
        }

        # --- Layer 1: Atomic Append to JSONL Journal (Audit & Disaster Recovery) ---
        with self._journal_lock:
            with open(self.journal_path, "a", encoding="utf-8") as jf:
                jf.write(json.dumps(lead_record, ensure_ascii=False) + "\n")
                jf.flush()

        # --- Layer 2: SQLite Relational Database Insert with concurrency retry ---
        max_retries = 3
        backoffs = [0.05, 0.1, 0.2]
        for attempt in range(max_retries):
            try:
                with self._connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO consultation_leads (
                            lead_id, created_at, patient_name, patient_phone,
                            normalized_phone, context_topic, promo_code, channel,
                            source, page_url, notes, sync_status, sync_attempts, raw_payload
                        ) VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        );
                    """, (
                        lead_id, created_at, patient_name, patient_phone,
                        normalized_phone, context_topic, promo_code, channel,
                        source, page_url, notes, "PENDING_SYNC", 0, lead_record["raw_payload"]
                    ))
                    conn.commit()
                break
            except sqlite3.OperationalError as oe:
                if "locked" in str(oe).lower() and attempt < max_retries - 1:
                    time.sleep(backoffs[attempt])
                    continue
                raise

        logger.info(f"Lead recorded locally: {lead_id} ({patient_name}, {patient_phone}) -> PENDING_SYNC")
        return lead_id

    def dispatch_lead(self, lead_id: str, timeout: int = 15) -> bool:
        """
        Dispatches a specific lead to the Apps Script endpoint.
        Handles HTTP redirects (HTTP 302 Found) automatically.
        Updates status to SYNCED_TO_SHEET on success.
        """
        lead = self.get_lead(lead_id)
        if not lead:
            logger.error(f"Cannot dispatch non-existent lead_id: {lead_id}")
            return False

        if not requests:
            logger.error("Python 'requests' package not available for HTTP dispatch")
            return False

        post_body = {
            "timestamp": lead["created_at"],
            "lead_id": lead["lead_id"],
            "patient_name": lead["patient_name"],
            "patient_phone": lead["patient_phone"],
            "normalized_phone": lead["normalized_phone"],
            "context_topic": lead["context_topic"],
            "promo_code": lead["promo_code"],
            "source": lead["source"],
            "page_url": lead["page_url"],
            "notes": lead["notes"],
            "crm_status": "NEW"
        }

        attempts = lead.get("sync_attempts", 0) + 1
        synced_at = None
        last_error = None
        is_success = False

        try:
            # Apps Script Web App responds with 302 redirect to echo URL
            response = requests.post(
                self.endpoint_url,
                json=post_body,
                headers={"Content-Type": "application/json"},
                allow_redirects=True,
                timeout=timeout
            )

            if response.status_code == 200:
                try:
                    resp_data = response.json()
                    if resp_data.get("status") == "success":
                        is_success = True
                    else:
                        last_error = f"Apps Script returned non-success: {response.text[:200]}"
                except Exception:
                    # Some Apps Script setups return HTML on success
                    if "success" in response.text.lower() or "lead recorded" in response.text.lower():
                        is_success = True
                    else:
                        last_error = f"Unexpected response text: {response.text[:200]}"
            else:
                last_error = f"HTTP {response.status_code}: {response.text[:200]}"

        except Exception as e:
            last_error = f"Dispatch network exception: {str(e)}"
            logger.warning(f"Lead dispatch failed for {lead_id}: {last_error}")

        # Update SQLite record
        with self._connect() as conn:
            cursor = conn.cursor()
            if is_success:
                synced_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
                cursor.execute("""
                    UPDATE consultation_leads
                    SET sync_status = 'SYNCED_TO_SHEET',
                        sync_attempts = ?,
                        synced_at = ?,
                        last_error = NULL
                    WHERE lead_id = ?;
                """, (attempts, synced_at, lead_id))
                logger.info(f"Lead {lead_id} successfully synced to Google Sheet via Apps Script!")
            else:
                cursor.execute("""
                    UPDATE consultation_leads
                    SET sync_attempts = ?,
                        last_error = ?
                    WHERE lead_id = ?;
                """, (attempts, last_error, lead_id))
            conn.commit()

        return is_success

    def sync_pending_queue(self, max_items: int = 50, timeout: int = 15) -> Dict[str, Any]:
        """
        Sweeps through all leads with PENDING_SYNC status and attempts sync.
        Returns a summary report dictionary.
        """
        pending = self.get_pending_leads(limit=max_items)
        synced_count = 0
        failed_count = 0
        results = []

        logger.info(f"Starting queue sweep: {len(pending)} pending leads to process.")

        for lead in pending:
            lead_id = lead["lead_id"]
            success = self.dispatch_lead(lead_id, timeout=timeout)
            if success:
                synced_count += 1
                results.append({"lead_id": lead_id, "status": "SYNCED_TO_SHEET"})
            else:
                failed_count += 1
                results.append({"lead_id": lead_id, "status": "PENDING_SYNC"})

        remaining = len(self.get_pending_leads(limit=1000))
        report = {
            "processed": len(pending),
            "synced": synced_count,
            "failed": failed_count,
            "remaining_pending": remaining,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "details": results
        }
        logger.info(f"Queue sweep completed: {synced_count} synced, {failed_count} failed, {remaining} remaining.")
        return report

    def get_lead(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single lead dictionary by lead_id."""
        with self._connect(row_factory=True) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM consultation_leads WHERE lead_id = ?;", (lead_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_pending_leads(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves leads that are waiting for sync."""
        with self._connect(row_factory=True) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM consultation_leads 
                WHERE sync_status = 'PENDING_SYNC'
                ORDER BY id ASC 
                LIMIT ?;
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        """Returns comprehensive storage and sync statistics."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM consultation_leads;")
            total_db = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM consultation_leads WHERE sync_status = 'PENDING_SYNC';")
            pending_db = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM consultation_leads WHERE sync_status = 'SYNCED_TO_SHEET';")
            synced_db = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM consultation_leads WHERE sync_status = 'FAILED_FATAL';")
            failed_db = cursor.fetchone()[0]

        # Count journal lines
        journal_lines = 0
        if self.journal_path.is_file():
            with open(self.journal_path, "r", encoding="utf-8") as jf:
                journal_lines = sum(1 for _ in jf)

        return {
            "total_leads_in_sqlite": total_db,
            "pending_sync": pending_db,
            "synced_to_sheet": synced_db,
            "failed_fatal": failed_db,
            "journal_entries_in_jsonl": journal_lines,
            "db_path": str(self.db_path),
            "journal_path": str(self.journal_path),
            "endpoint_url": self.endpoint_url
        }

    def recover_from_journal(self) -> int:
        """
        Disaster Recovery: Reconstructs SQLite database from the append-only JSONL journal.
        Returns the number of leads restored.
        """
        if not self.journal_path.is_file():
            logger.warning(f"No journal file found at {self.journal_path}")
            return 0

        restored_count = 0
        with open(self.journal_path, "r", encoding="utf-8") as jf:
            for line in jf:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    lead_id = entry.get("lead_id")
                    if not lead_id:
                        continue

                    # Check if already in SQLite
                    existing = self.get_lead(lead_id)
                    if not existing:
                        with self._connect() as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO consultation_leads (
                                    lead_id, created_at, patient_name, patient_phone,
                                    normalized_phone, context_topic, promo_code, channel,
                                    source, page_url, notes, sync_status, sync_attempts, raw_payload
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                            """, (
                                lead_id,
                                entry.get("created_at") or datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                entry.get("patient_name") or "مريضة هيلينج تاتش",
                                entry.get("patient_phone") or "",
                                entry.get("normalized_phone") or "",
                                entry.get("context_topic") or "استشارة عامة",
                                entry.get("promo_code") or "HT10",
                                entry.get("channel") or "whatsapp",
                                entry.get("source") or "journal_recovery",
                                entry.get("page_url") or "",
                                entry.get("notes") or "مسترجع من سجل الطوارئ JSONL",
                                entry.get("sync_status") or "PENDING_SYNC",
                                entry.get("sync_attempts", 0),
                                entry.get("raw_payload") or "{}"
                            ))
                            conn.commit()
                        restored_count += 1
                except Exception as e:
                    logger.error(f"Error parsing journal line: {e}")

        logger.info(f"Disaster Recovery: Successfully restored {restored_count} leads into SQLite from JSONL journal.")
        return restored_count


def record_and_sync(payload: Dict[str, Any], engine: Optional[CRMSyncEngine] = None) -> Tuple[str, bool]:
    """
    High-level convenience function:
    1. Records lead locally (Layer 1 SQLite + Layer 2 JSONL).
    2. Immediately attempts live dispatch to Google Apps Script.
    3. Returns (lead_id, was_synced_immediately).
    """
    eng = engine or CRMSyncEngine()
    lead_id = eng.record_lead(payload)
    synced = eng.dispatch_lead(lead_id)
    return lead_id, synced


def parse_args():
    parser = argparse.ArgumentParser(
        description="Healing Touch Egypt — Dual-Layer Offline CRM Sync Engine (Zero-GCP)"
    )
    parser.add_argument("--record", action="store_true", help="Record a new consultation lead")
    parser.add_argument("--name", type=str, default="مريضة تجريبية", help="Patient name")
    parser.add_argument("--phone", type=str, default="01155803307", help="Patient phone number")
    parser.add_argument("--topic", type=str, default="بروتوكول تعافي جراحة التجميل والندبات", help="Surgical case / topic")
    parser.add_argument("--promo", type=str, default="HT10", help="Promo code")
    parser.add_argument("--source", type=str, default="cli_admin", help="Source channel")
    parser.add_argument("--notes", type=str, default="مسجل عبر سطر الأوامر", help="Additional notes")

    parser.add_argument("--sync-queue", action="store_true", help="Sweep and sync pending leads in queue")
    parser.add_argument("--stats", action="store_true", help="Display local CRM storage statistics")
    parser.add_argument("--recover-journal", action="store_true", help="Recover SQLite DB from JSONL journal")
    parser.add_argument("--test-connection", action="store_true", help="Test GET connection to Apps Script Web App")

    return parser.parse_args()


def main():
    args = parse_args()
    engine = CRMSyncEngine()

    if args.stats or (len(sys.argv) == 1):
        stats = engine.get_stats()
        print("=" * 65)
        print("[Healing Touch Egypt] Local CRM Engine Status (Zero-GCP)")
        print("=" * 65)
        print(f"  • SQLite Database:      {stats['db_path']}")
        print(f"  • JSONL Audit Journal:  {stats['journal_path']}")
        print(f"  • Total Leads in DB:    {stats['total_leads_in_sqlite']}")
        print(f"  • Pending Sync:         {stats['pending_sync']}")
        print(f"  • Synced to Sheet:      {stats['synced_to_sheet']}")
        print(f"  • Journal Entries:      {stats['journal_entries_in_jsonl']}")
        print(f"  • Apps Script Endpoint: {stats['endpoint_url']}")
        print("=" * 65)
        if len(sys.argv) == 1:
            return

    if args.test_connection:
        print(f"[*] Testing GET connection to: {engine.endpoint_url}")
        try:
            r = requests.get(engine.endpoint_url, timeout=10)
            print(f"  [+] Status Code: {r.status_code}")
            print(f"  [+] Response: {r.text[:300]}")
        except Exception as e:
            print(f"  [-] Connection error: {e}")

    if args.record:
        payload = {
            "patient_name": args.name,
            "patient_phone": args.phone,
            "context_topic": args.topic,
            "promo_code": args.promo,
            "source": args.source,
            "notes": args.notes
        }
        lead_id, synced = record_and_sync(payload, engine)
        print(f"  [+] Lead created: {lead_id}")
        print(f"  [+] Live Sync Status: {'SYNCED_TO_SHEET (Live)' if synced else 'QUEUED_OFFLINE (Pending Sync)'}")

    if args.sync_queue:
        print("[*] Sweeping pending CRM queue...")
        result = engine.sync_pending_queue()
        print(f"  [+] Processed: {result['processed']}")
        print(f"  [+] Successfully Synced: {result['synced']}")
        print(f"  [+] Failed / Re-queued: {result['failed']}")
        print(f"  [+] Remaining in Queue: {result['remaining_pending']}")

    if args.recover_journal:
        print("[*] Initiating Disaster Recovery from JSONL journal...")
        restored = engine.recover_from_journal()
        print(f"  [+] Restored {restored} leads from journal into SQLite.")


if __name__ == "__main__":
    main()
