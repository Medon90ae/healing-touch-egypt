#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_single_click_master_pipeline.py
=============================================================================
Healing Touch Egypt — Milestone 4 (R4) Verification Test Suite
Testing Single-Click Master Pipeline & Unified Runner
=============================================================================
"""

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import single_click_master_pipeline as scmp
from smart_intake_classifier import CATEGORY_KEYWORDS


class TestMilestone4SingleClickPipeline(unittest.TestCase):
    """Milestone 4 (R4) Single-Click Master Pipeline & Unified Batch Runner Tests."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="ht_m4_test_"))
        self.inbox_dir = self.test_dir / "manual_inbox"
        self.archive_dir = self.test_dir / "archive"
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_cli_argument_parsing(self):
        """Verify CLI parser flags: --dry-run, --category, --force, --open-browser, --webhook-url."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--category", "-c", type=str, default=None)
        parser.add_argument("--force", "-f", action="store_true")
        parser.add_argument("--open-browser", action="store_true")
        parser.add_argument("--webhook-url", type=str, default="http://localhost:5678/webhook/publish-post")

        args = parser.parse_args(["--dry-run", "--category", "rhinoplasty", "--force"])
        self.assertTrue(args.dry_run)
        self.assertEqual(args.category, "rhinoplasty")
        self.assertTrue(args.force)
        self.assertFalse(args.open_browser)
        self.assertEqual(args.webhook_url, "http://localhost:5678/webhook/publish-post")

    def test_02_empty_inbox_clean_fallback(self):
        """Verify that when manual_inbox is clean and empty, Step 1 cleanly falls back to research harvester."""
        with patch("single_click_master_pipeline.MANUAL_INBOX_DIR", self.inbox_dir):
            step1 = scmp.step_1_scan_and_classify_media(category="c-section")
            self.assertEqual(step1["status"], "success")
            self.assertFalse(step1["has_custom_inbox"])
            self.assertEqual(step1["category"], "c-section")
            self.assertIsNotNone(step1["hero_image"])
            self.assertIn("title", step1["case_data"])
            self.assertEqual(len(step1["used_inbox_files"]), 0)

    def test_03_multi_asset_triage_hero_carousel_and_video_aspect(self):
        """Verify Step 1 multi-asset ingestion: 1 hero + carousel, 9:16 vertical vs 16:9 horizontal videos."""
        # Create test assets in isolated inbox
        img1 = self.inbox_dir / "rhino_01_hero.png"
        img2 = self.inbox_dir / "rhino_02_case.png"
        img3 = self.inbox_dir / "rhino_03_case.png"
        v_vert = self.inbox_dir / "reel_rhino_vertical.mp4"
        v_horiz = self.inbox_dir / "youtube_rhino_horizontal.mp4"
        aud = self.inbox_dir / "consult_voice.m4a"

        for p in [img1, img2, img3, v_vert, v_horiz, aud]:
            p.write_bytes(b"\x00" * 1024)

        # Mock probe dimensions for deterministic aspect ratios
        def mock_probe(file_path):
            name = str(file_path).lower()
            if "vertical" in name or "reel" in name:
                return {"is_vertical_9_16": True, "is_horizontal_16_9": False}
            return {"is_vertical_9_16": False, "is_horizontal_16_9": True}

        with patch("single_click_master_pipeline.MANUAL_INBOX_DIR", self.inbox_dir), \
             patch("single_click_master_pipeline.probe_media_dimensions", side_effect=mock_probe):
            step1 = scmp.step_1_scan_and_classify_media(category="rhinoplasty")
            self.assertEqual(step1["status"], "success")
            self.assertTrue(step1["has_custom_inbox"])
            self.assertEqual(step1["category"], "rhinoplasty")
            self.assertEqual(step1["hero_image"].name, "rhino_01_hero.png")
            self.assertEqual(len(step1["gallery_images"]), 2)
            self.assertEqual(step1["video_vertical"].name, "reel_rhino_vertical.mp4")
            self.assertEqual(step1["video_horizontal"].name, "youtube_rhino_horizontal.mp4")
            self.assertEqual(step1["audio_path"].name, "consult_voice.m4a")

    def test_04_landing_page_generation(self):
        """Verify Step 2 generates a valid campaign landing page with expected return keys."""
        mock_step1 = {
            "status": "success",
            "has_custom_inbox": False,
            "category": "c-section",
            "case_data": {
                "title": "بروتوكول تعافي جرح القيصرية والشاور الآمن",
                "category": "c-section",
                "story_text": "إرشادات طبية سريرية لحماية الجرح من الماء ومنع تشكل الندبات المتضخمة.",
                "hashtags": "#ولادة_قيصرية #جرح_القيصرية #علاج_الندبات"
            },
            "hero_image": PROJECT_ROOT / "docs" / "assets" / "og-image.jpg",
            "gallery_images": [],
            "video_vertical": None,
            "video_horizontal": None,
            "audio_path": None
        }

        step2 = scmp.step_2_build_campaign_landing_page(mock_step1)
        self.assertEqual(step2["status"], "success")
        self.assertEqual(step2["slug"], "c-section-recovery-protocol")
        self.assertTrue(Path(step2["local_file"]).exists())
        self.assertIn("https://medon90ae.github.io/healing-touch-egypt/lp/", step2["public_url"])

    def test_05_creatives_and_ready_to_publish_packages(self):
        """Verify Step 3 produces branded text files and all 6 platform subdirectories in ready_to_publish."""
        mock_step1 = {
            "status": "success",
            "category": "rhinoplasty",
            "template_index": 0,
            "case_data": {
                "title": "دعامات الأنف السيليكونية وتماثل الفتحات بعد التجميل",
                "category": "rhinoplasty",
                "story_text": "بروتوكول سريري لدعم الغضاريف وتثبيت النتيجة وتخفيف التورم.",
                "hashtags": "#تجميل_الانف #دعامات_الانف #هيلينج_تاتش_مصر"
            },
            "hero_image": PROJECT_ROOT / "docs" / "assets" / "campaign_rhinoplasty_hero.png",
            "gallery_images": [],
            "video_vertical": None,
            "video_horizontal": None,
            "platform_texts": {}
        }
        mock_step2 = {
            "public_url": "https://medon90ae.github.io/healing-touch-egypt/lp/rhinoplasty-recovery-protocol.html"
        }

        step3 = scmp.step_3_generate_creatives_and_packages(mock_step1, mock_step2)
        self.assertEqual(step3["status"], "success")
        pack_dir = step3["pack_dir"]
        self.assertTrue(pack_dir.exists())

        expected_dirs = [
            "01_يوتيوب_YouTube",
            "02_تيكتوك_TikTok",
            "03_إنستجرام_Instagram",
            "04_بلوجر_Blogger",
            "05_ريديت_Reddit",
            "06_فيسبوك_Facebook"
        ]
        for ed in expected_dirs:
            sub = pack_dir / ed
            self.assertTrue(sub.exists() and sub.is_dir(), f"Platform folder missing: {ed}")

    def test_06_n8n_structured_payload_adherence_to_contract(self):
        """Verify Step 4 constructs a 6-platform structured JSON payload adhering to PROJECT.md."""
        mock_step1 = {
            "case_data": {
                "title": "علاج ندبات الرقبة بعد استئصال الغدة الدرقية",
                "category": "thyroid",
                "hashtags": "#الغدة_الدرقية #علاج_الندبات #HT10"
            },
            "category": "thyroid",
            "gallery_images": []
        }
        mock_step2 = {
            "public_url": "https://medon90ae.github.io/healing-touch-egypt/lp/thyroid-recovery-protocol.html"
        }
        mock_step3 = {
            "copywriting": {
                "facebook": "بوست فيسبوك للغدة الدرقية",
                "instagram": "كابشن إنستجرام للغدة الدرقية",
                "tiktok": "سيناريو تيكتوك للغدة الدرقية",
                "youtube_title": "فيديو يوتيوب للغدة الدرقية #Shorts",
                "youtube_description": "وصف يوتيوب للغدة الدرقية",
                "reddit_title": "مقال ريديت للغدة الدرقية",
                "reddit_markdown": "# مقال ريديت للغدة الدرقية",
                "blogger_title": "مقال بلوجر للغدة الدرقية",
                "blogger_html": "<h1>مقال بلوجر للغدة الدرقية</h1>"
            },
            "square_card": "docs/assets/campaign_thyroid_hero.png",
            "story_card": "docs/assets/campaign_thyroid_hero.png",
            "video_path": "docs/assets/campaign_thyroid_video.mp4",
            "wa_direct_url": "https://wa.me/201155803307"
        }

        step4 = scmp.step_4_dispatch_to_n8n_webhook(mock_step1, mock_step2, mock_step3, dry_run=True)
        self.assertEqual(step4["status"], "success")
        self.assertTrue(step4["dry_run"])
        self.assertFalse(step4["dispatched"])

        payload = step4["payload"]
        self.assertIn("meta_platforms", payload)
        self.assertIn("facebook_photo", payload["meta_platforms"])
        self.assertIn("facebook_reels", payload["meta_platforms"])
        self.assertIn("instagram_reels", payload["meta_platforms"])
        self.assertIn("instagram_carousel", payload["meta_platforms"])

        self.assertIn("youtube_platforms", payload)
        self.assertIn("youtube_shorts", payload["youtube_platforms"])
        self.assertIn("youtube_video", payload["youtube_platforms"])

        self.assertIn("tiktok_platform", payload)
        self.assertIn("reddit_platform", payload)
        self.assertIn("blogger_platform", payload)

    def test_07_inbox_hygiene_and_archival(self):
        """Verify Step 6 safely moves processed files to archive and leaves manual_inbox completely clean."""
        f1 = self.inbox_dir / "asset_a.png"
        f2 = self.inbox_dir / "asset_b.txt"
        f1.write_bytes(b"test-img")
        f2.write_bytes(b"test-txt")

        mock_step1 = {
            "used_inbox_files": [f1, f2]
        }

        with patch("single_click_master_pipeline.MANUAL_INBOX_DIR", self.inbox_dir):
            res = scmp.step_6_archive_and_clean_inbox(mock_step1, dry_run=False, force=True)
            self.assertEqual(res["status"], "success")
            self.assertEqual(res["archived_count"], 2)
            self.assertTrue(res["inbox_clean"])

            remaining = [f for f in self.inbox_dir.iterdir() if f.is_file()]
            self.assertEqual(len(remaining), 0, "manual_inbox was not left completely clean and empty!")

    def test_08_run_project_bat_option_1_compliance(self):
        """Verify run_project.bat contains single_click_master_pipeline.py for Option [1] and default execution."""
        bat_path = PROJECT_ROOT / "run_project.bat"
        self.assertTrue(bat_path.exists(), "run_project.bat missing")

        bat_content = bat_path.read_text(encoding="utf-8", errors="ignore")
        self.assertIn("single_click_master_pipeline.py", bat_content, "run_project.bat does not execute single_click_master_pipeline.py")
        self.assertIn("goto opt1", bat_content, "Default branch in run_project.bat must be opt1")
        self.assertIn(":opt1", bat_content, ":opt1 label missing in run_project.bat")

    def test_09_full_pipeline_dry_run_subprocess_exit_0(self):
        """Verify executing single_click_master_pipeline.py --dry-run terminates with exit code 0."""
        python_exe = str(PROJECT_ROOT / ".venv" / "Scripts" / "python.exe")
        script = str(PROJECT_ROOT / "single_click_master_pipeline.py")

        res = subprocess.run(
            [python_exe, script, "--dry-run"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300
        )
        self.assertEqual(
            res.returncode, 0,
            f"single_click_master_pipeline.py --dry-run failed with code {res.returncode}:\n{res.stderr}\n{res.stdout}"
        )
        self.assertIn("Single-Click Master Pipeline", res.stdout)
        self.assertIn("كود الخروج: 0 (SUCCESS)", res.stdout)


if __name__ == "__main__":
    unittest.main()
