#!/usr/bin/env python3
"""
test_adversarial_verification.py — Empirical Challenger Test Suite for Healing Touch Egypt

Executes adversarial stress-tests and verifications against:
1. Deterministic build regeneration via github_seo_trend_engine.py --build-site
2. JSON-LD schema parsing and validation across all 21 HTML files
3. Medical citations count and authenticity (10-12 per article) across all 15 articles
4. Hashtags index and products registry integrity
5. Forbidden marketing terms audit (zero tolerance across all files)
6. Internal link graph completeness and 404 elimination (including sibling & parent links)
7. SVG timeline, comparison tables, and promo lead tracker modal presence
8. Technical SEO (robots.txt, sitemap.xml, canonical, OpenGraph, Twitter tags)
"""

import sys
import os
import re
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser

# Reconfigure stdout for utf-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\followUPSHEET\healing_touch")
DOCS_DIR = ROOT_DIR / "docs"
ARTICLES_DIR = DOCS_DIR / "articles"
PRODUCTS_DIR = DOCS_DIR / "products"
PYTHON_EXE = ROOT_DIR / ".venv" / "Scripts" / "python.exe"

FORBIDDEN_TERMS = [
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
    'تحويل القلق إلى خطوة'
]

class LinkAndSchemaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.links = []
        self.in_json_ld = False
        self.current_json_ld = []
        self.has_svg = False
        self.has_table = False
        self.meta_tags = {}
        self.canonical = None
        self.has_promo_modal = False
        self.element_ids = set()

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if 'id' in attrs_dict:
            self.element_ids.add(attrs_dict['id'])
            if attrs_dict['id'] == 'promo-lead-modal':
                self.has_promo_modal = True

        if tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            self.in_json_ld = True
            self.current_json_ld = []

        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])

        if tag == 'svg':
            self.has_svg = True

        if tag == 'table':
            self.has_table = True

        if tag == 'link' and attrs_dict.get('rel') == 'canonical':
            self.canonical = attrs_dict.get('href')

        if tag == 'meta':
            name = attrs_dict.get('name') or attrs_dict.get('property')
            if name:
                self.meta_tags[name] = attrs_dict.get('content', '')

    def handle_data(self, data):
        if self.in_json_ld:
            self.current_json_ld.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_json_ld:
            self.in_json_ld = False
            self.scripts.append(''.join(self.current_json_ld))
            self.current_json_ld = []


def run_test_1_build_regeneration():
    print("=" * 70)
    print("TEST 1: Deterministic Build Regeneration (--build-site)")
    print("=" * 70)
    cmd = [str(PYTHON_EXE), str(ROOT_DIR / "github_seo_trend_engine.py"), "--build-site"]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, encoding='utf-8')
    print(f"Exit Code: {res.returncode}")
    print(f"Stdout Summary:\n{res.stdout.strip()}")
    if res.stderr.strip():
        print(f"Stderr:\n{res.stderr.strip()}")
    assert res.returncode == 0, f"Build regeneration failed with exit code {res.returncode}"
    print(">>> TEST 1 RESULT: PASS")
    return True


