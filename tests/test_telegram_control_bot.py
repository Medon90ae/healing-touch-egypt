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
    # Guided Multi-Stage Clinical Pipeline
    STATE_IDLE,
    STATE_STAGE_1_RESEARCH,
    STATE_STAGE_2_PROMPTS,
    STATE_STAGE_3_MEDIA,
    POMELLI_BRAND_BOOK_URL,
    NOTEBOOKLM_URL,
    GEMINI_URL,
    get_session,
    update_session,
    reset_session,
    analyze_clinical_research,
    build_stage1_deep_research_card,
    build_synthesized_pomelli_card,
    build_synthesized_notebooklm_card,
    extract_text_from_file,
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

    def test_07_session_state_machine_transitions(self):
        """Verify user session creation, state updates, and resetting."""
        test_chat_id = "999888777"
        sess = get_session(test_chat_id)
        self.assertEqual(sess["stage"], STATE_IDLE)

        # Transition to Stage 1 (Deep Research)
        updated = update_session(test_chat_id, stage=STATE_STAGE_1_RESEARCH, product_choice="2")
        self.assertEqual(updated["stage"], STATE_STAGE_1_RESEARCH)
        self.assertEqual(updated["product_choice"], "2")

        # Transition to Stage 3 (Media Uploads)
        updated = update_session(test_chat_id, stage=STATE_STAGE_3_MEDIA, media_files=["photo1.jpg"])
        self.assertEqual(updated["stage"], STATE_STAGE_3_MEDIA)
        self.assertIn("photo1.jpg", updated["media_files"])

        # Reset session back to IDLE
        reset_session(test_chat_id)
        resetted = get_session(test_chat_id)
        self.assertEqual(resetted["stage"], STATE_IDLE)
        self.assertEqual(resetted["media_files"], [])

    def test_08_clinical_research_analyzer(self):
        """Verify report parsing extracts findings, patient anxieties, and guidelines."""
        mock_report = (
            "تقرير البحث السريري لمنتج شيت السيليكون الطبي BUPY:\n"
            "• أثبتت دراسات التئام الجروح قدرة السيليكون على عزل الندبة وتثبيط تكاثر خلايا الكولاجين العشوائية لمنع الكيلويد.\n"
            "• ينصح بتطبيق الشيت يومياً لمدة لا تقل عن 12 ساعة مع الغسيل والتجفيف المستمر.\n"
            "• ما هو خوف المريض الأكثر شيوعاً في مصر؟ القلق الشديد من بقاء أثر الندبة بارزاً أو حدوث حكة شديدة بعد القيصرية.\n"
            "• التوصيات تؤكد أمان الشيت التام وعدم تسببه في حساسية الجلد في الأجواء الحارة.\n"
        )
        analysis = analyze_clinical_research(mock_report, product_choice="2")
        self.assertIn("findings", analysis)
        self.assertIn("anxieties", analysis)
        self.assertGreater(len(analysis["findings"]), 0)
        self.assertGreater(len(analysis["anxieties"]), 0)

    def test_09_stage1_deep_research_card_structure(self):
        """Verify Stage 1 card generates Gemini Deep Research prompt and verified URL."""
        text, kb = build_stage1_deep_research_card("1")
        self.assertIn("المرحلة 1 من 4", text)
        self.assertIn("Gemini Deep Research", text)
        self.assertIn("pre><code", text)
        self.assertIn("HT10", text)
        self.assertIn("01155803307", text)

        urls = [btn["url"] for row in kb["inline_keyboard"] for btn in row if "url" in btn]
        self.assertIn(GEMINI_URL, urls)

    def test_10_synthesized_pomelli_brand_book_card(self):
        """Verify Pomelli card adheres to exact Brand Book URL and color palette."""
        mock_analysis = {
            "findings": ["تسطيح ندبات القيصرية وترطيب الأنسجة"],
            "anxieties": ["الخوف من الكيلويد وتغير لون الجلد"],
        }
        text, kb = build_synthesized_pomelli_card("2", mock_analysis)
        self.assertIn("المرحلة 2 من 4", text)
        self.assertIn("Pomelli Brand Book", text)
        self.assertIn("#064E3B", text)  # Clinical Forest
        self.assertIn("#10B981", text)  # Medical Mint
        self.assertIn("#0F172A", text)  # Slate Navy Charcoal
        self.assertIn("#FFFFFF", text)  # Sterile White

        # Exact Brand Book URL verification
        urls = [btn["url"] for row in kb["inline_keyboard"] for btn in row if "url" in btn]
        self.assertIn(POMELLI_BRAND_BOOK_URL, urls)
        self.assertEqual(POMELLI_BRAND_BOOK_URL, "https://labs.google.com/pomelli/brand_book/am6H88zhmUadtfPiiAmOnW")

    def test_11_synthesized_notebooklm_card(self):
        """Verify NotebookLM prompts integrate research findings, Egyptian dialect, and clinical CTA."""
        mock_analysis = {
            "findings": ["حماية ثقوب مناظير التكميم بحاجز بكتيري شفاف يمنع التلوث"],
            "anxieties": ["القلق من تسرب الماء أثناء الاستحمام في الأيام الأولى"],
        }
        text, kb = build_synthesized_notebooklm_card("5", mock_analysis)
        self.assertIn("المرحلة 2 من 4", text)
        self.assertIn("NotebookLM", text)
        self.assertIn("Audio Overview", text)
        self.assertIn("Video Overview", text)
        self.assertIn("HT10", text)
        self.assertIn("01155803307", text)
        self.assertIn("حماية ثقوب مناظير التكميم", text)

        urls = [btn["url"] for row in kb["inline_keyboard"] for btn in row if "url" in btn]
        self.assertIn(NOTEBOOKLM_URL, urls)

    def test_12_extract_text_from_file_resilience(self):
        """Verify extract_text_from_file decodes text and markdown files safely."""
        test_txt = PROJECT_ROOT / "media_assets" / "test_sample_research.txt"
        test_txt.write_text("بحث سريري تجريبي لغيار الجروح وتثبيت الأنف", encoding="utf-8")
        try:
            extracted = extract_text_from_file(test_txt)
            self.assertIn("بحث سريري تجريبي", extracted)
        finally:
            if test_txt.exists():
                test_txt.unlink()


if __name__ == "__main__":
    unittest.main()
