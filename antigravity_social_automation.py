#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | Healing Touch Egypt (مصر 2026)
المحرك الشامل الموحد للأتمتة والتصميم والنشر (Unified Omnichannel & Studio Engine)
=============================================================================
يجمع هذا المحرك الموحد كل قدرات المشروع في ملف مركزي واحد:
1. محرك الصور السريرية الذكي (Pexels & Pixabay APIs) مع ذاكرة منع التكرار.
2. محرك القصص والحالات السريرية الواقعية (Clinical Case Storytelling) بالدوران التلقائي.
3. استوديو أوتو-كانفا الآلي (بطاقات 1080x1080 + ستوري 1080x1920 + فيديو TikTok/Reels MP4).
4. محرك التكامل مع Google NotebookLM (تصدير الموسوعة الطبية + دمج البودكاست الصوتي بالفيديو).
5. محرك مدونات جوجل (Google Blogger HTML & Atom XML) وملف Canva Bulk Create CSV.
6. النشر التلقائي عبر Meta Graph API لفيسبوك وإنستجرام وتحديث Google Sheet ورادار الجروبات.
=============================================================================
"""

import argparse
import asyncio
import datetime as dt
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import webbrowser
import campaign_landing_engine as cle
from datetime import datetime
from smart_intake_classifier import (
    scan_and_triage_manual_inbox,
    archive_used_inbox_files,
    route_platform_text_files,
    extract_clean_content,
    find_active_inbox_files,
    read_resilient_text,
    classify_file_category
)
from pathlib import Path

try:
    from scripts.dispatch_n8n_bridge import dispatch_to_n8n_webhook, build_omnichannel_payload
except ImportError:
    from dispatch_n8n_bridge import dispatch_to_n8n_webhook, build_omnichannel_payload

import pandas as pd
import requests
from dotenv import load_dotenv, set_key
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# =============================================================================
# 🔑 إعدادات مفاتيح الـ API والمسارات المركزية
# =============================================================================
APP_ID = os.getenv("APP_ID", "28911377768496017")
APP_SECRET = os.getenv("APP_SECRET", "43ee937c862a90a7a398cab351c70748")
FB_PAGE_ID = os.getenv("FB_PAGE_ID", "1371809382684781")
META_PERMANENT_PAGE_TOKEN = os.getenv(
    "META_PERMANENT_PAGE_TOKEN",
    "EAGa2vrHbu5EBS2RdBgJZCFhGkZC1whXiZAmGXgCAMFYMiiXCEXf2PMreCLaflMZB1BSu2dbL5BZAHXUqB7RrGfGrmzILldLCzqdTWVm4Na3ynLU05zywVqbB8FqCrpRVOtyxOUcyCZA9ZAxk2pep2U2Oi4JNRFsijUrku3K2AGQ8ZCFLrFsZAd1SF4JBvmpLDNGK61eg4nf51a5nCFh4oMNPH",
)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "rCqtbakBSGAMfnzmfjkx4xmWEJcDLAtzsUI42rPp0rIHYq8WomGSBNg1")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "58231818-9dc7b3231582430edf38f9343")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k")
CONTENT_TAB_NAME = "جدول المحتوى والنشر الآلي (Antigravity)"
CONTENT_TAB_GID = os.getenv("CONTENT_TAB_GID", "1119996693")
PROBLEMS_TAB_NAME = "مصفوفة مشاكل العملاء والردود الذكية"
GROUPS_TAB_NAME = "خريطة الجروبات والمجتمعات المستهدفة"
GRAPH_API_VERSION = "v21.0"

MEDIA_DIR = BASE_DIR / "media_assets"
CASES_DIR = MEDIA_DIR / "downloaded_cases"
BRANDED_DIR = MEDIA_DIR / "branded_designs"
BLOGGER_DIR = MEDIA_DIR / "blogger_posts"
NOTEBOOKLM_DIR = MEDIA_DIR / "notebooklm_hub"
NOTEBOOK_AUDIO_DIR = NOTEBOOKLM_DIR / "audio_inputs"
NOTEBOOK_ARCHIVE_DIR = NOTEBOOKLM_DIR / "daily_sources_archive"
NOTEBOOK_PIC_DIR = NOTEBOOKLM_DIR / "pic"
MANUAL_INBOX_DIR = MEDIA_DIR / "manual_inbox"

for d in (MEDIA_DIR, CASES_DIR, BRANDED_DIR, BLOGGER_DIR, NOTEBOOKLM_DIR, NOTEBOOK_AUDIO_DIR, NOTEBOOK_ARCHIVE_DIR, NOTEBOOK_PIC_DIR, MANUAL_INBOX_DIR):
    d.mkdir(parents=True, exist_ok=True)

PUBLISHED_LOG_PATH = BASE_DIR / "published_posts_log.json"
USED_IMAGES_FILE = MEDIA_DIR / "used_images_log.json"
HISTORY_FILE = MEDIA_DIR / "clinical_posts_history.json"
BULK_CSV_PATH = MEDIA_DIR / "canva_bulk_import.csv"

DEFAULT_SURGICAL_KEYWORDS = [
    "شاور بعد القيصرية",
    "أثر جرح القيصرية",
    "تورم الأرنبة",
    "بلاستر 3M",
    "دعامة الأنف",
    "جروح التكميم",
]

# =============================================================================
# 📸 القسم الأول: محرك الصور السريرية الذكي (Pexels & Pixabay) مع فلتر الأمان الطبي
# =============================================================================
import base64

CATEGORY_SEARCH_QUERIES = {
    "c-section": [
        "mother holding newborn baby hospital bed",
        "female doctor consulting patient clinic",
        "medical wound dressing bandage first aid",
        "pediatrician mother baby hospital",
        "pharmacist medical care consultation",
    ],
    "rhinoplasty": [
        "plastic surgeon doctor consulting female patient",
        "medical adhesive tape bandage first aid",
        "dermatologist examining face skin clinic",
        "cosmetic clinic doctor consultation",
        "facial skincare clinic examination",
    ],
    "bariatric": [
        "surgeon doctor consulting patient hospital",
        "medical spray bottle first aid pharmacy",
        "hospital patient recovery bed doctor",
        "nutritionist doctor consultation clinic",
    ],
    "thyroid": [
        "doctor examining patient neck clinic",
        "endocrinologist medical consultation hospital",
        "dermatology clinic skin care doctor",
        "medical bandage tape pharmacy",
    ],
    "general": [
        "doctor patient consultation medical clinic",
        "medical adhesive tape bandage first aid",
        "female doctor hospital clinic",
        "pharmacist healthcare consultation",
    ],
}

FORBIDDEN_IMAGE_KEYWORDS = [
    "nude", "naked", "bikini", "underwear", "lingerie", "bra", "topless",
    "sexy", "do not download", "sensual", "erotic", "boudoir", "tattoo",
    "kiss", "beach", "swimsuit", "cleavage", "intimate"
]


def is_safe_clinical_image(alt_or_tags: str) -> bool:
    """فلتر صارم لاستبعاد أي صور غير محتشمة أو غير طبية لا تناسب المجتمع المصري."""
    t = (alt_or_tags or "").lower()
    if any(bad in t for bad in FORBIDDEN_IMAGE_KEYWORDS):
        return False
    return True


def load_used_images() -> set:
    if USED_IMAGES_FILE.exists():
        try:
            return set(json.loads(USED_IMAGES_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def mark_image_as_used(img_id: str):
    used = load_used_images()
    used.add(str(img_id))
    try:
        USED_IMAGES_FILE.write_text(json.dumps(list(used), ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def detect_category_from_text(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["قيصرية", "ولادة", "بطن", "كلويد", "c-section", "سيلكون", "بوبي"]):
        return "c-section"
    elif any(k in t for k in ["أنف", "ارنبة", "غضروف", "دعامة", "نوستريل", "rhinoplasty", "ميكروبور"]):
        return "rhinoplasty"
    elif any(k in t for k in ["تكميم", "منظار", "سمنة", "أوبسايت", "opsite", "bariatric"]):
        return "bariatric"
    elif any(k in t for k in ["غدة", "رقبة", "تثدي", "صدر", "thyroid"]):
        return "thyroid"
    return "general"


def search_pexels_photo(query: str, exclude_ids: set = None) -> dict:
    if not PEXELS_API_KEY:
        return {}
    exclude_ids = exclude_ids or set()
    try:
        page_num = random.randint(1, 3)
        url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page=15&page={page_num}&orientation=landscape"
        res = requests.get(url, headers={"Authorization": PEXELS_API_KEY}, timeout=12)
        if res.status_code == 200:
            photos = [p for p in res.json().get("photos", []) if is_safe_clinical_image(p.get("alt", ""))]
            fresh = [p for p in photos if str(p.get("id")) not in exclude_ids]
            candidates = fresh if fresh else photos
            if candidates:
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
        print(f"[!] تنبيه Pexels: {e}")
    return {}


def search_pixabay_photo(query: str, exclude_ids: set = None) -> dict:
    if not PIXABAY_API_KEY:
        return {}
    exclude_ids = exclude_ids or set()
    try:
        page_num = random.randint(1, 2)
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={urllib.parse.quote(query)}&image_type=photo&safesearch=true&category=health&per_page=15&page={page_num}&orientation=horizontal"
        res = requests.get(url, timeout=12)
        if res.status_code == 200:
            hits = [h for h in res.json().get("hits", []) if is_safe_clinical_image(h.get("tags", ""))]
            fresh = [h for h in hits if str(h.get("id")) not in exclude_ids]
            candidates = fresh if fresh else hits
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
        print(f"[!] تنبيه Pixabay: {e}")
    return {}


def get_clinical_case_photo(topic_text: str, custom_category: str = None) -> dict:
    import random
    cat = custom_category or detect_category_from_text(topic_text)
    
    # 🌟 الاعتماد الحصري بنسبة 100% على جلسات تصوير منتجات Pomelli الطبية المعتمدة للمشروع (منع Pexels/Pixabay نهائياً)
    pomelli_lib = MEDIA_DIR / "pomelli_library"
    if pomelli_lib.exists():
        candidates = list(pomelli_lib.glob("*.png")) + list(pomelli_lib.glob("*.jpg"))
        if candidates:
            # تصفية ذكية حسب التخصص إن أمكن
            matched = [c for c in candidates if cat in c.name.lower()] or candidates
            chosen = random.choice(matched)
            print(f"[+] 🎨 تم اعتماد صورة منتج سريرية فائقة الدقة من جلسات Pomelli المعتمدة: {chosen.name}")
            return {
                "id": chosen.stem,
                "image_url": "",
                "source": "Pomelli Studio",
                "alt": f"جلسة تصوير طبية لمنتجات هيلينج تاتش مصر - {cat}",
                "photographer": "Healing Touch Egypt Clinical Studio",
                "local_path": str(chosen),
            }

    # إذا لم تتوفر مكتبة Pomelli، نستخدم الصور المعتمدة في docs/assets
    docs_assets = BASE_DIR / "docs" / "assets"
    for ext in [".png", ".jpg"]:
        cand = docs_assets / f"campaign_{cat}_hero{ext}"
        if cand.exists():
            return {
                "id": cand.stem,
                "image_url": "",
                "source": "Clinical Library",
                "alt": f"منتجات هيلينج تاتش مصر - {cat}",
                "photographer": "Healing Touch Egypt",
                "local_path": str(cand),
            }

    og_img = docs_assets / "og-image.jpg"
    if og_img.exists():
        return {
            "id": "og-image",
            "image_url": "",
            "source": "Clinical Library",
            "alt": f"منتجات هيلينج تاتش مصر - {cat}",
            "photographer": "Healing Touch Egypt",
            "local_path": str(og_img),
        }

    return {}


# =============================================================================
# 📖 القسم الثاني: بنك القصص والحالات السريرية الواقعية والدوران التلقائي
# =============================================================================
CLINICAL_STORIES_TEMPLATES = [
    {
        "category": "c-section",
        "title": "حالة جرح القيصرية والشاور والندبة البارزة",
        "story_text": """أمهات كتير بيبعتوا يسألونا في التوجيه السريري:
"أنا والدة قيصري بقالي أسبوعين وخايفة من شكل الجرح، والمية لو لمسته هيلتهب؟ وليه حاسة بحيل أو خط ناشف ومكلكع تحت الجلد؟"

طيب مبدئياً.. تعالي نفهم ده بيحصل إزاي بهدوء:

الجرح بعد العملية بيمر بـ 3 طبقات التئام، والجسم في الأول بيبعت ألياف كولاجين مكثفة عشان يقفل المكان بسرعة.. الألياف دي لو متعاملناش معاها بوعي، بتبدأ تبرز وتتحول لندبة متضخمة (Hypertrophic Scar) أو كلويد بارز ولونه غامق!

عشان كده مهم جداً نقسم خطة التعافي لخطوات علمية بسيطة:

١. في أول أسبوعين (ممنوع وصول المية العادية أو الصابون للجرح):
كتير بيفتكروا إن الغيار العادي كفاية، لكن الشاش والقطن بيمتصوا المية وبيفضل الجرح رطب من جوه وده بيئة مثالية للبكتيريا والالتهاب.
الحل الطبي المعتمد: استخدام ضمادات الفيلم الشفاف المقاوم للمية (3M Tegaderm +Pad)؛ بتعمل عزل 100% وتسمحلك تاخدي شاور كامل بأمان تام والجلد يتنفس.

٢. بعد التئام السطح وفك الغرز وسقوط القشور (عادة من اليوم العاشر للرابع عشر):
هنا بتبدأ مرحلة "فرد وتسطيح الندبة". الأمهات اللي بيكتفوا بمرهم مضاد حيوي بس بيفوتهم أهم توقيت لمنع بروز الكلويد!

٣. القاعدة الذهبية لجراحي التجميل عالمياً: (شرائح السيليكون الطبي - Medical Silicone Sheets):
شيت السيليكون الطبي (زي رول BUPY الطبي القابل للغسيل وإعادة الاستخدام) بيشتغل زي "قالب ضغط وترطيب هادئ"؛ بيمنع تبخر الرطوبة من الجلد، ويجبر ألياف الكولاجين إنها تتنظم بشكل مستوي وموازي للجلد بدل ما تبرز لفوق، ويخفي الحكة والاحمرار بنسبة تتجاوز 85%.

٤. أخطاء شائعة بتأخر النتيجة:
- وضع مراهم تقيلة أو زيوت قبل شيت السيليكون (بيمنع التصاقه ويفقده فاعليته).
- الاستعجال والتوقف بعد أسبوع (الجلد بيحتاج من 8 إلى 12 أسبوع عشان يعيد تشكيل نفسه بالكامل).

💡 لو عندك أي استفسار عن مرحلة جرحك بعد القيصرية وحابة إرشاد سريري موثوق لحالتك:
تقدري تتواصلي مباشرة للحصول على توجيه سريري مجاني مع استشاري التعافي عبر واتساب:
💬 رابط الدليل السريري والتواصل المباشر:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=c-section
(أو مباشرة عبر واتساب: 01155803307)""",
        "hashtags": "#ولادة_قيصرية_مصر #جرح_القيصرية #علاج_الندبات #شيت_سيليكون_بوبي #ضمادات_تيجاديرم #صحة_المراة_مصر #امهات_مصر #مامي_جديدة #علاج_الكلويد #هيلينج_تاتش_مصر",
    },
    {
        "category": "rhinoplasty",
        "title": "حالة تورم أرنبة الأنف وتماثل الفتحات بعد التجميل",
        "story_text": """بنات كتير بعد فك جبيرة الأنف بيجيلهم قلق شديد:
"الأرنبة وارمة جداً وحاسة إن في فتحة أكبر من فتحة أو مش متماثلين، واللصقات العادية بتعملي حساسية وحبوب بيضا تحت الجلد!"

مبدئياً.. دي مرحلة طبيعية بيمر بيها 95% من حالات تجميل الأنف، والسر كله في فهم بيولوجيا الأنسجة بعد إزالة الجبيرة:

١. ليه الأرنبة بتورم بعد فك الجبيرة؟
الجبيرة كانت عاملة ضغط مستمر، وأول ما بتتشال، السوائل اللمفاوية بتتجمع في طرف الأنف (Supratip Edema) خصوصاً لأصحاب الجلد السميك (Thick Skin).

٢. خطورة اللصقات العادية غير المسامية:
اللصقات التجارية غير المخصصة لجراحة الأنف بتمنع مسام الجلد من التنفس، وبتسيب صمغ كيميائي يسبب التهابات وحبوب صديدية، والأخطر إنها بتضغط بشكل غير متساوي فتشوه نزول التورم!

٣. القاعدة السريرية المثبتة في أبحاث 2026:
- استخدام بلاستر ورقي طبي مسامي مخصص (3M Micropore Tan البيج الأصلي): خفيف جداً، لونه بيج تجميلي غير ملفت، بيوفر ضغط هادئ يصرّف السوائل بدون حساسية.
- الحفاظ على تماثل الفتحتين بدعامة السيليكون الطبية (Nostril Retainer): قوى الانكماش الندبي بعد قص الفتحات بتشد الغضاريف، واستخدام دعامة السيليكون بالمقاس المضبوط بيحافظ على تماثل الفتحتين بنسبة 94% وفق دراسات MDPI السريرية.

٤. نصيحة للمتابعة:
ممنوع شد اللصقة بعنف؛ لازم ترطيبها بمية دافية قبل الإزالة عشان متسحبش الجلد وتزود التورم.