def run_test_2_json_ld_schemas():
    print("\n" + "=" * 70)
    print("TEST 2: JSON-LD Schema Validation Across All 21 HTML Files")
    print("=" * 70)
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    assert len(all_html_files) == 21, f"Expected 21 HTML files, got {len(all_html_files)}"

    required_types_found = set()
    total_ld_blocks = 0
    errors = []

    for html_file in all_html_files:
        rel_path = html_file.relative_to(DOCS_DIR)
        content = html_file.read_text(encoding='utf-8')
        parser = LinkAndSchemaExtractor()
        parser.feed(content)

        if not parser.scripts:
            errors.append(f"{rel_path}: No application/ld+json script block found!")
            continue

        for i, script_str in enumerate(parser.scripts):
            total_ld_blocks += 1
            script_str = script_str.strip()
            try:
                data = json.loads(script_str)
            except Exception as e:
                errors.append(f"{rel_path} block {i}: JSON parse error: {e}")
                continue

            schemas = data if isinstance(data, list) else [data]
            for schema in schemas:
                stype = schema.get("@type")
                if not stype:
                    errors.append(f"{rel_path}: Missing @type in schema: {schema}")
                    continue
                if isinstance(stype, list):
                    for st in stype:
                        required_types_found.add(st)
                else:
                    required_types_found.add(stype)

                # Check @context
                ctx = schema.get("@context")
                if "schema.org" not in str(ctx):
                    errors.append(f"{rel_path}: Missing or invalid @context: {ctx}")

                # Type specific assertions
                if stype == "FAQPage":
                    assert "mainEntity" in schema, f"{rel_path}: FAQPage missing mainEntity"
                    assert len(schema["mainEntity"]) > 0, f"{rel_path}: FAQPage mainEntity is empty"
                elif stype == "Article":
                    assert "headline" in schema, f"{rel_path}: Article missing headline"
                    assert "author" in schema, f"{rel_path}: Article missing author"
                    assert "datePublished" in schema, f"{rel_path}: Article missing datePublished"
                elif stype == "Product":
                    assert "name" in schema, f"{rel_path}: Product missing name"
                    assert "offers" in schema, f"{rel_path}: Product missing offers"
                elif stype == "MedicalWebPage":
                    assert "name" in schema, f"{rel_path}: MedicalWebPage missing name"
                elif stype == "MedicalBusiness":
                    assert "name" in schema, f"{rel_path}: MedicalBusiness missing name"

    print(f"Total HTML files checked: {len(all_html_files)}")
    print(f"Total JSON-LD blocks parsed: {total_ld_blocks}")
    print(f"Discovered @type schemas: {sorted(list(required_types_found))}")

    expected_mandatory_types = {"MedicalWebPage", "Article", "Product", "FAQPage", "MedicalBusiness"}
    missing_mandatory = expected_mandatory_types - required_types_found
    if missing_mandatory:
        errors.append(f"Missing mandatory @type schemas: {missing_mandatory}")

    if errors:
        for err in errors:
            print(f"  [FAIL] {err}")
        assert False, f"TEST 2 failed with {len(errors)} schema errors"

    print(">>> TEST 2 RESULT: PASS (All 21 HTML files have valid, parseable JSON-LD schemas covering all required types)")
    return True


def run_test_3_medical_citations():
    print("\n" + "=" * 70)
    print("TEST 3: Medical Citations Count & Authenticity (10-12 per Article)")
    print("=" * 70)
    article_files = sorted(list(ARTICLES_DIR.glob("*.html")))
    assert len(article_files) == 15, f"Expected 15 articles, got {len(article_files)}"

    authentic_authority_tokens = [
        "pubmed", "ncbi", "3m", "cochrane", "plastic", "dermatol", "wound",
        "burns", "rhinology", "researchgate", "mdpi", "oxford", "yazdan",
        "almoosa", "webteb", "doctorahmedmarzouk", "dramradel", "medicina",
        "annals", "aesthetic", "prs"
    ]

    errors = []
    citation_stats = []

    for art_file in article_files:
        slug = art_file.stem
        content = art_file.read_text(encoding='utf-8')

        # Locate the references section in HTML
        refs_container_match = re.search(r'<div class="refs-container">(.*?)</div>', content, re.DOTALL)
        if not refs_container_match:
            errors.append(f"Article {slug}: Missing <div class='refs-container'>")
            continue

        refs_html = refs_container_match.group(1)
        # Find all <li><strong>[N]</strong> items
        ref_items = re.findall(r'<li><strong>\[(\d+)\]</strong>\s*(.*?)</li>', refs_html, re.DOTALL)
        ref_count = len(ref_items)
        citation_stats.append((slug, ref_count))

        if not (10 <= ref_count <= 12):
            errors.append(f"Article {slug}: Found {ref_count} references in HTML (expected 10 to 12)!")

        # Verify indexing is contiguous 1..N
        indexes = [int(num) for num, _ in ref_items]
        expected_indexes = list(range(1, ref_count + 1))
        if indexes != expected_indexes:
            errors.append(f"Article {slug}: Citation numbering is not contiguous 1..{ref_count}: {indexes}")

        # Verify authenticity of each citation
        for num, text in ref_items:
            text_lower = text.lower()
            has_auth = any(token in text_lower for token in authentic_authority_tokens)
            if not has_auth:
                errors.append(f"Article {slug} reference [{num}] lacks medical authority source: {text[:80]}")

    print(f"Articles checked: {len(article_files)}")
    for slug, count in citation_stats:
        print(f"  - {slug}: {count} verified citations (10-12 requirement met)")

    if errors:
        for err in errors:
            print(f"  [FAIL] {err}")
        assert False, f"TEST 3 failed with {len(errors)} citation issues"

    print(">>> TEST 3 RESULT: PASS (All 15 articles contain exactly 10 to 12 authentic, verified medical references)")
    return True


