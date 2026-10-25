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

for d in (MEDIA_DIR, CASES_DIR, BRANDED_DIR, BLOGGER_DIR, NOTEBOOKLM_DIR, NOTEBOOK_AUDIO_DIR):
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

    raw_path = Path(raw_img_path).resolve()
    b64_data = base64.b64encode(raw_path.read_bytes()).decode("ascii")
    bg_uri = f"data:image/jpeg;base64,{b64_data}"
    slug = f"branded_{cat}_{raw_path.stem}"
    square_png = BRANDED_DIR / f"{slug}_square.png"
    story_png = BRANDED_DIR / f"{slug}_story.png"

    print(f"[*] 🎨 جاري تصميم بوست أوتو-كانفا للموضوع: {title}...")
    asyncio.run(_render_image_playwright(build_card_html(title, badge, key_tip, bg_uri, "square"), square_png, 1080, 1080))
    asyncio.run(_render_image_playwright(build_card_html(title, badge, key_tip, bg_uri, "story"), story_png, 1080, 1920))
    print(f"[+] ✅ تم حفظ بطاقات السوشيال ميديا: {square_png.name} & {story_png.name}")

    return {"square_path": str(square_png), "story_path": str(story_png), "title": title, "badge": badge, "key_tip": key_tip}


def generate_tiktok_reel_video(story_card_path: str, duration_sec: int = 8) -> str:
    """تحويل البطاقة الطولية إلى فيديو MP4 مع دمج تلقائي لصوت البودكاست من NotebookLM إن وجد."""
    in_path = Path(story_card_path).resolve()
    out_mp4 = BRANDED_DIR / f"{in_path.stem}_reel.mp4"

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
    """تجهيز ملف المعرفة الشامل الجاهز للرفع المباشر في Google NotebookLM لتوليد البودكاست والخرائط الذهنية."""
    registry_path = BASE_DIR / "products_registry.json"
    products_data = []
    if registry_path.exists():
        try:
            products_data = json.loads(registry_path.read_text(encoding="utf-8")).get("products", [])
        except Exception:
            pass

    md_lines = [
        "# 🌿 الدليل المرجعي الشامل لمشروع هيلينج تاتش مصر (Healing Touch Egypt - NotebookLM Master Source)",
        f"**تاريخ التحديث:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "**الهوية:** منصة استشارات وعناية طبية متخصصة في التعافي بعد العمليات الجراحية وعلاج الندبات في مصر.",
        "**العرض الحصري المعتمد:** كود الخصم `HT10` يمنح العميل (شحن مجاني لكافة محافظات مصر + حق فتح ومعاينة الشحنة قبل الدفع).",
        "**التواصل المباشر للاستشارة المجانية مع أخصائية العناية بالتعافي:** واتساب `01155803307`.",
        "\n---\n## 📦 أولاً: قائمة المنتجات الطبية المعتمدة ومواصفاتها وأسعارها:",
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
        "\n---\n## 💡 رابعاً: أوامر مقترحة (Prompts) للنسخ داخل Google NotebookLM:\n"
        "1. **لتوليد بودكاست صوتي (Audio Overview):**\n"
        '   `ناقشا باللهجة المصرية الودودة والاحترافية مشاكل الأمهات بعد الولادة القيصرية وحالات تجميل الأنف والتكميم، وكيف تساعدهم منتجات هيلينج تاتش الطبية الأصلية مع كود الخصم HT10 والاستشارة المجانية مع أخصائية التعافي.`\n'
        "2. **لتوليد سكربتات فيديوهات ريلز وتيك توك:**\n"
        '   `استخرج 5 سكربتات فيديو قصيرة (30 ثانية) بأسلوب طبي شيق يبدأ بسؤال شائع من المريض وينتهي بالحل العلمي من منتجات هيلينج تاتش.`'
    )

    out_file = NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md"
    out_file.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"[+] 🧠 تم تحديث حزمة Google NotebookLM بنجاح: {out_file}")
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


def open_tabs_in_default_windows_browser(fb_post_url: str, problems_df: pd.DataFrame, open_groups_radar: bool = True):
    if fb_post_url:
        print(f"\n[🔗 فيسبوك] فتح رابط البوست المنشور على صفحتك:\n    {fb_post_url}")
        open_url_in_default_browser(fb_post_url)

    if open_groups_radar:
        print("\n[🔍 رادار الجروبات] فتح تبويبات البحث عن مشاكل العملاء في متصفحك الافتراضي...")
        first_reply_copied = False
        if problems_df is not None and not problems_df.empty:
            for idx, row in problems_df.iterrows():
                keywords_raw = str(row.get("الكلمات البحثية لرصد المشكلة", ""))
                smart_reply = str(row.get("نص الرد التفاعلي الجاهز لجذب العميل (80% نصيحة + 20% توجيه للصفحة)", ""))
                parts = [p.strip() for p in keywords_raw.replace(",", "،").split("،") if p.strip()]
                if not parts:
                    continue
                first_keyword = f"{parts[0]} {parts[1]}" if (len(parts) > 1 and (len(parts[0].split()) == 1 or parts[0] == "عدم تماثل")) else parts[0]
                search_url = f"https://www.facebook.com/search/posts?q={urllib.parse.quote(first_keyword)}"
                if not first_reply_copied and smart_reply:
                    copy_to_windows_clipboard(smart_reply)
                    first_reply_copied = True
                    print(f"\n📋 [تم نسخ أول رد استشاري في الحافظة Clipboard جاهز للصق Ctrl+V]:\n   {smart_reply}\n")
                print(f"   • فتح تبويب بحث ({idx + 1}): '{first_keyword}'")
                open_url_in_default_browser(search_url)
        else:
            for kw in DEFAULT_SURGICAL_KEYWORDS:
                open_url_in_default_browser(f"https://www.facebook.com/search/posts?q={urllib.parse.quote(kw)}")


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
        return True, ""

    ok, permalink = publish_facebook_graph_api(post_data, square_img_path)
    if ok:
        record_post_history(chosen_idx, tmpl["title"])
    return ok, permalink


def main():
    parser = argparse.ArgumentParser(description="المحرك الموحد لمشروع هيلينج تاتش مصر")
    parser.add_argument(
        "--mode",
        choices=["all", "auto-daily", "publish", "dry-run", "groups", "notebooklm", "open-latest"],
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

    if args.mode == "notebooklm":
        export_notebooklm_master_source()
        return

    if args.mode == "groups":
        problems_df = fetch_sheet_tab(PROBLEMS_TAB_NAME)
        open_tabs_in_default_windows_browser(fb_post_url="", problems_df=problems_df, open_groups_radar=True)
        return

    if args.mode == "open-latest":
        log = load_published_log()
        latest_url = log[-1].get("permalink_url", "") if log else f"https://www.facebook.com/{FB_PAGE_ID}"
        problems_df = fetch_sheet_tab(PROBLEMS_TAB_NAME)
        open_tabs_in_default_windows_browser(fb_post_url=latest_url, problems_df=problems_df, open_groups_radar=True)
        return

    is_dry = args.dry_run or (args.mode == "dry-run")
    ok, permalink = run_unified_studio_and_publish(template_idx=args.index, dry_run=is_dry)

    if not is_dry and args.mode == "all":
        try:
            problems_df = fetch_sheet_tab(PROBLEMS_TAB_NAME)
        except Exception:
            problems_df = pd.DataFrame()
        open_tabs_in_default_windows_browser(fb_post_url=permalink, problems_df=problems_df, open_groups_radar=True)


if __name__ == "__main__":
    main()
