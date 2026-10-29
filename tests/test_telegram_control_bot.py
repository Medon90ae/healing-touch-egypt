# -*- coding: utf-8 -*-
"""
Tests for Telegram Control Bot (scripts/telegram_control_bot.py)
Verifies:
- Menu keyboards structure and callbacks.
- Products catalog metadata integrity.
- Authorization gate logic for Chat ID.
- Service management scripts exist and follow CRLF conventions.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import telegram_control_bot
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

    def test_13_reviews_menu_button_exists_in_main_menu(self):
        """R5: Verify menu_reviews button exists in build_main_menu_keyboard()."""
        kb = build_main_menu_keyboard()
        self.assertIn("inline_keyboard", kb)
        rows = kb["inline_keyboard"]
        callbacks = [btn["callback_data"] for row in rows for btn in row if "callback_data" in btn]
        self.assertIn(
            "menu_reviews", callbacks,
            "Main menu inline keyboard must include callback 'menu_reviews' for [🌟 إدارة وأرشفة تجارب المرضى والعملاء]."
        )
        review_btn = next((btn for row in rows for btn in row if btn.get("callback_data") == "menu_reviews"), None)
        self.assertIsNotNone(review_btn)
        self.assertTrue(
            any(k in review_btn["text"] for k in ["تجارب", "المرضى", "العملاء"]),
            f"Review button text '{review_btn['text']}' must mention patient reviews."
        )

    def test_14_reviews_intake_callbacks_and_submenu_keyboard(self):
        """R5: Verify review intake callbacks (rev_prod_1 .. rev_prod_5, rev_privacy_templates)."""
        import telegram_control_bot as bot
        build_hub = getattr(bot, "build_reviews_hub_keyboard", None)
        self.assertIsNotNone(
            build_hub,
            "telegram_control_bot must define 'build_reviews_hub_keyboard()' for R5 review intake hub."
        )
        kb = build_hub()
        self.assertIn("inline_keyboard", kb)
        rows = kb["inline_keyboard"]
        callbacks = [btn["callback_data"] for row in rows for btn in row if "callback_data" in btn]

        for i in range(1, 6):
            self.assertIn(
                f"rev_prod_{i}", callbacks,
                f"Reviews submenu must contain callback 'rev_prod_{i}' for product {i}."
            )
        self.assertIn(
            "rev_privacy_templates", callbacks,
            "Reviews submenu must contain callback 'rev_privacy_templates'."
        )

    def test_15_reviews_session_state_transitions(self):
        """R5: Verify session state transitions into STATE_STAGE_REVIEW_INTAKE."""
        import telegram_control_bot as bot
        state_intake = getattr(bot, "STATE_STAGE_REVIEW_INTAKE", None)
        self.assertIsNotNone(
            state_intake,
            "telegram_control_bot must define 'STATE_STAGE_REVIEW_INTAKE' state constant."
        )
        test_chat = "777666555"
        reset_session(test_chat)
        sess = get_session(test_chat)
        self.assertEqual(sess["stage"], STATE_IDLE)

        # Transition into STATE_STAGE_REVIEW_INTAKE
        updated = update_session(test_chat, stage=state_intake, review_product_id="2")
        self.assertEqual(updated["stage"], state_intake)
        self.assertEqual(updated.get("review_product_id"), "2")

        # Verify persistence and retrieval
        current = get_session(test_chat)
        self.assertEqual(current["stage"], state_intake)

        # Reset back to IDLE
        reset_session(test_chat)
        resetted = get_session(test_chat)
        self.assertEqual(resetted["stage"], STATE_IDLE)

    def test_16_reviews_directory_intake_schema(self):
        """R5: Verify reviews directory intake schema (media_assets/client_reviews/{product_id}/ and reviews_metadata.json)."""
        import telegram_control_bot as bot
        intake_fn = getattr(bot, "intake_client_review_asset", None)
        self.assertIsNotNone(
            intake_fn,
            "telegram_control_bot must define 'intake_client_review_asset' for storing patient reviews."
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            with patch.object(bot, "CLIENT_REVIEWS_DIR", tmp_path / "client_reviews", create=True):
                meta = intake_fn(
                    product_id="bupy-silicone-scar-sheet",
                    rating=5,
                    patient_pseudonym="أم قيصرية - القاهرة",
                    surgery_type="ولادة قيصرية (اليوم 21)",
                    review_text="شيت السيليكون ممتاز جداً في تسطيح الندبة بعد أسبوعين من الالتزام.",
                    photo_bytes=b"fake-jpeg-photo",
                    audio_bytes=b"fake-mp3-voice",
                    photo_filename="csection_scar_day21.jpg",
                    audio_filename="voice_feedback.mp3"
                )
                self.assertIsNotNone(meta)
                self.assertEqual(meta["product_id"], "bupy-silicone-scar-sheet")
                self.assertEqual(meta["rating"], 5)
                self.assertEqual(meta["patient_pseudonym"], "أم قيصرية - القاهرة")
                self.assertEqual(meta["privacy_status"], "anonymized_approved")

                # Verify directory structure
                prod_dir = tmp_path / "client_reviews" / "bupy-silicone-scar-sheet"
                self.assertTrue(prod_dir.exists())
                self.assertTrue((prod_dir / "photos").exists())
                self.assertTrue((prod_dir / "audio").exists())

                # Verify metadata file
                meta_file = prod_dir / "reviews_metadata.json"
                self.assertTrue(meta_file.exists())
                records = json.loads(meta_file.read_text(encoding="utf-8"))
                self.assertIsInstance(records, list)
                self.assertEqual(len(records), 1)
                self.assertEqual(records[0]["review_id"], meta["review_id"])

    def test_17_medical_privacy_compliant_review_templates(self):
        """R5: Verify medical privacy compliant review templates (anonymized patient details, zero prohibited titles, approved HT10 link)."""
        import telegram_control_bot as bot
        tpl_fn = getattr(bot, "build_medical_privacy_review_templates", None)
        self.assertIsNotNone(
            tpl_fn,
            "telegram_control_bot must define 'build_medical_privacy_review_templates' for generating compliant posts."
        )
        sample_meta = {
            "review_id": "rev_test_001",
            "product_id": "bupy-silicone-scar-sheet",
            "product_name": "BUPY Silicone Scar Sheets",
            "timestamp": "2026-10-29T17:30:00",
            "rating": 5,
            "patient_pseudonym": "أم قيصرية - القاهرة",
            "surgery_type": "ولادة قيصرية (اليوم 21)",
            "review_text": "شيت السيليكون فرق جدا في تسطيح الندبة بعد أسبوعين من الاستخدام المنتظم.",
            "specialist_advice": "ينصح بالاستمرار على شيت السيليكون لمدة 12 ساعة يومياً لحماية الأنسجة."
        }
        templates = tpl_fn(sample_meta)
        self.assertIn("instagram_carousel", templates)
        self.assertIn("tiktok_reels_script", templates)
        self.assertIn("blogger_snippet", templates)

        # 1. Anonymized patient details: Patient pseudonym present, no leaked full name
        for k, text in templates.items():
            self.assertIn(sample_meta["patient_pseudonym"], text, f"Template {k} must include anonymized patient pseudonym.")
            # 2. Healthcare compliance: ZERO prohibited doctor titles
            self.assertNotIn("طبيبة", text, f"Template {k} must not use prohibited title 'طبيبة'.")
            self.assertNotIn("الدكتورة", text, f"Template {k} must not use prohibited title 'الدكتورة'.")
            self.assertIn("أخصائية العناية بالتعافي", text, f"Template {k} must use approved title 'أخصائية العناية بالتعافي'.")
            # 3. Approved WhatsApp consultation link with HT10
            self.assertIn("https://wa.me/201155803307", text, f"Template {k} must include official WhatsApp link.")
            self.assertIn("HT10", text, f"Template {k} must include promo code HT10.")


if __name__ == "__main__":
    unittest.main()