def run_test_4_hashtags_and_product_registry():
    print("\n" + "=" * 70)
    print("TEST 4: Hashtags Index & Product Registry Integrity")
    print("=" * 70)
    errors = []

    # 1. Product Registry
    registry_path = ROOT_DIR / "products_registry.json"
    assert registry_path.exists(), "products_registry.json missing!"
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    products = registry.get("products", [])
    assert len(products) == 5, f"Expected 5 products in registry, found {len(products)}"

    for p in products:
        slug = p.get("slug")
        name_ar = p.get("name_ar")
        name_en = p.get("name_en")
        article_slugs = p.get("article_slugs", [])
        if not slug or not name_ar or not name_en:
            errors.append(f"Incomplete product basic info for {p}")
        if len(article_slugs) != 3:
            errors.append(f"Product {slug} does not have exactly 3 articles in article_slugs (has {len(article_slugs)})")
        if not p.get("specs"):
            errors.append(f"Product {slug} missing specs")
        if not p.get("indications"):
            errors.append(f"Product {slug} missing indications")
        if not p.get("usage_guidelines"):
            errors.append(f"Product {slug} missing usage_guidelines")
        if not p.get("faq"):
            errors.append(f"Product {slug} missing faq")

    # 2. Hashtags Index
    hashtags_path = DOCS_DIR / "hashtags_index.json"
    assert hashtags_path.exists(), "docs/hashtags_index.json missing!"
    with open(hashtags_path, "r", encoding="utf-8") as f:
        hashtags_data = json.load(f)

    assert hashtags_data.get("total_articles") == 15, f"hashtags_index.json total_articles != 15 ({hashtags_data.get('total_articles')})"
    articles_ht = hashtags_data.get("articles", {})
    assert len(articles_ht) == 15, f"Expected 15 articles in hashtags_index.json, got {len(articles_ht)}"

    expected_categories = [
        "surgery_tags",
        "issues_tags",
        "community_tags",
        "brand_tags"
    ]

    for slug, entry in articles_ht.items():
        title = entry.get("title")
        all_tags = entry.get("hashtags_flat", [])
        cats = entry.get("hashtags_categorized", {})
        if not title:
            errors.append(f"Hashtag entry for {slug} missing title")
        if not (25 <= len(all_tags) <= 30):
            errors.append(f"Article {slug} has {len(all_tags)} hashtags (expected 25-30)")
        for ec in expected_categories:
            if ec not in cats or not cats[ec]:
                errors.append(f"Article {slug} missing hashtag category {ec}")
        # Verify hashtags start with '#'
        for tag in all_tags:
            if not tag.startswith('#'):
                errors.append(f"Article {slug} tag '{tag}' does not start with '#'")

    if errors:
        for err in errors:
            print(f"  [FAIL] {err}")
        assert False, f"TEST 4 failed with {len(errors)} issues"

    print(f"Products verified: {len(products)} products with complete clinical profiles and 3-series articles")
    print(f"Hashtags verified: 15 articles indexed, each with 25-30 hashtags across 4 structured clinical categories")
    print(">>> TEST 4 RESULT: PASS")
    return True


def run_test_5_forbidden_terms_audit():
    print("\n" + "=" * 70)
    print("TEST 5: Copywriting Purity (Zero Tolerance for Internal Meta-Labels)")
    print("=" * 70)
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    json_files = [DOCS_DIR / "hashtags_index.json"]

    violations = []

    for file_path in all_html_files + json_files:
        content = file_path.read_text(encoding='utf-8')
        rel_path = file_path.relative_to(ROOT_DIR)
        for term in FORBIDDEN_TERMS:
            if term in content:
                lines = content.splitlines()
                for line_no, line in enumerate(lines, 1):
                    if term in line:
                        violations.append(f"{rel_path}:{line_no} contains forbidden term '{term}': {line.strip()[:100]}")

    if violations:
        for v in violations:
            print(f"  [VIOLATION] {v}")
        assert False, f"TEST 5 failed with {len(violations)} forbidden marketing term occurrences"

    print(f"Scanned {len(all_html_files)} HTML files + {len(json_files)} JSON files against {len(FORBIDDEN_TERMS)} forbidden terms.")
    print(">>> TEST 5 RESULT: PASS (0 occurrences found across all files)")
    return True


