#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك النشر الشامل (Omnichannel Publishing Hub)
فيسبوك + إنستجرام + تيك توك ريلز + مدونات جوجل + استوديو كانفا في ضغطة واحدة
=============================================================================
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from clinical_image_engine import get_clinical_case_photo
from canva_card_generator import generate_branded_card, generate_tiktok_reel_video, export_canva_bulk_csv
from blogger_publisher import format_clinical_case_for_blogger, generate_blogger_atom_xml
from clinical_story_publisher import (
    CLINICAL_STORIES_TEMPLATES,
    get_next_template_index,
    record_post_history
)
from antigravity_social_automation import publish_facebook_graph_api, FB_PAGE_ID as META_PAGE_ID, META_PERMANENT_PAGE_TOKEN, GRAPH_API_VERSION
import requests


def check_instagram_account() -> str:
    """التحقق مما إذا كان حساب إنستجرام مربوطاً بصفحة الفيسبوك في ميتا بزنس."""
    if not META_PERMANENT_PAGE_TOKEN or not META_PAGE_ID:
        return ""
    try:
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{META_PAGE_ID}"
        res = requests.get(
            url,
            params={"fields": "instagram_business_account", "access_token": META_PERMANENT_PAGE_TOKEN},
            timeout=10
        ).json()
        ig_acc = res.get("instagram_business_account", {})
        return ig_acc.get("id", "")
    except Exception:
        return ""


def publish_omnichannel(template_idx: int = None, dry_run: bool = False):
    print("=" * 65)
    print("🌿 هيلينج تاتش مصر | تشغيل محرك النشر الشامل وتوليد المحتوى")
    print("=" * 65)

    # 1. اختيار الحالة السريرية التالية
    chosen_idx = get_next_template_index(template_idx)
    tmpl = CLINICAL_STORIES_TEMPLATES[chosen_idx]
    print(f"[*] 📖 [حالة رقم {chosen_idx + 1} من {len(CLINICAL_STORIES_TEMPLATES)}]: {tmpl['title']}")

    # 2. جلب صورة طبية طازجة من Pexels أو Pixabay
    photo_info = get_clinical_case_photo(tmpl["title"], tmpl["category"])
    raw_img = photo_info.get("local_path", "")
    print(f"[*] 📸 تم اختيار صورة جديدة: {Path(raw_img).name} (المصدر: {photo_info.get('source')})")

    # 3. تشغيل استوديو أوتو-كانفا لتصميم البطاقات المربعة والطولية
    cards = generate_branded_card(tmpl, raw_img)
    square_img_path = cards["square_path"]
    story_img_path = cards["story_path"]

    # 4. توليد فيديو TikTok / Instagram Reels متحرك
    video_path = generate_tiktok_reel_video(story_img_path, duration_sec=7)

    # 5. تصدير ملف Canva Bulk CSV
    export_canva_bulk_csv(CLINICAL_STORIES_TEMPLATES)

    # 6. تجهيز مقال مدونة جوجل (Google Blogger)
    blogger_post = format_clinical_case_for_blogger(tmpl, photo_info, square_img_path)
    generate_blogger_atom_xml([blogger_post])

    # 7. فحص حساب إنستجرام
    ig_id = check_instagram_account()
    if ig_id:
        print(f"[+] 📸 تم اكتشاف حساب إنستجرام متصل: ID={ig_id}")
    else:
        print("[i] حساب إنستجرام غير مربوط بعد بصفحة فيسبوك في Meta Business Suite.")

    # تجهيز كابشن النشر
    post_data = {
        "day": f"دراسة حالة سريرية ({chosen_idx + 1}) - {tmpl['title']}",
        "caption": tmpl["story_text"],
        "hashtags": tmpl["hashtags"],
        "row_index": -1
    }

    if dry_run:
        record_post_history(chosen_idx, tmpl['title'])
        print("\n" + "=" * 65)
        print("🔍 معاينة مخرجات المحرك الشامل (DRY RUN - جاهز للنشر):")
        print("=" * 65)
        print(f"1. بطاقة فيسبوك وإنستجرام المصممة: {square_img_path}")
        print(f"2. بطاقة الستوري وتيك توك: {story_img_path}")
        print(f"3. فيديو TikTok & Reels المتحرك: {video_path}")
        print(f"4. مقال مدونة جوجل HTML: {blogger_post['file_path']}")
        print(f"5. ملف استيراد بلوجر الرسمي: media_assets/blogger_posts/blogger_import_feed.xml")
        print(f"6. ملف Canva Bulk Create: media_assets/canva_bulk_import.csv")
        print("\nنص المنشور:")
        print(tmpl['story_text'][:300] + "...\n[باقي النص مع رابط الواتساب والهاشتاجات]")
        print("=" * 65)
        return True

    # النشر الفعلي على فيسبوك مع الصورة المصممة بنمط كانفا
    print(f"\n[*] 🚀 جاري نشر البطاقة المصممة على صفحة فيسبوك...")
    ok, permalink = publish_facebook_graph_api(post_data, square_img_path)
    if ok:
        record_post_history(chosen_idx, tmpl['title'])
        print(f"🎉 ✅ تم النشر بنجاح على فيسبوك!")
        print(f"🔗 رابط المنشور: {permalink}")
    else:
        print("[!] فشل النشر على فيسبوك.")

    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="محرك النشر الشامل")
    parser.add_argument("--index", type=int, default=None, help="رقم الحالة يدوياً")
    parser.add_argument("--dry-run", action="store_true", help="توليد ومعاينة كافة التصاميم والفيديوهات والمقالات دون النشر")
    args = parser.parse_args()
    publish_omnichannel(args.index, dry_run=args.dry_run)
