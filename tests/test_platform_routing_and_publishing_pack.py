# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | اختبارات التحقق الصارمة والشاملة (2026)
Tests for Platform Router (R1), Clean Content Extractor (R2),
Dynamic Ready-to-Publish Pack Engine (R3), and Campaign Publishing (R4).
=============================================================================
"""

import sys
import os
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "scripts"))

from smart_intake_classifier import (
    scan_and_triage_manual_inbox,
    route_platform_text_files,
    extract_clean_content,
    classify_file_category,
    find_active_inbox_files
)
from scripts.build_ready_to_publish_pack import get_latest_pack_dir, get_active_assets


def run_all_tests():
    total_passed = 0
    total_failed = 0

    def assert_true(cond, name, msg=""):
        nonlocal total_passed, total_failed
        if cond:
            print(f"  [PASS] {name}")
            total_passed += 1
        else:
            print(f"  [FAIL] {name}: {msg}")
            total_failed += 1

    print("=" * 70)
    print("🧪 بدء الاختبارات التجريبية الصارمة لمنظومة التوجيه والنشر (R1, R2, R3, R4)")
    print("=" * 70)

    # =========================================================================
    # 1. اختبارات موجه المنصات R1 (Platform Router)
    # =========================================================================
    print("\n[المرحلة 1] اختبار ذكاء توجيه وفرز ملفات المنصات (R1)...")
    inbox_dir = BASE_DIR / "media_assets" / "manual_inbox"
    triage = scan_and_triage_manual_inbox(inbox_dir)
    p_texts = triage.get("platform_texts", {})

    assert_true(triage["detected_category"] == "rhinoplasty", "R1_CATEGORY_DETECTED", f"Expected rhinoplasty, got {triage['detected_category']}")
    assert_true(p_texts.get("facebook") is not None and "فيسبوك" in p_texts["facebook"].name, "R1_FB_ROUTED", "Facebook file not routed")
    assert_true(p_texts.get("instagram") is not None and "إنستجرام" in p_texts["instagram"].name, "R1_IG_ROUTED", "Instagram file not routed")
    assert_true(p_texts.get("tiktok") is not None and "تيك" in p_texts["tiktok"].name, "R1_TT_ROUTED", "TikTok file not routed")
    assert_true(p_texts.get("youtube") is not None and "يوتيوب" in p_texts["youtube"].name, "R1_YT_ROUTED", "YouTube file not routed")
    assert_true(p_texts.get("blogger") is not None and "الدليل الطبي الشامل" in p_texts["blogger"].name, "R1_BLOGGER_ROUTED", "Blogger file not routed")
    assert_true(p_texts.get("reddit") is not None and "دعامات الأنف بعد التجميل" in p_texts["reddit"].name, "R1_REDDIT_ROUTED", "Reddit file not routed")

    # اختبار عزل المنصات
    assigned_files = [v for k, v in p_texts.items() if k != "general" and v is not None]
    assert_true(len(assigned_files) == len(set(assigned_files)), "R1_PLATFORM_ISOLATION", "Duplicate file assigned to multiple platforms")

    # =========================================================================
    # 2. اختبارات مستخرج المحتوى السريري النظيف R2 (Clean Content Extractor)
    # =========================================================================
    print("\n[المرحلة 2] اختبار استخراج متن المحتوى السريري الفعلي (R2)...")
    landing_url = "https://medon90ae.github.io/healing-touch-egypt/lp/rhinoplasty-recovery-protocol.html"
    whatsapp_url = "https://wa.me/201155803307?text=HT10"

    # فيسبوك
    fb_res = extract_clean_content(p_texts["facebook"], "facebook", landing_url=landing_url, whatsapp_url=whatsapp_url)
    fb_cap = fb_res["caption"]
    assert_true(fb_cap.startswith("عزيزتي الأخت والأم"), "R2_FB_CLEAN_START", f"Start was: {fb_cap[:50]}")
    assert_true("المشروع:  منصة هيلينج تاتش" not in fb_cap, "R2_FB_NO_PROJECT_HEADER", "Found internal project header in FB caption")
    assert_true("السيو الموجه" not in fb_cap, "R2_FB_NO_SEO_HEADER", "Found SEO header in FB caption")
    assert_true("HT10" in fb_cap, "R2_FB_HAS_HT10", "HT10 code missing in FB caption")
    assert_true("01155803307" in fb_cap, "R2_FB_HAS_PHONE", "Phone number missing in FB caption")
    assert_true(landing_url in fb_cap, "R2_FB_HAS_LANDING_URL", "Landing URL missing in FB caption")
    assert_true(len(fb_cap) > 2000, "R2_FB_FULL_NARRATIVE_PRESERVED", f"FB caption too short ({len(fb_cap)} chars) - premature truncation suspected")

    # إنستجرام
    ig_res = extract_clean_content(p_texts["instagram"], "instagram", landing_url=landing_url, whatsapp_url=whatsapp_url)
    ig_cap = ig_res["caption"]
    assert_true("المشروع:" not in ig_cap and "السيو الموجه" not in ig_cap, "R2_IG_NO_HEADERS", "Headers found in IG caption")
    assert_true("HT10" in ig_cap, "R2_IG_HAS_HT10", "HT10 missing in IG caption")
    assert_true("01155803307" in ig_cap, "R2_IG_HAS_PHONE", "Phone missing in IG caption")
    assert_true(len(ig_cap) <= 2200, "R2_IG_WITHIN_LIMITS", f"IG caption exceeds 2200 char limit ({len(ig_cap)} chars)")

    # تيك توك
    tt_res = extract_clean_content(p_texts["tiktok"], "tiktok", landing_url=landing_url, whatsapp_url=whatsapp_url)
    tt_cap = tt_res["caption"]
    assert_true("المشروع:" not in tt_cap and "حزمة تيك توك" not in tt_cap, "R2_TT_NO_HEADERS", "Headers found in TT caption")
    assert_true("HT10" in tt_cap, "R2_TT_HAS_HT10", "HT10 missing in TT caption")

    # يوتيوب
    yt_res = extract_clean_content(p_texts["youtube"], "youtube", landing_url=landing_url, whatsapp_url=whatsapp_url)
    assert_true("دعامات الأنف" in yt_res["title"], "R2_YT_TITLE_MATCH", f"Title: {yt_res['title']}")
    assert_true(len(yt_res["tags"].split(",")) >= 10, "R2_YT_TAGS_PARSED", "Tags not parsed")
    assert_true("المشروع:" not in yt_res["description"], "R2_YT_NO_HEADERS", "Headers found in YT description")

    # بلوجر
    bl_res = extract_clean_content(p_texts["blogger"], "blogger", landing_url=landing_url, whatsapp_url=whatsapp_url)
    assert_true("<table" in bl_res["html_content"], "R2_BLOGGER_TABLE_RENDERED", "Comparison table not rendered in HTML")
    assert_true("<h2" in bl_res["html_content"], "R2_BLOGGER_H2_HEADINGS", "Headings not rendered in HTML")
    assert_true("HT10" in bl_res["html_content"], "R2_BLOGGER_HAS_HT10", "HT10 missing in Blogger HTML")

    # ريديت
    rd_res = extract_clean_content(p_texts["reddit"], "reddit", landing_url=landing_url, whatsapp_url=whatsapp_url)
    assert_true(rd_res["markdown"].startswith("# "), "R2_REDDIT_MARKDOWN_HEADER", "Markdown heading missing")
    assert_true("PMID" in rd_res["markdown"], "R2_REDDIT_RESEARCH_CITATIONS", "PubMed citations missing")

    # =========================================================================
    # 3. اختبارات حزمة ready_to_publish المؤرخة R3 (Pack Engine)
    # =========================================================================
    print("\n[المرحلة 3] فحص حزمة ready_to_publish المؤرخة للتأكد من خلوها 100% من نصوص القيصرية (R3)...")
    pack_dir = get_latest_pack_dir("rhinoplasty")
    assert_true(pack_dir.exists() and pack_dir.is_dir(), "R3_PACK_EXISTS", f"Pack dir does not exist: {pack_dir}")

    required_folders = [
        "01_يوتيوب_YouTube",
        "02_تيكتوك_TikTok",
        "03_إنستجرام_Instagram",
        "04_بلوجر_Blogger",
        "05_ريديت_Reddit",
        "06_فيسبوك_Facebook"
    ]
    for rf in required_folders:
        assert_true((pack_dir / rf).exists() and (pack_dir / rf).is_dir(), f"R3_FOLDER_{rf}", f"Folder {rf} missing")

    # فحص صارم لكافة ملفات الحزمة ضد كلمات جرح القيصرية والشاور
    text_extensions = [".txt", ".md", ".html"]
    all_pack_files = [f for f in pack_dir.rglob("*") if f.is_file() and f.suffix.lower() in text_extensions]
    forbidden_terms = ["جرح القيصرية", "الولادة القيصرية", "الشاور الآمن", "tegaderm", "تيجاديرم", "كلويد القيصرية"]

    violations = []
    for pf in all_pack_files:
        content = pf.read_text(encoding="utf-8", errors="ignore").lower()
        for term in forbidden_terms:
            if term.lower() in content:
                violations.append((pf.relative_to(pack_dir), term))

    assert_true(len(violations) == 0, "R3_ZERO_CSECTION_VIOLATIONS", f"Found c-section mentions in rhinoplasty pack: {violations}")

    # فحص تطابق المحتوى في اليوتيوب وبلوجر مع دعامات الأنف
    yt_file = pack_dir / "01_يوتيوب_YouTube" / "بيانات_الفيديو_عنوان_ووصف_وهاشتاجات.txt"
    yt_text = yt_file.read_text(encoding="utf-8")
    assert_true("دعامات الأنف" in yt_text and "تماثل" in yt_text, "R3_YT_CONTENT_RHINOPLASTY", "YouTube data does not match rhinoplasty")

    bl_file = pack_dir / "04_بلوجر_Blogger" / "مقال_بلوجر_جاهز_للنشر.html"
    bl_text = bl_file.read_text(encoding="utf-8")
    assert_true("دعامات الانف" in bl_text and "تماثل الفتحات" in bl_text, "R3_BLOGGER_CONTENT_RHINOPLASTY", "Blogger HTML does not match rhinoplasty")

    # =========================================================================
    # 4. اختبارات النشر والتحديث السليم لحملة دعامات الأنف R4
    # =========================================================================
    print("\n[المرحلة 4] فحص سجل النشر الحقيقي في منشورات فيسبوك (R4)...")
    import json
    log_file = BASE_DIR / "published_posts_log.json"
    assert_true(log_file.exists(), "R4_LOG_EXISTS", "published_posts_log.json missing")

    log_data = json.loads(log_file.read_text(encoding="utf-8"))
    last_post = log_data[-1]

    assert_true(any(k in last_post["caption"] for k in ["دعامة الأنف", "دعامات الانف", "دعامات الأنف", "تجميل الأنف"]), "R4_LAST_POST_RHINOPLASTY", "Last post caption is not rhinoplasty")
    assert_true("المشروع:" not in last_post["caption"], "R4_LAST_POST_NO_TECH_HEADER", "Technical header in last post")
    assert_true("HT10" in last_post["caption"], "R4_LAST_POST_HAS_HT10", "HT10 missing in last post")
    assert_true("01155803307" in last_post["caption"], "R4_LAST_POST_HAS_PHONE", "Phone missing in last post")
    assert_true("permalink_url" in last_post and "facebook.com" in last_post["permalink_url"], "R4_LAST_POST_VALID_PERMALINK", "Invalid Facebook permalink")

    # =========================================================================
    # 5. اختبارات الحالات الحدية والهجومية الصارمة (Adversarial Edge Cases)
    # =========================================================================
    print("\n[المرحلة 5] اختبارات الحالات الحدية ومحاولات كسر المنظومة (Adversarial Probing)...")

    # 1. اختبار التوجيه بالصيغ والتهجئات الشائعة في اللهجات العربية
    variant_files = [
        "فيس بوك.txt",
        "انستغرام.txt",
        "تيكتوك.txt",
        "يو تيوب.txt",
        "الدليل الطبي الشامل.txt",
        "التقرير السريري الشامل.txt"
    ]
    v_routed = route_platform_text_files(variant_files)
    assert_true(v_routed["facebook"] is not None and "فيس بوك" in v_routed["facebook"].name, "EDGE_R1_FB_VARIANT_SPACE", "فيس بوك not routed")
    assert_true(v_routed["instagram"] is not None and "انستغرام" in v_routed["instagram"].name, "EDGE_R1_IG_VARIANT_GHAYN", "انستغرام not routed")
    assert_true(v_routed["tiktok"] is not None and "تيكتوك" in v_routed["tiktok"].name, "EDGE_R1_TT_VARIANT_CONCAT", "تيكتوك not routed")
    assert_true(v_routed["youtube"] is not None and "يو تيوب" in v_routed["youtube"].name, "EDGE_R1_YT_VARIANT_SPACE", "يو تيوب not routed")
    assert_true(v_routed["blogger"] is not None and "الدليل الطبي الشامل" in v_routed["blogger"].name, "EDGE_R1_BLOGGER_VARIANT", "الدليل الطبي الشامل not routed")
    assert_true(v_routed["reddit"] is not None and "التقرير السريري الشامل" in v_routed["reddit"].name, "EDGE_R1_REDDIT_VARIANT", "التقرير السريري الشامل not routed")

    # 2. اختبار عدم الخلط بين كلمة (تكتيكات) ومنصة تيك توك
    tactics_file = ["تكتيكات_التعافي_الجراحي.txt"]
    tac_routed = route_platform_text_files(tactics_file)
    assert_true(tac_routed["tiktok"] is None, "EDGE_R1_TACTICS_NOT_TIKTOK", "تكتيكات erroneously matched to TikTok!")
    assert_true(len(tac_routed["general"]) == 1, "EDGE_R1_TACTICS_IN_GENERAL", "Tactics file not in general")

    # 3. اختبار عزل الملفات المتنازعة لمنع التكرار (Collision Isolation)
    collision_files = ["facebook_tiktok_post.txt"]
    col_routed = route_platform_text_files(collision_files)
    col_assigned = [v for k, v in col_routed.items() if k != "general" and v is not None]
    assert_true(len(col_assigned) == 1, "EDGE_R1_COLLISION_SINGLE_ALLOCATION", f"Collision file assigned to multiple platforms: {col_assigned}")

    # 4. اختبار تمرير بايتات خام (bytes) بترميز UTF-8 و CP1256
    arabic_sample_utf8 = "📝 نص المنشور الكامل:\nهذا منشور سريري معتمد لدعامات الأنف وتماثل الفتحات.\n#تجميل_الانف"
    arabic_sample_cp1256 = "نص المنشور الكامل:\nهذا منشور سريري معتمد لدعامات الأنف وتماثل الفتحات.\n#تجميل_الانف"
    utf8_bytes = arabic_sample_utf8.encode("utf-8")
    cp1256_bytes = arabic_sample_cp1256.encode("cp1256")

    res_utf8 = extract_clean_content(utf8_bytes, "facebook")
    assert_true("هذا منشور سريري معتمد" in res_utf8["caption"], "EDGE_R2_BYTES_UTF8", "UTF-8 bytes extraction failed")

    res_cp1256 = extract_clean_content(cp1256_bytes, "facebook")
    assert_true("هذا منشور سريري معتمد" in res_cp1256["caption"], "EDGE_R2_BYTES_CP1256", "CP1256 bytes extraction failed")

    # 5. اختبار الحفاظ على عناوين الماركداون (### عنوان) في متن فيسبوك وعدم تحويلها لهاشتاجات
    markdown_fb = """نص المنشور:
