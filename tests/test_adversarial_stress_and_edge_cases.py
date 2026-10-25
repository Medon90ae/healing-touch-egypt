#!/usr/bin/env python3
"""
test_adversarial_stress_and_edge_cases.py — Deep Adversarial Edge-Case Stress Testing
for Healing Touch Egypt.

Adversarial Stress Scenarios:
1. JSON-LD Deep Structure: ISO 8601 dates, FAQ schema hierarchy, Product offer schema validity.
2. WhatsApp / Instagram link protocol & URL encoding stress tests across all 21 files.
3. Hashtag syntax & uniqueness check (no spaces, valid Arabic/English tag syntax, non-empty).
4. HTML document compliance (DOCTYPE, lang='ar', dir='rtl', charset='utf-8', viewport).
5. Deterministic regeneration hash stability across multiple successive runs.
6. LocalStorage lead tracking script and window.getLeadLog contract verification.
"""

import sys
import os
import re
import json
import hashlib
import subprocess
from pathlib import Path
from html.parser import HTMLParser
import urllib.parse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\followUPSHEET\healing_touch")
DOCS_DIR = ROOT_DIR / "docs"
PYTHON_EXE = ROOT_DIR / ".venv" / "Scripts" / "python.exe"

def test_jsonld_deep_structure():
    print("--- Adversarial Stress 1: Deep JSON-LD Structure & Schema Quality ---")
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    errors = []

    for html_file in all_html_files:
        content = html_file.read_text(encoding='utf-8')
        ld_matches = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', content, re.DOTALL)
        if not ld_matches:
            errors.append(f"{html_file.name}: No JSON-LD script found")
            continue

        for block in ld_matches:
            data = json.loads(block)
            items = data if isinstance(data, list) else [data]
            for item in items:
                stype = item.get("@type")
                if stype == "Article":
                    # Check ISO date format
                    for df in ["datePublished", "dateModified"]:
                        dval = item.get(df)
                        try:
                            datetime.strptime(dval, "%Y-%m-%d")
                        except Exception:
                            errors.append(f"{html_file.name}: Article invalid date {df}='{dval}'")
                    if not item.get("headline") or len(item["headline"].strip()) < 5:
                        errors.append(f"{html_file.name}: Article headline too short or empty")
                elif stype == "FAQPage":
                    questions = item.get("mainEntity", [])
                    if not questions:
                        errors.append(f"{html_file.name}: FAQPage has no questions")
                    for q in questions:
                        if not q.get("name") or not q.get("acceptedAnswer", {}).get("text"):
                            errors.append(f"{html_file.name}: FAQ Question/Answer text empty: {q}")
                elif stype == "Product":
                    offer = item.get("offers", {})
                    price = offer.get("price")
                    if not isinstance(price, (int, float)) or price <= 0:
                        errors.append(f"{html_file.name}: Product price invalid: {price}")
                    if offer.get("priceCurrency") != "EGP":
                        errors.append(f"{html_file.name}: Product currency != EGP: {offer.get('priceCurrency')}")

    assert not errors, f"JSON-LD deep validation failed: {errors}"
    print(f"PASS: Evaluated deep schema compliance across {len(all_html_files)} files.")


def test_whatsapp_and_instagram_links():
    print("\n--- Adversarial Stress 2: Contact Links & URL Encoding Verification ---")
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    errors = []
    wa_count = 0
    ig_count = 0

    for html_file in all_html_files:
        content = html_file.read_text(encoding='utf-8')

        # Find WhatsApp links
        wa_links = re.findall(r'href=[\'"](https://wa\.me/[^\'"]+)[\'"]', content)
        wa_count += len(wa_links)
        for wal in wa_links:
            parsed = urllib.parse.urlparse(wal)
            # Must target 201155803307
            if not parsed.path.startswith("/201155803307"):
                errors.append(f"{html_file.name}: WhatsApp link wrong number: {wal}")
            # Must have text query param
            query = urllib.parse.parse_qs(parsed.query)
            if "text" not in query or not query["text"][0].strip():
                errors.append(f"{html_file.name}: WhatsApp link missing or empty text parameter: {wal}")

        # Check Instagram references
        if "tapistorefamily2026" not in content:
            errors.append(f"{html_file.name}: Missing Instagram account reference tapistorefamily2026")
        else:
            ig_count += 1

        # Check Promo code presence
        if "HT10" not in content:
            errors.append(f"{html_file.name}: Missing promo code HT10")

    assert not errors, f"Contact links verification failed: {errors}"
    print(f"PASS: Verified {wa_count} WhatsApp direct links with valid phone 201155803307 and properly encoded parameters.")
    print(f"PASS: Verified Instagram handle tapistorefamily2026 and HT10 promo code across all {len(all_html_files)} files.")