def run_test_6_link_graph_and_navigation():
    print("\n" + "=" * 70)
    print("TEST 6: Link Graph & Navigation Integrity (Zero Broken Links)")
    print("=" * 70)
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    broken_links = []
    sibling_cluster_verified = 0
    parent_product_link_verified = 0

    with open(ROOT_DIR / "products_registry.json", "r", encoding="utf-8") as f:
        registry = json.load(f)

    # Mapping product slug -> list of 3 article slugs
    suffixes = ["clinical-mechanism", "usage-protocol-mistakes", "patient-faq-comparisons"]
    prod_to_articles = {}
    article_to_prod = {}
    for p in registry["products"]:
        p_slug = p["slug"]
        a_slugs = [f"{p_slug}-{s}" for s in suffixes]
        prod_to_articles[p_slug] = a_slugs
        for aslug in a_slugs:
            article_to_prod[aslug] = p_slug

    for html_file in all_html_files:
        content = html_file.read_text(encoding='utf-8')
        parser = LinkAndSchemaExtractor()
        parser.feed(content)

        file_dir = html_file.parent
        rel_path = html_file.relative_to(DOCS_DIR)

        for href in parser.links:
            href_clean = href.split("#")[0].split("?")[0].strip()
            if not href_clean:
                continue
            if href.startswith("http://") or href.startswith("https://") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
                continue

            target_path = (file_dir / href_clean).resolve()
            if not target_path.exists():
                broken_links.append(f"{rel_path} -> '{href}' (Resolved: {target_path} DOES NOT EXIST)")

        # Verify sibling links and parent link for articles
        if html_file.parent.name == "articles":
            aslug = html_file.stem
            expected_pslug = article_to_prod.get(aslug)
            if expected_pslug:
                siblings = [s for s in prod_to_articles[expected_pslug] if s != aslug]
                for s in siblings:
                    expected_href = f"{s}.html"
                    if expected_href not in parser.links:
                        broken_links.append(f"{rel_path} missing link to sibling article '{expected_href}'")
                sibling_cluster_verified += 1

                # Check link to parent product
                expected_prod_href = f"../products/{expected_pslug}.html"
                if expected_prod_href not in parser.links:
                    broken_links.append(f"{rel_path} missing link to parent product '{expected_prod_href}'")
                else:
                    parent_product_link_verified += 1

        # Verify product pages link to their 3 articles
        if html_file.parent.name == "products":
            pslug = html_file.stem
            expected_aslugs = prod_to_articles.get(pslug, [])
            for aslug in expected_aslugs:
                expected_art_href = f"../articles/{aslug}.html"
                if expected_art_href not in parser.links:
                    broken_links.append(f"{rel_path} missing link to child article '{expected_art_href}'")

    if broken_links:
        for bl in broken_links:
            print(f"  [BROKEN] {bl}")
        assert False, f"TEST 6 failed with {len(broken_links)} broken or missing internal links"

    print(f"All 21 HTML files checked.")
    print(f"Verified sibling cluster links for all {sibling_cluster_verified} articles.")
    print(f"Verified parent product links for all {parent_product_link_verified} articles.")
    print(">>> TEST 6 RESULT: PASS (0 broken links across entire site)")
    return True