💡 عندك استفسار عن مقاس دعامة الأنف أو طريقة اللصق المناسبة لنوع جلدك؟
تواصلي الآن مع استشاري التعافي للحصول على إرشاد سريري مجاني:
💬 رابط الدليل السريري والتواصل المباشر:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=rhinoplasty
(أو مباشرة عبر واتساب: 01155803307)""",
        "hashtags": "#تجميل_الانف_مصر #عملية_تجميل_الانف #تورم_الانف_بعد_العملية #بلاستر_3m_البيج #دعامة_الانف_السيليكون #ارنبة_الانف #هيلينج_تاتش_مصر #جراحة_تجميل_مصر",
    },
    {
        "category": "bariatric",
        "title": "حالة ثقوب المنظار بعد التكميم وتحسس البلاستر ورعب الاستحمام",
        "story_text": """حالات كتير جداً بعد عمليات التكميم وتحويل المسار بيسألونا في قلق:
"عندي 4 أو 5 ثقوب في بطني، البلاستر العادي عامل احمرار وحكة رهيبة، ومحرومة من الشاور بقالي أسبوعين وخايفة من تلوث الجروح!"

مبدئياً.. دي مشكلة شائعة لدى 80% من مرضى جراحات السمنة والحل الطبي بسيط جداً:

١. ليه البلاستر العادي بيعمل حساسية شديدة في البطن؟
الجلد في منطقة البطن بعد العملية بيكون مشدود وحساس، وصمغ البلاستر التجاري بيسحب الطبقة القرنية السطحية مع كل غيار مسبباً التهاب تماسي واحمرار يشبه الحروق!

٢. خطورة الشاور بالغيار المبلول:
القطن لما يلمس مية الشاور بيفضل رطب لساعات، وده بيزود فرص العدوى الميكروبية بثقوب المنظار.

٣. الحل المعتمد في مراكز جراحة السمنة:
- استخدام بخاخ الفيلم الشفاف الطبي (Smith & Nephew Opsite Spray): رشة واحدة بتعمل طبقة ميكروسكوبية عازلة للماء والبكتيريا 100%، تسمحلك تاخد شاور فوري، وفي نفس الوقت بتسيب مسام الجلد تتنفس وتتخلص من العرق.
- بعد التئام الثقوب: استخدام قصاصات شيت السيليكون الطبي (BUPY) لمنع تحول الثقوب لندبات غامقة أو بارزة.

💡 حابب تعرف الطريقة الصحيحة للغيار على ثقوب المنظار حسب أيام عمليتك؟
تواصل الآن للحصول على توجيه سريري مجاني مع استشاري التعافي عبر واتساب:
💬 رابط الدليل السريري والتواصل المباشر:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=bariatric
(أو مباشرة عبر واتساب: 01155803307)""",
        "hashtags": "#تكميم_المعدة_مصر #جراحة_السمنة #تحويل_مسار #ثقوب_المنظار #بخاخ_اوبسايت #علاج_الندبات #هيلينج_تاتش_مصر #رابطة_المتكممين",
    },
    {
        "category": "thyroid",
        "title": "حالة ندبة الرقبة بعد استئصال الغدة الدرقية وحمايتها من الشمس",
        "story_text": """سيدات كتير بعد جراحة استئصال الغدة الدرقية بيكون الهاجس الأكبر عندهم:
"الخط اللي في رقبتي لونه أحمر وواضح جداً، وكل الناس بتبص عليه! إزاي أخفيه وأمنع إنه يفضل معلم طول العمر؟"

منطقة الرقبة من أدق مناطق الجسم لأن الجلد فيها رقيق جداً ومعرض لحركة مستمرة ولأشعة الشمس المباشرة:

١. التئام جرح الرقبة محتاج هدوء ميكانيكي:
حركة الرقبة والبلع بتعمل قوى شد مستمرة على حواف الجرح، وده بيحفز خلايا الفايبروبلاست تفرز كولاجين زائد فيبرز الخط ويبقى عريض.

٢. خطورة الشمس المباشرة:
أشعة الشمس فوق البنفسجية بتنشط صبغة الميلانين في أنسجة الندبة حديثة الالتئام، فبتتحول للون بني داكن دائم صعب جداً تفتيحه لاحقاً!

٣. البروتوكول الطبي الوقائي:
- استخدام شيت السيليكون الطبي (BUPY): بيعمل ترطيب وضغط متزن يمنع بروز الندبة ويقلل احمرارها خلال 8-12 أسبوعاً.
- التثبيت الخفي: استخدام بلاستر 3M Micropore البيج الأصلي لتثبيت الأطراف وحماية الجرح من أشعة الشمس المباشرة أثناء الخروج.

💡 عندك استفسار عن مرحلة جرح الغدة والتوقيت السليم لبدء السيليكون؟
تواصلي مباشرة مع استشاري التعافي لإرشاد سريري مجاني:
💬 رابط الدليل السريري والتواصل المباشر:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=thyroid
(أو مباشرة عبر واتساب: 01155803307)""",
        "hashtags": "#استئصال_الغدة_الدرقية #جراحة_الغدة #ندبات_الرقبة #شيت_سيليكون_بوبي #بلاستر_3m_البيج #هيلينج_تاتش_مصر #تجميل_الجروح",
    },
    {
        "category": "c-section",
        "title": "حالة بروز كلويد القيصرية القديم والحكة الشديدة بعد 6 أشهر",
        "story_text": """كتير من الأمهات بيكلمونا بعد الولادة بست شهور أو سنة:
"الجرح كان كويس، بس فجأة قلب لونه أحمر داكن وبقى بارز زي الحبل، وفيه حكة ونغزات فظيعة بتخليني مش طايقة الهدوم تلمسه!"

هنا بنشرحلهم إن ده "كلويد نشط" (Active Keloid Scar) أو ندبة متضخمة:

١. ليه الندبة بتهرش وتبرز بعد شهور؟
ألياف الكولاجين لما بتفقد الرطوبة (Transepidermal Water Loss)، الخلايا بتفتكر إن الجرح لسه مفتوح وبتفضل تنتج كولاجين عشوائي يرتفع فوق مستوى الجلد، والأوعية الدموية الدقيقة بتسبب الاحمرار والحكة.

٢. هل الجراحة تاني هي الحل؟
استئصال الكلويد جراحياً بدون حماية بيرجع الكلويد أكبر بنسبة 70%!

٣. الحل الطبي السريري المعتمد:
- استخدام شيت السيليكون الطبي BUPY يومياً من 12 إلى 20 ساعة:
شيت السيليكون بيعمل ترطيب مستمر للطبقة المتقرنة، ويقلل تدفق الدم الزائد في الندبة فيطفي الاحمرار والحكة فوراً خلال أيام، ومع الاستمرار بيسوي الندبة بالجلد تدريجياً.
- ميزة رول BUPY (عرض 4 سم في طول 3 متر): اقتصادي جداً، بيكفي علاج 4 إلى 6 شهور لأنه بيتغسل بمية دافية ويتكرر استخدامه.

💡 لو عندك كلويد بارز أو نغزات في جرح قديم وحابة تعرفي خطة العلاج المناسبة:
تواصلي مع استشاري التعافي لإرشاد سريري مجاني:
💬 رابط الدليل السريري والتواصل المباشر:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=c-section
(أو مباشرة عبر واتساب: 01155803307)""",
        "hashtags": "#كلويد_القيصرية #علاج_الكلويد #ندبات_الولادة #شيت_سيليكون_بوبي #حكة_الجرح #هيلينج_تاتش_مصر #امهات_مصر",
    },
    {
        "category": "rhinoplasty",
        "title": "حالة تورم الأنف العريض والجلد السميك وحبوب البلاستر",
        "story_text": """أصحاب الجلد السميك (Thick Skin) بعد تجميل الأنف بيعانوا من أزمة متكررة:
"الجلد بيفرز دهون عالية تحت البلاستر العادي، فبيعمل حبوب صديدية وبثور بيضاء، ولما بشيل البلاستر بيكون مؤلم جداً وبيسحب الجلد معاه!"

التعامل مع جلد الأنف بعد الجراحة له تكنيك طبي خاص:

١. مسامية البلاستر هي كلمة السر:
البلاستر الأبيض التجاري بيكون مشمع ومكتوم، فبيحبس العرق والإفرازات الدهنية تحت الجلد ويسبب التهاب حويصلات الشعر (Folliculitis).

٢. الحل الطبي القياسي لعيادات التجميل:
- بلاستر 3M Micropore Tan البيج الأصلي (كود 1533-0): مصنوع من ألياف الرايون غير المنسوجة الدقيقة جداً، بيسمح للبشرة بالتنفس 100% ويفرغ الدهون بدون احتباس.
- صمغه الطبي (Hypoallergenic) لطيف على الأنسجة ولا يترك أثراً لزجاً عند الإزالة.

٣. نصيحة قبل إزالة اللصقة:
بللي اللصقة بقطنة بمية دافية أو زيت أطفال خفيف وانتظري دقيقتين عشان تنزل بسلاسة بدون أي شد لغضاريف الأنف.

💡 محتاجة مساعدة في مقاس البلاستر الأنسب لأنفك وطريقة اللصق الصحيحة؟
تواصلي الآن للحصول على استشارة سريرية مجانية مع استشاري التعافي:
💬 رابط الدليل السريري والتواصل المباشر:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=rhinoplasty
(أو مباشرة عبر واتساب: 01155803307)""",
        "hashtags": "#تجميل_الانف_اللحمي #تجميل_الانف_مصر #بلاستر_3m_البيج #حبوب_الانف_بعد_العملية #ارنبة_الانف #هيلينج_تاتش_مصر",
    },
]


def load_post_history() -> list:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def record_post_history(template_idx: int, title: str):
    history = load_post_history()
    history.append({"index": template_idx, "title": title, "timestamp": datetime.now().isoformat()})
    try:
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def get_next_template_index(manual_idx: int = None) -> int:
    total = len(CLINICAL_STORIES_TEMPLATES)
    if manual_idx is not None:
        return manual_idx % total
    history = load_post_history()
    if not history:
        return 0
    return (history[-1].get("index", 0) + 1) % total


# =============================================================================
# 🎨 القسم الثالث: استوديو أوتو-كانفا + دمج صوت NotebookLM في فيديو TikTok/Reels
# =============================================================================
def build_card_html(title: str, category_badge: str, key_tip: str, bg_image_uri: str, format_type: str = "square") -> str:
    is_story = format_type == "story"
    width = 1080
    height = 1920 if is_story else 1080
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: {width}px; height: {height}px; overflow: hidden;
      font-family: 'Cairo', sans-serif; position: relative;
      background: #064E3B; color: #FFFFFF;
    }}
    .bg-img {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover; filter: brightness(0.85) contrast(1.08);
    }}
    .gradient-overlay {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: linear-gradient(180deg, rgba(6,78,59,0.82) 0%, rgba(6,78,59,0.20) 35%, rgba(15,23,42,0.58) 68%, rgba(6,78,59,0.92) 100%);
    }}
    .card-content {{
      position: relative; z-index: 10; width: 100%; height: 100%;
      padding: {'100px 70px' if is_story else '70px'};
      display: flex; flex-direction: column; justify-content: space-between;
    }}
    .header-bar {{ display: flex; justify-content: space-between; align-items: center; }}
    .brand-pill {{
      display: flex; align-items: center; gap: 14px;
      background: rgba(255,255,255,0.15); backdrop-filter: blur(12px);
      border: 1.5px solid rgba(255,255,255,0.3); padding: 10px 24px; border-radius: 40px;
    }}
    .brand-icon {{
      width: 42px; height: 42px; background: #10B981; border-radius: 50%;
      display: flex; align-items: center; justify-content: center; font-size: 24px;
    }}
    .brand-text {{ font-size: 26px; font-weight: 800; }}
    .category-badge {{
      background: #F59E0B; color: #78350F; font-size: 22px; font-weight: 900;
      padding: 10px 24px; border-radius: 30px; box-shadow: 0 4px 15px rgba(245,158,11,0.4);
    }}
    .center-box {{ margin: auto 0; }}
    .medical-sub {{ color: #34D399; font-size: 26px; font-weight: 700; margin-bottom: 16px; }}
    .main-title {{
      font-size: {'56px' if is_story else '48px'}; font-weight: 900;
      line-height: 1.3; margin-bottom: 24px; text-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }}
    .key-tip-box {{
      background: rgba(255,255,255,0.12); backdrop-filter: blur(16px);
      border-right: 6px solid #10B981; padding: 24px 28px; border-radius: 16px;
      font-size: 26px; line-height: 1.5; font-weight: 600; color: #F1F5F9;
    }}
    .footer-bar {{ display: flex; justify-content: space-between; align-items: center; gap: 20px; }}
    .promo-card {{
      background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
      color: #92400E; padding: 16px 26px; border-radius: 20px;
      font-size: 24px; font-weight: 800; border: 2px dashed #D97706;
    }}
    .cta-button {{
      background: #25D366; color: #FFFFFF; padding: 18px 36px;
      border-radius: 20px; font-size: 26px; font-weight: 800;
    }}
  </style>
</head>
<body>
  <img src="{bg_image_uri}" class="bg-img" alt="Case Background" />
  <div class="gradient-overlay"></div>
  <div class="card-content">
    <div class="header-bar">
      <div class="brand-pill">
        <div class="brand-icon">🌿</div>
        <div class="brand-text">هيلينج تاتش مصر</div>
      </div>
      <div class="category-badge">{category_badge}</div>
    </div>
    <div class="center-box">
      <div class="medical-sub">🩺 دراسة حالة سريرية وبروتوكول التعافي</div>
      <h1 class="main-title">{title}</h1>
      <div class="key-tip-box">💡 <strong>القاعدة السريرية:</strong> {key_tip}</div>
    </div>
    <div class="footer-bar">
      <div class="promo-card">🎁 كود: <strong>HT10</strong> (شحن مجاني + حق المعاينة)</div>
      <div class="cta-button">💬 استشارة مجانية: 01155803307</div>
    </div>
  </div>
</body>
</html>"""


async def _render_image_playwright(html_code: str, output_path: Path, width: int, height: int):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        await page.set_content(html_code, wait_until="networkidle")
        await page.screenshot(path=str(output_path), full_page=True)
        await browser.close()


def generate_branded_card(case_info: dict, raw_img_path: str) -> dict:
    title = case_info.get("title", "بروتوكول العناية الجراحية")
    cat = case_info.get("category", "c-section")
    cat_badges = {
        "c-section": "الولادة القيصرية",
        "rhinoplasty": "تجميل الأنف",
        "bariatric": "جراحات السمنة",
        "thyroid": "جراحة الغدة والرقبة",
        "general": "عناية ما بعد الجراحة",
    }
    badge = cat_badges.get(cat, "عناية طبية متخصصة")
    tips_map = {
        "c-section": "عزل الماء 100% بضمادات Tegaderm + تسطيح الندبة بشيت السيليكون BUPY.",
        "rhinoplasty": "تفريغ تورم الأرنبة ببلاستر 3M البيج المسامي وتماثل الفتحات بدعامة السيليكون.",
        "bariatric": "حماية ثقوب المنظار من بكتيريا الاستحمام فوراً بطبقة بخاخ Opsite الشفافة.",
        "thyroid": "حماية ندبة الرقبة من أشعة الشمس بـ 3M وترطيبها بـ BUPY لمنع التصبغ الداكن.",
        "general": "الالتزام بالبروتوكول السريري يقلل فترة التئام الجروح بنسبة تفوق 75%.",
    }
    key_tip = tips_map.get(cat, tips_map["general"])

    date_str = datetime.now().strftime("%Y-%m-%d")
    if raw_img_path and Path(raw_img_path).is_file():
        raw_path = Path(raw_img_path).resolve()
    else:
        fallback_file = (BASE_DIR / "docs" / "assets" / "og-image.jpg").resolve()
        raw_path = fallback_file if fallback_file.is_file() else Path(raw_img_path).resolve()
    b64_data = base64.b64encode(raw_path.read_bytes()).decode("ascii")
    bg_uri = f"data:image/jpeg;base64,{b64_data}"
    
    # أسماء واضحة وصريحة تحدد التاريخ والمنصة ونوع المحتوى
    square_png = BRANDED_DIR / f"{date_str}_[فيسبوك_وإنستجرام_بوست]_{cat}.png"
    story_png = BRANDED_DIR / f"{date_str}_[إنستجرام_ستوري]_{cat}.png"

    print(f"[*] 🎨 جاري تصميم بوست أوتو-كانفا للموضوع: {title}...")
    asyncio.run(_render_image_playwright(build_card_html(title, badge, key_tip, bg_uri, "square"), square_png, 1080, 1080))
    asyncio.run(_render_image_playwright(build_card_html(title, badge, key_tip, bg_uri, "story"), story_png, 1080, 1920))
    print(f"[+] ✅ تم حفظ بطاقات السوشيال ميديا الواضحة:\n   • {square_png.name}\n   • {story_png.name}")

    return {"square_path": str(square_png), "story_path": str(story_png), "title": title, "badge": badge, "key_tip": key_tip}


