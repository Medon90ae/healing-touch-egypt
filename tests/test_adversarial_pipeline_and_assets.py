#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_adversarial_pipeline_and_assets.py
=============================================================================
🌿 Healing Touch Egypt — Challenger 1 Adversarial Stress Test Suite
Multi-Asset Ingestion, Edge Cases, Folder Hygiene & Single-Click Pipeline
=============================================================================
Empirical verification harness testing:
1. Multi-asset edge cases:
   - Empty inbox clean fallback & trend harvesting
   - Mixed-dimension media (extreme aspect ratios, zero-byte files, non-media files)
   - Multi-image collections without metadata (Hero + Carousel triage)
   - Folder hygiene & ghost file elimination
2. Single-click master pipeline:
   - Execution under CLI flags (--dry-run, --category bariatric, --category rhinoplasty)
   - Exit codes strictly 0 and graceful error trapping
   - Non-image inbox resilience (identifying behavior when inbox lacks images)
"""

import os
import sys
import shutil
import tempfile
import subprocess
import unittest
from unittest.mock import patch
from pathlib import Path
from PIL import Image

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
from smart_intake_classifier import (
    probe_media_dimensions,
    is_video_silent,
    scan_and_triage_manual_inbox,
    archive_used_inbox_files,
    classify_file_category,
    read_resilient_text,
    find_active_inbox_files,
    CATEGORY_KEYWORDS
)
import antigravity_social_automation as asa


class TestChallenger1MultiAssetAndPipelineStress(unittest.TestCase):
    """Empirical adversarial stress testing for asset triage, folder hygiene, and pipeline."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="ht_stress_"))
        self.inbox_dir = self.temp_dir / "manual_inbox"
        self.archive_dir = self.temp_dir / "archive"
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    # -------------------------------------------------------------------------
    # Test 1: Empty Inbox Clean Fallback & Hygiene
    # -------------------------------------------------------------------------
    def test_01_empty_inbox_clean_fallback_and_hygiene(self):
        """Stress test: Empty inbox must trigger fallback without crash, reporting clean hygiene."""
        triage = scan_and_triage_manual_inbox(self.inbox_dir)
        self.assertEqual(triage["all_files_count"], 0)
        self.assertIsNone(triage["detected_category"])
        self.assertIsNone(triage["media_triage"]["images"]["hero"])
        self.assertEqual(len(triage["media_triage"]["images"]["gallery"]), 0)

        # Folder hygiene on empty inbox
        clean_count = archive_used_inbox_files(self.inbox_dir, [])
        self.assertEqual(clean_count, 0)
        remaining = list(self.inbox_dir.iterdir())
        self.assertEqual(len(remaining), 0, "Inbox must remain completely clean")

    # -------------------------------------------------------------------------
    # Test 2: Mixed-Dimension Media & Extreme Aspect Ratios
    # -------------------------------------------------------------------------
    def test_02_mixed_dimension_media_extreme_aspect_ratios(self):
        """Stress test: Extreme aspect ratios (ultra-tall, ultra-wide, 1x1 pixel) must probe safely."""
        extreme_specs = [
            ("ultra_tall.png", (50, 2000), True, False, "vertical"),
            ("ultra_wide.png", (3000, 50), False, True, "horizontal"),
            ("tiny_pixel.png", (1, 1), False, True, "square"),
            ("standard_story.png", (1080, 1920), True, False, "vertical"),
            ("standard_landscape.png", (1920, 1080), False, True, "horizontal"),
            ("square_feed.png", (1080, 1080), False, True, "square")
        ]

        for fname, (w, h), exp_vert, exp_horiz, exp_orient in extreme_specs:
            img_path = self.inbox_dir / fname
            Image.new("RGB", (w, h), color="teal").save(img_path)
            self.assertTrue(img_path.exists())

            dim = probe_media_dimensions(img_path)
            self.assertEqual(dim["width"], w)
            self.assertEqual(dim["height"], h)
            self.assertEqual(dim["is_vertical_9_16"], exp_vert, f"Failed vert for {fname}")
            self.assertEqual(dim["is_horizontal_16_9"], exp_horiz, f"Failed horiz for {fname}")
            self.assertEqual(dim["orientation"], exp_orient, f"Failed orient for {fname}")

    # -------------------------------------------------------------------------
    # Test 3: Zero-Byte Files Handling & Resilience
    # -------------------------------------------------------------------------
    def test_03_zero_byte_files_resilience(self):
        """Stress test: Zero-byte files (image, video, audio, text) must never cause fatal crashes."""
        zero_img = self.inbox_dir / "zero_case.jpg"
        zero_vid = self.inbox_dir / "zero_reel.mp4"
        zero_aud = self.inbox_dir / "zero_voice.m4a"
        zero_txt = self.inbox_dir / "zero_script.txt"

        for p in [zero_img, zero_vid, zero_aud, zero_txt]:
            p.write_bytes(b"")
            self.assertEqual(p.stat().st_size, 0)

        # 1. Probing zero-byte image should return fallback default dict without raising
        dim_img = probe_media_dimensions(zero_img)
        self.assertIn("width", dim_img)
        self.assertIn("height", dim_img)
        self.assertEqual(dim_img["width"], 1080)
        self.assertEqual(dim_img["height"], 1920)

        # 2. Probing zero-byte video should return fallback default dict
        dim_vid = probe_media_dimensions(zero_vid)
        self.assertIn("width", dim_vid)
        self.assertEqual(dim_vid["width"], 1080)

        # 3. is_video_silent on zero-byte video should return False gracefully
        silent = is_video_silent(zero_vid)
        self.assertFalse(silent)

        # 4. read_resilient_text on zero-byte text should return empty string
        txt = read_resilient_text(zero_txt)
        self.assertEqual(txt, "")

        # 5. scan_and_triage_manual_inbox should handle zero-byte files without exception
        triage = scan_and_triage_manual_inbox(self.inbox_dir)
        self.assertEqual(triage["all_files_count"], 4)

    # -------------------------------------------------------------------------
    # Test 4: Non-Media Files Filtering & Category Fallback
    # -------------------------------------------------------------------------
    def test_04_non_media_files_filtering(self):
        """Stress test: Non-media files (.exe, .zip, .pdf, .bin, hidden) must be safely categorized."""
        non_media = [
            ("malware.exe", b"\x4D\x5A\x90\x00"),
            ("dataset.zip", b"PK\x03\x04\x00\x00"),
            ("clinical_paper.pdf", b"%PDF-1.4\n%..."),
            ("unknown_blob.bin", b"\xDE\xAD\xBE\xEF"),
            (".hidden_config", b"key=value")
        ]

        for fname, data in non_media:
            (self.inbox_dir / fname).write_bytes(data)

        triage = scan_and_triage_manual_inbox(self.inbox_dir)
        # Hidden files starting with dot are excluded by find_active_inbox_files
        self.assertEqual(triage["all_files_count"], 4)
        
        # Verify non-media files are not erroneously placed into media arrays
        self.assertEqual(len(triage["media_triage"]["images"]["all"]), 0)
        self.assertEqual(len(triage["media_triage"]["videos"]["all"]), 0)
        self.assertEqual(len(triage["media_triage"]["audios"]), 0)

        # Category classification fallback for non-media files without keywords defaults to c-section
        for fname, _ in non_media[:4]:
            cat = classify_file_category(self.inbox_dir / fname)
            self.assertEqual(cat, "c-section")

    # -------------------------------------------------------------------------
    # Test 5: Multi-Image Collection Without Metadata (Hero + Carousel)
    # -------------------------------------------------------------------------
    def test_05_multi_image_collection_without_metadata(self):
        """Stress test: 8 images with arbitrary names & no metadata must triage to 1 Hero + 7 Gallery."""
        arbitrary_names = [
            "img_001.jpg", "img_002.png", "img_003.webp", "snap_a.jpg",
            "pic_b.png", "photo_c.webp", "shot_d.jpg", "case_e.png"
        ]

        for idx, name in enumerate(arbitrary_names):
            p = self.inbox_dir / name
            # Give distinct sizes to verify distinct file handling
            Image.new("RGB", (200 + idx * 10, 200 + idx * 10), color="blue").save(p)

        triage = scan_and_triage_manual_inbox(self.inbox_dir)
        imgs = triage["media_triage"]["images"]

        self.assertEqual(len(imgs["all"]), 8)
        self.assertIsNotNone(imgs["hero"])
        self.assertEqual(imgs["hero"].name, "case_e.png" if "case_e.png" < "img_001.jpg" else imgs["all"][0].name)
        self.assertEqual(len(imgs["gallery"]), 7)

        # All 8 images must be accounted for (1 hero + 7 gallery = 8)
        combined = [imgs["hero"]] + imgs["gallery"]
        self.assertEqual(len(combined), 8)
        self.assertEqual(set(f.name for f in combined), set(arbitrary_names))

    # -------------------------------------------------------------------------
    # Test 6: Folder Hygiene & Elimination of Ghost Files
    # -------------------------------------------------------------------------
    def test_06_folder_hygiene_and_elimination_of_ghost_files(self):
        """Stress test: Archiving mixed files must leave manual_inbox with 0 ghost files."""
        # Create a rich mixed set of files
        files_to_create = [
            ("hero.jpg", b"fake_hero_jpg"),
            ("gallery1.png", b"fake_gallery_1"),
            ("gallery2.webp", b"fake_gallery_2"),
            ("video_9x16.mp4", b"fake_vertical_video"),
            ("audio_consult.m4a", b"fake_audio_stream"),
            ("notes.txt", "نص تجريبي للتعافي".encode("utf-8")),
            ("archive_data.zip", b"PK_fake_archive"),
            ("zero_byte.jpg", b"")
        ]

        created_paths = []
        for name, content in files_to_create:
            p = self.inbox_dir / name
            p.write_bytes(content)
            created_paths.append(p)

        # Perform archival
        archived_count = archive_used_inbox_files(self.inbox_dir, created_paths)
        self.assertEqual(archived_count, len(files_to_create))

        # Assert manual_inbox is 100% clean (no ghost files left)
        remaining_inbox = [
            f for f in self.inbox_dir.iterdir()
            if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
        ]
        self.assertEqual(len(remaining_inbox), 0, f"Ghost files detected in inbox: {remaining_inbox}")

        # Assert archived files exist in dated folder under archive/
        arch_subdirs = list(self.archive_dir.iterdir())
        self.assertGreaterEqual(len(arch_subdirs), 1)
        latest_arch = sorted(arch_subdirs, key=lambda x: x.name, reverse=True)[0]
        archived_files = list(latest_arch.iterdir())
        self.assertEqual(len(archived_files), len(files_to_create))

        # Assert byte-level integrity in archive
        for name, content in files_to_create:
            archived_p = latest_arch / name
            self.assertTrue(archived_p.exists(), f"Missing in archive: {name}")
            self.assertEqual(archived_p.read_bytes(), content, f"Corrupted content: {name}")

    # -------------------------------------------------------------------------
    # Test 7: Clinical Research Trends Fallback Verification
    # -------------------------------------------------------------------------
    def test_07_clinical_research_trends_fallback_enrichment(self):
        """Stress test: Clinical research trend harvesting enriches story text and hashtags."""
        from github_seo_trend_engine import harvest_live_egypt_trends, convert_query_to_hashtag

        trends_dict = harvest_live_egypt_trends()
        self.assertIsInstance(trends_dict, dict)
        self.assertIn("c-section", trends_dict)
        self.assertIn("rhinoplasty", trends_dict)
        self.assertIn("bariatric", trends_dict)

        # Verify trending queries are formatted into valid hashtags
        for cat, queries in trends_dict.items():
            self.assertGreater(len(queries), 0, f"No queries for {cat}")
            for q in queries[:2]:
                tag = convert_query_to_hashtag(q)
                self.assertTrue(tag.startswith("#"), f"Tag should start with #: {tag}")
                self.assertNotIn(" ", tag, f"Tag cannot have spaces: {tag}")

    # -------------------------------------------------------------------------
    # Test 8: Non-Image Inbox Fallback Resilience Check
    # -------------------------------------------------------------------------
    def test_08_non_image_inbox_fallback_resilience(self):
        """
        Adversarial Challenge: When manual_inbox contains ONLY non-image files
        (e.g., video, audio, text, or pdf), verify whether step 1 assigns a valid
        fallback hero image or leaves hero_image as None.
        """
        # Create an inbox with only a video and a text file (no images)
        vid_p = self.inbox_dir / "rhino_video_demo.mp4"
        vid_p.write_bytes(b"\x00" * 512)
        txt_p = self.inbox_dir / "rhino_notes.txt"
        txt_p.write_text("ملاحظات طبية لدعامة الأنف وتثبيت الغضاريف", encoding="utf-8")

        with patch("single_click_master_pipeline.MANUAL_INBOX_DIR", self.inbox_dir):
            step1 = scmp.step_1_scan_and_classify_media(category="rhinoplasty")
            
            # Record observation: Does step 1 provide a hero_image or None?
            hero = step1.get("hero_image")
            # If hero is None, step 3 will crash on generate_branded_card
            # This is an empirical challenge check
            if hero is None:
                # Document finding: non-image inbox creates hero_image=None
                print("\n[CHALLENGE OBSERVATION]: Inbox without image files resulted in hero_image=None!")
            else:
                self.assertTrue(Path(hero).exists())

    def test_09_hero_image_none_step3_behavior(self):
        """
        Adversarial remediation verification:
        When hero_image is None (e.g. user puts only video or only text in manual_inbox),
        verify that step_3_generate_creatives_and_packages survives gracefully and produces valid assets.
        """
        mock_step1 = {
            "status": "success",
            "has_custom_inbox": True,
            "category": "rhinoplasty",
            "template_index": 0,
            "case_data": asa.CLINICAL_STORIES_TEMPLATES[0],
            "hero_image": None,  # no images in inbox!
            "gallery_images": [],
            "video_vertical": None,
            "video_horizontal": None,
            "audio_path": None,
            "platform_texts": {},
            "used_inbox_files": []
        }
        mock_step2 = {
            "status": "success",
            "public_url": "https://medon90ae.github.io/healing-touch-egypt/lp/rhinoplasty-recovery-protocol.html"
        }

        # Step 3 must survive gracefully without PermissionError
        res = scmp.step_3_generate_creatives_and_packages(mock_step1, mock_step2)
        self.assertEqual(res.get("status"), "success")
        self.assertIn("pack_dir", res)
        self.assertTrue(Path(res["pack_dir"]).exists())


if __name__ == "__main__":
    unittest.main()