عزيزتي الأخت والأم سلامتك وسلامة كل عزيز عليك.
### 1. المقدمة السريرية
هذا هو الشرح السريري لبيولوجيا الأنسجة والتعافي.
### 2. الحل الطبي المعتمد
وهذا هو الحل السريري بدعامات السيليكون.
#تجميل_الانف #مصر"""
    fb_md_res = extract_clean_content(markdown_fb, "facebook")
    assert_true("### 1. المقدمة السريرية" in fb_md_res["body"], "EDGE_R2_MARKDOWN_HEADING_IN_BODY", "Markdown heading was stripped from body")
    assert_true("###" not in fb_md_res["hashtags"], "EDGE_R2_MARKDOWN_HEADING_NOT_IN_TAGS", "Markdown heading was moved to hashtags")
    assert_true("#تجميل_الانف" in fb_md_res["hashtags"], "EDGE_R2_HASHTAGS_PRESERVED", "Hashtags missing from tags block")

    # 6. اختبار إزالة الترويسات الفنية داخل الأقواس أو القوائم حتى بدون علامة بداية (Brackets & Bullets Purge)
    bracketed_sample = """[المشروع: منصة هيلينج تاتش مصر]
- السيو الموجه: تجميل الأنف
- تاريخ الإنتاج: 28 أكتوبر 2026
عزيزتي الأخت والأم سلامتك وسلامة كل عزيز عليك بعد العملية ونفهمك بيولوجيا التعافي بالتفصيل."""
    br_res = extract_clean_content(bracketed_sample, "facebook")
    assert_true("المشروع" not in br_res["caption"], "EDGE_R2_BRACKETED_PROJECT_PURGED", "Bracketed project header leaked")
    assert_true("السيو الموجه" not in br_res["caption"], "EDGE_R2_BULLETED_SEO_PURGED", "Bulleted SEO header leaked")
    assert_true("تاريخ الإنتاج" not in br_res["caption"], "EDGE_R2_BULLETED_DATE_PURGED", "Bulleted date header leaked")

    # 7. اختبار عدم حذف الفقرة الأولى في بلوجر عند وجود وصف تعريفي في نفس السطر
    blogger_single_line_desc = """الدليل الطبي الشامل: تجميل الأنف
الوصف التعريفي: هذا هو الوصف التعريفي السريع لحالة التعافي.
المقدمة السريرية الأولى التي كتبها الطبيب ويجب ألا تحذف أبداً.
الفقرة الثانية من المقال الطبي الهام."""
    bl_single_res = extract_clean_content(blogger_single_line_desc, "blogger")
    assert_true("المقدمة السريرية الأولى" in bl_single_res["html_content"], "EDGE_R2_BLOGGER_FIRST_PARA_PRESERVED", "Blogger first paragraph deleted by meta description")
    assert_true("هذا هو الوصف التعريفي السريع" in bl_single_res["meta_description"], "EDGE_R2_BLOGGER_META_PARSED", "Meta description not parsed")

    # 8. اختبار تحويل جداول الماركداون (|...|) وجداول الفاصلة العربية (،) في بلوجر
    blogger_pipe_table = """الدليل الطبي الشامل: تجميل الأنف

| وجه المقارنة | الغيار العادي | دعامة السيليكون |
| --- | --- | --- |
| مقاومة الماء | ضعيفة | ممتازة |
| الحماية | عادية | فائقة |"""
    bl_pipe_res = extract_clean_content(blogger_pipe_table, "blogger")
    assert_true("<table" in bl_pipe_res["html_content"], "EDGE_R2_BLOGGER_PIPE_TABLE", "Markdown pipe table not converted to HTML table")

    blogger_arabic_comma_table = """الدليل الطبي الشامل: تجميل الأنف

وجه المقارنة، الغيار التقليدي، دعامة السيليكون
مقاومة الماء، ضعيفة جداً، ممتازة ومعتمدة"""
    bl_ar_comma_res = extract_clean_content(blogger_arabic_comma_table, "blogger")
    assert_true("<table" in bl_ar_comma_res["html_content"], "EDGE_R2_BLOGGER_ARABIC_COMMA_TABLE", "Arabic comma table not converted to HTML table")

    # 9. اختبار عدم تحويل جملة عادية تحتوي فواصل إلى جدول منفرد (Sentence False Positive)
    blogger_sentence_with_commas = """الدليل الطبي الشامل: تجميل الأنف

تعتبر دعامات السيليكون حلاً رائعاً, خفيفاً على الأنف, ومريحاً في التنفس.
الفقرة التالية تستعرض فوائد الاستخدام."""
    bl_sent_res = extract_clean_content(blogger_sentence_with_commas, "blogger")
    assert_true("<table" not in bl_sent_res["html_content"], "EDGE_R2_BLOGGER_SENTENCE_NOT_TABLE", "Single sentence with commas falsely converted to table")

    # 10. اختبار أولوية مطابقة الاسم ومنع اختطاف فيسبوك لملفات المنصات الأخرى بسبب ترويسة (نص المنشور الكامل)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        yt_cand = tdp / "youtube_content.txt"
        yt_cand.write_text("حزمة سيو يوتيوب\nنص المنشور الكامل للنشر المباشر:\nفيديو يوتيوب", encoding="utf-8")
        fb_cand = tdp / "facebook_post.txt"
        fb_cand.write_text("بوست فيسبوك عادي", encoding="utf-8")
        routed_prio = route_platform_text_files([yt_cand, fb_cand])
        assert_true(routed_prio["facebook"] is not None and routed_prio["facebook"].name == "facebook_post.txt", "EDGE_R1_NAME_PRIORITY_FB", f"Facebook snatched wrong file: {routed_prio['facebook']}")
        assert_true(routed_prio["youtube"] is not None and routed_prio["youtube"].name == "youtube_content.txt", "EDGE_R1_NAME_PRIORITY_YT", f"YouTube lost its file: {routed_prio['youtube']}")

    # 11. اختبار أسماء snake_case (fb_..., ig_..., yt_...)
    snake_candidates = ["fb_rhino.txt", "ig_rhino.txt", "yt_rhino.txt"]
    snake_routed = route_platform_text_files(snake_candidates)
    assert_true(snake_routed["facebook"] is not None and snake_routed["facebook"].name == "fb_rhino.txt", "EDGE_R1_SNAKE_CASE_FB", "fb_rhino not routed")
    assert_true(snake_routed["instagram"] is not None and snake_routed["instagram"].name == "ig_rhino.txt", "EDGE_R1_SNAKE_CASE_IG", "ig_rhino not routed")
    assert_true(snake_routed["youtube"] is not None and snake_routed["youtube"].name == "yt_rhino.txt", "EDGE_R1_SNAKE_CASE_YT", "yt_rhino not routed")

    # 12. اختبار منع تكرار العنوان في مقال ريديت (Reddit Title Deduplication)
    reddit_raw_sample = "التقرير السريري الشامل: استراتيجيات التعافي المتقدمة\nمقدمة سريرية هامة توضح تفاصيل التعافي."
    rd_clean = extract_clean_content(reddit_raw_sample, "reddit")
    first_lines = rd_clean["markdown"].splitlines()[:4]
    title_matches = [l for l in first_lines if "استراتيجيات التعافي المتقدمة" in l]
    assert_true(len(title_matches) == 1, "EDGE_R2_REDDIT_NO_DUPLICATE_TITLE", f"Reddit title duplicated in top lines: {first_lines}")

    # 13. اختبار عدم تكرار بادئة الماركداون (# #) إذا كان السطر الأول يحتوي #
    reddit_hash_sample = "# استراتيجيات التعافي المتقدمة\nمقدمة سريرية هامة."
    rd_hash_clean = extract_clean_content(reddit_hash_sample, "reddit")
    assert_true(not rd_hash_clean["markdown"].startswith("# #"), "EDGE_R2_REDDIT_CLEAN_HEADING", "Double hash in reddit heading")

    # 14. اختبار خلو وسم <h1> في مقال بلوجر من علامة #
    blogger_hash_title = "# دعامات الأنف بعد التجميل\nالوصف التعريفي: وصف سريري سريع\nالفقرة الأولى من المقال."
    bl_hash_res = extract_clean_content(blogger_hash_title, "blogger")
    assert_true("<h1>#" not in bl_hash_res["html_content"] and "<h1 style=" in bl_hash_res["html_content"] and not bl_hash_res["title"].startswith("#"), "EDGE_R2_BLOGGER_NO_HASH_IN_H1", f"Markdown # leaked into Blogger h1: {bl_hash_res['title']}")

    # 15. اختبار جداول بلوجر المفصولة بفاصل Tab من برامج الجداول
    blogger_tab_table = "الدليل الطبي الشامل: تجميل الأنف\n\nالميزة\tالدعامة السيليكونية\tالقطن التقليدي\nالمقاومة\tفائقة\tمنعدمة"
    bl_tab_res = extract_clean_content(blogger_tab_table, "blogger")
    assert_true("<table" in bl_tab_res["html_content"], "EDGE_R2_BLOGGER_TAB_TABLE", "Tab-delimited table not parsed into HTML table")

    # 16. اختبار توليد حزمة لحملة مختلفة (Bariatric) ديناميكياً والتأكد من نقاء محتواها وعزل التخصص
    from scripts.build_ready_to_publish_pack import generate_pack
    bariatric_pack = generate_pack(category="bariatric")
    assert_true(bariatric_pack.exists() and (bariatric_pack / "01_يوتيوب_YouTube").exists(), "EDGE_R3_DYNAMIC_CATEGORY_PACK", "Dynamic category pack generation failed")

    bar_yt = (bariatric_pack / "01_يوتيوب_YouTube" / "بيانات_الفيديو_عنوان_ووصف_وهاشتاجات.txt").read_text(encoding="utf-8")
    assert_true(any(k in bar_yt for k in ["تكميم", "سمنة", "منظار"]), "EDGE_R3_BARIATRIC_CONTENT", "Bariatric pack missing bariatric keywords")
    assert_true("دعامات الأنف" not in bar_yt, "EDGE_R3_NO_RHINO_IN_BARIATRIC", "Rhinoplasty content leaked into bariatric pack")

    bar_guide = (bariatric_pack / "00_دليل_النشر_السريع.txt").read_text(encoding="utf-8")
    assert_true("bariatric" in bar_guide, "EDGE_R3_BARIATRIC_GUIDE", "Guide does not state bariatric")

    # 17. اختبار نظافة جدول مقال بلوجر الحقيقي وعدم تحويل فقرات المقال إلى جداول مشوهة
    blogger_real_tables = re.findall(r"<table.*?</table>", bl_res["html_content"], re.DOTALL)
    assert_true(len(blogger_real_tables) == 1, "EDGE_R2_BLOGGER_EXACTLY_ONE_TABLE", f"Expected exactly 1 comparison table, found {len(blogger_real_tables)} (paragraph table contamination detected)")

    # 18. اختبار تحويل العناوين المرقمة في مقال بلوجر إلى وسم h2 بنجاح (Section 1 and Section 7)
    assert_true("<h2" in bl_res["html_content"] and "1. المقدمة السريرية" in bl_res["html_content"] and "7. جدول مقارنة" in bl_res["html_content"], "EDGE_R2_BLOGGER_SECTION_HEADINGS_H2", "Numbered section headings not converted to h2")

    # 19. اختبار الحفاظ على نقطة وكسر السطر للسطر السابق قبل رابط الواتساب في فيسبوك
    assert_true("بالتفصيل." in fb_cap and "\n👉 رابط الاستشارة" in fb_cap, "EDGE_R2_FB_PRESERVES_PRECEDING_PERIOD", "Preceding line terminator or punctuation swallowed by regex")

    print("\n" + "=" * 70)
    print(f"🏁 نتيجة الاختبارات: تم اجتياز {total_passed} اختبار بنجاح | إخفاقات: {total_failed}")
    print("=" * 70)

    if total_failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_all_tests()