def generate_tiktok_reel_video(story_card_path: str, duration_sec: int = 8) -> str:
    """تحويل البطاقة الطولية إلى فيديو MP4 مع دمج تلقائي لصوت البودكاست وتسمية واضحة للمنصة والتاريخ."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    in_path = Path(story_card_path).resolve()
    # استخراج اسم الحالة مثل c-section أو rhinoplasty
    cat_tag = in_path.stem.split("]_")[-1] if "]_" in in_path.stem else "case"
    out_mp4 = BRANDED_DIR / f"{date_str}_[فيديو_تيكتوك_وريلز]_{cat_tag}.mp4"

    if out_mp4.exists() and out_mp4.stat().st_size > 50000:
        print(f"[*] 🎬 تم العثور على فيديو الريلز المولد اليوم ({out_mp4.name}) — استخدام الفيديو الجاهز فوراً.")
        return str(out_mp4)

    # البحث عن أحدث ملف صوتي من NotebookLM في مجلد audio_inputs
    audio_files = sorted(
        list(NOTEBOOK_AUDIO_DIR.glob("*.mp3")) + list(NOTEBOOK_AUDIO_DIR.glob("*.wav")) + list(NOTEBOOK_AUDIO_DIR.glob("*.m4a")),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    vf_filter = (
        f"zoompan=z='min(zoom+0.0012,1.15)':d={duration_sec}*25:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,"
        f"format=yuv420p"
    )

    if audio_files:
        chosen_audio = audio_files[0]
        print(f"[*] 🎙️ تم اكتشاف بودكاست NotebookLM صوتي ({chosen_audio.name}) — جاري دمجه في فيديو الريلز...")
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(in_path),
            "-i", str(chosen_audio),
            "-vf", vf_filter,
            "-c:v", "libx264", "-preset", "faster", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k",
            "-shortest", "-t", "60",
            str(out_mp4),
        ]
    else:
        print(f"[*] 🎬 جاري إنتاج فيديو Reels/TikTok متحرك ({duration_sec} ثوانٍ)...")
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(in_path),
            "-vf", vf_filter,
            "-t", str(duration_sec),
            "-c:v", "libx264", "-preset", "faster", "-pix_fmt", "yuv420p",
            str(out_mp4),
        ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
        if out_mp4.exists():
            print(f"[+] 🚀 تم إنشاء فيديو TikTok/Reels: {out_mp4.name}")
            return str(out_mp4)
    except Exception as e:
        print(f"[!] تنبيه إنشاء الفيديو: {e}")
    return ""


def export_canva_bulk_csv(cases_list: list):
    lines = ["Title,CategoryBadge,KeyTip,PromoCode,WhatsAppContact,TrackingLink"]
    for c in cases_list:
        title = c.get("title", "").replace(",", " ")
        cat = c.get("category", "c-section")
        code = "HT10"
        link = f"https://medon90ae.github.io/healing-touch-egypt/wa.html?case={cat}&code={code}"
        lines.append(f'"{title}","{cat}","استشارة مجانية مع أخصائية التعافي","{code}","201155803307","{link}"')
    BULK_CSV_PATH.write_text("\n".join(lines), encoding="utf-8-sig")


# =============================================================================
# 📝 القسم الرابع: محرك مدونات جوجل (Google Blogger) وحزمة Google NotebookLM
# =============================================================================
def format_clinical_case_for_blogger(case_data: dict, photo_info: dict) -> dict:
    title = case_data.get("title", "بروتوكول العناية الجراحية")
    cat = case_data.get("category", "c-section")
    raw_story = case_data.get("story_text", "")
    hashtags = case_data.get("hashtags", "")
    tags_list = [t.replace("#", "").strip() for t in hashtags.split() if t.startswith("#")]
    labels_str = ", ".join(tags_list[:6])

    paragraphs = raw_story.split("\n\n")
    html_paragraphs = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean or "واتساب:" in p_clean or "كود" in p_clean:
            continue
        if p_clean.startswith(("١.", "٢.", "٣.", "٤.")):
            lines = p_clean.split("\n")
            html_paragraphs.append(
                f'<div style="background:#F0FDF4; border-right:5px solid #10B981; padding:16px 20px; border-radius:10px; margin:16px 0;">'
                f'<h3 style="color:#065F46; margin:0 0 8px 0;">{lines[0]}</h3>'
                f'<p style="color:#1E293B; margin:0; line-height:1.7;">{"<br>".join(lines[1:])}</p></div>'
            )
        else:
            html_paragraphs.append(f'<p style="color:#334155; font-size:1.05rem; line-height:1.8;">{p_clean.replace(chr(10), "<br>")}</p>')

    tracking_link = f"https://medon90ae.github.io/healing-touch-egypt/wa.html?case={cat}&code=HT10"
    img_tag = (
        f'<div style="text-align:center; margin:24px 0;"><img src="{photo_info.get("image_url", "")}" alt="{title}" style="max-width:100%; border-radius:14px;" /></div>'
        if photo_info.get("image_url")
        else ""
    )

    full_html = f"""<div dir="rtl" style="font-family:'Cairo', sans-serif; max-width:800px; margin:auto; background:#fff; padding:24px; border-radius:16px; border:1px solid #E2E8F0;">
        <h1 style="color:#065F46;">{title}</h1>
        {img_tag}
        {"".join(html_paragraphs)}
        <div style="background:#ECFDF5; border:2px solid #10B981; border-radius:16px; padding:24px; text-align:center; margin-top:32px;">
            <h3 style="color:#065F46;">احصل على استشارة مجانية مع أخصائية العناية بالتعافي</h3>
            <a href="{tracking_link}" target="_blank" style="background:#25D366; color:#fff; padding:14px 28px; text-decoration:none; border-radius:12px; font-weight:bold; display:inline-block;">💬 تواصل عبر واتساب وتفعيل كود HT10</a>
        </div>
    </div>"""

    html_file = BLOGGER_DIR / f"blogger_{cat}.html"
    html_file.write_text(full_html, encoding="utf-8")
    return {"title": title, "labels": labels_str, "html_content": full_html, "file_path": str(html_file)}


def generate_blogger_atom_xml(posts_list: list) -> str:
    now_iso = dt.datetime.now(dt.timezone.utc).isoformat()
    entries = []
    for i, p in enumerate(posts_list):
        esc = p["html_content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        labels_xml = "\n".join([f'<category scheme="http://www.blogger.com/atom/ns#" term="{t.strip()}" />' for t in p["labels"].split(",") if t.strip()])
        entries.append(
            f"<entry><id>tag:blogger.com,1999:post-{i+1}</id><published>{now_iso}</published><updated>{now_iso}</updated>"
            f"<title type='text'>{p['title']}</title><content type='html'>{esc}</content>{labels_xml}</entry>"
        )
    xml_path = BLOGGER_DIR / "blogger_import_feed.xml"
    xml_path.write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom">'
        f"<title>مدونة هيلينج تاتش مصر</title><updated>{now_iso}</updated>{''.join(entries)}</feed>",
        encoding="utf-8",
    )
    return str(xml_path)


PRODUCT_PROMPT_CONFIGS = {
    "1": {
        "id": "3m-tegaderm-plus-pad",
        "name_ar": "ضمادة تيغاديرم الشفافة المقاومة للماء (3M Tegaderm +Pad Film)",
        "category": "c-section",
        "category_badge": "عزل مائي وحماية الجروح",
        "clinical_focus": "الاستحمام الآمن دون بلل للجرح، عزل ميكروبي 100% مع نفاذية لبخار العرق والغازات، حماية جروح القيصرية والعمليات الجراحية والقساطر",
        "target_keywords_egypt": [
            "لزقة تيجاديرم ضد الميه",
            "ضمادة 3M تيجاديرم",
            "الاستحمام بعد القيصرية",
            "بلاستر جروح العمليات ضد الماء",
            "غيار الجرح بعد العملية",
            "الاستحمام بعد الولادة القيصرية",
            "حماية جرح العملية من الماء",
            "لاصقة تيجاديرم في مصر"
        ],
        "long_tail_queries_egypt": [
            "امتى اقدر اخد شاور بعد عملية القيصرية بامان",
            "ازاي احمي جرح العملية من مية الشاور والصابون",
            "لزقة ضد المية للجروح في الصيدليات مصر",
            "شكل جرح القيصرية بعد اسبوع وطريقة تغييره",
            "علاج حساسية والتهاب الجلد من بلاستر الجروح العادي",
            "طريقة نزع ضمادة تيجاديرم بدون الم او شد للجلد"
        ],
        "egypt_hashtags": [
            "#الولادة_القيصرية_مصر",
            "#جرح_القيصرية",
            "#استحمام_بعد_العملية",
            "#تيجاديرم",
            "#صحة_المرأة_مصر",
            "#تعافي_الجروح_مصر",
            "#مستلزمات_طبية_مصر"
        ],
        "gemini_research_queries": [
            "3M Tegaderm waterproof dressing post-surgical wound showering protocol Cochrane guidelines",
            "Transepidermal water vapor transmission rate semipermeable film dressings surgical site infection",
            "Best practice post-cesarean wound care showering safety evidence-based review",
            "توقيت الاستحمام الآمن بعد الولادة القيصرية واستخدام الضمادات المقاومة للماء",
            "الفرق بين الشاش التقليدي وضمادات الفيلم الشفاف شبه المنفذة في منع التهاب الجروح"
        ],
        "pomelli_prompt_1_1": "Hyper-realistic clinical studio shot of genuine 3M Tegaderm +Pad sterile waterproof transparent film dressing resting on a pristine white medical tray, subtle sterile water droplets beading on the transparent surface demonstrating total water resistance, soft indirect natural lighting, modern high-end surgical suite aesthetic, 8k resolution, documentary medical photography, zero text clutter, authentic healthcare guidance.",
        "pomelli_prompt_9_16": "Vertical 9:16 aesthetic healthcare photography of 3M Tegaderm transparent waterproof dressing applied neatly over a simulated clean post-surgical dressing model, soft clinical morning light, clean teal and mint green background tones, ultra-realistic texture of breathable semi-permeable film, professional surgical recovery guide, 8k resolution.",
        "patient_anxieties": [
            "خوف المريضة من دخول الماء أو الصابون لخط الجرح أثناء الاستحمام وتسببه في التهاب أو صديد",
            "قلق المريضة من كتمة الجرح والتعرق تحت اللصقة إذا كانت غير مسامية",
            "ألم إزالة الضمادة وشدها للجلد المحيط بالجرح الحساس بعد العملية"
        ]
    },
    "2": {
        "id": "bupy-silicone-scar-sheet",
        "name_ar": "شيت السيليكون المطور للندبات (BUPY Medical Silicone Scar Sheet)",
        "category": "c-section",
        "category_badge": "علاج وتسطيح الندبات",
        "clinical_focus": "تسطيح ندبات القيصرية والجراحة، منع وعلاج الكيلويد والندبات المتضخمة، ترطيب ألياف الكولاجين وإزالة الحكة والاحمرار",
        "target_keywords_egypt": [
            "شيت سيليكون للندبات",
            "شيت سيليكون بوبي BUPY",
            "علاج ندبة القيصرية",
            "ازالة اثار الجروح والعمليات",
            "لاصقات سيليكون للندبات في مصر",
            "تسطيح الكلويد بعد الجراحة",
            "سيليكون شيت مصر",
            "علاج اثر خياطة القيصرية"
        ],
        "long_tail_queries_egypt": [
            "امتى ابدأ احط شيت السيليكون على جرح القيصرية",
            "ازاي اتخلص من خط القيصرية البارز والاحمر",
            "شيت سيليكون قابل للغسيل والاستخدام المتكرر",
            "افضل علاج للندبات البارزة والكيلويد في مصر",
            "ازاي اقلل الحكة والنغز في مكان جرح العملية",
            "الفرق بين جل السيليكون وشيت السيليكون للندبات"
        ],
        "egypt_hashtags": [
            "#علاج_الندبات_مصر",
            "#شيت_سيليكون",
            "#ندبة_القيصرية",
            "#تجميل_الجروح_مصر",
            "#كلويد",
            "#هيلينج_تاتش_مصر",
            "#ندبات_العمليات"
        ],
        "gemini_research_queries": [
            "Medical grade silicone gel sheeting hypertrophic scar keloid clinical trials PubMed",
            "Mechanism of action silicone sheet stratum corneum hydration collagen downregulation",
            "Optimal duration daily wear silicone scar sheets post-operative scar management",
            "بروتوكول تسطيح ندبة القيصرية بشيت السيليكون الطبي ومدة الاستخدام اليومي",
            "علاج الكلويد والندبات المتضخمة بعد العمليات الجراحية بدون تدخل جراحي"
        ],
        "pomelli_prompt_1_1": "Commercial clinical aesthetic photography of BUPY Medical Silicone Scar Sheet roll partially unrolled on a clean neutral stone surface, ultra-soft flexible medical-grade silicone texture catching gentle diffuse lighting, elegant minimalist dermatology clinic setting, 8k resolution, authentic medical realism, zero commercial graphics, calm reassuring healthcare visual.",
        "pomelli_prompt_9_16": "Vertical 9:16 editorial dermatology photograph showing translucent BUPY silicone scar sheet being gently held with medical tweezers above a clean clinical sterile field, soft green and neutral tones, demonstrating smooth flexible elasticity, professional scar therapy guidance aesthetic, 8k hyper-realistic.",
        "patient_anxieties": [
            "خوف المريضة من تحول خط الجرح إلى حبل بارز أحمر أو كلويد دائم يشوه المظهر",
            "الحكة الشديدة والنغزات المزعجة في مكان الندبة التي تجعل لمس الملابس مؤلماً",
            "الشكوك حول فاعلية منتجات علاج الندبات بعد شهور من العملية وهل ما زال الوقت متاحاً للعلاج"
        ]
    },
    "3": {
        "id": "3m-micropore-tan-tape-1533-0",
        "name_ar": "شريط ميكروبور الطبي الملون (3M Micropore Tan Surgical Tape 1533-0)",
        "category": "rhinoplasty",
        "category_badge": "دعم الأنف وجروح الرقبة",
        "clinical_focus": "تثبيت الأنف بعد عمليات التجميل وتصريف التورم اللمفاوي، حماية ندبات الرقبة وجراحة الغدة من أشعة الشمس، شريط ورقي طبي مسامي مضاد للحساسية",
        "target_keywords_egypt": [
            "بلاستر 3M بيج",
            "شريط ميكروبور تان 1533-0",
            "لصقات الانف بعد التجميل",
            "تثبيت الانف بعد العمليه",
            "حماية ندبة الغدة الدرقية من الشمس",
            "بلاستر طبي مضاد للحساسية",
            "بلاستر تجميل الانف 3m مصر",
            "شريط ورقي طبي مسامي"
        ],
        "long_tail_queries_egypt": [
            "طريقة وضع بلاستر تجميل الانف لتصريف التورم",
            "لصقات الانف بعد العملية 3m الاصلية في مصر",
            "ازاي احمي جرح الرقبة والغدة من الاسمرار والشمس",
            "حل الحبوب والبثور تحت بلاستر الانف في الصيف",
            "الفرق بين البلاستر الورقي العادي وبلاستر 3M المسامي",
            "كم مدة وضع بلاستر الانف بعد فك الجبيرة"
        ],
        "egypt_hashtags": [
            "#تجميل_الانف_مصر",
            "#بلاستر_الانف",
            "#تورم_الانف_بعد_التجميل",
            "#جراحة_الغدة_الدرقية",
            "#تجميل_مصر",
            "#راينوبلاستي_مصر",
            "#بلاستك_سيرجري_مصر"
        ],
        "gemini_research_queries": [
            "Post-rhinoplasty taping with microporous surgical tape supratip edema reduction clinical study",
            "Rayon microporous surgical tape skin irritation hypoallergenic properties randomized trial",
            "Sun protection for fresh surgical scars thyroidectomy neck incision micropore tape",
            "طريقة لصق بلاستر 3M البيج لتصريف تورم أرنبة الأنف بعد إزالة الجبيرة",
            "حماية جرح استئصال الغدة الدرقية في الرقبة من أشعة الشمس والتصبغ"
        ],
        "pomelli_prompt_1_1": "Macro clinical studio photograph of authentic 3M Micropore Tan surgical tape rolls with textured breathable rayon weave, positioned on a frosted glass surface next to a surgical caliper, soft clinical ring light, pristine sterile atmosphere, 8k resolution, realistic medical photography.",
        "pomelli_prompt_9_16": "Vertical 9:16 aesthetic medical visual of 3M beige micropore tape strips arranged neatly on a surgical tray, subtle shadows, calm aesthetic surgery clinic ambiance, demonstrating fine porosity and skin-tone blend, professional medical guidance realism, 8k.",
        "patient_anxieties": [
            "الذعر من تورم أرنبة الأنف أو عدم تناسق النزول بعد فك الجبيرة",
            "ظهور حبوب صديدية وبثور بيضاء وحساسية جلدية بسبب اللصقات العادية الرديئة المكتومة",
            "تصبغ خط جرح الغدة في الرقبة وتحوله إلى لون داكن دائم بسبب التعرض للشمس"
        ]
    },
    "4": {
        "id": "silicone-nostril-retainer",
        "name_ar": "دعامات الأنف السيليكونية الطبية (Silicone Nostril Retainer)",
        "category": "rhinoplasty",
        "category_badge": "تناسق فتحات الأنف",
        "clinical_focus": "الحفاظ على تماثل وتناسق فتحات الأنف بعد عمليات التجميل، مقاومة قوى الانكماش الندبي للغضاريف، دعم مجرى التنفس بعد قص جناح الأنف",
        "target_keywords_egypt": [
            "دعامات الانف السيليكون",
            "نوستريل ريتينر مصر",
            "تماثل فتحات الانف بعد التجميل",
            "منع انكماش فتحات الانف",
            "دعامات السيليكون بعد تصغير الانف",
            "مجرى التنفس بعد تجميل الانف",
            "مقاسات دعامات الانف السيليكونية"
        ],
        "long_tail_queries_egypt": [
            "ازاي احافظ على تماثل فتحات الانف بعد عملية التجميل",
            "امتى البس دعامة الانف السيليكون وكم ساعة في اليوم",
            "طريقة تنظيف وتعقيم دعامات فتحات الانف في البيت",
            "علاج انسداد وصعوبة التنفس بعد قص جناح الانف",
            "ازاي اختار مقاس دعامة الانف السيليكونية المناسب لحالتي"
        ],
        "egypt_hashtags": [
            "#تجميل_الانف_مصر",
            "#فتحات_الانف",
            "#دعامات_الانف",
            "#جراحة_التجميل_مصر",
            "#تنفس_افضل",
            "#عمليات_التجميل_مصر"
        ],
        "gemini_research_queries": [
            "Silicone nostril retainer post-rhinoplasty alar base symmetry clinical evaluation",
            "Prevention of nostril stenosis and cicatricial contraction after cosmetic rhinoplasty",
            "Nostril retainer sizing and care protocol post-operative rhinoplasty MDPI studies",
            "أهمية دعامة الأنف السيليكون في تماثل الفتحات ومنع التليف بعد التجميل",
            "كيفية تنظيف واختيار مقاس دعامة الأنف السيليكونية بعد العملية"
        ],
        "pomelli_prompt_1_1": "Ultra-clean clinical macro photography of medical-grade transparent silicone nostril retainers resting in a sterile petri dish on a white examination surface, gentle diffuse LED lighting, crystal-clear anatomical curved contours, surgical precision, 8k resolution, authoritative clinical clarity.",
        "pomelli_prompt_9_16": "Vertical 9:16 high-end surgical photography of medical silicone nostril retainer held delicately in sterile gloved fingers, soft clinical background, showcasing flexible medical silicone softness and ergonomic contouring, reassuring medical educational aesthetic, 8k.",
        "patient_anxieties": [
            "قلق المريض من وجود فتحة أنف أكبر من الأخرى أو انكماش فتحة بعد العملية",
            "صعوبة التنفس أو تضيق مجرى الهواء أثناء نوم المريض في الأسابيع الأولى",
            "الخوف من ألم ارتداء الدعامة أو تسببها في تجريح الأنسجة الداخلية الحساسة"
        ]
    },
    "5": {
        "id": "smith-nephew-opsite-spray",
        "name_ar": "سبراي أوبسايت العازل للجروح (Smith & Nephew Opsite Post-Op Spray)",
        "category": "bariatric",
        "category_badge": "عزل ثقوب المناظير",
        "clinical_focus": "عزل فوري لثقوب مناظير جراحات السمنة والتكميم، حاجز ميكروبي شفاف مقاوم للماء يتيح الاستحمام، يتيح تنفس الجلد وتبخر العرق دون غيارات لاصقة مؤلمة",
        "target_keywords_egypt": [
            "سبراي اوبسايت للجروح",
            "بخاخ opsite بعد التكميم",
            "عزل ثقوب منظار التكميم",
            "الاستحمام بعد عملية التكميم",
            "سبراي عازل للماء للجروح",
            "علاج التهاب الجلد من بلاستر المنظار",
            "بخاخ اوبسايت في مصر"
        ],
        "long_tail_queries_egypt": [
            "ازاي اخد شاور بعد عملية التكميم بثقوب المنظار بامان",
            "طريقة رش سبراي اوبسايت على ثقوب المنظار",
            "بديل البلاستر اللاصق لثقوب منظار المرارة والتكميم",
            "متى تلتئم جروح وثقوب منظار التكميم في البطن",
            "حماية ثقوب المنظار من العرق والتلوث في الصيف بمصر"
        ],
        "egypt_hashtags": [
            "#تكميم_المعدة_مصر",
            "#جراحة_السمنة_مصر",
            "#ثقوب_المنظار",
            "#سبراي_اوبسايت",
            "#شاور_بعد_العملية",
            "#تعافي_التكميم_مصر"
        ],
        "gemini_research_queries": [
            "Smith Nephew Opsite spray transparent dressing laparoscopic port site infection Cochrane",
            "Waterproof spray-on dressing bariatric sleeve gastrectomy recovery showering protocol",
            "Comparative study spray dressings vs conventional adhesive tapes in laparoscopic wounds",
            "طريقة استخدام سبراي أوبسايت على ثقوب منظار التكميم والاستحمام الفوري",
            "علاج تحسس والتهاب جلد البطن من بلاستر ثقوب المنظار بعد جراحة السمنة"
        ],
        "pomelli_prompt_1_1": "Crisp pharmaceutical studio photograph of Smith & Nephew Opsite Post-Op Spray canister on a clean surgical steel surface, fine transparent micro-mist droplets catching soft edge lighting, modern laparoscopic surgery clinic context, 8k resolution, authentic medical realism.",
        "pomelli_prompt_9_16": "Vertical 9:16 healthcare commercial photograph showing transparent Opsite aerosol spray canister next to clean sterile gauze on a minimalist teal clinical background, soft natural lighting, highlighting waterproof breathable barrier concept, professional surgical recovery guide, 8k.",
        "patient_anxieties": [
            "المعاناة من ألم نزع البلاستر المتكرر من جلد البطن الحساس والتهابه بعد التكميم",
            "الخوف من التهاب ثقوب المنظار أو تلوثها بمياه الاستحمام",
            "الحاجة لحل سريع وعازل يسمح بحرية الحركة والاستحمام دون الحاجة لغيارات معقدة"
        ]
    },
    "6": {
        "id": "all-clinical-solutions",
        "name_ar": "المحفظة السريرية الشاملة - كافة المنتجات الخمسة المعتمدة لهيلينج تاتش مصر",
        "category": "all",
        "category_badge": "بروتوكولات التعافي الجراحي المتكاملة",
        "clinical_focus": "الحلول السريرية المتكاملة لمنع الندبات، عزل الجروح المقاوم للماء، تثبيت تجميل الأنف، وتأمين ثقوب المناظير بعد العمليات الجراحية في مصر",
        "target_keywords_egypt": [
            "مستلزمات التعافي بعد الجراحة في مصر",
            "شيت سيليكون للندبات مصر",
            "ضمادات تيجاديرم ضد الماء",
            "بلاستر 3M تجميل الانف",
            "دعامات الانف السيليكونية",
            "سبراي اوبسايت للجروح",
            "بروتوكول هيلينج تاتش مصر"
        ],
        "long_tail_queries_egypt": [
            "افضل روتين للعناية بالجروح بعد العمليات الجراحية في مصر",
            "ازاي احمي جرح العملية من التلوث والماء بعد الخروج من المستشفى",
            "طرق منع تكون الندبات البارزة والكلويد بعد العمليات",
            "مستلزمات طبية معتمدة للتعافي بعد التجميل والقيصرية والتكميم"
        ],
        "egypt_hashtags": [
            "#جراحة_مصر",
            "#تعافي_الجروح_مصر",
            "#الولادة_القيصرية_مصر",
            "#تجميل_الانف_مصر",
            "#تكميم_المعدة_مصر",
            "#هيلينج_تاتش_مصر"
        ],
        "gemini_research_queries": [
            "Comprehensive post-operative wound care and scar prevention evidence-based guidelines",
            "Comparative efficacy of modern silicone dressings vs traditional wound dressings",
            "Best clinical practices for outpatient surgical recovery in warm climates"
        ],
        "pomelli_prompt_1_1": "Luxury pharmaceutical commercial flatlay photograph of Healing Touch Egypt surgical recovery collection: 3M Tegaderm dressing, BUPY silicone scar sheet roll, 3M Micropore tan tape, silicone nostril retainers, and Opsite spray arranged elegantly on clean white marble, soft natural morning clinic lighting, pristine sterile aesthetic, 8k resolution, documentary medical photography.",
        "pomelli_prompt_9_16": "Vertical 9:16 clinical editorial photograph showcasing the complete surgical recovery essentials kit by Healing Touch Egypt on a frosted glass tray, soft teal medical background, warm clinical lighting, conveying total recovery reassurance and sterile excellence, 8k.",
        "patient_anxieties": [
            "الحيرة والتشتت في اختيار المستلزمات الطبية الأصلية بعد الخروج من المستشفى",
            "الخوف من حدوث مضاعفات أو تلوث الجرح بسبب سوء العناية في المنزل",
            "الحاجة لتوجيه سريري موثوق من أخصائيين يفهمون طبيعة الجرح وتوقيت كل خطوة"
        ]
    }
}


def prompt_user_for_product_selection() -> str:
    """عرض قائمة تفاعلية للمستخدم لاختيار المنتج المطلوب للتركيز عليه في برومبتات اليوم."""
    print("\n" + "=" * 68)
    print("🌿 هيلينج تاتش مصر | اختر المنتج الطبي ليكون محور البحث والمحتوى اليوم:")
    print("=" * 68)
    print("  [1] ضمادة تيغاديرم الشفافة المقاومة للماء (3M Tegaderm +Pad Film)")
    print("      • المحور: الاستحمام الآمن دون بلل، حماية الجروح والعمليات والقساطر")
    print("  [2] شيت السيليكون المطور للندبات (BUPY Medical Silicone Scar Sheet)")
    print("      • المحور: علاج وتسطيح ندبات القيصرية والجراحة، منع الكيلويد، ترطيب الكولاجين")
    print("  [3] شريط ميكروبور الطبي الملون (3M Micropore Tan Surgical Tape 1533-0)")
    print("      • المحور: تثبيت الأنف بعد التجميل، وقاية ندبات الغدة والرقبة من الشمس")
    print("  [4] دعامات الأنف السيليكونية الطبية (Silicone Nostril Retainer)")
    print("      • المحور: دعم فتحات الأنف، منع انكماش الغضاريف وتماثل الأنف بعد التجميل")
    print("  [5] سبراي أوبسايت العازل للجروح (Smith & Nephew Opsite Post-Op Spray)")
    print("      • المحور: عزل ثقوب مناظير التكميم والسمنة، حاجز ميكروبي فوري شفاف")
    print("  [6] إعداد حزمة شاملة لجميع المنتجات الخمسة معاً")
    print("=" * 68)
    
    choice = ""
    try:
        choice = input("اختر رقم المنتج (1-6) [اضغط Enter لاختيار 1 افتراضياً]: ").strip()
    except Exception:
        choice = "1"
        
    if choice not in ("1", "2", "3", "4", "5", "6"):
        choice = "1"
    return choice


def export_notebooklm_master_source(product_choice: str = None, interactive: bool = False) -> str:
    """تجهيز ملف المعرفة والبرومبت الموحد الشامل الجاهز للرفع المباشر في Google NotebookLM مع برومبتات مخصصة لكل منصة ومصادر PubMed وسيو مصر."""
    if product_choice is None:
        if interactive and sys.stdin and sys.stdin.isatty():
            product_choice = prompt_user_for_product_selection()
        else:
            product_choice = "1"
            
    is_all = product_choice == "6"
    selected_cfg = PRODUCT_PROMPT_CONFIGS.get(product_choice, PRODUCT_PROMPT_CONFIGS["1"])
    prod_name = selected_cfg["name_ar"]

    now = datetime.now()
    date_display = now.strftime("%Y-%m-%d %I:%M %p")
    timestamp_filename = now.strftime("%Y-%m-%d_%H-%M-%S")

    # 1. جلب رادار ترندات بحث جوجل مصر الصاعدة والكلمات الأكثر بحثاً
    live_trend_queries = []
    rising_breakouts = []
    try:
        from github_seo_trend_engine import harvest_live_egypt_trends
        live_map = harvest_live_egypt_trends()
        cat_key = selected_cfg["category"]
        if cat_key == "all":
            for c, q_list in live_map.items():
                for q in q_list:
                    if q not in live_trend_queries:
                        live_trend_queries.append(q)
        else:
            live_trend_queries = live_map.get(cat_key, [])

        live_reg_path = BASE_DIR / "media_assets" / "live_trends_registry.json"
        if live_reg_path.exists():
            try:
                reg_json = json.loads(live_reg_path.read_text(encoding="utf-8"))
                rising_breakouts = [rb.get("query", "") for rb in reg_json.get("rising_breakouts", []) if rb.get("query")]
            except Exception:
                pass
    except Exception as e:
        print(f"[!] تنبيه جلب ترندات مصر: {e}")

    # 2. استكشاف أحدث الأبحاث السريرية الحقيقية من PubMed / NCBI لهذا المنتج
    discovered_studies = []
    try:
        from clinical_research_harvester import harvest_pubmed_studies
        print(f"\n[*] 🔬 جاري استكشاف أحدث الأبحاث والدراسات السريرية من PubMed / NCBI لـ ({prod_name})...")
        search_target = "1" if is_all else product_choice
        discovered_studies = harvest_pubmed_studies(search_target, max_results=3)
        if discovered_studies:
            print(f"[+] 📚 تم رصد وتوثيق {len(discovered_studies)} أبحاث طبية جديدة في الموسوعة وسجل الأبحاث:")
            for s in discovered_studies:
                print(f"    • [{s['pub_year']}] {s['title'][:70]}...")
                print(f"      🔗 {s['url']}")
    except Exception as e:
        print(f"[!] تنبيه استكشاف PubMed: {e}")

    # تحضير الكلمات الدلالية والأسئلة والهاشتاجات لمصر
    target_kws = selected_cfg.get("target_keywords_egypt", [])
    long_tails = selected_cfg.get("long_tail_queries_egypt", [])
    hashtags_list = selected_cfg.get("egypt_hashtags", [])

    kws_joined = "، ".join(target_kws[:6])
    long_tails_formatted = "\n".join([f"• {lt}" for lt in long_tails[:5]])
    live_trends_formatted = "\n".join([f"• {tq}" for tq in live_trend_queries[:6]]) if live_trend_queries else "• جرح العملية وطرق الاستحمام\n• منع الندبات بعد الجراحة"
    hashtags_joined = " ".join(hashtags_list)

    pubmed_refs_text = ""
    if discovered_studies:
        pubmed_refs_text = "\n".join([f"• [{s['pub_year']}] {s['title']} -> {s['url']}" for s in discovered_studies])
    else:
        pubmed_refs_text = "• [NCBI/PMC2918339] The Efficacy of Silicone Gel for Treatment of Scars -> https://pmc.ncbi.nlm.nih.gov/articles/PMC2918339/\n• [PubMed 28570253] Review of Silicone Gel Sheeting for Scar Prevention -> https://pubmed.ncbi.nlm.nih.gov/28570253/"

    # 3. بناء ملف البرومبتات الشامل PROMPTS_PACK_TODAY.txt و .md
    prompts_pack_lines = [
        "=====================================================================",
        "🌿 هيلينج تاتش مصر | حزمة البرومبتات وأوامر السيو للمنصات (SEO EGYPT 2026)",
        f"🎯 المنتج ومحور التركيز: {prod_name}",
        f"📅 تاريخ ووقت التوليد: {date_display}",
        "📍 النطاق الجغرافي المستهدف: جمهورية مصر العربية (Local SEO & Audience - Egypt)",
        "=====================================================================",
        "",
        "---------------------------------------------------------------------",
        "🔥 رادار ترندات بحث جوجل مصر والكلمات الصاعدة (Google Search Trends Egypt):",
        "---------------------------------------------------------------------",
        "📌 الكلمات المفتاحية الأساسية المستهدفة بمصر (Focus Keywords):",
    ]
    for kw in target_kws:
        prompts_pack_lines.append(f"  • {kw}")
    prompts_pack_lines.extend([
        "",
        "📌 الجمل والأسئلة البحثية الطويلة الأكثر تداولاً في مصر (Long-Tail Patient Inquiries):",
    ])
    for lt in long_tails:
        prompts_pack_lines.append(f"  • {lt}")
    if live_trend_queries:
        prompts_pack_lines.extend([
            "",
            "📌 تساؤلات ومصطلحات بحث جوجل مصر الصاعدة هذا الأسبوع (Google Suggest gl=eg):",
        ])
        for tq in live_trend_queries[:8]:
            prompts_pack_lines.append(f"  • {tq}")
    if rising_breakouts:
        prompts_pack_lines.extend([
            "",
            "⚡ كلمات صاعدة حديثاً برادار الترندات (Rising Breakouts):",
        ])
        for rb in rising_breakouts[:4]:
            prompts_pack_lines.append(f"  • {rb}")
    prompts_pack_lines.extend([
        "",
        f"📌 الهاشتاجات السريرية المقترحة للمنصات داخل مصر: {hashtags_joined}",
        "",
        "=====================================================================",
        "1️⃣ برومبت البحث المعمق في Gemini Deep Research (أبحاث سريرية وترندات مصر):",
        "=====================================================================",
        "```text",
        "بصفتك باحثاً إكلينيكياً واستشارياً في جراحة التعافي وعلاج الندبات في مصر:",
        f"أريد بحثاً سريرياً دقيقاً وموثقاً حول: {selected_cfg['clinical_focus']}.",
        "",
        "الأسئلة السريرية والبحثية المحددة المطلوب الإجابة عليها تفصيلياً:",
    ])
    for q in selected_cfg["gemini_research_queries"]:
        prompts_pack_lines.append(f"• {q}")
    prompts_pack_lines.extend([
        "",
        "مخاوف وتساؤلات المرضى المقلقة في مصر المطلوب طمأنتهم علمياً بشأنها:",
    ])
    for anz in selected_cfg["patient_anxieties"]:
        prompts_pack_lines.append(f"• {anz}")
    prompts_pack_lines.extend([
        "",
        "تساؤلات وترندات بحث جوجل مصر الصاعدة هذا الأسبوع للإجابة عليها:",
        live_trends_formatted,
        "",
        "الشروط الصارمة للمحتوى الناتج:",
        "1. نبرة طبية توجيهية هادئة تشرح فسيولوجيا التئام الأنسجة وتبدد المخاوف دون تهويل.",
        "2. استهداف الجمهور المصري وتقديم إجابات تناسب الظروف البيئية والصحية في مصر (كالصيف والعرق وطريقة الغيار المنزلي).",
        "3. منع تام لأي عروض تسويقية أو خصومات أو أسعار؛ التركيز 100% على الإرشاد والدعم والتثقيف الصحي.",
        "4. إدراج توجيه واضح للتواصل مع أخصائي التعافي عبر واتساب 01155803307 بكود الأولوية السريرية HT10.",
        "",
        "روابط أحدث أبحاث PubMed السريرية المعتمدة للاستشهاد بها ودعم المحتوى:",
        pubmed_refs_text,
        "```",
        "",
        "=====================================================================",
        "2️⃣ برومبتات توليد الصور الطبية في Google Pomelli (صور واقعية سريرية 4K):",
        "=====================================================================",
        "📌 [أولاً: مقاس البوست المربع 1:1 - مخصص للموقع وفيسبوك وإنستجرام Feed]:",
        "```text",
        selected_cfg["pomelli_prompt_1_1"],
        "```",
        "",
        "📌 [ثانياً: مقاس الستوري والريلز العمودي 9:16 - مخصص لإنستجرام وتيك توك وستوري]:",
        "```text",
        selected_cfg["pomelli_prompt_9_16"],
        "```",
        "",
        "=====================================================================",
        "3️⃣ برومبتات استوديو Google NotebookLM (أدوات Video Overview و Audio Overview):",
        "=====================================================================",
        "📌 [أمر الفيديو التوضيحي Video Overview]:",
        "```text",
        f"أنشئ فيديو شارحاً تفاعلياً (Explainer Video) لحالة التعافي باستخدام {prod_name} يركز على بيولوجيا التئام الأنسجة وطريقة العناية السليمة بالخطوات، بنبرة طمأنينة علمية راقية تجيب على قلق المريض المصري من الندبات والالتهاب ومخاوف الاستحمام، مع التنويه لحق معاينة الشحنة قبل الاستلام والتواصل واتساب 01155803307 بكود HT10.",
        "```",
        "",
        "📌 [أمر البودكاست الصوتي Audio Overview (حوار استشاري سريري)]:",
        "```text",
        f"قم بتوليد حوار صوتي بين اثنين من استشاريي التعافي الطبي باللهجة المصرية الراقية يشرحان فيه بأسلوب ودي مريح للمريض أهمية {prod_name} في مرحلة التعافي، وكيفية التغلب على الحكة أو القلق بعد العملية وتصحيح المفاهيم الخاطئة الشائعة في مصر.",
        "```",
        "",
        "=====================================================================",
        "4️⃣ برومبت إنتاج محتوى وسيو يوتيوب مصر (YouTube Long-form Video + Shorts SEO):",
        "=====================================================================",
        "```text",
        "بصفتك كبير استشاريي إنتاج الفيديو الطبي والسيو السريري في مصر (Clinical Video SEO Specialist - Egypt):",
        f"نحن نطبق استراتيجية سيو متقدمة موجهة لمحركات بحث يوتيوب وجوجل في جمهورية مصر العربية (Local Video SEO Egypt) لمساعدة المرضى بعد العمليات الجراحية والتجميلية.",
        f"الموضوع السريري: {prod_name} - {selected_cfg['clinical_focus']}.",
        "",
        "الكلمات المفتاحية الإلزامية التي يجب تضمينها بشكل طبيعي في العنوان والوصف والسكريبت:",
        f"• {kws_joined}",
        "",
        "الأسئلة الأكثر بحثاً في مصر المطلوب الإجابة عليها بالفيديو:",
        long_tails_formatted,
        "",
        "المطلوب إنتاجه تفصيلياً وبدقة تامة:",
        "1. [العنوان السريري الجذاب]: عنوان أقل من 60 حرفاً يدمج الكلمة المفتاحية الأولى ويثير الطمأنينة بدون أي تهويل أو كليك بيت تجاري.",
        "2. [سكريبت الفيديو الكامل 16:9 (مدته 3 إلى 5 دقائق)]:",
        "   • أول 15 ثانية (Hook): مخاطبة مباشرة لأكبر خوف يقلق المريض المصري بعد العملية (كالاستحمام أو شكل الجرح).",
        "   • الدقيقة 1-2 (فسيولوجيا الأنسجة): شرح مبسط لكيفية تعافي الجرح ولماذا الطرق التقليدية المتبعة في البيوت تضر بالأنسجة.",
        "   • الدقيقة 2-4 (البروتوكول السريري العملي): خطوات العناية العملية بالترتيب باستخدام المستلزم الطبي الأصلي بأمان.",
        "   • الخاتمة (CTA): طمأنة المريض والتوجيه الهادئ لطلب استشارة سريرية مجانية من أخصائي التعافي عبر واتساب 01155803307 مع كود المعاينة والشحن المجاني HT10.",
        "3. [سكريبت شورتس عمودي 9:16 (أقل من 59 ثانية)]: سكريبت سريع، مركز، يعالج سؤالاً واحداً ملحاً بصورة مكثفة.",
        "4. [وصف الفيديو المهيأ لسيو يوتيوب مصر SEO Description]:",
        "   • فقرة افتتاحية غنية بالكلمات المفتاحية.",
        "   • الطوابع الزمنية والفصول (Timestamps / Chapters).",
        "   • روابط المراجع الطبية المرفقة أدناه ورابط البوابة (https://medon90ae.github.io/healing-touch-egypt/portal/).",
        "5. [قائمة التاغات الدلالية Tags]: 20 تاغ بحثي نشط في يوتيوب مصر مفصولة بفواصل.",
        "",
        "القواعد الإلزامية: منع تام لذكر أي أسعار أو خصومات؛ كود HT10 يمنح حق المعاينة وفتح الشحنة قبل الاستلام مع شحن مجاني؛ النبرة طبية توجيهية وقورة.",
        "```",
        "",
        "=====================================================================",
        "5️⃣ برومبت فيديو تيك توك مصر (TikTok Egypt SEO Script & Viral Hook):",
        "=====================================================================",
        "```text",
        "بصفتك صانع محتوى طبي رقمي متخصص في خوارزميات تيك توك في مصر (TikTok Medical SEO - Egypt):",
        f"نحن نستهدف خوارزمية تيك توك والجمهور المصري المهتم بالتعافي بعد العمليات (القيصرية / التجميل / المناظير).",
        f"الموضوع السريري: {prod_name} - {selected_cfg['clinical_focus']}.",
        f"الكلمات والعبارات المستهدفة بمصر: {kws_joined}",
        "",
        "المطلوب إنتاجه بدقة تامة:",
        "1. [الهوك البصري والنفسي في أول ثانيتين]: جملة افتتاحية قوية تظهر على الشاشة وتنطق فوراً لتوقف التمرير (مثلاً: 'لو لسه خارج من العمليات في مصر ومرعوب من مية الشاور.. ركز في الكام ثانية دول').",
        "2. [سكريبت الفيديو (مدة 45 إلى 55 ثانية)]:",
        "   • اللهجة: لهجة مصرية بيضاء راقية ومحترمة (تجمع بين الوقار الطبي واللغة القريبة من المريض المصري).",
        "   • توجيهات المشاهد (Visual & B-roll Cues): كتابة ما يظهر في الكادر وما يقوم به مقدم الفيديو بالتفصيل بين أقواس.",
        "   • النص المكتوب على الشاشة (On-Screen Text): العبارات الرئيسية التي تظهر أثناء الحديث لتثبيت المعلومة السريرية.",
        "   • تقديم المعلومة السريرية المنقذة والحل الصحيح بهدوء دون استعجال.",
        "3. [الكابشن والهاشتاجات]:",
        "   • كابشن تيك توك قصير ومحفز يحث على حفظ الفيديو (Save).",
        f"   • هاشتاجات سيو تيك توك في مصر: {hashtags_joined}",
        "```",
        "",
        "=====================================================================",
        "6️⃣ برومبت إنستجرام مصر (Instagram Reels & Clinical Carousel Guide):",
        "=====================================================================",
        "```text",
        "بصفتك مصمم محتوى سريري واستراتيجي إنستجرام في مصر (Instagram Medical Content & SEO Egypt):",
        f"المحتوى مخصص للجمهور المصري على إنستجرام مع مراعاة السيو الداخلي لإنستجرام (Instagram Search SEO - Egypt).",
        f"الموضوع السريري: {prod_name} - {selected_cfg['clinical_focus']}.",
        f"الكلمات المستهدفة: {kws_joined}",
        "",
        "المطلوب إنتاجه:",
        "1. [دليل الكاروسيل السريري (Clinical Carousel - 7 شرائح توعوية)]:",
        "   • الشريحة 1 (الغلاف): عنوان عريض يبرز الخطأ الشائع في رعاية الجروح بعد العمليات في مصر.",
        "   • الشريحة 2 (المشكلة الحقيقية): مخاوف المرضى الواقعية (التهاب، عرق في الصيف، بقع داكنة، ألم نزع الغيار).",
        "   • الشريحة 3 (الفسيولوجيا): ماذا يحدث لطبقات الجلد وألياف الكولاجين علمياً؟",
        "   • الشريحة 4 و 5 (الحل العملي خطوة بخطوة): كيف تطبق المستلزم الطبي بصورة صحيحة وبأمان؟",
        "   • الشريحة 6 (الدليل العلمي): استشهاد سريع بإحدى دراسات PubMed المرفقة أدناه لتعزيز الثقة الطبية.",
        "   • الشريحة 7 (الخاتمة): بطاقة التوجيه السريري المجاني عبر واتساب 01155803307 بكود HT10 وحق المعاينة قبل الاستلام.",
        "2. [سكريبت ريلز عمودي 9:16 (50 ثانية)]: نص مريح للعين مع توجيه بصري واضح.",
        f"3. [كابشن إنستجرام المهيأ للسيو]: نص منسق بالرموز التعبيرية الطبية وهاشتاجات إنستجرام مصر: {hashtags_joined}.",
        "```",
        "",
        "=====================================================================",
        "7️⃣ برومبت مقال مدونة بلوجر (Blogger Medical Blog Post - Google Search Egypt SEO):",
        "=====================================================================",
        "```text",
        "بصفتك كبير كتاب المحتوى الطبي واستشاري السيو المتخصص في محرك بحث جوجل مصر (Google Search SEO gl=eg & Medical E-E-A-T):",
        "نريد كتابة مقال طبي استشاري شامل ومطول (1200 إلى 1500 كلمة) مهيأ للتصدر في المرتبة الأولى بنتائج بحث جوجل في جمهورية مصر العربية.",
        f"الكلمة المفتاحية الرئيسية (Focus Keyword): {target_kws[0] if target_kws else prod_name}",
        f"الكلمات المفتاحية الثانوية (Secondary Keywords): {kws_joined}",
        "الأسئلة الطويلة وتساؤلات محرك البحث في مصر (Long-tail Inquiries):",
        long_tails_formatted,
        "",
        "الهيكل الإلزامي للمقال:",
        "1. [عنوان المقال الرئيسي H1]: مدمج فيه الكلمة المفتاحية الرئيسية والهدف الجغرافي (مصر) مع وعد سريري واضح وموثوق.",
        "2. [المقدمة السريرية]: كسر المخاوف وشرح فسيولوجيا مرحلة التعافي بأسلوب مطمئن وموجه للقارئ المصري.",
        "3. [عناوين فرعية H2 و H3]: تجيب مباشرة وبدقة على الأسئلة الشائعة التي يبحث عنها المصريون في جوجل.",
        "4. [جدول مقارنة سريري (HTML Table)]: مقارنة موضوعية بين 'العناية التقليدية (الشاش والبلاستر العادي)' و 'البروتوكول السريري المعتمد'.",
        "5. [قسم الأدلة السريرية والدراسات]: الاستشهاد المباشر بدراسات PubMed المرفقة أدناه مع أرقام PMID.",
        "6. [قسم الأسئلة الشائعة FAQ بتنسيق Schema]: 4 أسئلة حيوية وإجاباتها السريرية المباشرة (مثل: الاستحمام، العرق في الصيف، مدة العلاج، طريقة إزالة الغيار).",
        "7. [الروابط الداخلية ودعوة اتخاذ الإجراء CTA]: التوجيه لزيارة البوابة التفاعلية (https://medon90ae.github.io/healing-touch-egypt/portal/) والتواصل السريري المجاني عبر واتساب 01155803307 مع كود الفحص قبل الاستلام HT10.",
        "8. [الوصف التعريفي Meta Description]: 155 حرفاً جذاباً ومحفزاً للنقر على نتائج بحث جوجل مصر.",
        "```",
        "",
        "=====================================================================",
        "8️⃣ برومبت مجتمعات ريديت (Reddit - r/Egypt & r/AskEgypt Discussion Post):",
        "=====================================================================",
        "```text",
        "بصفتك أخصائي رعاية صحية تشارك خبرتك السريرية في مجتمعات ريديت المصرية (r/Egypt و r/AskEgypt):",
        "نريد كتابة منشور نقاشي استشاري غير دعائي تماماً (Non-promotional Clinical Discussion) يهدف لتثقيف المرضى بعد العمليات وتصحيح المفاهيم الخاطئة الشائعة في مصر.",
        f"الموضوع: نصائح عملية وإكلينيكية للتعامل مع الجروح بعد العمليات في مصر وتفادي الندبات ومضاعفات الماء والالتهاب الخاصة بـ ({prod_name}).",
        "الأسلوب: نقاش أخوي راقٍ مبني على أحدث الأبحاث الطبية، يفكك خرافات شائعة (مثل: منع الاستحمام لأسابيع، وضع بودرة أو كحول على الجروح، أو استخدام بلاستر يسلخ الجلد الحساس).",
        "المخرجات:",
        "1. عنوان منشور ريديت يثير التساؤل الطبي ويدعو للنقاش.",
        "2. نص المنشور بصيغة Markdown، مدعوم بأدلة علمية وملاحظات سريرية واقعية.",
        "3. خاتمة تفتح باب النقاش: 'لو حد عنده استفسار عن مرحلة تعافي جرحه بعد عمليته، يكتب في التعليقات وسأساعده بما أثبتته الدراسات العلمية'.",
        "```",
        "",
        "=====================================================================",
        "9️⃣ برومبت فيسبوك مصر (Facebook Post - Empathetic Medical Storytelling):",
        "=====================================================================",
        "```text",
        "بصفتك استشاري التواصل السريري في مصر:",
        "نريد كتابة منشور فيسبوك مؤثر موجه للأمهات والمرضى بعد العمليات في مصر مع استهداف خوارزميات فيسبوك في مصر.",
        f"الموضوع السريري: {prod_name} - {selected_cfg['clinical_focus']}.",
        f"الكلمات والاهتمامات: {kws_joined}",
        "",
        "المطلوب إنتاجه:",
        "1. بوست مكتوب بنبرة تعاطف سريري إنسانية راقية تلامس مشاعر المريض وأسرته عند العودة للمنزل بعد العملية وقلق الأيام الأولى.",
        "2. إجابة حاسمة على مخاوف شائعة في البيوت المصرية (الخوف من بلل الجرح، الحكة الشديدة، التورم، أو تحسس الجلد من اللصقات الرديئة).",
        "3. إرشاد المريض لحقه في فحص ومعاينة مستلزماته الطبية قبل الاستلام مع شحن مجاني بكود HT10، والتواصل مع أخصائي التعافي عبر واتساب 01155803307.",
        f"4. هاشتاجات فيسبوك مصرية مناسبة: {hashtags_joined}",
        "```",
        "",
        "=====================================================================",
        "🔟 أحدث الأبحاث والمراجع الطبية الحقيقية المستكشفة من PubMed / NCBI:",
        "=====================================================================",
    ])
    if discovered_studies:
        for idx, s in enumerate(discovered_studies, 1):
            prompts_pack_lines.append(f"[{idx}] {s['title']}")
            prompts_pack_lines.append(f"    • المجلة وسنة النشر: {s['journal']} ({s['pub_year']}) | PMID: {s['pmid']}")
            prompts_pack_lines.append(f"    • الرابط المباشر للدراسة: {s['url']}")
            prompts_pack_lines.append(f"    • الأهمية السريرية: {s['summary_ar']}\n")
    else:
        prompts_pack_lines.append("• دراسة ترطيب الأنسجة وتسكين الندبات (NCBI PMC2918339): https://pmc.ncbi.nlm.nih.gov/articles/PMC2918339/")
        prompts_pack_lines.append("• دراسة الوقاية من الكيلويد وتسطيح الندبات (PubMed 28570253): https://pubmed.ncbi.nlm.nih.gov/28570253/\n")

    prompts_pack_lines.extend([
        "---------------------------------------------------------------------",
        "📥 الخطوة التالية ببساطة:",
        "---------------------------------------------------------------------",
        "1. انسخ البرومبت المخصص لكل منصة أعلاه واستخدمه في شات الذكاء الاصطناعي (Gemini, Claude, ChatGPT, NotebookLM).",
        "2. احفظ مخرجاتك (الفيديوهات .mp4، الصوتيات، النصوص .txt، الصور) وضعها في مجلد الاستقبال:",
        f"   👉 {MANUAL_INBOX_DIR}",
        "3. بعد وضع الملفات، شغّل run_project.bat واضغط [1]؛ سيتولى النظام آلياً:",
        "   • قراءة وتصنيف كافة الملفات التي رفعتها.",
        "   • بناء وتحديث صفحات الهبوط المتعددة (Multi-Angle LPs) الخاصة بهذا المنتج.",
        "   • تحديث الموقع الكامل وتطبيق البوابة ونشر التغييرات مباشرة إلى GitHub Pages.",
        "   • تجهيز وفصل مخرجات كل منصة في مجلد مؤرخ داخل ready_to_publish وفتحه أمامك فوراً!",
        "=====================================================================",
    ])

    prompts_pack_txt = "\n".join(prompts_pack_lines)

    # حفظ في manual_inbox بصيغتي TXT و MD
    prompts_pack_file = MANUAL_INBOX_DIR / "PROMPTS_PACK_TODAY.txt"
    prompts_pack_file.write_text(prompts_pack_txt, encoding="utf-8")

    prompts_pack_md = MANUAL_INBOX_DIR / "PROMPTS_PACK_TODAY.md"
    prompts_pack_md.write_text(prompts_pack_txt, encoding="utf-8")

    # حفظ في notebooklm_hub
    (NOTEBOOKLM_DIR / "PROMPTS_PACK_TODAY.md").write_text(prompts_pack_txt, encoding="utf-8")
    hub_archive = NOTEBOOKLM_DIR / "archive"
    hub_archive.mkdir(parents=True, exist_ok=True)
    (hub_archive / f"Prompts_Pack_{timestamp_filename}.md").write_text(prompts_pack_txt, encoding="utf-8")

    # تجهيز ملف المعرفة المصدر لـ NotebookLM
    md_lines = [
        "# 🌿 الدليل السريري وحزمة المعرفة الموحدة – هيلينج تاتش مصر",
        f"**تاريخ ووقت التوليد:** {date_display}",
        f"**محور التركيز السريري:** {prod_name}",
        "**المهمة الأساسية:** التوجيه السريري والدعم التثقيفي للمرضى بعد العمليات الجراحية وتبديد المخاوف وإرشادهم لبروتوكولات التعافي المعتمدة 2026 دون أي ضغط تجاري أو أسعار.",
        "**رابط الاستشارة المجانية المباشر:** `https://medon90ae.github.io/healing-touch-egypt/wa.html` | واتساب: `01155803307`",
        "\n" + "=" * 60,
        "## 🎯 توجيهات استوديو Google NotebookLM وسيو مصر:",
        "=" * 60,
        "1. اعتمد حصرياً على الحقائق السريرية الموثقة في هذا الملف والمراجع العلمية.",
        "2. أجب على كافة استفسارات وتساؤلات المرضى بنبرة علمية داعمة وهادئة وموجهة للجمهور في مصر.",
        "3. استخدم أدوات الاستوديو (Video Overview, Audio Overview, Study Guide) لإنتاج محتوى غني.",
        "\n## 🩺 أولاً: تفاصيل المنتج ومحور الحل السريري:",
        f"### {prod_name}",
        f"- **التصنيف:** {selected_cfg['category_badge']}",
        f"- **التركيز السريري:** {selected_cfg['clinical_focus']}",
        "",
        "### الكلمات المفتاحية الأكثر بحثاً في مصر:",
    ]
    for kw in target_kws:
        md_lines.append(f"- {kw}")
    md_lines.append("\n### التساؤلات والمخاوف السريرية للمرضى في مصر:")
    for anz in selected_cfg["patient_anxieties"]:
        md_lines.append(f"- {anz}")
    for lt in long_tails:
        md_lines.append(f"- {lt}")

    md_lines.append("\n## 📚 ثانياً: المراجع السريرية والأبحاث المعتمدة:")
    if discovered_studies:
        md_lines.append("### 🔬 أبحاث PubMed / NCBI الحديثة المستكشفة اليوم:")
        for s in discovered_studies:
            md_lines.append(f"- [{s['title']} ({s['journal']} - {s['pub_year']})]({s['url']}) — {s['summary_ar']}")
    md_lines.append("- [1] [The Efficacy of Silicone Gel for the Treatment of Hypertrophic Scars and Keloids (NCBI / PMC2918339)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2918339/)")
    md_lines.append("- [2] [Review of Silicone Gel Sheeting and Silicone Gel for Prevention of Hypertrophic Scars (PubMed 28570253)](https://pubmed.ncbi.nlm.nih.gov/28570253/)")
    md_lines.append("- [3] [3M Tegaderm +Pad Film Dressing Clinical Summary (3M Medical Division)](https://multimedia.3m.com/mws/media/864087O/tegaderm-pad-film-dressing-clinical-summary.pdf)")
    md_lines.append("- [4] [Dressings and topical agents for preventing surgical site infections (Cochrane Systematic Reviews)](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD011048.pub2/full)")
    md_lines.append("- [5] [Effect of Postrhinoplasty Taping on Postoperative Edema (ResearchGate)](https://www.researchgate.net/publication/295878140_Effect_of_Postrhinoplasty_Taping_on_Postoperative_Edema_and_Nasal_Draping_A_Randomized_Clinical_Trial)")

    master_file = NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md"
    master_file.write_text("\n".join(md_lines), encoding="utf-8")
    
    timestamp_file = NOTEBOOKLM_DIR / f"Healing_Touch_Brief_{timestamp_filename}.md"
    timestamp_file.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"[+] 🎯 تم توليد وتجهيز حزمة البرومبتات وسيو مصر للمنتج ({prod_name}) بنجاح!")
    print(f"    👉 ملف البرومبتات المباشر: {prompts_pack_file}")
    print(f"    👉 ملف المعرفة لـ NotebookLM: {master_file}")
    
    return str(master_file)


def copy_to_windows_clipboard(text: str):
    if not text or sys.platform != "win32":
        return
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value ([Console]::In.ReadToEnd())"],
            input=text.encode("utf-8"),
            check=False,
            timeout=5,
        )
    except Exception:
        pass


def open_url_in_default_browser(url: str):
    if not url:
        return
    try:
        if hasattr(os, "startfile"):
            os.startfile(url)
        else:
            webbrowser.open_new_tab(url)
    except Exception:
        webbrowser.open_new_tab(url)
    time.sleep(0.45)


def fetch_sheet_tab(tab_name: str) -> pd.DataFrame:
    encoded_tab = urllib.parse.quote(tab_name)
    csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_tab}&_ts={int(time.time())}"
    resp = requests.get(csv_url, timeout=30)
    if resp.status_code in (401, 403) or "<!DOCTYPE html>" in resp.text[:200]:
        raise PermissionError(f"تعذر قراءة التبويب '{tab_name}' من Google Sheet.")
    resp.raise_for_status()
    return pd.read_csv(io.StringIO(resp.text)).fillna("")


def load_published_log() -> list:
    if PUBLISHED_LOG_PATH.exists():
        try:
            return json.loads(PUBLISHED_LOG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def record_published_post(post_data: dict, post_id: str = "", permalink_url: str = ""):
    log = load_published_log()
    log.append(
        {
            "row_index": post_data.get("row_index"),
            "day": post_data.get("day", ""),
            "hook": post_data.get("hook", ""),
            "caption": post_data.get("caption", ""),
            "hashtags": post_data.get("hashtags", ""),
            "post_id": post_id,
            "permalink_url": permalink_url,
            "published_at": datetime.now().isoformat(),
        }
    )
    PUBLISHED_LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_facebook_post_permalink(post_id: str) -> str:
    if not post_id:
        return ""
    try:
        p_res = requests.get(
            f"https://graph.facebook.com/{GRAPH_API_VERSION}/{post_id}",
            params={"fields": "permalink_url", "access_token": META_PERMANENT_PAGE_TOKEN},
            timeout=20,
        ).json()
        if p_res.get("permalink_url"):
            return str(p_res["permalink_url"])
    except Exception:
        pass
    if "_" in post_id:
        page_part, story_part = post_id.split("_", 1)
        return f"https://www.facebook.com/{page_part}/posts/{story_part}"
    return f"https://www.facebook.com/{post_id}"


def publish_facebook_graph_api(post_data: dict, image_path_or_url: str = "") -> tuple[bool, str]:
    if not META_PERMANENT_PAGE_TOKEN or "PUT_YOUR" in META_PERMANENT_PAGE_TOKEN:
        print("[!] لم يتم وضع META_PERMANENT_PAGE_TOKEN بعد.")
        return False, ""

    full_message = f"{post_data['caption']}\n\n{post_data['hashtags']}"
    print(f"[Meta Graph API] جاري نشر ({post_data['day']}) على صفحة فيسبوك ({FB_PAGE_ID})...")

    if image_path_or_url and os.path.isfile(image_path_or_url):
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{FB_PAGE_ID}/photos"
        with open(image_path_or_url, "rb") as img_file:
            res = requests.post(
                url,
                data={"caption": full_message, "access_token": META_PERMANENT_PAGE_TOKEN},
                files={"source": img_file},
                timeout=60,
            ).json()
    elif image_path_or_url.startswith("http"):
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{FB_PAGE_ID}/photos"
        res = requests.post(
            url,
            data={"url": image_path_or_url, "caption": full_message, "access_token": META_PERMANENT_PAGE_TOKEN},
            timeout=60,
        ).json()
    else:
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{FB_PAGE_ID}/feed"
        res = requests.post(
            url,
            data={"message": full_message, "access_token": META_PERMANENT_PAGE_TOKEN},
            timeout=30,
        ).json()

    if "id" in res:
        post_id = str(res.get("post_id") or res["id"])
        permalink_url = fetch_facebook_post_permalink(post_id)
        print(f"[+] تم النشر على فيسبوك بنجاح عبر Graph API! Post ID: {post_id}")
        print(f"[+] رابط المنشور المباشر: {permalink_url}")
        record_published_post(post_data, post_id, permalink_url)
        return True, permalink_url

    print(f"[!] خطأ في نشر فيسبوك Graph API: {res}")
    return False, ""


# بيانات إنستجرام الرسمية للنشر المباشر
IG_USER_ID = os.getenv("IG_USER_ID", "27911522148524499")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAT1F8BF5HBBZAGE1RXlsX3JiNENqUFNfMVVRVGpkSXBQalNLell2UXFjZAGhucUJyb3dxeHhHbF9DNXJQekdNVUlUUGVLQmdreW95OGZAwYW8zaVhSNVB1OFhycjJqdkl4UTdneExPZA2FGTUtpaHZAKSUQ1TVF3Tk5tMnRjVGgzUQZDZD")


def publish_instagram_graph_api(caption: str, image_url: str = "") -> bool:
    """نشر تلقائي للبوست على حساب Instagram Business المرتبط عبر Meta Graph API."""
    user_id = os.getenv("IG_USER_ID", IG_USER_ID)
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN", INSTAGRAM_ACCESS_TOKEN)
    if not token or not user_id:
        return False
    try:
        # استخدام رابط صورة عام وموثوق معتمد لدى خوادم إنستجرام
        media_url = image_url if image_url.startswith("http") else "https://raw.githubusercontent.com/Medon90ae/healing-touch-egypt/main/docs/assets/og-image.jpg"
        print(f"[Instagram API] جاري النشر التلقائي المباشر على إنستجرام (@mohamedahmedalahmady)...")
        create_res = requests.post(
            f"https://graph.instagram.com/v21.0/{user_id}/media",
            data={"image_url": media_url, "caption": caption[:2100], "access_token": token},
            timeout=35,
        ).json()
        if "id" in create_res:
            creation_id = create_res["id"]
            publish_res = requests.post(
                f"https://graph.instagram.com/v21.0/{user_id}/media_publish",
                data={"creation_id": creation_id, "access_token": token},
                timeout=35,
            ).json()
            if "id" in publish_res:
                post_id = publish_res['id']
                try:
                    p_info = requests.get(f"https://graph.instagram.com/v21.0/{post_id}?fields=permalink&access_token={token}", timeout=10).json()
                    ig_permalink = p_info.get("permalink", f"https://www.instagram.com/")
                except Exception:
                    ig_permalink = "https://www.instagram.com/"
                print(f"[+] 📸 تم النشر تلقائياً وحياً على إنستجرام بنجاح!\n   • الرابط المباشر للمنشور: {ig_permalink}")
                return True
            else:
                print(f"[!] خطأ نشر إنستجرام في مرحلة النشر: {publish_res}")
        else:
            print(f"[!] خطأ نشر إنستجرام في مرحلة إنشاء الحاوية: {create_res}")
    except Exception as e:
        print(f"[!] استثناء نشر إنستجرام: {e}")
    return False


# =============================================================================
# 🤖 القسم السادس: النشر التلقائي على Reddit API + مدونة جوجل Blogger
# =============================================================================
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "uHHEj4680_jmB1rrt6yTXw")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "_xfBnP9uNQMDhEUaOwC2ap_sJfIqHw")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "Dull-Nectarine4963")
REDDIT_REFRESH_TOKEN = os.getenv("REDDIT_REFRESH_TOKEN", "")
BLOGGER_BLOG_ID = os.getenv("BLOGGER_BLOG_ID", "6258225961862592152")
BLOGGER_SECRET_EMAIL = os.getenv("BLOGGER_SECRET_EMAIL", "medon90ae.healing-touch-egypt@blogger.com")
APPS_SCRIPT_WEBHOOK = "https://script.google.com/macros/s/AKfycbwDYeWbB9SjUqX1RXH7DaZ8yqG6V5Ay7yAiJ9L27Du1pJ8zb-NVgXzw6oz_0wJVp8Fr/exec"


def authorize_reddit_permanent_token():
    """فتح نافذة تفويض Reddit بنقرة واحدة واستقبال مفتاح النشر الدائم تلقائياً على localhost:8000."""
    from http.server import BaseHTTPRequestHandler, HTTPServer

    auth_code_holder = {"code": None}

    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            if "code" in qs:
                auth_code_holder["code"] = qs["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<html><body style='font-family:sans-serif;text-align:center;padding:50px;'><h2>✅ تم ربط حساب Reddit بنجاح! يمكنك إغلاق هذه النافذة الآن.</h2></body></html>".encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
        def log_message(self, format, *args):
            return

    auth_url = (
        f"https://www.reddit.com/api/v1/authorize?client_id={REDDIT_CLIENT_ID}"
        f"&response_type=code&state=healingtouch&redirect_uri=http://localhost:8000"
        f"&duration=permanent&scope=submit+identity+read"
    )
    print("[*] 🌐 جاري فتح صفحة الموافقة في متصفحك لربط حساب Reddit الدائم...")
    open_url_in_default_browser(auth_url)

    server = HTTPServer(("localhost", 8000), OAuthHandler)
    server.timeout = 300
    print("[*] ⏳ في انتظار ضغطك على زر 'Allow' في المتصفح (المهلة: 5 دقائق)...")
    server.handle_request()

    code = auth_code_holder.get("code")
    if not code:
        print("[!] لم يتم استلام كود التفويض.")
        return ""

    token_res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET),
        data={"grant_type": "authorization_code", "code": code, "redirect_uri": "http://localhost:8000"},
        headers={"User-Agent": f"windows:healing_touch:v1.0 (by /u/{REDDIT_USERNAME})"},
        timeout=20,
    ).json()

    refresh_token = token_res.get("refresh_token", "")
    if refresh_token:
        set_key(str(ENV_PATH), "REDDIT_REFRESH_TOKEN", refresh_token)
        print(f"[+] 🎉 تم حفظ مفتاح Reddit الدائم بنجاح في .env!")
        return refresh_token
    print(f"[!] خطأ في استخراج توكن Reddit: {token_res}")
    return ""


def publish_to_reddit_api(title: str, body_text: str) -> tuple[bool, str]:
    """النشر التلقائي المباشر على حساب Reddit عبر الـ API الرسمي."""
    refresh_tok = os.getenv("REDDIT_REFRESH_TOKEN", "") or REDDIT_REFRESH_TOKEN
    if not refresh_tok:
        print("[i] حساب Reddit جاهز للربط: شغّل خيار ربط Reddit مرة واحدة لتفعيل النشر التلقائي.")
        return False, ""

    try:
        user_agent = f"windows:healing_touch:v1.0 (by /u/{REDDIT_USERNAME})"
        tok_res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET),
            data={"grant_type": "refresh_token", "refresh_token": refresh_tok},
            headers={"User-Agent": user_agent},
            timeout=20,
        ).json()
        access_token = tok_res.get("access_token")
        if not access_token:
            return False, ""

        submit_res = requests.post(
            "https://oauth.reddit.com/api/submit",
            headers={"Authorization": f"bearer {access_token}", "User-Agent": user_agent},
            data={
                "sr": f"u_{REDDIT_USERNAME}",
                "kind": "self",
                "title": title,
                "text": body_text,
                "api_type": "json",
            },
            timeout=25,
        ).json()
        post_url = submit_res.get("json", {}).get("data", {}).get("url", "")
        if post_url:
            print(f"[+] 🤖 تم النشر تلقائياً على Reddit بنجاح! الرابط: {post_url}")
            return True, post_url
    except Exception as e:
        print(f"[!] تنبيه نشر Reddit: {e}")
    return False, ""


def publish_to_blogger_webhook(blogger_post: dict) -> bool:
    """إرسال المقال تلقائياً إلى الإيميل السري لمدونة بلوجر عبر جسر Google Apps Script."""
    try:
        res = requests.post(
            APPS_SCRIPT_WEBHOOK,
            json={
                "action": "publish_blogger",
                "to_email": BLOGGER_SECRET_EMAIL,
                "subject": blogger_post["title"],
                "html_body": blogger_post["html_content"],
            },
            timeout=15,
        )
        if res.status_code == 200:
            print(f"[+] 📝 تم النشر تلقائياً على مدونة جوجل (Blogger) عبر البريد السري ({BLOGGER_SECRET_EMAIL})!")
            return True
    except Exception:
        pass
    return False


def open_tabs_in_default_windows_browser(fb_post_url: str = "", blogger_post_file: str = ""):
    """فتح روابط المنصات المطلوبة للنشر والمراجعة ومجلدات العمل تلقائياً وبشكل نظيف وسلس."""
    print("\n" + "=" * 65)
    print("🌐 [روابط النشر والتحقق السريع في المتصفح]:")
    print("=" * 65)

    # 1. فتح بوست فيسبوك المنشور حديثاً
    if fb_post_url:
        print(f"   • [فيسبوك] عرض المنشور المباشر: {fb_post_url}")
        open_url_in_default_browser(fb_post_url)
    else:
        open_url_in_default_browser(f"https://www.facebook.com/{FB_PAGE_ID}")

    # 2. فتح مدونة جوجل Blogger للمعاينة والمراجعة ونسخ المقال تلقائياً للحافظة
    blogger_url = f"https://draft.blogger.com/blog/posts/{BLOGGER_BLOG_ID}"
    print(f"   • [بلوجر] عرض مدونة جوجل: {blogger_url}")
    try:
        if blogger_post_file and Path(blogger_post_file).exists():
            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", f"Get-Content -LiteralPath '{Path(blogger_post_file).resolve()}' -Raw -Encoding UTF8 | Set-Clipboard"],
                timeout=5,
                capture_output=True,
            )
            print("   • [بلوجر 📋] تم نسخ مقال HTML بالكامل تلقائياً إلى الحافظة! فقط اضغط '+ مشاركة جديدة' ثم Ctrl+V ثم نشر!")
    except Exception:
        pass
    open_url_in_default_browser(blogger_url)

    # 3. فتح صفحة رفع البوست لإنستجرام
    ig_upload_url = "https://www.instagram.com/"
    print(f"   • [إنستجرام] فتح صفحة إنستجرام للرفع المباشر: {ig_upload_url}")
    open_url_in_default_browser(ig_upload_url)

    # 4. فتح صفحة رفع الفيديو لتيك توك
    tiktok_upload_url = "https://www.tiktok.com/creator-center/upload?from=upload"
    print(f"   • [تيك توك] فتح صفحة رفع فيديو تيك توك: {tiktok_upload_url}")
    open_url_in_default_browser(tiktok_upload_url)


def read_resilient_text(file_path: Path) -> str:
    """قراءة مرنة للنصوص العربية بمختلف التراميز (UTF-8, Windows-1256 ANSI, مع استبدال الأخطاء كخيار أخير لمنع الانهيار)."""
    try:
        raw_bytes = file_path.read_bytes()
    except Exception as e:
        print(f"[!] خطأ قراءة الملف {file_path.name}: {e}")
        return ""

    for enc in ("utf-8", "cp1256", "windows-1256"):
        try:
            return raw_bytes.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def run_unified_studio_and_publish(template_idx: int = None, dry_run: bool = False) -> tuple[bool, str]:
    """الدورة الموحدة الشاملة: رصد الترند الصاعد + اختيار الحالة + صورة جديدة + تصميم كانفا + فيديو ريلز + بلوجر + NotebookLM + نشر."""
    print("=" * 65)
    print("🌿 هيلينج تاتش مصر | المحرك الشامل للتصميم والفيديو والترندات والنشر")
    print("=" * 65)

    # مسح وفحص صندوق manual_inbox بالمصنف الذكي التلقائي
    inbox_triage = scan_and_triage_manual_inbox(MANUAL_INBOX_DIR)
    used_inbox_files = []

    if template_idx is not None:
        chosen_idx = get_next_template_index(template_idx)
    elif inbox_triage.get("detected_category"):
        det_cat = inbox_triage["detected_category"]
        matched_idx = next((i for i, t in enumerate(CLINICAL_STORIES_TEMPLATES) if t.get("category") == det_cat), None)
        if matched_idx is not None:
            chosen_idx = matched_idx
            print(f"[*] 🤖 [المصنف الذكي]: تم رصد مدخلات مرفوعة خاصة بتخصص ({det_cat})، وتوجيه النشر تلقائياً لها!")
        else:
            chosen_idx = get_next_template_index(template_idx)
    else:
        chosen_idx = get_next_template_index(template_idx)

    tmpl = dict(CLINICAL_STORIES_TEMPLATES[chosen_idx])
    print(f"[*] 📖 [حالة رقم {chosen_idx + 1} من {len(CLINICAL_STORIES_TEMPLATES)}]: {tmpl['title']}")

    # 1. سحب الترندات الصاعدة الحية من جوجل مصر وانعكاسها على البوست والهاشتاجات
    live_trends_list = []
    try:
        from github_seo_trend_engine import harvest_live_egypt_trends, convert_query_to_hashtag
        cat_lookup = "thyroid-gynecomastia" if tmpl["category"] == "thyroid" else tmpl["category"]
        live_trends_list = harvest_live_egypt_trends().get(cat_lookup, [])
        if live_trends_list:
            print(f"[*] 🔥 ترندات جوجل مصر الصاعدة المرصودة لهذه الحالة: {live_trends_list[:4]}")
            trend_line = f"\n\n📈 من أكثر تساؤلات الحالات الصاعدة في بحث جوجل مصر هذا الأسبوع:\n• " + "\n• ".join(live_trends_list[:3])
            tmpl["story_text"] = tmpl["story_text"] + trend_line
            live_tags = " ".join([convert_query_to_hashtag(q) for q in live_trends_list[:4] if len(q.split()) <= 5])
            if live_tags:
                tmpl["hashtags"] = f"{tmpl['hashtags']} {live_tags}"
    except Exception as e:
        print(f"[!] تنبيه سحب الترندات الحية: {e}")

    # 📥 فحص واستيعاب كافة ملفات manual_inbox فورياً وتوجيهها للمشروع
    inbox_files = find_active_inbox_files(MANUAL_INBOX_DIR)
    
    inbox_videos = [f for f in inbox_files if f.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm"]]
    inbox_audios = [f for f in inbox_files if f.suffix.lower() in [".m4a", ".mp3", ".wav", ".aac"]]
    inbox_images = [f for f in inbox_files if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
    inbox_texts = [f for f in inbox_files if f.suffix.lower() in [".txt", ".md"]]
    inbox_htmls = [f for f in inbox_files if f.suffix.lower() in [".html", ".htm"]]

    # توجيه ملفات المنصات المرفوعة (R1) المطابقة لتخصص الحملة الحالية
    cat_inbox_texts = [f for f in inbox_texts if classify_file_category(f) == tmpl['category']]
    platform_routed = route_platform_text_files(cat_inbox_texts if cat_inbox_texts else inbox_texts) if (inbox_triage.get("detected_category") == tmpl['category'] or cat_inbox_texts) else {}
    for p_plat, p_file in platform_routed.items():
        if isinstance(p_file, Path) and p_file not in used_inbox_files:
            used_inbox_files.append(p_file)

    # 1. معالجة الفيديوهات المرفوعة وفرز الأبعاد (R1: Multi-Video Aspect Ratio Routing)
    from smart_intake_classifier import CATEGORY_KEYWORDS, probe_media_dimensions, is_video_silent, merge_silent_video_with_audio
    cat_keywords = CATEGORY_KEYWORDS.get(tmpl['category'], [])
    
    vertical_vids = []
    horizontal_vids = []
    for v in inbox_videos:
        dim = probe_media_dimensions(v)
        if dim.get("is_vertical_9_16"):
            vertical_vids.append(v)
        else:
            horizontal_vids.append(v)

    def match_cat_vid(vids_list):
        matches = [v for v in vids_list if tmpl['category'] in v.name.lower() or any(kw.lower() in v.name.lower() for kw in cat_keywords)]
        return matches[0] if matches else (vids_list[0] if vids_list else None)

    chosen_v_vid = match_cat_vid(vertical_vids)
    chosen_h_vid = match_cat_vid(horizontal_vids)

    dest_h_vid = BASE_DIR / "docs" / "assets" / f"campaign_{tmpl['category']}_video.mp4"
    dest_v_vid = BASE_DIR / "docs" / "assets" / f"campaign_{tmpl['category']}_video_9x16.mp4"
    dest_portal_vid = BASE_DIR / "portal_app" / "public" / "assets" / f"campaign_{tmpl['category']}_video.mp4"
    dest_docs_portal_vid = BASE_DIR / "docs" / "portal" / "assets" / f"campaign_{tmpl['category']}_video.mp4"

    video_path = ""
    uploaded_video_rel = ""

    if chosen_h_vid:
        used_inbox_files.append(chosen_h_vid)
        try:
            shutil.copy2(str(chosen_h_vid), str(dest_h_vid))
            dest_portal_vid.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(chosen_h_vid), str(dest_portal_vid))
            dest_docs_portal_vid.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(chosen_h_vid), str(dest_docs_portal_vid))
            video_path = str(dest_h_vid)
            uploaded_video_rel = f"../assets/{dest_h_vid.name}"
            print(f"[+] 🎬 تم اعتماد ونشر الفيديو العرضي (16:9 لليوتيوب واللاندنج): {chosen_h_vid.name}")
        except Exception as e:
            print(f"[!] تنبيه نسخ الفيديو العرضي: {e}")
            video_path = str(chosen_h_vid)

    if chosen_v_vid:
        used_inbox_files.append(chosen_v_vid)
        try:
            shutil.copy2(str(chosen_v_vid), str(dest_v_vid))
            if not video_path:
                video_path = str(dest_v_vid)
                uploaded_video_rel = f"../assets/{dest_v_vid.name}"
            print(f"[+] 📱 تم اعتماد ونشر الفيديو الطولي (9:16 للريلز وتيك توك وشورتس): {chosen_v_vid.name}")
        except Exception as e:
            print(f"[!] تنبيه نسخ الفيديو الطولي: {e}")
            if not video_path:
                video_path = str(chosen_v_vid)

    # إضافة باقي الفيديوهات المرفوعة للملفات المعالجة لمنع أي تراكم
    for v in inbox_videos:
        if v not in used_inbox_files:
            used_inbox_files.append(v)

    # 2. معالجة الصوت المرفوع ودعم الدمج مع الفيديو الصامت
    dest_docs_aud = None
    if inbox_audios:
        chosen_aud = inbox_audios[0]
        used_inbox_files.append(chosen_aud)
        dest_aud = NOTEBOOK_AUDIO_DIR / chosen_aud.name
        dest_docs_aud = BASE_DIR / "docs" / "assets" / f"campaign_{tmpl['category']}_audio{chosen_aud.suffix}"
        try:
            shutil.copy2(str(chosen_aud), str(dest_aud))
            shutil.copy2(str(chosen_aud), str(dest_docs_aud))
            print(f"[+] 🎙️ تم اعتماد ونشر التعليق الصوتي المرفوع: {chosen_aud.name}")
        except Exception as e:
            print(f"[!] تنبيه نسخ الصوت: {e}")

        # دمج الصوت مع أي فيديو صامت مرفوع
        for v_cand in [chosen_h_vid, chosen_v_vid]:
            if v_cand and is_video_silent(v_cand):
                merged_dest = BASE_DIR / "docs" / "assets" / f"merged_{v_cand.name}"
                if merge_silent_video_with_audio(v_cand, chosen_aud, merged_dest):
                    print(f"[+] 🎧 تم بنجاح دمج الصوت السريري مع الفيديو الصامت المرفوع: {merged_dest.name}")
                    if v_cand == chosen_h_vid:
                        shutil.copy2(str(merged_dest), str(dest_h_vid))
                    elif v_cand == chosen_v_vid:
                        shutil.copy2(str(merged_dest), str(dest_v_vid))

        for a in inbox_audios:
            if a not in used_inbox_files:
                used_inbox_files.append(a)

    # 3. استيعاب المتن السريري للحالة
    src_text_file = platform_routed.get("facebook") or platform_routed.get("blogger") or (inbox_texts[0] if inbox_texts else None)
    if src_text_file:
        custom_extracted = extract_clean_content(src_text_file, "facebook")
        if custom_extracted.get("body") and len(custom_extracted["body"]) > 50:
            clean_body_sanitized = custom_extracted["body"].replace("كود الخصم والمعاينة", "كود المعاينة والشحن المجاني").replace("كود الخصم", "كود المعاينة")
            tmpl["story_text"] = clean_body_sanitized
            print(f"[+] 📝 تم استيعاب وصياغة المتن السريري المرفوع من ({src_text_file.name}) بدون أي ترويسات تقنية!")

    # 4. معالجة الصور المرفوعة (R1: Multi-Image Ingestion & Clinical Gallery Carousel)
    gallery_paths = []
    if inbox_images:
        # الصورة الأولى هي Hero Cover
        sorted_imgs = sorted(inbox_images, key=lambda x: (abs(x.stat().st_size - 1.5 * 1024 * 1024)))
        chosen_img = sorted_imgs[0]
        used_inbox_files.append(chosen_img)
        
        dest_hero_img = BASE_DIR / "docs" / "assets" / f"campaign_{tmpl['category']}_hero.png"
        try:
            shutil.copy2(str(chosen_img), str(dest_hero_img))
            square_img_path = str(dest_hero_img)
            story_img_path = str(dest_hero_img)
            print(f"[+] 🎨 تم اعتماد صورة الغلاف الرئيسية Hero Cover ({chosen_img.name})!")
        except Exception:
            square_img_path = str(chosen_img)
            story_img_path = str(chosen_img)

        # باقي الصور تُوزع كمعرض سريري وكاروسيل للمنصات وصفحة الهبوط
        gallery_dir = BASE_DIR / "docs" / "assets" / "gallery"
        gallery_dir.mkdir(parents=True, exist_ok=True)
        remaining_imgs = [im for im in inbox_images if im != chosen_img]
        for g_idx, g_img in enumerate(remaining_imgs):
            used_inbox_files.append(g_img)
            dest_g = gallery_dir / f"campaign_{tmpl['category']}_case_{g_idx+1}.png"
            try:
                shutil.copy2(str(g_img), str(dest_g))
                gallery_paths.append(str(dest_g))
            except Exception:
                gallery_paths.append(str(g_img))
        if gallery_paths:
            print(f"[+] 📸 تم توجيه {len(gallery_paths)} صور سريرية إضافية إلى معرض الحالات السريرية (Clinical Cases Carousel)!")
    else:
        photo_info = get_clinical_case_photo(tmpl["title"], tmpl["category"])
        raw_img = photo_info.get("local_path", "")
        cards = generate_branded_card(tmpl, raw_img) if raw_img else {"square_path": "", "story_path": ""}
        square_img_path = cards.get("square_path", "") or raw_img
        story_img_path = cards.get("story_path", "")

    # إذا لم يكن هناك فيديو مرفوع، ننشئ فيديو ريلز من الصورة
    if not video_path and story_img_path:
        video_path = generate_tiktok_reel_video(story_img_path, duration_sec=8)

    export_canva_bulk_csv(CLINICAL_STORIES_TEMPLATES)
    blogger_post = format_clinical_case_for_blogger(tmpl, {"image_url": "../assets/og-image.jpg"})
    generate_blogger_atom_xml([blogger_post])
    notebook_file = str(NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md")

    # 5. ملفات HTML مخصصة
    custom_stitch_html = ""
    if inbox_htmls:
        custom_stitch_html = inbox_htmls[0].read_text(encoding="utf-8")
        used_inbox_files.append(inbox_htmls[0])

    # توليد وتحديث كافة صفحات الهبوط متعددة الزوايا للمنتجات الطبية
    try:
        multi_lps = cle.generate_all_multi_angle_product_lps()
        print(f"[+] 🌐 تم بناء وتحديث {len(multi_lps)} صفحة هبوط مستقلة ومتخصصة لكل منتج في docs/lp/!")
    except Exception as e:
        print(f"[!] تنبيه تحديث صفحات الهبوط: {e}")

    lp_res = cle.build_campaign_landing_page(
        case_data=tmpl,
        media_assets={
            "hero_path": square_img_path,
            "square_path": square_img_path,
            "story_path": story_img_path,
            "gallery_paths": gallery_paths,
            "video_horizontal": str(dest_h_vid) if chosen_h_vid else video_path,
            "video_vertical": str(dest_v_vid) if chosen_v_vid else "",
            "audio_path": str(dest_docs_aud) if dest_docs_aud else ""
        },
        custom_stitch_html=custom_stitch_html
    )
    lp_url = lp_res["public_url"]

    # تجهيز نصوص المنصات بتاريخ اليوم مدمجاً برابط صفحة الهبوط الجديدة ورابط واتساب المباشر
    date_str = datetime.now().strftime("%Y-%m-%d")
    category_messages = {
        "c-section": "أهلاً بحضرتك، محتاجة استشارة بخصوص جرح القيصرية والشاور الآمن، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "bariatric": "أهلاً بحضرتك، محتاج استشارة بخصوص حماية ثقوب المنظار بعد عملية التكميم، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "rhinoplasty": "أهلاً بحضرتك، محتاج استشارة بخصوص بلاستر 3M ودعامة الأنف لتثبيت النتيجة وتخفيف التورم، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "thyroid": "أهلاً بحضرتك، محتاجة استشارة بخصوص حماية ندبة الرقبة بعد استئصال الغدة الدرقية وتسطيحها، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "keloid": "أهلاً بحضرتك، محتاج استشارة بخصوص شيت السيليكون الطبي لتسطيح وتفتيح الندبة البارزة، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
    }
    wa_msg = category_messages.get(tmpl.get("category", "general"), "أهلاً بحضرتك في هيلينج تاتش مصر، محتاج استشارة بخصوص التعافي بعد عمليتي، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.")
    wa_direct_url = f"https://wa.me/201155803307?text={urllib.parse.quote(wa_msg)}" 
    
    # 1. إعداد نصوص كل منصة بالموجه الذكي ومستخرج المحتوى السريري النظيف (R1 + R2)
    fb_file = platform_routed.get("facebook")
    if fb_file:
        fb_res = extract_clean_content(fb_file, "facebook", landing_url=lp_url, whatsapp_url=wa_direct_url)
        facebook_caption = fb_res["caption"]
        print(f"[+] 📘 [المصنف الذكي]: تم توجيه ملف ({fb_file.name}) حصرياً لفيسبوك واستخراج المتن السريري الكامل الخالي من الترويسات!")
    else:
        clean_story_text = tmpl['story_text'].strip()
        facebook_caption = f"""🌿 {tmpl['title']}

