# -*- coding: utf-8 -*-
"""
tests/test_clinical_cleanup_guardrails.py
=============================================================================
Authoritative E2E Clinical Cleanup & Technical Guardrails Test Suite
Healing Touch Egypt (هيلينج تاتش مصر)
Requirements Reference: ORIGINAL_REQUEST.md (## 2026-10-29T16:59:02Z, R1–R4)

Verifies:
1. R1: Zero occurrences of "حاسبة جاهزية الاستحمام" in portal_app and docs.
2. R1: Zero occurrences of "الجدول الزمني السريري للتعافي والتئام الأنسجة" in portal_app and docs.
3. R1: Patient reviews section suppression in portal_app.
4. R1: Zero occurrences of visible raw phone digits (01155803307) in docs HTML files.
5. R1: All consultation CTAs strictly route to approved WhatsApp URL with HT10:
       https://wa.me/201155803307?text=... (with HT10 code).
6. R4: Ready-to-publish 6-platform pack completeness:
       - YouTube: 16:9 full video script, 9:16 Shorts script, 15 search tags.
       - TikTok: Viral hook script in Egyptian dialect, SEO caption and hashtags.
       - Instagram & Facebook: 7-slide medical carousel guide, post & reels captions.
       - Blogger: Long-form clinical article (1200+ words) with valid FAQPage schema.
       - Landing Page: HTML file with clinical support links and approved HT10 CTA.
=============================================================================
"""

import os
import re
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

PORTAL_SRC = PROJECT_ROOT / "portal_app" / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
OFFICIAL_PHONE = "201155803307"
RAW_PHONE_LOCAL = "01155803307"


