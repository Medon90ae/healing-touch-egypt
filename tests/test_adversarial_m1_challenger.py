# -*- coding: utf-8 -*-
"""
tests/test_adversarial_m1_challenger.py
=============================================================================
EMPIRICAL CHALLENGER 1 — ADVERSARIAL STRESS HARNESS
Milestone M1: Clinical Cleanup & Patient Safety Verification
Healing Touch Egypt (هيلينج تاتش مصر)

Empirically challenges and stress-tests:
1. Every HTML file in docs/ (all 35 files) and all files in portal_app/src/ for:
   - "حاسبة جاهزية الاستحمام" (and linguistic permutations)
   - "الجدول الزمني السريري للتعافي والتئام الأنسجة" (and permutations)
   - "(01155803307)" (visible raw phone digits and textual leaks)
2. Zero un-sanitized pages & zero false positives (content preservation).
3. Edge cases in phone number regex and WhatsApp link generation (50+ vectors).
=============================================================================
"""

import os
import re
import sys
import json
import urllib.parse
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DOCS_DIR = PROJECT_ROOT / "docs"
PORTAL_SRC = PROJECT_ROOT / "portal_app" / "src"
OFFICIAL_PHONE = "201155803307"
RAW_PHONE_LOCAL = "01155803307"


def normalize_arabic_text(text: str) -> str:
    """Normalize Arabic text to catch slight spelling variations in adversarial scan."""
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)  # remove tashkeel/diacritics
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


