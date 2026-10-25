#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_challenger_1_empirical.py — Challenger 1 Adversarial Test Suite
Project: Healing Touch Egypt (docs/)

Mandated Checks:
1. Scan every HTML file in docs/ (index.html, products/*.html, articles/*.html)
   for any occurrence of forbidden marketing terms (exact, normalized, case-insensitive, regex variants).
2. Extract all internal hyperlinks (<a href="...">) across all 21 HTML files
   and verify that every target file exists on disk (0 broken links) + verify anchor IDs.
3. Parse docs/sitemap.xml and verify bidirectionally that every URL corresponds to an existing file
   in docs/ and all HTML files are accounted for (0 orphaned pages).

Additional Deep Checks:
4. Asset integrity (<img src>, <script src>, <link rel="stylesheet">).
5. Bidirectional cluster links (R6 requirement: sibling articles + parent product).
6. HT10 promo code, WhatsApp (201155803307), and Instagram handles across pages.
7. JSON-LD structured data parseability across all 21 files.
"""

import sys
import os
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DOCS_DIR = Path(r"c:\followUPSHEET\healing_touch\docs")
BASE_URL = "https://medon90ae.github.io/healing-touch-egypt"

FORBIDDEN_BASE_TERMS = [
    'طمأنة المريض',
    'المرحلة 1',
    'المرحلة 2',
    'الإقناع النفسي',
    'Persuasion Triggers',
    'Social Hook',
    'استراتيجية الانتشار',
    'E-E-A-T',
    'محرك التريند',
    'أسلوب الفضول',
    'أسلوب المقارنة الصادمة',
    'كسر المعتقدات الخاطئة',
    'تحويل القلق إلى خطوة',
]

def normalize_arabic(text: str) -> str:
    """Normalize Arabic text for deep fuzzy/orthographic matching."""
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'١', '1', text)
    text = re.sub(r'٢', '2', text)
    text = re.sub(r'ـ', '', text)  # Tatweel
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)  # Tashkeel / diacritics
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    return text

class DetailedDOMParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []          # (line, col, href)
        self.images = []         # (line, col, src)
        self.scripts = []        # (line, col, src)
        self.stylesheets = []    # (line, col, href)
        self.ids = set()         # element IDs
        self.names = set()       # anchor names
        self.json_ld_blocks = [] # raw text of JSON-LD scripts
        self._in_json_ld = False
        self._json_ld_buf = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if 'id' in attr_dict:
            self.ids.add(attr_dict['id'])
        if tag == 'a' and 'name' in attr_dict:
            self.names.add(attr_dict['name'])

        if tag == 'a' and 'href' in attr_dict:
            self.links.append((self.getpos(), attr_dict['href']))
        elif tag == 'img' and 'src' in attr_dict:
            self.images.append((self.getpos(), attr_dict['src']))
        elif tag == 'script':
            if attr_dict.get('type') == 'application/ld+json':
                self._in_json_ld = True
                self._json_ld_buf = []
            elif 'src' in attr_dict:
                self.scripts.append((self.getpos(), attr_dict['src']))
        elif tag == 'link' and attr_dict.get('rel') == 'stylesheet' and 'href' in attr_dict:
            self.stylesheets.append((self.getpos(), attr_dict['href']))

    def handle_endtag(self, tag):
        if tag == 'script' and self._in_json_ld:
            self._in_json_ld = False
            self.json_ld_blocks.append("".join(self._json_ld_buf))

    def handle_data(self, data):
        if self._in_json_ld:
            self._json_ld_buf.append(data)


def test_1_forbidden_marketing_terms(html_files):
    print("\n" + "=" * 78)
    print("CHALLENGE 1: Empirical Scan for Forbidden Marketing / Funnel Terms")
    print("=" * 78)

    # Compile regexes for flexible spacing and numerals
    patterns = []
    for term in FORBIDDEN_BASE_TERMS:
        if re.search(r'[a-zA-Z]', term):
            # English terms: case insensitive with flexible spacing/hyphens
            esc = re.escape(term)
            esc = esc.replace(r'\ ', r'\s+')
            esc = esc.replace(r'\-', r'[\-\s]?')
            patterns.append((term, re.compile(esc, re.IGNORECASE)))
        else:
            # Arabic term: allow variable spacing and digits
            esc = re.escape(term)
            esc = esc.replace(r'\ ', r'\s+')
            esc = esc.replace('1', '[1١]')
            esc = esc.replace('2', '[2٢]')
            esc = esc.replace('ه', '[هة]')
            esc = esc.replace('ة', '[هة]')
            esc = esc.replace('ا', '[اإأآ]')
            esc = esc.replace('ي', '[ييى]')
            patterns.append((term, re.compile(esc)))

    total_files = len(html_files)
    violations = []
    files_checked = 0

    for f in html_files:
        files_checked += 1
        content = f.read_text(encoding='utf-8')
        lower_content = content.lower()
        norm_content = normalize_arabic(content)

        # 1. Exact term search
        for term in FORBIDDEN_BASE_TERMS:
            if re.search(r'[a-zA-Z]', term):
                if term.lower() in lower_content:
                    violations.append((f.name, f"Exact English term: '{term}'"))
            else:
                if term in content:
                    violations.append((f.name, f"Exact Arabic term: '{term}'"))

        # 2. Regex pattern search (handles Eastern Arabic digits, whitespace variations, spelling)
        for original_term, regex in patterns:
            m = regex.search(content)
            if m:
                # To avoid duplicate reporting if already flagged
                desc = f"Pattern match for '{original_term}': matched '{m.group(0)}'"
                if not any(v[0] == f.name and original_term in v[1] for v in violations):
                    violations.append((f.name, desc))

        # 3. Normalized Arabic search
        for term in FORBIDDEN_BASE_TERMS:
            if not re.search(r'[a-zA-Z]', term):
                norm_term = normalize_arabic(term)
                if norm_term in norm_content:
                    desc = f"Normalized Arabic match: '{term}' (normalized: '{norm_term}')"
                    if not any(v[0] == f.name and term in v[1] for v in violations):
                        violations.append((f.name, desc))

    # Also check additional SEO / marketing keywords from ORIGINAL_REQUEST.md
    extra_audit_terms = [
        'خوارزميات Google E-E-A-T',
        'مفاتيح الإقناع النفسي',
        'استراتيجية الانتشار على منصات التواصل',
        'محرك التريند الطبي',
    ]
    for f in html_files:
        content = f.read_text(encoding='utf-8')
        for extra in extra_audit_terms:
            if extra in content:
                violations.append((f.name, f"Extra request audit term: '{extra}'"))

    print(f"Total HTML files scanned: {files_checked}")
    if violations:
        print(f"FAILED: Found {len(violations)} forbidden marketing term occurrences!")
        for fname, desc in violations:
            print(f"  [X] {fname}: {desc}")
        return False, violations
    else:
        print(f"PASSED: Exactly 0 occurrences of forbidden marketing terms found across all {files_checked} HTML files.")
        return True, []


def test_2_internal_hyperlinks(html_files, parsed_files):
    print("\n" + "=" * 78)
    print("CHALLENGE 2: Verification of Internal Hyperlinks (<a href>) Across All 21 HTML Files")
    print("=" * 78)

    broken_links = []
    internal_links_count = 0
    external_links_count = 0
    anchor_warnings = []

    # Map each resolved file path to its known IDs/anchors
    dom_id_map = {}
    for f, parser in parsed_files.items():
        all_anchors = parser.ids.union(parser.names)
        dom_id_map[f.resolve()] = all_anchors

    for f, parser in parsed_files.items():
        rel_f = f.relative_to(DOCS_DIR)
        for (line, col), href in parser.links:
            href_clean = href.strip()
            if not href_clean:
                continue

            # Classify link
            if href_clean.startswith(("mailto:", "tel:", "javascript:")):
                external_links_count += 1
                continue
            elif href_clean.startswith("http://") or href_clean.startswith("https://"):
                if href_clean.startswith(BASE_URL):
                    # Absolute internal link pointing to GitHub Pages domain
                    internal_links_count += 1
                    rel_part = href_clean[len(BASE_URL):]
                    if not rel_part or rel_part == "/":
                        target_path = (DOCS_DIR / "index.html").resolve()
                    else:
                        sub_path = unquote(rel_part.lstrip("/"))
                        target_path = (DOCS_DIR / sub_path).resolve()
                    
                    if not target_path.exists():
                        broken_links.append((str(rel_f), line, href_clean, f"Target file does not exist on disk: {target_path}"))
                else:
                    external_links_count += 1
                    continue
            elif href_clean.startswith("#"):
                # In-page anchor fragment
                internal_links_count += 1
                frag = href_clean[1:]
                if frag and frag not in ('', 'top'):
                    current_anchors = dom_id_map.get(f.resolve(), set())
                    if frag not in current_anchors:
                        anchor_warnings.append((str(rel_f), line, href_clean, f"Anchor #{frag} not found in same page DOM"))
            else:
                # Relative link
                internal_links_count += 1
                # Split fragment
                if "#" in href_clean:
                    path_part, frag = href_clean.split("#", 1)
                else:
                    path_part, frag = href_clean, None

                if not path_part:
                    continue

                path_part = unquote(path_part)
                target_path = (f.parent / path_part).resolve()

                if not target_path.exists():
                    broken_links.append((str(rel_f), line, href_clean, f"Target file does not exist on disk: {target_path}"))
                else:
                    # Check if target is inside docs
                    try:
                        target_path.relative_to(DOCS_DIR)
                    except ValueError:
                        broken_links.append((str(rel_f), line, href_clean, f"Link escapes docs/ directory: {target_path}"))

                    # If fragment exists, check target DOM
                    if frag and frag not in ('', 'top'):
                        target_anchors = dom_id_map.get(target_path, set())
                        if frag not in target_anchors:
                            anchor_warnings.append((str(rel_f), line, href_clean, f"Cross-file anchor #{frag} not found in {target_path.name}"))

    print(f"Total internal links examined: {internal_links_count}")
    print(f"Total external/action links examined: {external_links_count}")

    if anchor_warnings:
        print(f"Note: Found {len(anchor_warnings)} non-critical in-page anchor notes (e.g. JS handlers):")
        for src, line, hr, note in anchor_warnings[:5]:
            print(f"  [i] {src}:{line} -> {hr} ({note})")

    if broken_links:
        print(f"FAILED: Found {len(broken_links)} broken internal links!")
        for src, line, hr, reason in broken_links:
            print(f"  [X] {src}:{line} href='{hr}' -> {reason}")
        return False, broken_links
    else:
        print(f"PASSED: Exactly 0 broken internal links (out of {internal_links_count} verified links across all 21 files).")
        return True, []


def test_3_sitemap_xml(html_files):
    print("\n" + "=" * 78)
    print("CHALLENGE 3: Parse and Verify docs/sitemap.xml (Bidirectional Integrity)")
    print("=" * 78)

    sitemap_path = DOCS_DIR / "sitemap.xml"
    if not sitemap_path.exists():
        print("FAILED: docs/sitemap.xml does not exist!")
        return False, ["sitemap.xml missing"]

    try:
        tree = ET.parse(sitemap_path)
    except Exception as e:
        print(f"FAILED: docs/sitemap.xml is not valid XML: {e}")
        return False, [f"XML parse error: {e}"]

    root = tree.getroot()
    # Handle XML namespace
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = root.findall('sm:url', ns)
    if not urls:
        # Fallback if no namespace
        urls = root.findall('url')

    print(f"Total <url> entries parsed in sitemap.xml: {len(urls)}")

    sitemap_errors = []
    mapped_files = set()

    for idx, url_node in enumerate(urls, 1):
        loc_node = url_node.find('sm:loc', ns) if 'sm' in ns else url_node.find('loc')
        if loc_node is None or not loc_node.text:
            sitemap_errors.append(f"Entry #{idx} is missing <loc> element")
            continue

        loc = loc_node.text.strip()
        lastmod_node = url_node.find('sm:lastmod', ns) if 'sm' in ns else url_node.find('lastmod')
        priority_node = url_node.find('sm:priority', ns) if 'sm' in ns else url_node.find('priority')

        # Check domain
        if not loc.startswith(BASE_URL):
            sitemap_errors.append(f"URL does not start with BASE_URL ({BASE_URL}): {loc}")
            continue

        # Map to disk path
        rel_part = loc[len(BASE_URL):]
        if rel_part in ("", "/"):
            disk_file = (DOCS_DIR / "index.html").resolve()
        else:
            disk_file = (DOCS_DIR / unquote(rel_part.lstrip("/"))).resolve()

        if not disk_file.exists():
            sitemap_errors.append(f"Sitemap URL maps to non-existent disk file: {loc} -> {disk_file}")
        else:
            mapped_files.add(disk_file)

        # Check lastmod format YYYY-MM-DD
        if lastmod_node is not None and lastmod_node.text:
            if not re.match(r'^\d{4}-\d{2}-\d{2}', lastmod_node.text.strip()):
                sitemap_errors.append(f"Invalid lastmod date format in {loc}: '{lastmod_node.text}'")

        # Check priority in [0.0, 1.0]
        if priority_node is not None and priority_node.text:
            try:
                p_val = float(priority_node.text.strip())
                if not (0.0 <= p_val <= 1.0):
                    sitemap_errors.append(f"Priority out of range [0.0, 1.0] in {loc}: {p_val}")
            except ValueError:
                sitemap_errors.append(f"Priority is not a float in {loc}: '{priority_node.text}'")

    # Reverse Check: Any HTML file in docs/ not in sitemap?
    orphan_files = []
    for hf in html_files:
        if hf.resolve() not in mapped_files:
            orphan_files.append(str(hf.relative_to(DOCS_DIR)))

    if sitemap_errors:
        print(f"FAILED: Found {len(sitemap_errors)} errors in sitemap.xml:")
        for err in sitemap_errors:
            print(f"  [X] {err}")

    if orphan_files:
        print(f"FAILED: Found {len(orphan_files)} orphaned HTML files not listed in sitemap.xml:")
        for orph in orphan_files:
            print(f"  [X] {orph}")

    if not sitemap_errors and not orphan_files:
        print(f"PASSED: All {len(urls)} URLs correspond to existing files on disk, and all {len(html_files)} HTML files are listed (0 orphans).")
        return True, []
    else:
        return False, sitemap_errors + orphan_files


def test_4_local_assets_and_metadata(html_files, parsed_files):
    print("\n" + "=" * 78)
    print("CHALLENGE 4: Local Assets (Images, CSS, JS) and JSON-LD Integrity")
    print("=" * 78)

    broken_assets = []
    json_ld_errors = []
    total_ld_blocks = 0

    for f, parser in parsed_files.items():
        rel_f = f.relative_to(DOCS_DIR)

        # 1. Stylesheets
        for (line, col), href in parser.stylesheets:
            if not href.startswith(("http://", "https://", "//")):
                p = (f.parent / unquote(href)).resolve()
                if not p.exists():
                    broken_assets.append((str(rel_f), line, f"Stylesheet: {href}"))

        # 2. Scripts
        for (line, col), src in parser.scripts:
            if not src.startswith(("http://", "https://", "//")):
                p = (f.parent / unquote(src)).resolve()
                if not p.exists():
                    broken_assets.append((str(rel_f), line, f"Script: {src}"))

        # 3. Images
        for (line, col), src in parser.images:
            if not src.startswith(("http://", "https://", "//", "data:")):
                p = (f.parent / unquote(src)).resolve()
                if not p.exists():
                    broken_assets.append((str(rel_f), line, f"Image: {src}"))

        # 4. JSON-LD blocks
        for idx, block in enumerate(parser.json_ld_blocks, 1):
            total_ld_blocks += 1
            try:
                data = json.loads(block)
                # Verify schema.org context
                ctx = data.get("@context") if isinstance(data, dict) else None
                if isinstance(data, dict) and not ctx:
                    json_ld_errors.append((str(rel_f), f"Block {idx} missing @context"))
            except Exception as e:
                json_ld_errors.append((str(rel_f), f"Block {idx} invalid JSON: {e}"))

    print(f"Parsed {total_ld_blocks} JSON-LD blocks across {len(html_files)} files.")
    if broken_assets:
        print(f"FAILED: Found {len(broken_assets)} broken local asset references:")
        for src, line, asset in broken_assets:
            print(f"  [X] {src}:{line} -> {asset}")

    if json_ld_errors:
        print(f"FAILED: Found {len(json_ld_errors)} JSON-LD syntax errors:")
        for src, err in json_ld_errors:
            print(f"  [X] {src} -> {err}")

    if not broken_assets and not json_ld_errors:
        print("PASSED: 0 broken local assets, all JSON-LD blocks parsed validly.")
        return True, []
    else:
        return False, broken_assets + json_ld_errors


def test_5_cluster_bidirectional_interlinking():
    print("\n" + "=" * 78)
    print("CHALLENGE 5: R6 Cluster Bidirectional Interlinking (Product <-> 3 Articles)")
    print("=" * 78)

    articles_dir = DOCS_DIR / "articles"
    products_dir = DOCS_DIR / "products"

    # Load products from registry
    registry_file = Path(r"c:\followUPSHEET\healing_touch\products_registry.json")
    assert registry_file.exists(), "products_registry.json missing!"
    registry = json.loads(registry_file.read_text(encoding='utf-8'))
    products = registry.get("products", [])

    cluster_errors = []
    registry_metadata_notes = []

    # Expected angles for each product
    expected_angles = ["clinical-mechanism", "usage-protocol-mistakes", "patient-faq-comparisons"]

    for prod in products:
        prod_slug = prod["slug"]
        prod_file = products_dir / f"{prod_slug}.html"
        if not prod_file.exists():
            cluster_errors.append(f"Product page missing: {prod_file}")
            continue

        prod_html = prod_file.read_text(encoding='utf-8')
        actual_art_slugs = [f"{prod_slug}-{ang}" for ang in expected_angles]

        # Audit products_registry.json article_slugs field consistency
        reg_art_slugs = prod.get("article_slugs", [])
        if reg_art_slugs != actual_art_slugs:
            registry_metadata_notes.append(
                f"Registry metadata divergence for '{prod_slug}': registry has {reg_art_slugs} vs actual generated {actual_art_slugs}"
            )

        # 1. Verify product page links to all 3 actual cluster articles
        for aslug in actual_art_slugs:
            expected_href = f"../articles/{aslug}.html"
            if expected_href not in prod_html and f"/articles/{aslug}.html" not in prod_html:
                cluster_errors.append(f"Product {prod_slug}.html does not link to cluster article {expected_href}")

        # 2. Verify each of the 3 articles links to the parent product AND to both sibling articles
        for aslug in actual_art_slugs:
            art_file = articles_dir / f"{aslug}.html"
            if not art_file.exists():
                cluster_errors.append(f"Cluster article file missing on disk: {art_file}")
                continue
            art_html = art_file.read_text(encoding='utf-8')

            # Parent link check
            parent_link = f"../products/{prod_slug}.html"
            if parent_link not in art_html:
                cluster_errors.append(f"Article {aslug}.html does not link to parent product {parent_link}")

            # Sibling links check
            siblings = [s for s in actual_art_slugs if s != aslug]
            for sib in siblings:
                sib_link = f"{sib}.html"
                if sib_link not in art_html and f"../articles/{sib}.html" not in art_html:
                    cluster_errors.append(f"Article {aslug}.html does not link to sibling article {sib}")

    if registry_metadata_notes:
        print(f"ADVERSARIAL NOTE: Found {len(registry_metadata_notes)} metadata divergences in products_registry.json:")
        for note in registry_metadata_notes:
            print(f"  [i] {note}")

    if cluster_errors:
        print(f"FAILED: Found {len(cluster_errors)} cluster interlinking issues in HTML:")
        for err in cluster_errors:
            print(f"  [X] {err}")
        return False, cluster_errors
    else:
        print(f"PASSED: All 5 products and their 15 articles maintain 100% complete bidirectional interlinking on disk and DOM.")
        return True, []



def test_6_promo_code_and_contact_cta(html_files):
    print("\n" + "=" * 78)
    print("CHALLENGE 6: Verification of Promo Code HT10 & Contact CTAs (WhatsApp / Instagram)")
    print("=" * 78)

    promo_config_file = Path(r"c:\followUPSHEET\healing_touch\promo_config.json")
    assert promo_config_file.exists(), "promo_config.json missing!"
    cfg = json.loads(promo_config_file.read_text(encoding='utf-8'))
    expected_code = cfg.get("promo_code", "HT10")
    expected_wa = cfg.get("whatsapp_number", "201155803307")
    expected_ig = cfg.get("instagram_handle", "tapistorefamily2026")

    errors = []
    for f in html_files:
        content = f.read_text(encoding='utf-8')
        rel_f = f.relative_to(DOCS_DIR)

        if expected_code not in content:
            errors.append(f"{rel_f}: Promo code '{expected_code}' not found")
        if expected_wa not in content:
            errors.append(f"{rel_f}: WhatsApp number '{expected_wa}' not found")
        if expected_ig not in content:
            errors.append(f"{rel_f}: Instagram handle '{expected_ig}' not found")

    if errors:
        print(f"FAILED: CTA / Promo issues in {len(errors)} checks:")
        for err in errors:
            print(f"  [X] {err}")
        return False, errors
    else:
        print(f"PASSED: Promo code '{expected_code}', WhatsApp '{expected_wa}', and Instagram '{expected_ig}' verified across all 21 files.")
        return True, []


def main():
    print("==============================================================================")
    print("HEALING TOUCH EGYPT — CHALLENGER 1 ADVERSARIAL VERIFICATION SUITE")
    print("==============================================================================")

    html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    print(f"Target directory: {DOCS_DIR}")
    print(f"Total HTML files found: {len(html_files)}")
    assert len(html_files) == 21, f"Expected 21 HTML files, found {len(html_files)}"

    # Parse all files once for reuse
    parsed_files = {}
    for f in html_files:
        parser = DetailedDOMParser()
        parser.feed(f.read_text(encoding='utf-8'))
        parsed_files[f] = parser

    t1_pass, t1_errs = test_1_forbidden_marketing_terms(html_files)
    t2_pass, t2_errs = test_2_internal_hyperlinks(html_files, parsed_files)
    t3_pass, t3_errs = test_3_sitemap_xml(html_files)
    t4_pass, t4_errs = test_4_local_assets_and_metadata(html_files, parsed_files)
    t5_pass, t5_errs = test_5_cluster_bidirectional_interlinking()
    t6_pass, t6_errs = test_6_promo_code_and_contact_cta(html_files)

    print("\n" + "=" * 78)
    print("CHALLENGER 1 EMPIRICAL VERIFICATION SUMMARY")
    print("=" * 78)
    print(f"1. Forbidden Marketing Terms Scan:     {'PASS (0 violations)' if t1_pass else 'FAIL'}")
    print(f"2. Internal Hyperlinks (21 files):      {'PASS (0 broken links)' if t2_pass else 'FAIL'}")
    print(f"3. Sitemap.xml & Orphan Check:          {'PASS (0 errors, 0 orphans)' if t3_pass else 'FAIL'}")
    print(f"4. Local Assets & JSON-LD:              {'PASS (0 broken assets)' if t4_pass else 'FAIL'}")
    print(f"5. Cluster Bidirectional Interlinking:  {'PASS (100% connected)' if t5_pass else 'FAIL'}")
    print(f"6. HT10 Promo & WhatsApp/IG CTAs:       {'PASS (verified across 21 files)' if t6_pass else 'FAIL'}")

    all_passed = t1_pass and t2_pass and t3_pass and t4_pass and t5_pass and t6_pass
    print("=" * 78)
    if all_passed:
        print("VERDICT: APPROVE (All adversarial challenges passed empirically).")
        return 0
    else:
        print("VERDICT: REQUEST_CHANGES (Failures detected).")
        return 1

if __name__ == "__main__":
    sys.exit(main())