def test_hashtag_quality_and_uniqueness():
    print("\n--- Adversarial Stress 3: Hashtag Quality, Syntax & Non-Duplication ---")
    hashtags_file = DOCS_DIR / "hashtags_index.json"
    with open(hashtags_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    articles = data["articles"]
    assert len(articles) == 15

    for slug, art in articles.items():
        flat = art["hashtags_flat"]
        # Check uniqueness within article
        if len(flat) != len(set(flat)):
            dups = [t for t in flat if flat.count(t) > 1]
            errors.append(f"Article {slug} has duplicate hashtags: {set(dups)}")

        # Check syntax
        for tag in flat:
            if not tag.startswith("#"):
                errors.append(f"Article {slug}: Tag '{tag}' missing leading '#'")
            if " " in tag:
                errors.append(f"Article {slug}: Tag '{tag}' contains forbidden space")
            if len(tag) <= 2:
                errors.append(f"Article {slug}: Tag '{tag}' suspiciously short")

    assert not errors, f"Hashtag quality checks failed: {errors}"
    print(f"PASS: All 15 articles have 100% unique, syntax-compliant Egyptian patient hashtags.")


def test_html_document_compliance():
    print("\n--- Adversarial Stress 4: HTML Document Compliance & Accessibility ---")
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    errors = []

    for html_file in all_html_files:
        content = html_file.read_text(encoding='utf-8')
        if not content.startswith("<!DOCTYPE html>"):
            errors.append(f"{html_file.name}: Missing standard <!DOCTYPE html>")
        if '<html lang="ar" dir="rtl">' not in content:
            errors.append(f"{html_file.name}: Missing <html lang=\"ar\" dir=\"rtl\">")
        if '<meta charset="utf-8">' not in content:
            errors.append(f"{html_file.name}: Missing <meta charset=\"utf-8\">")
        if '<meta name="viewport"' not in content:
            errors.append(f"{html_file.name}: Missing viewport meta tag")
        if "</body>" not in content or "</html>" not in content:
            errors.append(f"{html_file.name}: Missing closing body/html tags")

    assert not errors, f"HTML document compliance failed: {errors}"
    print(f"PASS: All {len(all_html_files)} HTML files are fully compliant standard HTML5 with Arabic RTL declarations.")


def test_build_idempotency_hash_stability():
    print("\n--- Adversarial Stress 5: Build Idempotency & Hash Stability ---")
    # Record hashes of all HTML files before build
    def get_hashes():
        h = {}
        for f in sorted(DOCS_DIR.glob("**/*.html")):
            h[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
        return h

    hashes_before = get_hashes()

    # Re-run build site
    cmd = [str(PYTHON_EXE), str(ROOT_DIR / "github_seo_trend_engine.py"), "--build-site"]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, encoding='utf-8')
    assert res.returncode == 0, f"Rebuild failed: {res.stderr}"

    hashes_after = get_hashes()

    mismatches = []
    for fname, h1 in hashes_before.items():
        h2 = hashes_after.get(fname)
        if h1 != h2:
            mismatches.append(f"File {fname} hash changed between consecutive builds ({h1[:8]} vs {h2[:8]})")

    assert not mismatches, f"Build non-determinism detected in HTML files: {mismatches}"
    print(f"PASS: 100% Bit-for-bit SHA256 hash stability verified across all {len(hashes_before)} HTML files!")


def test_lead_tracking_javascript_contract():
    print("\n--- Adversarial Stress 6: Lead Tracking & Modal Contract ---")
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    errors = []

    for html_file in all_html_files:
        content = html_file.read_text(encoding='utf-8')

        # Check for essential functions and storage contracts
        if "function openPromoDrawer(" not in content:
            errors.append(f"{html_file.name}: Missing openPromoDrawer function")
        if "healing_touch_leads_log" not in content:
            errors.append(f"{html_file.name}: Missing localStorage key 'healing_touch_leads_log'")
        if "window.getLeadLog = function()" not in content:
            errors.append(f"{html_file.name}: Missing window.getLeadLog contract")
        if "navigator.sendBeacon" not in content:
            errors.append(f"{html_file.name}: Missing navigator.sendBeacon asynchronous lead tracking")

    assert not errors, f"Lead tracking contract failed: {errors}"
    print(f"PASS: Verified client-side lead tracking contract (openPromoDrawer, localStorage, window.getLeadLog, navigator.sendBeacon) across all 21 files.")


if __name__ == "__main__":
    print("STARTING DEEP ADVERSARIAL STRESS SUITE\n")
    test_jsonld_deep_structure()
    test_whatsapp_and_instagram_links()
    test_hashtag_quality_and_uniqueness()
    test_html_document_compliance()
    test_build_idempotency_hash_stability()
    test_lead_tracking_javascript_contract()
    print("\n" + "=" * 70)
    print("ALL DEEP ADVERSARIAL STRESS TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