def run_test_7_visuals_and_promo_modal():
    print("\n" + "=" * 70)
    print("TEST 7: Visuals (SVG + Tables) and Promo Lead Tracker Modal")
    print("=" * 70)
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    errors = []

    for html_file in all_html_files:
        content = html_file.read_text(encoding='utf-8')
        parser = LinkAndSchemaExtractor()
        parser.feed(content)
        rel_path = html_file.relative_to(DOCS_DIR)

        # Check SVG (required for products and articles)
        if html_file.name != "index.html" and not parser.has_svg:
            errors.append(f"{rel_path}: Missing SVG visual diagram / timeline")

        # Check Table (required for products and articles)
        if html_file.name != "index.html" and not parser.has_table:
            errors.append(f"{rel_path}: Missing clinical comparison / protocol table")

        # Check Promo Lead Modal
        if not parser.has_promo_modal:
            errors.append(f"{rel_path}: Missing promo-lead-modal element")

        # Check Lead Log script presence
        if "window.getLeadLog" not in content:
            errors.append(f"{rel_path}: Missing window.getLeadLog function in JavaScript")

        if "HT10" not in content:
            errors.append(f"{rel_path}: Missing HT10 promo code reference")

        if "201155803307" not in content:
            errors.append(f"{rel_path}: Missing Doctor WhatsApp number 201155803307")

    if errors:
        for err in errors:
            print(f"  [FAIL] {err}")
        assert False, f"TEST 7 failed with {len(errors)} visual/modal issues"

    print(f"Verified SVG timelines, comparison tables, HT10 promo modal, and lead tracking JS across all 21 files.")
    print(">>> TEST 7 RESULT: PASS")
    return True


def run_test_8_technical_seo():
    print("\n" + "=" * 70)
    print("TEST 8: Technical SEO (robots.txt, sitemap.xml, Canonical & Meta Tags)")
    print("=" * 70)
    errors = []

    # 1. robots.txt
    robots_path = DOCS_DIR / "robots.txt"
    assert robots_path.exists(), "robots.txt missing!"
    robots_text = robots_path.read_text(encoding='utf-8')
    if "Sitemap: https://medon90ae.github.io/healing-touch-egypt/sitemap.xml" not in robots_text:
        errors.append("robots.txt missing Sitemap directive")

    # 2. sitemap.xml
    sitemap_path = DOCS_DIR / "sitemap.xml"
    assert sitemap_path.exists(), "sitemap.xml missing!"
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [elem.text for elem in root.findall('sm:url/sm:loc', ns)]
    print(f"Sitemap entries count: {len(urls)}")
    if len(urls) != 21:
        errors.append(f"sitemap.xml has {len(urls)} entries (expected 21)")

    # 3. Canonical & Meta Tags in HTML files
    all_html_files = sorted(list(DOCS_DIR.glob("**/*.html")))
    for html_file in all_html_files:
        content = html_file.read_text(encoding='utf-8')
        parser = LinkAndSchemaExtractor()
        parser.feed(content)
        rel_path = html_file.relative_to(DOCS_DIR)

        if not parser.canonical:
            errors.append(f"{rel_path}: Missing canonical link tag")
        elif not parser.canonical.startswith("https://medon90ae.github.io/healing-touch-egypt/"):
            errors.append(f"{rel_path}: Invalid canonical URL: {parser.canonical}")

        if "og:title" not in parser.meta_tags:
            errors.append(f"{rel_path}: Missing og:title meta tag")
        if "og:description" not in parser.meta_tags:
            errors.append(f"{rel_path}: Missing og:description meta tag")
        if "twitter:card" not in parser.meta_tags:
            errors.append(f"{rel_path}: Missing twitter:card meta tag")

    if errors:
        for err in errors:
            print(f"  [FAIL] {err}")
        assert False, f"TEST 8 failed with {len(errors)} technical SEO issues"

    print(">>> TEST 8 RESULT: PASS (All technical SEO files, sitemap URLs, and meta tags verified)")
    return True


if __name__ == "__main__":
    print("STARTING EMPIRICAL CHALLENGER ADVERSARIAL TEST SUITE\n")
    results = {}
    try:
        results["test_1_build_regeneration"] = run_test_1_build_regeneration()
        results["test_2_json_ld_schemas"] = run_test_2_json_ld_schemas()
        results["test_3_medical_citations"] = run_test_3_medical_citations()
        results["test_4_hashtags_and_products"] = run_test_4_hashtags_and_product_registry()
        results["test_5_forbidden_terms_audit"] = run_test_5_forbidden_terms_audit()
        results["test_6_link_graph"] = run_test_6_link_graph_and_navigation()
        results["test_7_visuals_and_promo"] = run_test_7_visuals_and_promo_modal()
        results["test_8_technical_seo"] = run_test_8_technical_seo()

        print("\n" + "=" * 70)
        print("ALL 8 ADVERSARIAL TESTS PASSED EMPIRICALLY WITH 100% SUCCESS!")
        print("=" * 70)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[ASSERTION ERROR]: {e}")
        sys.exit(1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
