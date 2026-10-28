# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | اختبارات التحقق لـ Milestone 1
Multi-Asset Ingestion & Folder Hygiene (R1) Comprehensive Verification Suite
=============================================================================
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "scripts"))

from smart_intake_classifier import (
    probe_media_dimensions,
    is_video_silent,
    merge_silent_video_with_audio,
    scan_and_triage_manual_inbox,
    archive_used_inbox_files,
    find_active_inbox_files
)
from campaign_landing_engine import build_campaign_landing_page


def test_multi_asset_ingestion_and_hygiene():
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
    print("🧪 بدء اختبارات التحقق من استيعاب الميديا المتعددة ونظافة المجلد (M1 / R1)")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # 1. اختبار فحص أبعاد الفيديوهات وتصنيف النسبة (9:16 vs 16:9)
    # -------------------------------------------------------------------------
    print("\n[المرحلة 1] اختبار فحص وتصنيف أبعاد الفيديوهات عبر ffprobe...")
    inbox_dir = BASE_DIR / "media_assets" / "manual_inbox"
    
    # فحص الفيديوهات الموجودة في manual_inbox أو archive
    vids = list(inbox_dir.glob("*.mp4"))
    if not vids:
        arch = inbox_dir / "archive"
        if arch.exists():
            for d in sorted(arch.iterdir(), reverse=True):
                vids = list(d.glob("*.mp4"))
                if vids:
                    break

    horiz_found = False
    vert_found = False
    for v in vids:
        dim = probe_media_dimensions(v)
        assert_true("width" in dim and "height" in dim and "aspect_ratio" in dim, f"DIM_PROBE_{v.name}", f"Invalid dim dict: {dim}")
        if dim["is_horizontal_16_9"]:
            horiz_found = True
        if dim["is_vertical_9_16"]:
            vert_found = True

    assert_true(horiz_found, "M1_HORIZ_VIDEO_PROBED", "At least one horizontal (16:9) video successfully probed")
    assert_true(vert_found, "M1_VERT_VIDEO_PROBED", "At least one vertical (9:16) video successfully probed")

    # -------------------------------------------------------------------------
    # 2. اختبار فحص الصور المتعددة وتصنيفها إلى Hero و Gallery
    # -------------------------------------------------------------------------
    print("\n[المرحلة 2] اختبار تصنيف الصور المتعددة (Hero + Gallery Carousel)...")
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        # إنشاء 3 صور تجريبية
        from PIL import Image
        img1 = tdp / "case_photo_1.png"
        img2 = tdp / "case_photo_2.png"
        img3 = tdp / "case_photo_3.png"
        Image.new("RGB", (1080, 1080), color="teal").save(img1)
        Image.new("RGB", (1080, 1920), color="#10B981").save(img2)
        Image.new("RGB", (1920, 1080), color="blue").save(img3)

        triage_res = scan_and_triage_manual_inbox(tdp)
        media_tr = triage_res.get("media_triage", {})
        imgs_tr = media_tr.get("images", {})

        assert_true(imgs_tr.get("hero") is not None, "M1_HERO_IMAGE_ASSIGNED", "Hero image not assigned")
        assert_true(len(imgs_tr.get("gallery", [])) == 2, "M1_GALLERY_IMAGES_ASSIGNED", f"Expected 2 gallery images, got {len(imgs_tr.get('gallery', []))}")
        assert_true(imgs_tr["hero"].name == "case_photo_1.png", "M1_HERO_IS_FIRST", f"Hero is not first image: {imgs_tr['hero']}")

    # -------------------------------------------------------------------------
    # 3. اختبار بناء صفحة الهبوط وتوليد سكشن المعرض السريري والمودال
    # -------------------------------------------------------------------------
    print("\n[المرحلة 3] اختبار بناء صفحة الهبوط وسكشن clinical-cases-gallery والمودال...")
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        sample_hero = tdp / "hero.png"
        sample_g1 = tdp / "gallery_1.png"
        sample_g2 = tdp / "gallery_2.png"
        Image.new("RGB", (800, 800), color="green").save(sample_hero)
        Image.new("RGB", (800, 800), color="teal").save(sample_g1)
        Image.new("RGB", (800, 800), color="blue").save(sample_g2)

        case_data = {
            "title": "بروتوكول تجميل الأنف ودعامات السيليكون",
            "category": "rhinoplasty",
            "story_text": "شرح سريري تفصيلي لبيولوجيا التعافي وحماية غضاريف الأنف.",
            "hashtags": "#تجميل_الانف #مصر"
        }
        res_lp = build_campaign_landing_page(
            case_data=case_data,
            media_assets={
                "hero_path": str(sample_hero),
                "gallery_paths": [str(sample_g1), str(sample_g2)]
            }
        )

        lp_file = Path(res_lp["local_file"])
        assert_true(lp_file.exists(), "M1_LP_FILE_GENERATED", f"LP file does not exist: {lp_file}")
        lp_html = lp_file.read_text(encoding="utf-8")

        assert_true('<section class="clinical-cases-gallery">' in lp_html, "M1_GALLERY_SECTION_EXISTS", "Section clinical-cases-gallery missing in LP HTML")
        assert_true('class="gallery-carousel-track"' in lp_html, "M1_CAROUSEL_TRACK_EXISTS", "Carousel track missing in LP HTML")
        assert_true('id="galleryModal"' in lp_html, "M1_GALLERY_MODAL_EXISTS", "Gallery modal viewer missing in LP HTML")
        assert_true('openGalleryModal' in lp_html, "M1_MODAL_JS_EXISTS", "openGalleryModal JS missing in LP HTML")
        assert_true('scrollGallery' in lp_html, "M1_CAROUSEL_SCROLL_JS_EXISTS", "scrollGallery JS missing in LP HTML")
        assert_true('campaign_rhinoplasty_hero.png' in lp_html, "M1_HERO_IMAGE_IN_LP", "Hero image missing in LP HTML")

    # -------------------------------------------------------------------------
    # 4. اختبار نظافة المجلد والأرشفة المؤرخة في media_assets/archive/YYYY-MM-DD_HHMMSS/
    # -------------------------------------------------------------------------
    print("\n[المرحلة 4] اختبار نظافة المجلد والأرشفة المؤرخة (Folder Hygiene)...")
    with tempfile.TemporaryDirectory() as td:
        root_dir = Path(td)
        inbox_tmp = root_dir / "media_assets" / "manual_inbox"
        inbox_tmp.mkdir(parents=True, exist_ok=True)

        # وضع ملفات تجريبية في manual_inbox
        f1 = inbox_tmp / "video_case_1.mp4"
        f2 = inbox_tmp / "image_case_1.png"
        f3 = inbox_tmp / "notes.txt"
        f1.write_text("dummy video content")
        f2.write_text("dummy image content")
        f3.write_text("dummy notes content")

        assert_true(len(list(inbox_tmp.iterdir())) == 3, "M1_INBOX_POPULATED", "Temporary inbox not populated")

        # تشغيل الأرشفة
        archived_count = archive_used_inbox_files(inbox_tmp, [f1, f2, f3])
        assert_true(archived_count == 3, "M1_ARCHIVE_COUNT", f"Expected 3 archived files, got {archived_count}")

        # التحقق من أن manual_inbox أصبح نظيفاً وفارغاً تماماً
        remaining_in_inbox = [f for f in inbox_tmp.iterdir() if f.is_file()]
        assert_true(len(remaining_in_inbox) == 0, "M1_INBOX_CLEAN_AND_EMPTY", f"manual_inbox is not empty: {remaining_in_inbox}")

        # التحقق من أن الملفات نُقلت إلى media_assets/archive/YYYY-MM-DD_HHMMSS/
        archive_root = root_dir / "media_assets" / "archive"
        assert_true(archive_root.exists(), "M1_ARCHIVE_ROOT_EXISTS", "media_assets/archive does not exist")
        arch_subdirs = [d for d in archive_root.iterdir() if d.is_dir()]
        assert_true(len(arch_subdirs) == 1, "M1_DATED_ARCHIVE_FOLDER_CREATED", f"Expected 1 dated folder, got {len(arch_subdirs)}")
        archived_files = [f.name for f in arch_subdirs[0].iterdir() if f.is_file()]
        assert_true(set(archived_files) == {"video_case_1.mp4", "image_case_1.png", "notes.txt"}, "M1_ARCHIVED_FILES_MATCH", f"Archived files mismatch: {archived_files}")

    # -------------------------------------------------------------------------
    # 5. اختبار خلو menu.py من خطأ قيامة الأرشيف (Archive Resurrection Bug)
    # -------------------------------------------------------------------------
    print("\n[المرحلة 5] اختبار فحص خلو menu.py من استرجاع ملفات الأرشيف...")
    menu_file = BASE_DIR / "menu.py"
    menu_content = menu_file.read_text(encoding="utf-8")
    assert_true("shutil.copy2(str(lf), str(manual_inbox / lf.name))" not in menu_content, "M1_MENU_NO_ARCHIVE_RESURRECTION", "Archive resurrection copy loop still present in menu.py!")
    assert_true("جاري تلقائياً استعادة ملفات آخر حملة من الأرشيف" not in menu_content, "M1_MENU_NO_RESURRECTION_LOG", "Archive resurrection message still present in menu.py")

    print("\n" + "=" * 70)
    print(f"🏁 نتيجة اختبارات Milestone 1: تم اجتياز {total_passed} اختبار بنجاح | إخفاقات: {total_failed}")
    print("=" * 70)

    if total_failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test_multi_asset_ingestion_and_hygiene()
