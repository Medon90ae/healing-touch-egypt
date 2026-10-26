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
from datetime import datetime
from pathlib import Path

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
    cat = custom_category or detect_category_from_text(topic_text)
    raw_queries = CATEGORY_SEARCH_QUERIES.get(cat, CATEGORY_SEARCH_QUERIES["general"]).copy()
    random.shuffle(raw_queries)

    used_ids = load_used_images()
    photo_info = {}
    prefer_pexels = random.choice([True, False])

    for q in raw_queries:
        if prefer_pexels:
            photo_info = search_pexels_photo(q, exclude_ids=used_ids) or search_pixabay_photo(q, exclude_ids=used_ids)
        else:
            photo_info = search_pixabay_photo(q, exclude_ids=used_ids) or search_pexels_photo(q, exclude_ids=used_ids)
        if photo_info and photo_info.get("image_url"):
            break

    if not photo_info or not photo_info.get("image_url"):
        fb_q = random.choice(["hospital surgical recovery", "doctor patient consultation clinic", "dermatology skin care"])
        photo_info = search_pexels_photo(fb_q, exclude_ids=used_ids) or search_pixabay_photo(fb_q, exclude_ids=used_ids)

    if not photo_info or not photo_info.get("image_url"):
        return {}

    if photo_info.get("id"):
        mark_image_as_used(photo_info["id"])

    try:
        slug_id = f"case_{cat}_{photo_info['source'].lower()}_{photo_info['id']}"
        local_path = CASES_DIR / f"{slug_id}.jpg"
        if not local_path.exists():
            print(f"[*] 📥 جاري تنزيل صورة طبية جديدة من {photo_info['source']} ({photo_info['alt']})...")
            img_res = requests.get(photo_info["image_url"], timeout=20)
            if img_res.status_code == 200:
                local_path.write_bytes(img_res.content)
                print(f"[+] ✅ تم حفظ الصورة بنجاح: {local_path.name}")
        photo_info["local_path"] = str(local_path)
        return photo_info
    except Exception as exc:
        print(f"[!] خطأ في تنزيل الصورة: {exc}")
        return photo_info


