#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | Healing Touch Egypt
محرك البحث والتحميل الآلي لصور الحالات السريرية والطبية (Pexels & Pixabay APIs)
=============================================================================
"""

import os
import re
import sys
import json
import random
import urllib.parse
from pathlib import Path
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "rCqtbakBSGAMfnzmfjkx4xmWEJcDLAtzsUI42rPp0rIHYq8WomGSBNg1")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "58231818-9dc7b3231582430edf38f9343")

CASES_DIR = BASE_DIR / "media_assets" / "downloaded_cases"
CASES_DIR.mkdir(parents=True, exist_ok=True)
USED_IMAGES_FILE = BASE_DIR / "media_assets" / "used_images_log.json"


def load_used_images() -> set:
    """تحميل قائمة معرّفات الصور التي تم استخدامها سابقاً لتجنب التكرار."""
    if USED_IMAGES_FILE.exists():
        try:
            data = json.loads(USED_IMAGES_FILE.read_text(encoding="utf-8"))
            return set(data)
        except Exception:
            return set()
    return set()


def mark_image_as_used(img_id: str):
    """تسجيل معرّف الصورة كمستخدمة لمنع تكرارها في البوستات القادمة."""
    used = load_used_images()
    used.add(str(img_id))
    try:
        USED_IMAGES_FILE.write_text(json.dumps(list(used), ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[!] تنبيه في حفظ سجل الصور: {e}")

# خريطة الترجمة والكلمات المفتاحية الطبية لجلب أدق صور حالات واقعية
CATEGORY_SEARCH_QUERIES = {
    "c-section": [
        "cesarean recovery mother",
        "post surgery wound care bandage",
        "doctor examining patient scar",
        "hospital maternity recovery",
        "silicone scar care",
    ],
    "rhinoplasty": [
        "rhinoplasty nose bandage surgery",
        "nasal surgery recovery patient",
        "nose taping cosmetic surgery",
        "plastic surgery clinic consultation",
        "face bandage medical tape",
    ],
    "bariatric": [
        "laparoscopic surgery abdomen",
        "surgical wound dressing clinic",
        "patient abdominal recovery",
        "doctor examining wound dressing",
    ],
    "thyroid-gynecomastia": [
        "neck examination doctor patient",
        "thyroid surgery scar recovery",
        "chest scar tape recovery",
        "dermatology skin care consultation",
    ],
    "general": [
        "wound care bandage clinical",
        "doctor patient consultation clinic",
        "medical adhesive tape skin",
        "post surgery recovery hospital",
    ],
}


def detect_category_from_text(text: str) -> str:
    """استنتاج التخصص الجراحي من نص الموضوع أو العنوان."""
    t = text.lower()
    if any(k in t for k in ["قيصرية", "ولادة", "بطن", "كلويد", "c-section", "سيلكون", "بوبي"]):
        return "c-section"
    elif any(k in t for k in ["أنف", "ارنبة", "غضروف", "دعامة", "نوستريل", "rhinoplasty", "ميكروبور"]):
        return "rhinoplasty"
    elif any(k in t for k in ["تكميم", "منظار", "سمنة", "أوبسايت", "opsite", "bariatric"]):
        return "bariatric"
    elif any(k in t for k in ["غدة", "رقبة", "تثدي", "صدر", "thyroid"]):
        return "thyroid-gynecomastia"
    return "general"


def search_pexels_photo(query: str, exclude_ids: set = None) -> dict:
    """البحث في مكتبة Pexels الاحترافية مع اختيار صور متنوعة واستبعاد المكرر."""
    if not PEXELS_API_KEY:
        return {}
    exclude_ids = exclude_ids or set()
    try:
        page_num = random.randint(1, 3)
        url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page=15&page={page_num}&orientation=landscape"
        headers = {"Authorization": PEXELS_API_KEY}
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code == 200:
            data = res.json()
            photos = data.get("photos", [])
            # استبعاد الصور المستخدمة سابقاً
            fresh_photos = [p for p in photos if str(p.get("id")) not in exclude_ids]
            candidates = fresh_photos if fresh_photos else photos
            if candidates:
                # اختيار صورة عشوائياً من أفضل النتائج
                p = random.choice(candidates)
                img_url = p.get("src", {}).get("large") or p.get("src", {}).get("medium")
                return {
                    "source": "Pexels",
                    "id": str(p.get("id")),
                    "image_url": img_url,
                    "photographer": p.get("photographer", "Pexels Creator"),
                    "alt": p.get("alt") or query,
                }
    except Exception as e:
        print(f"[!] تنبيه في بحث Pexels: {e}")
    return {}


def search_pixabay_photo(query: str, exclude_ids: set = None) -> dict:
    """البحث في مكتبة Pixabay كبديل متنوع واستبعاد المكرر."""
    if not PIXABAY_API_KEY:
        return {}
    exclude_ids = exclude_ids or set()
    try:
        page_num = random.randint(1, 2)
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={urllib.parse.quote(query)}&image_type=photo&per_page=15&page={page_num}&orientation=horizontal"
        res = requests.get(url, timeout=12)
        if res.status_code == 200:
            data = res.json()
            hits = data.get("hits", [])
            fresh_hits = [h for h in hits if str(h.get("id")) not in exclude_ids]
            candidates = fresh_hits if fresh_hits else hits
            if candidates:
                h = random.choice(candidates)
                img_url = h.get("largeImageURL") or h.get("webformatURL")
                return {
                    "source": "Pixabay",
                    "id": str(h.get("id")),
                    "image_url": img_url,
                    "photographer": h.get("user", "Pixabay Creator"),
                    "alt": h.get("tags") or query,
                }
    except Exception as e:
        print(f"[!] تنبيه في بحث Pixabay: {e}")
    return {}


def get_clinical_case_photo(topic_text: str, custom_category: str = None) -> dict:
    """
    البحث وتنزيل صورة حالة طبية احترافية ملائمة للموضوع ومختلفة في كل مرة دون تكرار.
    """
    cat = custom_category or detect_category_from_text(topic_text)
    raw_queries = CATEGORY_SEARCH_QUERIES.get(cat, CATEGORY_SEARCH_QUERIES["general"]).copy()
    random.shuffle(raw_queries)

    used_ids = load_used_images()
    photo_info = {}

    # تنويع البدء بين Pexels و Pixabay بنسبة 50/50
    prefer_pexels = random.choice([True, False])

    for q in raw_queries:
        if prefer_pexels:
            photo_info = search_pexels_photo(q, exclude_ids=used_ids)
            if not photo_info:
                photo_info = search_pixabay_photo(q, exclude_ids=used_ids)
        else:
            photo_info = search_pixabay_photo(q, exclude_ids=used_ids)
            if not photo_info:
                photo_info = search_pexels_photo(q, exclude_ids=used_ids)

        if photo_info and photo_info.get("image_url"):
            break

    if not photo_info or not photo_info.get("image_url"):
        # محاولة بكلمات بديلة متنوعة
        fallback_queries = ["hospital surgical recovery", "doctor patient consultation clinic", "dermatology skin care clinic"]
        fb_query = random.choice(fallback_queries)
        photo_info = search_pexels_photo(fb_query, exclude_ids=used_ids) or search_pixabay_photo(fb_query, exclude_ids=used_ids)

    if not photo_info or not photo_info.get("image_url"):
        return {}

    # تسجيل معرّف الصورة كمستخدمة لمنع تكرارها
    if photo_info.get("id"):
        mark_image_as_used(photo_info["id"])

    # تنزيل الصورة محلياً وحفظها باسم فريد
    try:
        slug_id = f"case_{cat}_{photo_info['source'].lower()}_{photo_info['id']}"
        local_filename = f"{slug_id}.jpg"
        local_path = CASES_DIR / local_filename

        if not local_path.exists():
            print(f"[*] 📥 جاري تنزيل صورة جديدة ومميزة من {photo_info['source']} ({photo_info['alt']})...")
            img_res = requests.get(photo_info["image_url"], timeout=20)
            if img_res.status_code == 200:
                local_path.write_bytes(img_res.content)
                print(f"[+] ✅ تم حفظ الصورة بنجاح: {local_path.name} ({len(img_res.content)} بايت)")

        photo_info["local_path"] = str(local_path)
        return photo_info
    except Exception as exc:
        print(f"[!] خطأ في تنزيل الصورة: {exc}")
        return photo_info


if __name__ == "__main__":
    test_topics = [
        "جرح الولادة القيصرية والاستحمام",
        "تورم أرنبة الأنف بعد عملية التجميل",
        "جرح الغدة الدرقية في الرقبة والتثدي",
    ]
    for topic in test_topics:
        print(f"\n--- فحص الموضوع: {topic} ---")
        info = get_clinical_case_photo(topic)
        print("النتيجة:", info)
