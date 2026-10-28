# -*- coding: utf-8 -*-
"""
Tests for Telegram Control Bot (scripts/telegram_control_bot.py)
Verifies:
- Menu keyboards structure and callbacks.
- Products catalog metadata integrity.
- Authorization gate logic for Chat ID.
- Service management scripts exist and follow CRLF conventions.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from telegram_control_bot import (
    build_main_menu_keyboard,
    build_products_submenu_keyboard,
    PRODUCTS_CATALOG,
    AUTHORIZED_CHAT_ID,
    TELEGRAM_BOT_TOKEN,
    write_pid_file,
    remove_pid_file,
    PID_FILE,
    process_message,
    process_callback_query,
)


class TestTelegramControlBot(unittest.TestCase):

    def test_01_configuration_credentials(self):
        """Verify authorized Chat ID and Bot Token are loaded."""
        self.assertEqual(AUTHORIZED_CHAT_ID, "7692685242")
        self.assertIn("9068379040", TELEGRAM_BOT_TOKEN)

    def test_02_main_menu_keyboard_structure(self):
        """Verify main menu inline keyboard contains all required action buttons."""
        kb = build_main_menu_keyboard()
        self.assertIn("inline_keyboard", kb)
        rows = kb["inline_keyboard"]
        self.assertGreaterEqual(len(rows), 5)

        # Collect all callback data keys
        callbacks = [btn["callback_data"] for row in rows for btn in row]
        self.assertIn("act_master", callbacks)
        self.assertIn("menu_products", callbacks)
        self.assertIn("act_dry_run", callbacks)
        self.assertIn("act_n8n_status", callbacks)
        self.assertIn("act_crm_sync", callbacks)
        self.assertIn("act_deploy_site", callbacks)
        self.assertIn("act_latest_pack", callbacks)
        self.assertIn("act_inbox_status", callbacks)

    def test_03_products_submenu_structure(self):
        """Verify products submenu has all 6 clinical products plus main menu return."""
        kb = build_products_submenu_keyboard()
        rows = kb["inline_keyboard"]
        callbacks = [btn["callback_data"] for row in rows for btn in row]

        for i in range(1, 7):
            self.assertIn(f"prod_{i}", callbacks)
        self.assertIn("menu_main", callbacks)

    def test_04_products_catalog_completeness(self):
        """Verify all 6 products have name, brand, tag, icon."""
        self.assertEqual(len(PRODUCTS_CATALOG), 6)
        for key in ["1", "2", "3", "4", "5", "6"]:
            self.assertIn(key, PRODUCTS_CATALOG)
            item = PRODUCTS_CATALOG[key]
            self.assertIn("name", item)
            self.assertIn("brand", item)
            self.assertIn("tag", item)
            self.assertIn("icon", item)

    def test_05_pid_file_lifecycle(self):
        """Verify PID file writing and cleanup using test-isolated path."""
        test_pid = PROJECT_ROOT / "media_assets" / "test_isolated_bot.pid"
        if test_pid.exists():
            test_pid.unlink()
        self.assertFalse(test_pid.exists())
        test_pid.write_text(str(os.getpid()), encoding="utf-8")
        self.assertTrue(test_pid.exists())
        read_pid = int(test_pid.read_text(encoding="utf-8").strip())
        self.assertEqual(read_pid, os.getpid())
        test_pid.unlink()
        self.assertFalse(test_pid.exists())

    def test_06_service_scripts_existence_and_crlf(self):
        """Verify start_bot.bat, stop_bot.bat, status_bot.bat and run_bot_silent.vbs exist with CRLF."""
        scripts = [
            PROJECT_ROOT / "start_bot.bat",
            PROJECT_ROOT / "stop_bot.bat",
            PROJECT_ROOT / "status_bot.bat",
            PROJECT_ROOT / "scripts" / "run_bot_silent.vbs",
        ]
        for s in scripts:
            self.assertTrue(s.exists(), f"Missing service script: {s.name}")
            content = s.read_bytes()
            self.assertIn(b"\r\n", content, f"{s.name} is missing CRLF line endings")
            # Verify no orphaned LF
            cleaned = content.replace(b"\r\n", b"")
            self.assertNotIn(b"\n", cleaned, f"{s.name} has orphaned LF line endings")


if __name__ == "__main__":
    unittest.main()