# =============================================================================
# 📖 القسم الثاني: بنك القصص والحالات السريرية الواقعية والدوران التلقائي
# =============================================================================
CLINICAL_STORIES_TEMPLATES = [
    {
        "category": "c-section",
        "title": "حالة جرح القيصرية والشاور والندبة البارزة",
        "story_text": """أمهات كتير بيبعتوا يسألونا في الاستشارات:
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

💡 لو عندك أي استفسار عن مرحلة جرحك بعد القيصرية أو حابة تتأكدي من التوقيت المناسب لحالتك:
تقدري تتواصلي مباشرة للحصول على استشارة مجانية مع أخصائية العناية بالتعافي عبر واتساب:
💬 رابط الاستشارة المباشرة وتفعيل الخصم:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=c-section&code=HT10
(أو مباشرة عبر واتساب: 01155803307)
🎁 كود الخصم الحصري (HT10) يمنحك: شحن مجاني لكافة محافظات مصر + حق فتح ومعاينة الشحنة قبل الدفع.""",
        "hashtags": "#ولادة_قيصرية_مصر #جرح_القيصرية #علاج_الندبات #شيت_سيليكون_بوبي #ضمادات_تيجاديرم #كود_HT10 #صحة_المراة_مصر #امهات_مصر #مامي_جديدة #علاج_الكلويد #هيلينج_تاتش_مصر",
    },
    {
        "category": "rhinoplasty",
        "title": "حالة تورم أرنبة الأنف وتماثل الفتحات بعد التجميل",
        "story_text": """بنات كتير بعد فك جبيرة الأنف بيجيلهم قلق شديد:
"الأرنبة وارمة جداً وحاسة إن في فتحة أكبر من فتحة أو مش متماثلين، واللصقات العادية بتعملي حساسية وحبوب بيضا تحت الجلد!"

مبدئياً.. دي مرحلة بيمر بيها 95% من حالات تجميل الأنف، والسر كله في فهم بيولوجيا الأنسجة بعد إزالة الجبيرة:

١. ليه الأرنبة بتورم بعد فك الجبيرة؟
الجبيرة كانت عاملة ضغط مستمر، وأول ما بتتشال، السوائل اللمفاوية بتتجمع في طرف الأنف (Supratip Edema) خصوصاً لأصحاب الجلد السميك (Thick Skin).

٢. خطورة اللصقات العادية الرخيصة:
اللصقات التجارية غير المخصصة لجراحة الأنف بتمنع مسام الجلد من التنفس، وبتسيب صمغ كيميائي يسبب التهابات وحبوب صديدية، والأخطر إنها بتضغط بشكل غير متساوي فتشوه نزول التورم!

٣. القاعدة السريرية المثبتة في أبحاث 2026:
- استخدام بلاستر ورقي طبي مسامي مخصص (3M Micropore Tan البيج الأصلي): خفيف جداً، لونه بيج تجميلي غير ملفت، بيوفر ضغط هادئ يصرّف السوائل بدون حساسية.
- الحفاظ على تماثل الفتحتين بدعامة السيليكون الطبية (Nostril Retainer): قوى الانكماش الندبي بعد قص الفتحات بتشد الغضاريف، واستخدام دعامة السيليكون بالمقاس المضبوط بيحافظ على تماثل الفتحتين بنسبة 94% وفق دراسات MDPI السريرية.

٤. نصيحة للمتابعة:
ممنوع شد اللصقة بعنف؛ لازم ترطيبها بمية دافية قبل الإزالة عشان متسحبش الجلد وتزود التورم.

💡 عندك استفسار عن مقاس دعامة الأنف أو طريقة اللصق المناسبة لنوع جلدك؟
تواصلي الآن مع أخصائية العناية بالتعافي للحصول على استشارة مجانية:
💬 رابط الاستشارة المباشرة وتفعيل الخصم:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=rhinoplasty&code=HT10
(أو مباشرة عبر واتساب: 01155803307)
🎁 كود HT10 يضمن لكِ: شحن مجاني لكافة المحافظات + حق فتح ومعاينة الشحنة والتأكد من المقاس الأصلي قبل الدفع.""",
        "hashtags": "#تجميل_الانف_مصر #عملية_تجميل_الانف #تورم_الانف_بعد_العملية #بلاستر_3m_البيج #دعامة_الانف_السيليكون #ارنبة_الانف #كود_HT10 #هيلينج_تاتش_مصر #جراحة_تجميل_مصر",
    },
    {
        "category": "bariatric",
        "title": "حالة ثقوب المنظار بعد التكميم وتحسس البلاستر ورعب الاستحمام",
        "story_text": """حالات كتير جداً بعد عمليات التكميم وتحويل المسار بيسألونا في قلق:
"عندي 4 أو 5 ثقوب في بطني، البلاستر العادي عامل احمرار وحكة رهيبة، ومحرومة من الشاور بقالي أسبوعين وخايفة من تلوث الجروح!"

مبدئياً.. دي مشكلة 80% من مرضى جراحات السمنة والحل الطبي بسيط جداً:

١. ليه البلاستر العادي بيعمل حساسية شديدة في البطن؟
الجلد في منطقة البطن بعد العملية بيكون مشدود وحساس، وصمغ البلاستر التجاري بيسحب الطبقة القرنية السطحية مع كل غيار مسبباً التهاب تماسي واحمرار يشبه الحروق!

٢. خطورة الشاور بالغيار المبلول:
القطن لما يلمس مية الشاور بيفضل رطب لساعات، وده بيزود فرص العدوى الميكروبية بثقوب المنظار.

٣. الحل المعتمد في مراكز جراحة السمنة:
- استخدام بخاخ الفيلم الشفاف الطبي (Smith & Nephew Opsite Spray): رشة واحدة بتعمل طبقة ميكروسكوبية عازلة للماء والبكتيريا 100%، تسمحلك تاخد شاور فوري، وفي نفس الوقت بتسيب مسام الجلد تتنفس وتتخلص من العرق.
- بعد التئام الثقوب: استخدام قصاصات شيت السيليكون الطبي (BUPY) لمنع تحول الثقوب لندبات غامقة أو بارزة.

💡 حابب تعرف الطريقة الصحيحة للغيار على ثقوب المنظار حسب أيام عمليتك؟
تواصل الآن للحصول على استشارة مجانية مع أخصائية العناية بالتعافي عبر واتساب:
💬 رابط الاستشارة المباشرة وتفعيل الخصم:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=bariatric&code=HT10
(أو مباشرة عبر واتساب: 01155803307)
🎁 كود الخصم الحصري (HT10): شحن مجاني لكافة محافظات مصر + حق فتح ومعاينة الشحنة قبل الدفع.""",
        "hashtags": "#تكميم_المعدة_مصر #جراحة_السمنة #تحويل_مسار #ثقوب_المنظار #بخاخ_اوبسايت #علاج_الندبات #كود_HT10 #هيلينج_تاتش_مصر #رابطة_المتكممين",
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
تواصلي مباشرة مع أخصائية التعافي لاستشارة مجانية:
💬 رابط الاستشارة المباشرة وتفعيل الخصم:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=thyroid&code=HT10
(أو مباشرة عبر واتساب: 01155803307)
🎁 كود الخصم الحصري (HT10): شحن مجاني لكافة المحافظات + حق فتح ومعاينة الشحنة قبل الدفع.""",
        "hashtags": "#استئصال_الغدة_الدرقية #جراحة_الغدة #ندبات_الرقبة #شيت_سيليكون_بوبي #بلاستر_3m_البيج #كود_HT10 #هيلينج_تاتش_مصر #تجميل_الجروح",
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
تواصلي مع أخصائية العناية بالتعافي لاستشارة مجانية:
💬 رابط الاستشارة المباشرة وتفعيل الخصم:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=c-section&code=HT10
(أو مباشرة عبر واتساب: 01155803307)
🎁 كود الخصم الحصري (HT10): شحن مجاني لكافة محافظات مصر + حق فتح ومعاينة الشحنة قبل الدفع.""",
        "hashtags": "#كلويد_القيصرية #علاج_الكلويد #ندبات_الولادة #شيت_سيليكون_بوبي #حكة_الجرح #كود_HT10 #هيلينج_تاتش_مصر #امهات_مصر",
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
تواصلي الآن للحصول على استشارة مجانية مع أخصائية التعافي:
💬 رابط الاستشارة المباشرة وتفعيل الخصم:
👉 https://medon90ae.github.io/healing-touch-egypt/wa.html?case=rhinoplasty&code=HT10
(أو مباشرة عبر واتساب: 01155803307)
🎁 كود الخصم الحصري (HT10): شحن مجاني لكافة المحافظات + حق فتح ومعاينة الشحنة قبل الدفع.""",
        "hashtags": "#تجميل_الانف_اللحمي #تجميل_الانف_مصر #بلاستر_3m_البيج #حبوب_الانف_بعد_العملية #ارنبة_الانف #كود_HT10 #هيلينج_تاتش_مصر",
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
    raw_path = Path(raw_img_path).resolve()
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
        subprocess.run(cmd, capture_output=True, text=True, timeout=90)
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


def export_notebooklm_master_source() -> str:
    """تجهيز ملف المعرفة والبرومبت الموحد الشامل الجاهز للرفع المباشر في Google NotebookLM بدون الحاجة لكتابة برومبت يدوي."""
    registry_path = BASE_DIR / "products_registry.json"
    products_data = []
    if registry_path.exists():
        try:
            products_data = json.loads(registry_path.read_text(encoding="utf-8")).get("products", [])
        except Exception:
            pass

    # تاريخ ووقت دقيق لكل ضغطة على رقم 4
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    date_display = now.strftime("%Y-%m-%d %I:%M %p")

    md_lines = [
        "# 🌿 الدليل السريري وحزمة المحتوى والإنتاج الرقمي الموحد – هيلينج تاتش مصر",
        f"**تاريخ ووقت التوليد اللحظي:** {date_display}",
        "**المشروع:** منصة استشارات طبية متخصصة ومستلزمات التعافي بعد العمليات الجراحية وعلاج الندبات في مصر.",
        "**العرض المعتمد:** كود الخصم الحصري `HT10` (شحن مجاني لكافة المحافظات + حق فتح ومعاينة الشحنة قبل الدفع).",
        "**رابط الاستشارة المجانية عبر واتساب:** `01155803307` | رابط الحجز: `https://medon90ae.github.io/healing-touch-egypt/wa.html`",
        "\n" + "=" * 60,
        "## 🎯 البرومبت الهندسي الموحد المخصص لأدوات Google NotebookLM الاستوديو والإنتاج الكامل:",
        "=" * 60,
        "بصفتك كبير الاستشاريين السريريين ورئيس قطاع الإنتاج المرئي والمحتوى الطبي الرقمي في (هيلينج تاتش مصر):",
        "",
        "⚠️ تعليمات صارمة لنظام التوليد في NotebookLM:",
        "- تجاهل أي محادثات أو تقارير قديمة في الذاكرة بالكامل.",
        "- اعتمد حصرياً على أحدث بيانات هذا الملف والأسعار الحية والمراجع الطبية الـ 11 الموثقة.",
        "- المطلوب توليد الأصول الكاملة (فيديو، صوت، نصوص، مقالات، وتوجيه بصري) لتنزيلها وحفظها في مجلد الاستقبال manual_inbox.",
        "",
        "المطلوب إخراجه وتنفيذه عبر أدوات الاستوديو (Studio Panel) ومربع الحوار:",
        "",
        "1. 🎬 **فيديو توضيحي شارح متكامل (Explainer Video / Video Overview):**",
        "   - توليد فيديو شارح عبر أداة الفيديو بالاستوديو يوضح بيولوجيا التئام الأنسجة ومراحل التعافي واستخدام المنتجات الطبية الأصلية (3M, BUPY, Opsite).",
        "   - (ملاحظة: هذا الفيديو يغني تماماً عن الصوت المنفصل لاحتوائه على السرد الصوتي المتقن والعرض البصري معاً).",
        "",
        "2. 🎙️ **الملخص الصوتي / البودكاست الاستشاري (Audio Overview - اختياري):**",
        "   - حوار صوتي تفاعلي بين طبيبين بلهجة مصرية راقية يشرح مخاوف المرضى والأمهات، ويقدم بروتوكول التعافي وكود HT10 والاستشارة المجانية عبر واتساب 01155803307.",
        "",
        "3. 📝 **المقال الطبي والتقرير الشامل لسيو جوجل (Google Blogger SEO Article):**",
        "   - كتابة المقال الطبي الكامل بأسلوب احترافي يتصدر نتائج البحث (SEO H1, H2, H3).",
        "   - يتضمن جدول مقارنة سريرية شامل بين المنتجات والبدائل التجارية.",
        "   - توثيق المراجع الطبية المعتمدة (PubMed / Cochrane / NCBI) بروابطها المذكورة بالأسفل.",
        "",
        "4. 📱 **النصوص الكاملة الصريحة لجميع منصات التواصل (Full Copy - Ready to Publish):**",
        "   اكتب النصوص كاملة حرفياً بدون تلخيص أو نقاط عامة:",
        "   * **منشور فيسبوك طويل وقصصي (Clinical Storytelling):** يبدأ بسؤال ترند مقلق، يشرح علمياً، يطرح الحل بالأسعار وكود HT10، والواتساب وأقوى 10 هاشتاجات مصرية.",
        "   * **بوست وكابشن إنستجرام (Instagram Post & Story):** نص مركز مع استطلاع رأي (Poll) للستوري.",
        "   * **كابشن وهاشتاجات تيك توك وريلز (TikTok & Reels Captions):** نص جذاب وسريع مع هاشتاجات صاعدة.",
        "   * **منشور ونقاش مجتمعي لريديت (Reddit Community Discussion):** نقاش علمي موثق للدعم والتوعية الطبية.",
        "",
        "5. 🎨 **التوجيه البصري الواقعي للصورة (Realistic Visual Direction & Prompt):**",
        "   - بصفتك خبيراً، حدد الأسلوب البصري الأكثر واقعية وملاءمة للحالة (Clinical Realism / Sterile Studio / Macro Dermatology).",
        "   - برومبت إنجليزي وعربي لوصف لقطة الصورة الطبية المعقمة وظهور المنتجات الأصلية والإضاءة الهادئة المتناسقة مع صور مجلد pic المرفقة.",
        "",
        "📥 **التصدير والتنزيل:** قم بتصدير المحتوى كنص (.txt) والفيديو (.mp4) أو الصوت (.m4a) ليتم وضعه في C:\\followUPSHEET\\healing_touch\\media_assets\\manual_inbox.",
        "=" * 60,
        "\n## 📦 أولاً: قائمة المنتجات الطبية المعتمدة ومواصفاتها وأسعارها الحية المسحوبة من الشيت:",
    ]

    for p in products_data:
        md_lines.append(f"### • {p.get('name_ar')} ({p.get('name_en')})")
        md_lines.append(f"- **السعر الحالي:** {p.get('price_display')}")
        md_lines.append(f"- **التصنيف الجراحي:** {p.get('category_badge')}")
        md_lines.append(f"- **الوصف والآلية:** {p.get('short_summary')}")
        md_lines.append(f"- **المصادر السريرية:** {', '.join([c.get('title', '') for c in p.get('citations', [])[:3]])}\n")

    md_lines.append("\n---\n## 🩺 ثانياً: الحالات السريرية الواقعية وبروتوكولات العلاج:")
    for idx, story in enumerate(CLINICAL_STORIES_TEMPLATES, 1):
        md_lines.append(f"### الحالة ({idx}): {story['title']}")
        md_lines.append(story["story_text"])
        md_lines.append(f"**الهاشتاجات:** {story['hashtags']}\n")

    try:
        from github_seo_trend_engine import harvest_live_egypt_trends
        live_map = harvest_live_egypt_trends()
        md_lines.append("\n---\n## 📈 ثالثاً: مؤشر ترندات واستفسارات المرضى الصاعدة في بحث جوجل مصر (Live Egypt Search Trends):")
        for cat_k, q_list in live_map.items():
            md_lines.append(f"- **{cat_k}:** {' ، '.join(q_list[:6])}")
    except Exception:
        pass

    md_lines.append(
        "\n---\n## 💡 رابعاً: الأمر المباشر للنسخ واللصق داخل Google NotebookLM (Master Copy-Paste Prompt):\n"
        "انسخ هذا الأمر والصقه في شات NotebookLM (بعد فتح New Chat والتأكد من وضع علامة ✓ على أحدث ملف مصدر فقط):\n\n"
        "```text\n"
        "تجاهل أي محادثات أو تقارير سابقة بالكامل. بالاعتماد حصرياً على أحدث ملف مصدر تم رفعه اليوم (Healing_Touch_Brief): قم الآن بتوليد حزمة المحتوى والإنتاج الرقمي الكاملة لحالة اليوم:\n"
        "1. شغل أداة الفيديو التوضيحي (Video Overview / Explainer Video) في الاستوديو لإنشاء فيديو شارح يغني عن الصوت لاحتوائه على الشرح المرئي والصوتي معاً.\n"
        "2. اكتب النص الكامل غير المختصر لمنشور فيسبوك الطويل (قصة سريرية + أسعار المنتجات + كود HT10 + واتساب 01155803307 + 10 هاشتاجات ترند).\n"
        "3. اكتب نص بوست وإنستجرام وكابشن ستوري تفاعلي.\n"
        "4. اكتب مقال مدونة بلوجر كاملاً مع جدول مقارنة علمي والمراجع الطبية الـ 11 الموثقة بروابطها.\n"
        "5. اكتب كابشن تيك توك وريلز، ومنشور نقاش مجتمعي لريديت.\n"
        "6. حدد برومبت التوجيه البصري الواقعي للصورة المعقمة.\n"
        "ضع جميع النصوص في تقرير نصي كامل يمكنني تنزيله كملف (.txt) لأضعه مع الفيديو في C:\\followUPSHEET\\healing_touch\\media_assets\\manual_inbox.\n"
        "```\n"
    )

    md_lines.append(
        "\n---\n## 📚 خامساً: المراجع والأبحاث الطبية المعتمدة في هذا الدليل (11 مرجعاً موثقاً):\n"
        "[1] [The Efficacy of Silicone Gel for the Treatment of Hypertrophic Scars and Keloids (NCBI / PMC2918339)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2918339/) — أثبتت الدراسة السريرية أن شرائح السيليكون الطبي تقلل ارتفاع واحمرار الندبات الجراحية والكلويد بنسبة تتجاوز 80% عبر تنظيم ترطيب طبقة الكراتين وتقليل نشاط الكولاجين الزائد.\n"
        "[2] [Review of Silicone Gel Sheeting and Silicone Gel for the Prevention of Hypertrophic Scars (PubMed 28570253)](https://pubmed.ncbi.nlm.nih.gov/28570253/) — مراجعة منهجية تؤكد أن البدء المبكر في وضع شيت السيليكون فور التئام الجرح السطحي بعد العمليات يمنع تكون الندبات البارزة بشكل فعال ومستدام.\n"
        "[3] [Controlled Clinical Trial of Topical Silicone Gel Sheeting in Hypertrophic Scars (J Am Acad Dermatol / PubMed 8113473)](https://pubmed.ncbi.nlm.nih.gov/8113473/) — تجربة سريرية محكمة تثبت تفوق شرائح السيليكون القابلة لإعادة الاستخدام في تليين أنسجة الجرح وإخفاء خط الخياطة الجراحية مقارنة بالعلاجات التقليدية.\n"
        "[4] [كيفية استخدام لصقات السيليكون للندبات ومتى تظهر النتائج (مجموعة الموسى الصحية - 2025)](https://almoosahealthgroup.org/ar/article/%D9%84%D8%B5%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%B3%D9%8A%D9%84%D9%8A%D9%83%D9%88%D9%86/) — دليل طبي عربي شامل يوضح طريقة التدرج في ارتداء شرائح السيليكون من 4 ساعات حتى 24 ساعة يومياً بعد الولادة القيصرية والجراحات لتحقيق التسطيح التام.\n"
        "[5] [Clinical Applications of Topical Silicone in Post-Surgical Scar Management (Yazdan Medical Journal)](https://yazdanmedical.com/clinical-scar-management-protocols) — دراسة إكلينيكية حول بروتوكولات استخدام رول السيليكون الطبي لندبات الرقبة وجراحات الغدة الدرقية والتثدي والوقاية من حكة الأنسجة.\n"
        "[6] [3M Tegaderm +Pad Film Dressing & Opsite Post-Op Clinical Evidence Summary (3M Medical Division)](https://multimedia.3m.com/mws/media/864087O/tegaderm-pad-film-dressing-clinical-summary.pdf) — ملخص الدراسات المقارنة لضمادات 3M Tegaderm +Pad، والذي يثبت توفير حاجز عازل تماماً للماء والبكتيريا مع السماح للجلد بالتنفس والاستحمام الآمن بدون التهاب الجرح.\n"
        "[7] [طرق العناية بالجروح بعد العمليات الجراحية والوقاية من الندبات (ويب طب WebTeb)](https://www.webteb.com/articles/%D8%A7%D9%84%D8%B9%D9%86%D8%A7%D9%8A%D8%A9-%D8%A8%D8%A7%D9%84%D8%AC%D8%B1%D9%88%D8%AD-%D8%A8%D8%B9%D8%AF-%D8%A7%D9%84%D8%B9%D9%85%D9%84%D9%8A%D8%A7%D8%AA_20815) — دليل طبي سريري معتمد حول آليات التئام الأنسجة الجراحية ودور العزل المائي وتثبيت حواف الجرح في سرعة التعافي.\n"
        "[8] [Dressings and topical agents for preventing surgical site infections (Cochrane Systematic Reviews)](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD011048.pub2/full) — مراجعة كوكرين المنهجية التي تؤكد تفوق الضمادات الفيلمية شبه المنفذة في منع تسرب الميكروبات إلى خطوط الخياطة الجراحية.\n"
        "[9] [International Clinical Recommendations on Scar Management: An Updated Review (PRS Global Open)](https://journals.lww.com/prsgo/fulltext/2020/08000/international_clinical_recommendations_on_scar.21.aspx) — التوصيات الإكلينيكية الدولية لأطباء جراحة التجميل والتي تضع السيليكون الطبي والضغط الميكانيكي كعلاج أولي وقائي وعلاجي لجميع أنواع الجروح الجراحية.\n"
        "[10] [نصائح بعد عملية الولادة القيصرية ومتى يمكن الاستحمام بأمان (د. أحمد مرزوق - سبتمبر 2026)](https://www.doctorahmedmarzouk.com/ar/blogs/%D9%86%D8%B5%D8%A7%D8%A6%D8%AD-%D8%A8%D8%B9%D8%AF-%D8%B9%D9%85%D9%84%D9%8A%D8%A9-%D8%A7%D9%84%D9%88%D9%84%D8%A7%D8%AF%D8%A9-%D8%A7%D9%84%D9%82%D9%8A%D8%B5%D8%B1%D9%8A%D8%A9) — إرشادات طبية حول حماية جرح القيصرية من البلل والتلوث خلال الأسبوعين الأولين وكيفية العناية بمكان الخياطة التجميلية لمنع العدوى.\n"
        "[11] [Effect of Postrhinoplasty Taping on Postoperative Edema and Nasal Draping: A Randomized Clinical Trial (ResearchGate)](https://www.researchgate.net/publication/295878140_Effect_of_Postrhinoplasty_Taping_on_Postoperative_Edema_and_Nasal_Draping_A_Randomized_Clinical_Trial) — دراسة عشوائية محكمة على مرضى تجميل الأنف أثبتت أن استخدام شريط 3M Micropore الطبي بانتظام بعد فك الجبيرة يقلل سماكة الجلد وتورم أرنبة الأنف (Supratip Edema).\n"
    )

    today_str = datetime.now().strftime("%Y-%m-%d")
    timestamp_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_file = NOTEBOOK_ARCHIVE_DIR / f"Healing_Touch_Brief_{timestamp_filename}.md"
    archive_file.write_text("\n".join(md_lines), encoding="utf-8")

    out_file = NOTEBOOKLM_DIR / f"Healing_Touch_Brief_{timestamp_filename}.md"
    out_file.write_text("\n".join(md_lines), encoding="utf-8")

    # تحديث الملف الرئيسي الثابت أيضاً لمن يفضل الاستبدال
    master_file = NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md"
    master_file.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"[+] 🧠 تم إنشاء ملف المصدر المؤرخ بالوقت بنجاح: {out_file.name}")
    print(f"[+] 📁 تم حفظ نسخة في أرشيف الترندات الزمني: {archive_file}")

    # جلب صور طبية جديدة من Pexels و Pixabay وحفظها في مجلد pic بأسماء المنصات والتاريخ
    try:
        print("\n[*] 📸 جاري جلب صور طبية جديدة من Pexels و Pixabay لمجلد pic...")
        cat_samples = [("c-section", "ولادة قيصرية"), ("rhinoplasty", "تجميل أنف"), ("bariatric", "تكميم سمنة"), ("thyroid", "غدة درقية")]
        for cat_k, cat_name in cat_samples:
            photo = get_clinical_case_photo(f"حالة {cat_name}", cat_k)
            src_img = photo.get("local_path", "")
            if src_img and os.path.isfile(src_img):
                src_p = Path(src_img)
                # نسخ الصورة باسم فيسبوك وإنستجرام وتيك توك مع التاريخ والوقت
                fb_pic = NOTEBOOK_PIC_DIR / f"{timestamp_filename}_[فيسبوك_وإنستجرام]_{cat_k}_{src_p.name}"
                story_pic = NOTEBOOK_PIC_DIR / f"{timestamp_filename}_[تيكتوك_وستوري]_{cat_k}_{src_p.name}"
                shutil.copy2(src_img, fb_pic)
                shutil.copy2(src_img, story_pic)
        print(f"[+] 🖼️ تم تنزيل وتنظيم الصور الطبية بنجاح في: {NOTEBOOK_PIC_DIR}")
    except Exception as e:
        print(f"[!] تنبيه جلب الصور لمجلد pic: {e}")

    return str(out_file)


# =============================================================================
# 🚀 القسم الخامس: النشر عبر Meta Graph API وتحديث الشيت ورادار الجروبات
# =============================================================================
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
                print(f"[+] 📸 تم النشر تلقائياً وحياً على إنستجرام بنجاح! Post ID: {publish_res['id']}")
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
    server.timeout = 120
    print("[*] ⏳ في انتظار ضغطك على زر 'Allow' في المتصفح...")
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

    # 2. فتح مدونة جوجل Blogger للمعاينة والمراجعة
    blogger_url = f"https://draft.blogger.com/blog/posts/{BLOGGER_BLOG_ID}"
    print(f"   • [بلوجر] عرض مدونة جوجل: {blogger_url}")
    open_url_in_default_browser(blogger_url)

    # 3. فتح صفحة رفع البوست لإنستجرام
    ig_upload_url = "https://www.instagram.com/"
    print(f"   • [إنستجرام] فتح صفحة إنستجرام للرفع المباشر: {ig_upload_url}")
    open_url_in_default_browser(ig_upload_url)

    # 4. فتح صفحة رفع الفيديو لتيك توك
    tiktok_upload_url = "https://www.tiktok.com/creator-center/upload?from=upload"
    print(f"   • [تيك توك] فتح صفحة رفع فيديو تيك توك: {tiktok_upload_url}")
    open_url_in_default_browser(tiktok_upload_url)


def run_unified_studio_and_publish(template_idx: int = None, dry_run: bool = False) -> tuple[bool, str]:
    """الدورة الموحدة الشاملة: رصد الترند الصاعد + اختيار الحالة + صورة جديدة + تصميم كانفا + فيديو ريلز + بلوجر + NotebookLM + نشر."""
    print("=" * 65)
    print("🌿 هيلينج تاتش مصر | المحرك الشامل للتصميم والفيديو والترندات والنشر")
    print("=" * 65)

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

    photo_info = get_clinical_case_photo(tmpl["title"], tmpl["category"])
    raw_img = photo_info.get("local_path", "")
    print(f"[*] 📸 الصورة المختارة: {Path(raw_img).name if raw_img else 'افتراضية'} (المصدر: {photo_info.get('source')})")

    cards = generate_branded_card(tmpl, raw_img) if raw_img else {"square_path": "", "story_path": ""}
    square_img_path = cards.get("square_path", "") or raw_img
    story_img_path = cards.get("story_path", "")

    video_path = generate_tiktok_reel_video(story_img_path, duration_sec=8) if story_img_path else ""
    export_canva_bulk_csv(CLINICAL_STORIES_TEMPLATES)

    blogger_post = format_clinical_case_for_blogger(tmpl, photo_info)
    generate_blogger_atom_xml([blogger_post])
    notebook_file = export_notebooklm_master_source()

    # فحص مجلد الاستقبال الموحد manual_inbox إن وضع المستخدم به أي مخرج من NotebookLM (نص، صوت، فيديو، صورة)
    # 1. فحص الصوتيات الجديدة ونقلها أوتوماتيكياً لمجلد الصوت لدمجها فوراً
    for aud_f in list(MANUAL_INBOX_DIR.glob("*.m4a")) + list(MANUAL_INBOX_DIR.glob("*.mp3")) + list(MANUAL_INBOX_DIR.glob("*.wav")):
        dest_aud = NOTEBOOK_AUDIO_DIR / aud_f.name
        if not dest_aud.exists():
            shutil.copy2(str(aud_f), str(dest_aud))
            print(f"[+] 🎙️ تم التقاط ونقل ملف صوتي من manual_inbox إلى audio_inputs ({aud_f.name})!")

    # 2. فحص النصوص والمستندات (txt, md) المخصصة لحالة اليوم فقط
    txt_files = sorted(list(MANUAL_INBOX_DIR.glob("*.txt")) + list(MANUAL_INBOX_DIR.glob("*.md")), key=lambda x: x.stat().st_mtime, reverse=True)
    if txt_files:
        # البحث عن ملف نصي يتطابق مع الحالة الحالية أو استبعاد الملف المجمع الشامل
        target_kw = "csection" if tmpl["category"] == "c-section" else ("rhino" if tmpl["category"] == "rhinoplasty" else ("bariatric" if tmpl["category"] == "bariatric" else "thyroid"))
        matching_txt = next((f for f in txt_files if target_kw in f.name.lower()), None)
        chosen_txt = matching_txt if matching_txt else next((f for f in txt_files if "notebooklm_exported_pack" not in f.name and "حزمة" not in f.name), None)
        if chosen_txt:
            custom_text = chosen_txt.read_text(encoding="utf-8").strip()
            if custom_text and len(custom_text) > 50:
                print(f"[+] 📝 تم اكتشاف واعتماد نص سريري راقٍ لحالة اليوم من manual_inbox ({chosen_txt.name})!")
                tmpl["story_text"] = custom_text

    # 3. فحص الصور والتصاميم المخصصة من المستخدم (jpg, png)
    img_files = sorted(list(MANUAL_INBOX_DIR.glob("*.jpg")) + list(MANUAL_INBOX_DIR.glob("*.png")), key=lambda x: x.stat().st_mtime, reverse=True)
    if img_files:
        square_img_path = str(img_files[0])
        story_img_path = str(img_files[0])
        print(f"[+] 🎨 تم اكتشاف واعتماد تصميم يدوي راقٍ من manual_inbox ({Path(square_img_path).name})!")
    else:
        # إذا لم يضع المستخدم صورة يدوية، لا يتم التوليد الآلي العشوائي بل نعتمد الكارت الرسمي الموحد
        square_img_path = str(BASE_DIR / "docs" / "assets" / "og-image.jpg")
        story_img_path = square_img_path

    # 4. فحص الفيديوهات المباشرة (mp4)
    vid_files = sorted(list(MANUAL_INBOX_DIR.glob("*.mp4")), key=lambda x: x.stat().st_mtime, reverse=True)
    if vid_files:
        video_path = str(vid_files[0])
        print(f"[+] 🎬 تم اكتشاف واعتماد فيديو يدوي راقٍ من manual_inbox ({Path(video_path).name})!")

    # تجهيز ملفات نصوص صريحة ومستقلة لكل منصة (فيسبوك، إنستجرام، تيك توك، بلوجر، وريديت) بتاريخ اليوم
    date_str = datetime.now().strftime("%Y-%m-%d")
    full_caption = f"{tmpl['story_text']}\n\n{tmpl['hashtags']}"
    blogger_text = f"<h1>{blogger_post['title']}</h1>\n\n{blogger_post['html_content']}"
    reddit_text = f"**{tmpl['title']}**\n\n{tmpl['story_text']}\n\n---\n**استشارة مجانية عبر واتساب:** 01155803307\n**كود الخصم:** HT10 (شحن مجاني ومعاينة قبل الدفع)\n\n{tmpl['hashtags']}"
    
    (BRANDED_DIR / f"{date_str}_[نص_بوست_وستوري_إنستجرام].txt").write_text(full_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[نص_كابشن_وهاشتاجات_تيكتوك].txt").write_text(full_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[نص_منشور_فيسبوك].txt").write_text(full_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[مقال_مدونة_جوجل_Blogger].txt").write_text(blogger_text, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[منشور_ومقال_Reddit].txt").write_text(reddit_text, encoding="utf-8")
    
    copy_to_windows_clipboard(full_caption)
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
        "caption": tmpl["story_text"],
        "hashtags": tmpl["hashtags"],
        "row_index": -1,
    }

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
        print("\nالنص السريري (مدمج بالترندات الصاعدة):")
        print(tmpl["story_text"])
        print("\nالهاشتاجات (مدمجة بهاشتاجات الترند الحي):")
        print(tmpl["hashtags"])
        print("=" * 65)
        # فتح تبويبات المتصفح المطلوبة حتى في وضع المعاينة
        open_tabs_in_default_windows_browser(fb_post_url="", blogger_post_file=blogger_post['file_path'])
        return True, ""

    ok, permalink = publish_facebook_graph_api(post_data, square_img_path)
    publish_instagram_graph_api(f"{tmpl['story_text']}\n\n{tmpl['hashtags']}")
    publish_to_blogger_webhook(blogger_post)
    publish_to_reddit_api(tmpl["title"], f"{tmpl['story_text']}\n\n{tmpl['hashtags']}")
    if ok:
        record_post_history(chosen_idx, tmpl["title"])
    # فتح تبويبات المتصفح المطلوبة فوراً
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
        src_path = export_notebooklm_master_source()
        print("\n" + "=" * 65)
        print("🧠 [خطوات بسيطة للحصول على الفيديو والصوت والنصوص والمقالات كاملة]:")
        print("=" * 65)
        print(f"1. تم إنشاء وتحديث الملف المرجعي الحامل للبرومبت والتعليمات الصارمة:\n   👉 {src_path}")
        print("2. جاري فتح صفحة Google NotebookLM في متصفحك لرفع الملف أو تحديثه...")
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