class TestClinicalCleanupGuardrails(unittest.TestCase):
    """Clinical safety and technical compliance guardrails for Healing Touch Egypt."""

    def test_01_shower_readiness_calculator_zero_occurrences_in_portal_app_and_docs(self):
        """
        R1 Guardrail: Assert ZERO occurrences of 'حاسبة جاهزية الاستحمام'
        across portal_app/src/, docs/, and static site generators.
        """
        forbidden_phrases = [
            "حاسبة جاهزية الاستحمام",
            "حاسبة جاهزية الاستحمام ومراحل التئام القيصرية",
        ]

        violations = []

        # 1. Scan portal_app/src/
        if PORTAL_SRC.exists():
            for root, _, files in os.walk(PORTAL_SRC):
                for f in files:
                    if f.endswith((".ts", ".tsx", ".html", ".css", ".json")):
                        fpath = Path(root) / f
                        try:
                            content = fpath.read_text(encoding="utf-8", errors="ignore")
                        except Exception:
                            continue
                        for phrase in forbidden_phrases:
                            if phrase in content:
                                violations.append(f"portal_app: {fpath.relative_to(PROJECT_ROOT)} contains '{phrase}'")

        # 2. Scan docs/ HTML files
        if DOCS_DIR.exists():
            for hf in DOCS_DIR.rglob("*.html"):
                try:
                    content = hf.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                for phrase in forbidden_phrases:
                    if phrase in content:
                        violations.append(f"docs: {hf.relative_to(PROJECT_ROOT)} contains '{phrase}'")

        # 3. Scan site generators
        generators = [
            PROJECT_ROOT / "github_seo_trend_engine.py",
            PROJECT_ROOT / "campaign_landing_engine.py",
            PROJECT_ROOT / "scripts" / "build_ready_to_publish_pack.py",
        ]
        for gen in generators:
            if gen.exists():
                content = gen.read_text(encoding="utf-8", errors="ignore")
                for phrase in forbidden_phrases:
                    if phrase in content:
                        violations.append(f"generator: {gen.relative_to(PROJECT_ROOT)} contains '{phrase}'")

        self.assertEqual(
            len(violations), 0,
            f"R1 Violation: 'حاسبة جاهزية الاستحمام' must be completely eradicated (found {len(violations)} occurrences):\n"
            + "\n".join(violations[:20])
        )

    def test_02_fixed_clinical_timeline_zero_occurrences_in_portal_app_and_docs(self):
        """
        R1 Guardrail: Assert ZERO occurrences of 'الجدول الزمني السريري للتعافي والتئام الأنسجة'
        across portal_app/src/ and all docs/ HTML files.
        """
        forbidden_phrases = [
            "الجدول الزمني السريري للتعافي والتئام الأنسجة",
            "الجدول الزمني السريري للتعافي والتئام الأنسجة (من الأسبوع 1 حتى الشهر 3)",
        ]

        violations = []

        # 1. Scan portal_app/src/
        if PORTAL_SRC.exists():
            for root, _, files in os.walk(PORTAL_SRC):
                for f in files:
                    if f.endswith((".ts", ".tsx", ".html", ".css", ".json")):
                        fpath = Path(root) / f
                        try:
                            content = fpath.read_text(encoding="utf-8", errors="ignore")
                        except Exception:
                            continue
                        for phrase in forbidden_phrases:
                            if phrase in content:
                                violations.append(f"portal_app: {fpath.relative_to(PROJECT_ROOT)} contains '{phrase}'")

        # 2. Scan docs/ HTML files
        if DOCS_DIR.exists():
            for hf in DOCS_DIR.rglob("*.html"):
                try:
                    content = hf.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                for phrase in forbidden_phrases:
                    if phrase in content:
                        violations.append(f"docs: {hf.relative_to(PROJECT_ROOT)} contains '{phrase}'")

        # 3. Scan site generators
        gen = PROJECT_ROOT / "github_seo_trend_engine.py"
        if gen.exists():
            content = gen.read_text(encoding="utf-8", errors="ignore")
            for phrase in forbidden_phrases:
                if phrase in content:
                    violations.append(f"generator: {gen.relative_to(PROJECT_ROOT)} contains '{phrase}'")

        self.assertEqual(
            len(violations), 0,
            f"R1 Violation: Fixed clinical timeline must be completely removed (found {len(violations)} occurrences):\n"
            + "\n".join(violations[:20])
        )

    def test_03_patient_reviews_component_suppressed_in_portal_app(self):
        """
        R1 Guardrail: Verify unverified reviews/testimonials component is suppressed in portal_app
        until real verified patient evidence is supplied.
        """
        app_file = PORTAL_SRC / "App.tsx"
        self.assertTrue(app_file.exists(), "portal_app/src/App.tsx missing")
        app_code = app_file.read_text(encoding="utf-8", errors="ignore")

        # Check whether <ReviewsAndDoctorEndorsement is actively rendered (uncommented)
        active_render_pattern = re.compile(r'^\s*<ReviewsAndDoctorEndorsement\s', re.MULTILINE)
        has_active_render = bool(active_render_pattern.search(app_code))

        # Check whether component itself early returns null or has suppression flag
        comp_file = PORTAL_SRC / "components" / "ReviewsAndDoctorEndorsement.tsx"
        is_suppressed_internally = False
        if comp_file.exists():
            comp_code = comp_file.read_text(encoding="utf-8", errors="ignore")
            if "return null" in comp_code or "SHOW_REVIEWS = false" in comp_code or "SHOW_REVIEWS=false" in comp_code:
                is_suppressed_internally = True

        self.assertTrue(
            not has_active_render or is_suppressed_internally,
            "R1 Violation: ReviewsAndDoctorEndorsement must be suppressed in portal_app (either unmounted in App.tsx or early-returning null)."
        )

    def test_04_zero_visible_raw_phone_digits_in_docs_html(self):
        """
        R1 Guardrail: Assert ZERO occurrences of visible raw phone digits (01155803307)
        in visitor-facing HTML text across docs/ (outside of href="https://wa.me/..." and technical script tags).
        """
        if not DOCS_DIR.exists():
            self.skipTest("docs/ directory not found")

        violations = []
        raw_phone_in_parens = re.compile(r'\(\s*01155803307\s*\)')
        raw_phone_in_text = re.compile(r'>[^<]*01155803307[^<]*<')

        for hf in DOCS_DIR.rglob("*.html"):
            try:
                content = hf.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            # Check for visible (01155803307) in buttons or text
            if raw_phone_in_parens.search(content):
                violations.append(f"{hf.relative_to(PROJECT_ROOT)} contains visible '(01155803307)'")

            # Check for visible text node containing 01155803307
            # Filter out <script> and JSON-LD blocks
            clean_html = re.sub(r'<script[\s\S]*?</script>', '', content)
            matches = raw_phone_in_text.findall(clean_html)
            if matches:
                sample = matches[0].strip()
                violations.append(f"{hf.relative_to(PROJECT_ROOT)} contains visible text node '{sample}'")

        self.assertEqual(
            len(violations), 0,
            f"R1 Violation: Raw phone digits (01155803307) must be replaced with official WhatsApp link (found {len(violations)} occurrences):\n"
            + "\n".join(violations[:20])
        )

    def test_05_consultation_ctas_route_to_approved_whatsapp_url_with_ht10(self):
        """
        R1 Guardrail: Assert all consultation CTAs route to:
        https://wa.me/201155803307?text=... containing promo code HT10.
        """
        # 1. Verify global triage router
        triage_js = DOCS_DIR / "assets" / "whatsapp-triage.js"
        if triage_js.exists():
            triage_content = triage_js.read_text(encoding="utf-8")
            self.assertIn(OFFICIAL_PHONE, triage_content)
            self.assertIn("HT10", triage_content)

        # 2. Verify validation utility in portal_app
        val_file = PORTAL_SRC / "utils" / "validation.ts"
        if val_file.exists():
            val_content = val_file.read_text(encoding="utf-8")
            self.assertIn(OFFICIAL_PHONE, val_content)
            self.assertIn("HT10", val_content)

        # 3. Verify static docs direct WhatsApp links
        wa_link_pattern = re.compile(r'href=["\'](https://wa\.me/[^"\']+)["\']')
        wa_links_checked = 0
        invalid_links = []

        if DOCS_DIR.exists():
            for hf in DOCS_DIR.rglob("*.html"):
                try:
                    content = hf.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                for link in wa_link_pattern.findall(content):
                    wa_links_checked += 1
                    if OFFICIAL_PHONE not in link:
                        invalid_links.append(f"{hf.name}: {link} (wrong phone)")
                    if "HT10" not in link and "ht10" not in link.lower():
                        invalid_links.append(f"{hf.name}: {link} (missing HT10)")

        self.assertGreater(wa_links_checked, 0, "No WhatsApp consultation links found in docs!")
        self.assertEqual(
            len(invalid_links), 0,
            f"R1 Violation: WhatsApp consultation links must use phone {OFFICIAL_PHONE} and HT10 code:\n"
            + "\n".join(invalid_links[:20])
        )

    def test_06_ready_to_publish_pack_generator_youtube_16_9_and_9_16_and_15_tags(self):
        """
        R4 Guardrail: Assert YouTube pack completeness:
        - 16:9 full video script
        - 9:16 Shorts script
        - Minimum 15 search tags
        """
        from scripts.build_ready_to_publish_pack import generate_pack, READY_BASE_DIR

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ready = Path(tmp_dir) / "ready_to_publish"
            tmp_ready.mkdir(parents=True, exist_ok=True)

            import scripts.build_ready_to_publish_pack as bpack
            with patch.object(bpack, "READY_BASE_DIR", tmp_ready):
                pack_dir = bpack.generate_pack(category="rhinoplasty")
                self.assertIsNotNone(pack_dir)
                yt_dir = pack_dir / "01_يوتيوب_YouTube"
                self.assertTrue(yt_dir.exists(), "01_يوتيوب_YouTube folder missing")

                # 1. Full 16:9 video script
                full_script = yt_dir / "سكريبت_الفيديو_الكامل.txt"
                self.assertTrue(full_script.exists(), "YouTube 16:9 full script file missing")
                full_text = full_script.read_text(encoding="utf-8")
                self.assertGreater(len(full_text.strip()), 150, "YouTube 16:9 full script too short")

                # 2. Shorts 9:16 script
                shorts_file = yt_dir / "بيانات_الشورتس.txt"
                self.assertTrue(shorts_file.exists(), "YouTube Shorts file missing")
                shorts_text = shorts_file.read_text(encoding="utf-8")
                self.assertIn("HT10", shorts_text)

                # 3. Tags count >= 15
                video_info = yt_dir / "بيانات_الفيديو_عنوان_ووصف_وهاشتاجات.txt"
                self.assertTrue(video_info.exists(), "YouTube video info file missing")
                info_text = video_info.read_text(encoding="utf-8")
                tags_found = re.findall(r'#[\w_]+', info_text)
                self.assertGreaterEqual(
                    len(tags_found), 15,
                    f"R4 Violation: YouTube pack must contain at least 15 search tags, found {len(tags_found)}: {tags_found}"
                )

    def test_07_ready_to_publish_pack_generator_tiktok_viral_hook(self):
        """
        R4 Guardrail: Assert TikTok pack completeness:
        - Viral hook script in Egyptian dialect
        - Caption and hashtags
        - WhatsApp HT10 link
        """
        import scripts.build_ready_to_publish_pack as bpack

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ready = Path(tmp_dir) / "ready_to_publish"
            tmp_ready.mkdir(parents=True, exist_ok=True)

            with patch.object(bpack, "READY_BASE_DIR", tmp_ready):
                pack_dir = bpack.generate_pack(category="c-section")
                tt_dir = pack_dir / "02_تيكتوك_TikTok"
                self.assertTrue(tt_dir.exists(), "02_تيكتوك_TikTok folder missing")

                # Script with viral hook
                script_file = tt_dir / "سيناريو_تيكتوك_الرقمي.txt"
                self.assertTrue(script_file.exists(), "TikTok scenario file missing")
                script_text = script_file.read_text(encoding="utf-8")
                self.assertGreater(len(script_text.strip()), 100, "TikTok script too short")

                # Caption with HT10
                caption_file = tt_dir / "كابشن_وهاشتاجات_تيكتوك.txt"
                self.assertTrue(caption_file.exists(), "TikTok caption file missing")
                caption_text = caption_file.read_text(encoding="utf-8")
                self.assertIn("HT10", caption_text)
                self.assertIn(OFFICIAL_PHONE, caption_text)

    def test_08_ready_to_publish_pack_generator_instagram_facebook_carousel(self):
        """
        R4 Guardrail: Assert Instagram & Facebook pack completeness:
        - 7-slide medical carousel guide
        - Post & Reels caption
        """
        import scripts.build_ready_to_publish_pack as bpack

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ready = Path(tmp_dir) / "ready_to_publish"
            tmp_ready.mkdir(parents=True, exist_ok=True)

            with patch.object(bpack, "READY_BASE_DIR", tmp_ready):
                pack_dir = bpack.generate_pack(category="bariatric")
                ig_dir = pack_dir / "03_إنستجرام_Instagram"
                fb_dir = pack_dir / "06_فيسبوك_Facebook"

                self.assertTrue(ig_dir.exists(), "03_إنستجرام_Instagram folder missing")
                self.assertTrue(fb_dir.exists(), "06_فيسبوك_Facebook folder missing")

                # Carousel guide
                carousel_file = ig_dir / "دليل_الكاروسيل_السريري.txt"
                self.assertTrue(carousel_file.exists(), "Instagram carousel guide missing")
                carousel_text = carousel_file.read_text(encoding="utf-8")
                # Assert 7 slides structure
                for slide_num in range(1, 8):
                    self.assertTrue(
                        f"شريحة {slide_num}" in carousel_text or f"الشريحة {slide_num}" in carousel_text or f"Slide {slide_num}" in carousel_text,
                        f"Carousel guide must contain Slide {slide_num}"
                    )

                # Instagram Caption with HT10
                ig_caption = (ig_dir / "كابشن_وهاشتاجات_إنستجرام.txt").read_text(encoding="utf-8")
                self.assertIn("HT10", ig_caption)

                # Facebook Post
                fb_post = (fb_dir / "منشور_فيسبوك_السريري_والإنساني.txt").read_text(encoding="utf-8")
                self.assertIn("HT10", fb_post)

    def test_09_ready_to_publish_pack_generator_blogger_1200w_article_and_faq_schema(self):
        """
        R4 Guardrail: Assert Blogger article completeness:
        - Long-form clinical article (>= 1200 words)
        - Valid FAQPage schema markup
        """
        import scripts.build_ready_to_publish_pack as bpack

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ready = Path(tmp_dir) / "ready_to_publish"
            tmp_ready.mkdir(parents=True, exist_ok=True)

            with patch.object(bpack, "READY_BASE_DIR", tmp_ready):
                pack_dir = bpack.generate_pack(category="thyroid")
                bl_dir = pack_dir / "04_بلوجر_Blogger"
                self.assertTrue(bl_dir.exists(), "04_بلوجر_Blogger folder missing")

                bl_file = bl_dir / "مقال_بلوجر_جاهز_للنشر.html"
                self.assertTrue(bl_file.exists(), "Blogger HTML file missing")
                bl_html = bl_file.read_text(encoding="utf-8")

                # Word count check (strip HTML tags, count Arabic words)
                clean_text = re.sub(r'<[^>]+>', ' ', bl_html)
                words = [w for w in clean_text.split() if len(w) > 1]
                self.assertGreaterEqual(
                    len(words), 1200,
                    f"R4 Violation: Blogger article must contain at least 1200 words, found {len(words)}."
                )

                # FAQPage Schema check
                has_faq_schema = "FAQPage" in bl_html or "schema.org/FAQPage" in bl_html or "https://schema.org/FAQPage" in bl_html
                self.assertTrue(
                    has_faq_schema,
                    "R4 Violation: Blogger article must contain valid FAQPage schema markup."
                )

    def test_10_ready_to_publish_pack_generator_landing_page_html(self):
        """
        R4 Guardrail: Assert ready_to_publish pack includes complete visual HTML landing page
        with clinical support links and approved HT10 CTA.
        """
        import scripts.build_ready_to_publish_pack as bpack

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_ready = Path(tmp_dir) / "ready_to_publish"
            tmp_ready.mkdir(parents=True, exist_ok=True)

            with patch.object(bpack, "READY_BASE_DIR", tmp_ready):
                pack_dir = bpack.generate_pack(category="rhinoplasty")
                lp_dir = pack_dir / "07_صفحة_الهبوط_LandingPage"
                if not lp_dir.exists():
                    # Check if HTML file is placed at pack root
                    lp_files = list(pack_dir.glob("*.html"))
                else:
                    lp_files = list(lp_dir.glob("*.html"))

                self.assertGreater(
                    len(lp_files), 0,
                    "R4 Violation: Ready-to-publish pack must contain a dedicated visual HTML landing page file."
                )
                lp_html = lp_files[0].read_text(encoding="utf-8")
                self.assertIn("HT10", lp_html)
                self.assertIn(OFFICIAL_PHONE, lp_html)


if __name__ == "__main__":
    unittest.main()