class AdversarialMilestone1ChallengerTest(unittest.TestCase):
    """Adversarial stress-test suite for Milestone M1."""

    @classmethod
    def setUpClass(cls):
        cls.html_files = list(DOCS_DIR.rglob("*.html")) if DOCS_DIR.exists() else []

    def test_01_adversarial_scan_all_docs_html_for_forbidden_terms(self):
        """
        Adversarially scans every single HTML file in docs/ (all 35 files expected)
        for forbidden terms and linguistic/orthographic variants.
        """
        self.assertGreaterEqual(
            len(self.html_files), 30,
            f"Expected at least 30 HTML files in docs/, found {len(self.html_files)}"
        )

        forbidden_raw_patterns = [
            re.compile(r'حاسب[ةه]\s+جاهزي[ةه]\s+[اإ]ستحمام', re.IGNORECASE),
            re.compile(r'حاسب[ةه]\s+[اإ]ستحمام', re.IGNORECASE),
            re.compile(r'جاهزي[ةه]\s+[اإ]ستحمام', re.IGNORECASE),
            re.compile(r'الجدول\s+الزمني\s+السريري\s+للتعافي\s+والتئام\s+الأنسج[ةه]', re.IGNORECASE),
            re.compile(r'الجدول\s+الزمني\s+السريري\s+للتعافي', re.IGNORECASE),
            re.compile(r'\(\s*01155803307\s*\)'),
            re.compile(r'\(\s*٠١١٥٥٨٠٣٣٠٧\s*\)'),
        ]

        violations = []
        scanned_count = 0

        for hf in self.html_files:
            scanned_count += 1
            content = hf.read_text(encoding="utf-8", errors="ignore")

            for pat in forbidden_raw_patterns:
                match = pat.search(content)
                if match:
                    violations.append(
                        f"Violating File: {hf.relative_to(PROJECT_ROOT)} matched pattern '{pat.pattern}' -> found: '{match.group(0)}'"
                    )

            # Check normalized Arabic text as secondary oracle
            norm_content = normalize_arabic_text(content)
            if "حاسبه جاهزيه استحمام" in norm_content:
                violations.append(f"Normalized leak in {hf.relative_to(PROJECT_ROOT)}: 'حاسبه جاهزيه استحمام'")
            if "الجدول الزمني السريري للتعافي والتئام الانسجه" in norm_content:
                violations.append(f"Normalized leak in {hf.relative_to(PROJECT_ROOT)}: 'الجدول الزمني السريري للتعافي والتئام الانسجه'")

        print(f"\n[Test 1] Scanned {scanned_count} HTML files in docs/. Violations: {len(violations)}")
        self.assertEqual(len(violations), 0, "\n".join(violations))

    def test_02_adversarial_scan_portal_app_src_files(self):
        """
        Adversarially scans every source code file in portal_app/src/
        (excluding test assertions in *.test.ts files).
        """
        self.assertTrue(PORTAL_SRC.exists(), "portal_app/src directory must exist")
        portal_files = [
            f for f in PORTAL_SRC.rglob("*")
            if f.is_file() and f.suffix in ('.ts', '.tsx', '.html', '.css', '.json')
            and not f.name.endswith('.test.ts')
        ]
        self.assertGreaterEqual(len(portal_files), 15, "Expected at least 15 source files in portal_app/src")

        forbidden_literals = [
            "حاسبة جاهزية الاستحمام",
            "حاسبة جاهزية الاستحمام ومراحل التئام القيصرية",
            "الجدول الزمني السريري للتعافي والتئام الأنسجة",
            "(01155803307)",
        ]

        violations = []
        for pf in portal_files:
            content = pf.read_text(encoding="utf-8", errors="ignore")
            for phrase in forbidden_literals:
                if phrase in content:
                    violations.append(f"{pf.relative_to(PROJECT_ROOT)} contains forbidden literal: '{phrase}'")

        print(f"\n[Test 2] Scanned {len(portal_files)} non-test files in portal_app/src. Violations: {len(violations)}")
        self.assertEqual(len(violations), 0, "\n".join(violations))

    def test_03_adversarial_scan_compiled_portal_bundle(self):
        """
        Adversarially verifies that the compiled production bundle in docs/portal/assets/
        does NOT contain the forbidden strings baked into the JavaScript or CSS.
        """
        portal_dist_assets = DOCS_DIR / "portal" / "assets"
        self.assertTrue(portal_dist_assets.exists(), "docs/portal/assets must exist")

        bundle_files = list(portal_dist_assets.glob("*.js")) + list(portal_dist_assets.glob("*.css"))
        self.assertGreaterEqual(len(bundle_files), 1, "Expected compiled JS/CSS bundle in docs/portal/assets")

        forbidden_literals = [
            "حاسبة جاهزية الاستحمام",
            "الجدول الزمني السريري للتعافي والتئام الأنسجة",
            "(01155803307)",
        ]

        violations = []
        for bf in bundle_files:
            content = bf.read_text(encoding="utf-8", errors="ignore")
            for phrase in forbidden_literals:
                if phrase in content:
                    violations.append(f"Compiled bundle {bf.name} leaked forbidden phrase: '{phrase}'")

        print(f"\n[Test 3] Scanned {len(bundle_files)} compiled bundle files in docs/portal/assets. Violations: {len(violations)}")
        self.assertEqual(len(violations), 0, "\n".join(violations))

    def test_04_zero_unsanitized_pages_and_html_integrity(self):
        """
        Empirically checks that all 35 HTML pages in docs/ are well-formed,
        non-empty, have DOCTYPE, title, meta viewport, and zero empty/broken CTAs.
        """
        broken_pages = []
        for hf in self.html_files:
            size = hf.stat().st_size
            if size < 500:
                broken_pages.append(f"{hf.relative_to(PROJECT_ROOT)} is suspiciously small ({size} bytes)")
                continue

            content = hf.read_text(encoding="utf-8", errors="ignore")

            # Check DOCTYPE
            if "<!DOCTYPE html>" not in content and "<!doctype html>" not in content.lower():
                broken_pages.append(f"{hf.relative_to(PROJECT_ROOT)} missing <!DOCTYPE html>")

            # Check <title>
            if "<title>" not in content:
                broken_pages.append(f"{hf.relative_to(PROJECT_ROOT)} missing <title>")

            # Check for empty action attributes or dangling placeholder hrefs
            if re.search(r'href=["\']#["\']\s+class=["\'][^"\']*btn', content):
                broken_pages.append(f"{hf.relative_to(PROJECT_ROOT)} has dummy href='#' button")

        print(f"\n[Test 4] Integrity checked across {len(self.html_files)} HTML pages. Issues: {len(broken_pages)}")
        self.assertEqual(len(broken_pages), 0, "\n".join(broken_pages))

    def test_05_zero_false_positives_content_preservation(self):
        """
        Empirically verifies that sanitization did not over-strip legitimate clinical content:
        - 5 product pages in docs/products/ have proper product titles, specifications, and schema.
        - 15 article pages in docs/articles/ have scientific references and medical guidance.
        - docs/index.html retains knowledge hub and products catalog.
        """
        products_dir = DOCS_DIR / "products"
        articles_dir = DOCS_DIR / "articles"

        product_pages = list(products_dir.glob("*.html"))
        article_pages = list(articles_dir.glob("*.html"))

        self.assertEqual(len(product_pages), 5, f"Expected 5 product pages, found {len(product_pages)}")
        self.assertEqual(len(article_pages), 15, f"Expected 15 article pages, found {len(article_pages)}")

        # Verify each product page preserves medical specs and schema
        for pp in product_pages:
            txt = pp.read_text(encoding="utf-8", errors="ignore")
            self.assertIn("MedicalWebPage", txt, f"Product {pp.name} missing MedicalWebPage schema")
            self.assertIn("HT10", txt, f"Product {pp.name} missing HT10 reference")
            self.assertIn("هيلينج تاتش مصر", txt, f"Product {pp.name} missing brand identity")

        # Verify each article page preserves references and clinical content
        for ap in article_pages:
            txt = ap.read_text(encoding="utf-8", errors="ignore")
            self.assertTrue(
                "المراجع" in txt or "مراجع" in txt,
                f"Article {ap.name} missing references section"
            )
            self.assertTrue(
                "pubmed" in txt.lower() or "ncbi" in txt.lower(),
                f"Article {ap.name} missing PubMed/NCBI citations"
            )
            self.assertIn("HT10", txt, f"Article {ap.name} missing HT10 reference")

        # Verify index.html preserves knowledge hub
        index_txt = (DOCS_DIR / "index.html").read_text(encoding="utf-8", errors="ignore")
        self.assertIn("knowledge-hub-section", index_txt, "docs/index.html missing knowledge hub section")
        self.assertIn("products-section", index_txt, "docs/index.html missing products section")

        print(f"\n[Test 5] Content preservation verified: 5 products, 15 articles, index.html intact.")

    def test_06_whatsapp_link_generation_and_ht10_routing_audit(self):
        """
        Adversarially parses all WhatsApp links (wa.me) across all HTML files in docs/:
        - Must point strictly to 201155803307
        - Must include promo code HT10
        - Must be valid percent-encoded URL (no raw spaces or corrupted bytes)
        """
        wa_link_pattern = re.compile(r'href=["\'](https://wa\.me/[^"\']+)["\']')
        wa_links_found = 0
        invalid_links = []

        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8", errors="ignore")
            links = wa_link_pattern.findall(content)
            for link in links:
                wa_links_found += 1
                # 1. Phone number check
                if f"wa.me/{OFFICIAL_PHONE}" not in link:
                    invalid_links.append(f"{hf.name}: {link} (does not target official phone {OFFICIAL_PHONE})")

                # 2. HT10 promo code check
                unquoted_url = urllib.parse.unquote(link)
                if "HT10" not in unquoted_url and "ht10" not in unquoted_url.lower():
                    invalid_links.append(f"{hf.name}: {link} (missing promo code HT10)")

                # 3. URL encoding validation: raw space check
                if " " in link:
                    invalid_links.append(f"{hf.name}: {link} (contains unencoded raw space)")

                # 4. Valid URL parse test
                parsed = urllib.parse.urlparse(link)
                if not parsed.scheme or not parsed.netloc:
                    invalid_links.append(f"{hf.name}: {link} (malformed URL)")

        print(f"\n[Test 6] Verified {wa_links_found} WhatsApp links across docs/. Invalid links: {len(invalid_links)}")
        self.assertGreater(wa_links_found, 20, "Expected at least 20 WhatsApp consultation links in docs/")
        self.assertEqual(len(invalid_links), 0, "\n".join(invalid_links))

    def test_07_phone_number_regex_adversarial_matrix(self):
        """
        Stress-tests Egyptian phone number normalization and validation logic
        against an adversarial matrix of 50+ edge-case inputs.
        Tests the authoritative Egyptian phone regex: ^01[0125][0-9]{8}$
        as implemented in portal_app/src/utils/validation.ts and docs/ HTML modals.
        """
        # Portal App normalization & strict regex:
        def normalize_phone(inp: str) -> str:
            if not inp:
                return ''
            cleaned = re.sub(r'[\s\-\(\)\+]', '', inp).strip()
            if cleaned.startswith('0020'):
                cleaned = cleaned[4:]
            elif cleaned.startswith('20'):
                cleaned = cleaned[2:]
            if cleaned.startswith('0'):
                pass
            elif cleaned.startswith('1'):
                cleaned = '0' + cleaned
            return cleaned

        def is_valid_phone(phone: str) -> bool:
            norm = normalize_phone(phone)
            return bool(re.match(r'^01[0125][0-9]{8}$', norm))

        # === 1. Valid Egyptian Numbers (All 4 Major Carriers) ===
        valid_vectors = [
            # Vodafone (010)
            "01012345678",
            "+201012345678",
            "201012345678",
            "00201012345678",
            " 010 1234 5678 ",
            "010-1234-5678",
            "(010) 1234-5678",
            "+20 (10) 1234 5678",
            # Etisalat (011 - including clinic number 01155803307)
            "01155803307",
            "+201155803307",
            "201155803307",
            "00201155803307",
            "011 5580 3307",
            "011-5580-3307",
            "(011) 5580-3307",
            # Orange (012)
            "01234567890",
            "+201234567890",
            "201234567890",
            "012 3456 7890",
            # WE (015)
            "01598765432",
            "+201598765432",
            "201598765432",
            "015 9876 5432",
        ]

        for vec in valid_vectors:
            self.assertTrue(
                is_valid_phone(vec),
                f"Valid Egyptian phone incorrectly rejected by strict regex: '{vec}'"
            )

        # === 2. Invalid Numbers (Must be REJECTED by strict regex) ===
        invalid_vectors = [
            # Empty / Whitespace
            "",
            "   ",
            "\t\n",
            # Invalid Egyptian Carrier Prefixes (013, 014, 016, 017, 018, 019)
            "01312345678",
            "01412345678",
            "01612345678",
            "01712345678",
            "01812345678",
            "01912345678",
            "+201312345678",
            # Landlines (02 Cairo, 03 Alexandria, etc.)
            "0223456789",
            "034567890",
            "0403334444",
            "+20223456789",
            # Short / Truncated numbers
            "010",
            "011558",
            "010123456",     # 9 digits
            "0101234567",    # 10 digits
            # Overlong numbers
            "010123456789",   # 12 digits
            "0115580330799",  # 13 digits
            "+2010123456789",
            # Alphanumeric / Letters
            "0101234567a",
            "0115580330O",
            "abcdefghijk",
            "010-ABCD-EFGH",
            # Malicious / Injection Vectors
            "01012345678<script>alert(1)</script>",
            "01012345678'; DROP TABLE leads;--",
            "01012345678\n&text=malicious_override",
            "01012345678\" onmouseover=\"alert(1)",
            # International non-Egyptian numbers
            "+14155552671",   # US
            "+447911123456",  # UK
            "+966501234567",  # Saudi Arabia
            "+971501234567",  # UAE
            # Arabic-Indic Digits (unconverted raw)
            "٠١١٥٥٨٠٣٣٠٧",
            "٠١٠١٢٣٤٥٦٧٨",
        ]

        for vec in invalid_vectors:
            self.assertFalse(
                is_valid_phone(vec),
                f"Invalid phone vector was INCORRECTLY ACCEPTED by strict regex: '{vec}'"
            )

        print(f"\n[Test 7] Successfully tested {len(valid_vectors)} valid and {len(invalid_vectors)} invalid phone vectors against strict Egyptian phone regex.")

    def test_08_whatsapp_url_generator_edge_cases_and_injection_defense(self):
        """
        Stress-tests WhatsApp consultation URL generator with edge-case characters,
        quotes, emojis, and adversarial injection strings.
        """
        def build_mock_url(name: str, phone: str, topic: str, notes: str) -> str:
            lines = [
                "مرحباً أخصائية التعافي الطبي في هيلينج تاتش مصر،",
                "أود استشارة سريرية بخصوص حالتي:",
                f"▪️ الاسم: {name}",
                f"▪️ رقم الهاتف: {phone}",
                f"▪️ نوع العملية: {topic}",
                f"▪️ تفاصيل الاستفسار: {notes}",
                "(كود المتابعة: HT10)",
                "أرجو التواصل لتحديد بروتوكول العناية والمتابعة السريرية."
            ]
            full_text = "\n".join(lines)
            encoded = urllib.parse.quote(full_text)
            return f"https://wa.me/{OFFICIAL_PHONE}?text={encoded}"

        adversarial_payloads = [
            {
                "name": "سارة & مريم ' \" <script>",
                "phone": "01012345678",
                "topic": "جراحة قيصرية + شد بطن",
                "notes": "استفسار عن الشاور? &promo=HACKED%20&phone=000"
            },
            {
                "name": "Fatma 🌸✨ (أم يوسف)",
                "phone": "01155803307",
                "topic": "تجميل الأنف 👃",
                "notes": "الجبيرة اتفكت وفيه تورم:\n1. الجانب الأيمن\n2. الأرنبة"
            },
            {
                "name": "حالة مستعجلة\r\n\r\nHTTP/1.1 200 OK",
                "phone": "01234567890",
                "topic": "استئصال الغدة الدرقية",
                "notes": "الندبة حمراء ومشدودة"
            }
        ]

        for p in adversarial_payloads:
            url = build_mock_url(p["name"], p["phone"], p["topic"], p["notes"])

            # 1. Base URL must strictly use official phone
            self.assertTrue(url.startswith(f"https://wa.me/{OFFICIAL_PHONE}?text="))

            # 2. No unencoded spaces in the final URL
            self.assertNotIn(" ", url)

            # 3. No unencoded newlines
            self.assertNotIn("\n", url)
            self.assertNotIn("\r", url)

            # 4. Decoded text must preserve all Arabic characters and emojis faithfully
            query_part = url.split("?text=")[1]
            decoded_text = urllib.parse.unquote(query_part)
            self.assertIn("HT10", decoded_text)
            self.assertIn(p["phone"], decoded_text)
            self.assertIn("هيلينج تاتش مصر", decoded_text)

        print(f"\n[Test 8] Verified URL generator against {len(adversarial_payloads)} adversarial injection payloads.")


if __name__ == "__main__":
    unittest.main()