{clean_story_text}

━━━━━━━━━━━━━━━━━━━━━━━
🔗 رابط الدليل السريري وحاسبة التعافي المتخصصة:
👉 {lp_url}

💬 للتوجيه السريري المجاني والاستشارة عبر واتساب (01155803307):
👉 {wa_direct_url}

{tmpl['hashtags']}"""

    # كابشن إنستجرام المخصص
    ig_file = platform_routed.get("instagram")
    if ig_file:
        ig_res = extract_clean_content(ig_file, "instagram", landing_url=lp_url, whatsapp_url=wa_direct_url)
        instagram_caption = ig_res["caption"]
        print(f"[+] 📸 [المصنف الذكي]: تم توجيه ملف ({ig_file.name}) حصرياً لإنستجرام واستخراج الكابشن المعتمد!")
    else:
        instagram_caption = facebook_caption

    # كابشن تيك توك المخصص
    tt_file = platform_routed.get("tiktok")
    if tt_file:
        tt_res = extract_clean_content(tt_file, "tiktok", landing_url=lp_url, whatsapp_url=wa_direct_url)
        tiktok_caption = tt_res["caption"]
        print(f"[+] 📱 [المصنف الذكي]: تم توجيه ملف ({tt_file.name}) لحزمة وسيناريو تيك توك!")
    else:
        tiktok_caption = facebook_caption

    # مقال بلوجر المخصص
    bl_file = platform_routed.get("blogger")
    if bl_file:
        bl_res = extract_clean_content(bl_file, "blogger", landing_url=lp_url, whatsapp_url=wa_direct_url)
        blogger_post["title"] = bl_res["title"]
        blogger_post["html_content"] = bl_res["html_content"]
        blogger_text = f"<h1>{bl_res['title']}</h1>\n\n<p style='background:#ECFDF5;padding:12px;border-radius:10px;font-weight:bold;'>👉 <strong>رابط الدليل السريري وحجز الاستشارة المباشر:</strong> <a href='{lp_url}'>{lp_url}</a></p>\n\n{bl_res['html_content']}"
        print(f"[+] 📰 [المصنف الذكي]: تم توجيه ملف ({bl_file.name}) لمقال بلوجر وتوليد HTML المتكامل!")
    else:
        blogger_text = f"<h1>{blogger_post['title']}</h1>\n\n<p style='background:#ECFDF5;padding:12px;border-radius:10px;font-weight:bold;'>👉 <strong>رابط الدليل السريري وحجز الاستشارة المباشر:</strong> <a href='{lp_url}'>{lp_url}</a></p>\n\n{blogger_post['html_content']}"

    # مقال ريديت المخصص
    rd_file = platform_routed.get("reddit")
    if rd_file:
        rd_res = extract_clean_content(rd_file, "reddit", landing_url=lp_url, whatsapp_url=wa_direct_url)
        reddit_text = rd_res["markdown"]
        print(f"[+] 🔴 [المصنف الذكي]: تم توجيه ملف ({rd_file.name}) لمنشور ومقال ريديت الموثق!")
    else:
        reddit_text = f"**{tmpl['title']}**\n\n{tmpl['story_text']}\n\n---\n🔗 **[رابط الدليل السريري وحجز الاستشارة المباشر]({lp_url})**\n\n**للتوجيه السريري والاستشارة المجانية عبر واتساب:** 01155803307\n\n{tmpl['hashtags']}"

    # حفظ ملفات النصوص المخصصة لكل منصة في branded_designs
    (BRANDED_DIR / f"{date_str}_[نص_بوست_وستوري_إنستجرام].txt").write_text(instagram_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[نص_كابشن_وهاشتاجات_تيكتوك].txt").write_text(tiktok_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[نص_منشور_فيسبوك].txt").write_text(facebook_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[مقال_مدونة_جوجل_Blogger].txt").write_text(blogger_text, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[منشور_ومقال_Reddit].txt").write_text(reddit_text, encoding="utf-8")
    
    copy_to_windows_clipboard(facebook_caption)
    print(f"\n📄 [تم إنشاء ملفات النصوص المستقلة لكل منصة بتاريخ اليوم في مجلد branded_designs]:")
    print(f"   • {date_str}_[نص_منشور_فيسبوك].txt")
    print(f"   • {date_str}_[نص_بوست_وستوري_إنستجرام].txt")
    print(f"   • {date_str}_[نص_كابشن_وهاشتاجات_تيكتوك].txt")
    print(f"   • {date_str}_[مقال_مدونة_جوجل_Blogger].txt")
    print(f"   • {date_str}_[منشور_ومقال_Reddit].txt")

    # فتح مجلد التصميمات والفيديو تلقائياً في Windows Explorer (يحتوي على بوست إنستجرام المربع، وبطاقة الستوري، وفيديو تيك توك)
    try:
        branded_dir = str(BASE_DIR / "media_assets" / "branded_designs")
        os.startfile(branded_dir)
        print(f"📂 [تم فتح مجلد محتوى إنستجرام وتيك توك (الصور والفيديوهات)]: {branded_dir}")
    except Exception as e:
        print(f"[!] تنبيه فتح المجلد: {e}")

    post_data = {
        "day": f"دراسة حالة سريرية ({chosen_idx + 1}) - {tmpl['title']}",
        "caption": facebook_caption,
        "hashtags": "",
        "row_index": -1,
    }

    # تجهيز حزمة النشر الآلي الشامل لـ 6 منصات لمحرك n8n
    n8n_payload = build_omnichannel_payload(
        campaign_id=tmpl.get("category", "post_op_care"),
        theme="surgical_wound_and_scar_care",
        product_name=tmpl.get("title", "BUPY Silicone Scar Sheets 4cm x 3m"),
        promo_code="HT10",
        promo_text="كود الخصم: HT10 (شحن مجاني + حق فتح ومعاينة الشحنة قبل الدفع)",
        wa_link=wa_direct_url,
        landing_url=lp_url,
        hero_image=str(square_img_path),
        gallery_images=[str(square_img_path), str(story_img_path)],
        video_vertical=str(video_path),
        video_horizontal=str(video_path),
        copywriting={
            "facebook": facebook_caption,
            "instagram": instagram_caption,
            "tiktok": tiktok_caption,
            "youtube_title": f"{tmpl['title']} | هيلينج تاتش مصر #Shorts",
            "youtube_description": f"الدليل الطبي المعتمد لتعافي الجروح والندبات الجراحية في المنزل بدون مضاعفات\n\n🎁 كود الخصم: HT10 (شحن مجاني + حق فتح ومعاينة الشحنة قبل الدفع)\n🩺 استشارة مجانية مع أخصائية العناية بالتعافي: {wa_direct_url}\n\n{tmpl['hashtags']}",
            "reddit_title": blogger_post.get("title", tmpl["title"]),
            "reddit_markdown": reddit_text,
            "blogger_title": blogger_post.get("title", tmpl["title"]),
            "blogger_html": blogger_text
        },
        hashtags=tmpl.get("hashtags", "")
    )
    payload_file = BRANDED_DIR / f"{date_str}_[n8n_omnichannel_payload].json"
    payload_file.write_text(json.dumps(n8n_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if dry_run:
        record_post_history(chosen_idx, tmpl["title"])
        print("\n" + "=" * 65)
        print(f"🔍 معاينة المخرجات (DRY RUN - حالة رقم {chosen_idx + 1}):")
        print("=" * 65)
        print(f"1. تصميم فيسبوك وإنستجرام: {square_img_path}")
        print(f"2. بطاقة الستوري وتيك توك: {story_img_path}")
        print(f"3. فيديو TikTok & Reels MP4: {video_path}")
        print(f"4. مقال مدونة جوجل (Blogger): {blogger_post['file_path']}")
        print(f"5. حزمة Google NotebookLM: {notebook_file}")
        print(f"6. سجل الترندات الصاعدة الحية: {BASE_DIR / 'media_assets' / 'live_trends_registry.json'}")
        print(f"7. حزمة الـ 6 منصات لمحرك n8n: {payload_file}")
        print("\nالنص السريري لفيسبوك:")
        print(facebook_caption[:400] + "...")
        print("=" * 65)
        open_tabs_in_default_windows_browser(fb_post_url="", blogger_post_file=blogger_post['file_path'])
        return True, ""

    # رفع صفحة الهبوط وخريطة الموقع فورياً إلى GitHub Pages
    print("\n[*] 🌐 جاري رفع الـ Landing Page الجديدة إلى GitHub Pages...")
    try:
        subprocess.run(["git", "add", "docs"], cwd=str(BASE_DIR), check=False)
        subprocess.run(["git", "commit", "-m", f"feat(lp): deploy campaign landing page {tmpl.get('category')}"], cwd=str(BASE_DIR), check=False)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=False)
        print(f"[+] 🚀 تم نشر وتفعيل الـ Landing Page بنجاح على الرابط:\n   👉 {lp_url}")
    except Exception as e:
        print(f"[!] تنبيه رفع GitHub: {e}")

    # إرسال حزمة الـ 6 منصات لمحرك n8n عبر Webhook
    n8n_ok, n8n_res = dispatch_to_n8n_webhook(n8n_payload)
    if n8n_ok:
        print(f"[+] 🚀 [n8n Omnichannel Engine]: تم إرسال حزمة الـ 6 منصات بنجاح إلى n8n!")
    else:
        print(f"[!] ⚠️ [n8n Omnichannel Engine]: تنبيه إرسال الويب هوك: {n8n_res.get('error')}")

    ok, permalink = publish_facebook_graph_api(post_data, square_img_path)
    ig_image_url = f"https://raw.githubusercontent.com/Medon90ae/healing-touch-egypt/main/docs/assets/campaign_{tmpl['category']}_hero.png"
    publish_instagram_graph_api(instagram_caption, image_url=ig_image_url)
    publish_to_blogger_webhook(blogger_post)
    publish_to_reddit_api(blogger_post.get("title", tmpl["title"]), reddit_text)
    if ok:
        record_post_history(chosen_idx, tmpl["title"])

    # 📦 بناء وتجهيز حزمة ready_to_publish المؤرخة فورياً لنفس الحملة
    try:
        from scripts.build_ready_to_publish_pack import generate_pack
        pack_dir = generate_pack(category=tmpl['category'])
        print(f"[+] 📦 تم بناء وتحديث حزمة ready_to_publish المؤرخة للحملة بنجاح: {pack_dir.name}")
    except Exception as e:
        print(f"[!] تنبيه توليد حزمة ready_to_publish: {e}")

    # 🧹 تفريغ وأرشفة كافة الملفات المعالجة من manual_inbox لحفظ نظافة الصندوق بالكامل
    all_inbox_remaining = [
        f for f in MANUAL_INBOX_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]
    files_to_clean = list(set(used_inbox_files + all_inbox_remaining))
    if files_to_clean:
        archived_count = archive_used_inbox_files(MANUAL_INBOX_DIR, files_to_clean)
        if archived_count > 0:
            print(f"\n[+] 🧹 [تفريغ الصندوق]: تم تنظيف وأرشفة {archived_count} ملفات من manual_inbox إلى archive/ بنجاح!")

    # فتح تبويبات المتصفح المطلوبة فوراً
    open_url_in_default_browser(lp_url)
    open_tabs_in_default_windows_browser(fb_post_url=permalink, blogger_post_file=blogger_post['file_path'])
    return ok, permalink


def main():
    parser = argparse.ArgumentParser(description="المحرك الموحد لمشروع هيلينج تاتش مصر")
    parser.add_argument(
        "--mode",
        choices=["all", "auto-daily", "publish", "dry-run", "groups", "notebooklm", "open-latest", "auth-reddit"],
        default="all",
        help="وضع التشغيل الموحد",
    )
    parser.add_argument("--product", type=str, default=None, choices=["1", "2", "3", "4", "5", "6", "tegaderm", "bupy", "micropore", "nostril-retainer", "opsite", "all"], help="رقم المنتج المراد تحضير البرومبتات والمصادر له")
    parser.add_argument("--index", type=int, default=None, help="رقم القالب السريري اختيارياً")
    parser.add_argument("--dry-run", action="store_true", help="معاينة وتوليد الأصول دون النشر الفعلي")
    parser.add_argument("--check-sheet", action="store_true", help="فحص الاتصال بجدول Google Sheet")
    args = parser.parse_args()

    if args.check_sheet:
        for tab in [PROBLEMS_TAB_NAME, GROUPS_TAB_NAME, CONTENT_TAB_NAME]:
            df = fetch_sheet_tab(tab)
            print(f"✅ التبويب '{tab}': {len(df)} صف")
        return

    if args.mode == "auth-reddit":
        authorize_reddit_permanent_token()
        return

    if args.mode == "notebooklm":
        src_path = export_notebooklm_master_source(product_choice=args.product, interactive=True)
        print("\n" + "=" * 65)
        print("🧠 [خطوات بسيطة للحصول على الفيديو والصوت والنصوص والمقالات كاملة]:")
        print("=" * 65)
        print(f"1. تم إنشاء وتحديث الملف المرجعي الحامل للبرومبت والتعليمات الصارمة:\n   👉 {src_path}")
        print("2. 🌐 جاري فتح منصات وأدوات الذكاء الاصطناعي الأربعة (Pomelli + Stitch + Deep Research + NotebookLM)...")
        open_url_in_default_browser("https://labs.google.com/pomelli/campaigns")
        open_url_in_default_browser("https://stitch.withgoogle.com/")
        open_url_in_default_browser("https://gemini.google.com/")
        open_url_in_default_browser("https://notebooklm.google.com/")
        print("3. جاري فتح مجلد الحزمة ومجلد الصور الطبية pic وصندوق الاستقبال manual_inbox...")
        try:
            os.startfile(str(NOTEBOOKLM_DIR))
            os.startfile(str(NOTEBOOK_PIC_DIR))
            os.startfile(str(MANUAL_INBOX_DIR))
        except Exception:
            pass
        print("4. من واجهة Google NotebookLM:")
        print("   • افتح محادثة جديدة (New Chat) وتأكد من تحديد أحدث ملف فقط.")
        print("   • من لوحة الاستوديو (Studio): أنشئ الفيديو التوضيحي (Video Overview) - وهو يغني عن الصوت لاحتوائه على الشرح المرئي والصوتي معاً.")
        print("   • أنشئ المقالات والنصوص وحمّلها كملف نصي (.txt).")
        print(f"5. قم بتنزيل ملفاتك وضعها في مجلد الاستقبال المعتمد:\n   👉 {MANUAL_INBOX_DIR}")
        print("   وسيقوم المحرك بقراءتها ونشرها فوراً عند اختيار رقم [1] أو معاينتها برقم [2]!")
        print("=" * 65)
        return

    if args.mode == "groups":
        print("[*] تم دمج واستيعاب كلمات رادار الجروبات والترندات تلقائياً داخل قاعدة بيانات محرك السيو والمحتوى بدون الحاجة لفتح نوافذ يدوية.")
        return

    if args.mode == "open-latest":
        log = load_published_log()
        latest_url = log[-1].get("permalink_url", "") if log else f"https://www.facebook.com/{FB_PAGE_ID}"
        open_tabs_in_default_windows_browser(fb_post_url=latest_url)
        return

    is_dry = args.dry_run or (args.mode == "dry-run")
    ok, permalink = run_unified_studio_and_publish(template_idx=args.index, dry_run=is_dry)


if __name__ == "__main__":
    main()
