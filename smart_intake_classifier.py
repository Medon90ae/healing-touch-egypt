#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | Healing Touch Egypt
محرك الفرز والتصنيف الذكي التلقائي وموجه المنصات (Smart Intake & Platform Router)
=============================================================================
يتيح للمستخدم رمي أي ملف (فيديو، صورة، نص، صوت) في manual_inbox دون أي فرز يدوياً.
يقوم المحرك تلقائياً بـ:
1. قراءة المحتوى والاسم واستنتاج التخصص الجراحي المناسب ونوع الميديا.
2. التعرف الذكي على ملف كل منصة وتوجيهه لمنصته المحددة (فيسبوك، إنستجرام، تيك توك، يوتيوب، بلوجر، ريديت).
3. استخراج متن المحتوى الفعلي الخالي من أي ترويسات أو بيانات فنية ونظافة النشر بنسبة 100%.
4. أرشفة الملفات بعد الاستخدام تلقائياً.
"""

import os
import re
import json
import shutil
import subprocess
import urllib.parse
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    Image = None

# الكلمات الدلالية السريرية لكل تخصص جراحي (عربي + إنجليزي)
CATEGORY_KEYWORDS = {
    "rhinoplasty": [
        "أنف", "الانف", "تجميل أنف", "أرنبة", "ارنبة", "دعامة", "دعامات", "خياشيم",
        "غضروف", "غضاريف", "rhino", "rhinoplasty", "retainer", "nostril", "فتحات الأنف",
        "فتحات الانف", "قص الجناح", "تماثل", "نوستريل", "ريتينر", "سبيشلست", "جناح الأنف"
    ],
    "c-section": [
        "قيصر", "قيصرية", "كلويد", "شاور", "استحمام", "ولادة", "ندبة", "ندبات",
        "tegaderm", "bupy", "تيجاديرم", "بوبي", "شيت", "سيليكون", "csection",
        "c-section", "سيكاتريكس", "جرح الولادة", "فرد الندبة"
    ],
    "bariatric": [
        "تكميم", "سمنة", "منظار", "ثقوب", "ثقب", "تحويل مسار", "قص معدة",
        "opsite", "أوبسايت", "اوبسايت", "بخاخ", "رشاش", "bariatric", "sleeve"
    ],
    "thyroid": [
        "غدة", "درقية", "رقبة", "شمس", "عنق", "استئصال الغدة", "micropore",
        "ميكروبور", "بلاستر ورقي", "thyroid", "neck", "حماية الندبة من الشمس"
    ],
    "gynecomastia": [
        "تثدي", "صدر", "مشد", "شفط دهون الصدر", "gynecomastia", "compression"
    ],
    "tummy_tuck": [
        "شد بطن", "ترميم", "فتق", "مشد بطن", "tummy_tuck", "abdominoplasty"
    ]
}


def read_resilient_text(target: Path | str) -> str:
    """قراءة آمنة لملفات النصوص بدعم كافة ترميزات ويندوز الشائعة."""
    p = Path(target)
    if not p.exists() or not p.is_file():
        return ""
    for enc in ["utf-8-sig", "utf-8", "cp1256", "latin-1"]:
        try:
            return p.read_text(encoding=enc)
        except Exception:
            continue
    try:
        return p.read_bytes().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def find_active_inbox_files(inbox_dir: Path) -> list[Path]:
    """
    العثور على الملفات المرفوعة الحالية في manual_inbox.
    إذا كان الصندوق فارغاً، يتم فحص مجلدات archive واختيار ملفات أحدث حملة مؤرخة تلقائياً.
    """
    if not inbox_dir.exists():
        return []
    
    current_files = [
        f for f in inbox_dir.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]
    if current_files:
        return current_files

    # فحص الأرشيف في media_assets/archive أو manual_inbox/archive
    arch_dirs_to_check = []
    for candidate_root in [inbox_dir.parent / "archive", inbox_dir / "archive"]:
        if candidate_root.exists() and candidate_root.is_dir():
            for sdir in candidate_root.iterdir():
                if sdir.is_dir():
                    arch_dirs_to_check.append(sdir)
    arch_subdirs = sorted(arch_dirs_to_check, key=lambda x: x.name, reverse=True)
    for sdir in arch_subdirs:
        arch_files = [
            f for f in sdir.iterdir()
            if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
        ]
        if arch_files:
            return arch_files
    return []


def probe_media_dimensions(file_path: Path | str) -> dict:
    """
    فحص أبعاد الوسائط (صورة أو فيديو) وحساب نسبة العرض للارتفاع:
    - 9:16 طولي (Reels, Shorts, TikTok)
    - 16:9 عرضي (YouTube Main, Blogger, Landing Page)
    - 1:1 مربع
    """
    p = Path(file_path)
    default_res = {
        "width": 1080,
        "height": 1920,
        "aspect_ratio": 9 / 16,
        "is_vertical_9_16": True,
        "is_horizontal_16_9": False,
        "orientation": "vertical"
    }
    if not p.exists() or not p.is_file():
        return default_res

    ext = p.suffix.lower()
    # 1. إذا كان صورة
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp"]:
        if Image:
            try:
                with Image.open(p) as img:
                    w, h = img.size
                    ratio = w / h if h else 1.0
                    is_vert = (h > w)
                    return {
                        "width": w,
                        "height": h,
                        "aspect_ratio": ratio,
                        "is_vertical_9_16": is_vert,
                        "is_horizontal_16_9": (w >= h),
                        "orientation": "vertical" if is_vert else ("horizontal" if w > h else "square")
                    }
            except Exception:
                pass
        return default_res

    # 2. إذا كان فيديو
    if ext in [".mp4", ".mov", ".mkv", ".webm", ".avi"]:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "json",
            str(p)
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0 and res.stdout:
                data = json.loads(res.stdout)
                streams = data.get("streams", [])
                if streams:
                    w = int(streams[0].get("width", 1080))
                    h = int(streams[0].get("height", 1920))
                    ratio = w / h if h else 1.0
                    is_vert = (h > w)
                    return {
                        "width": w,
                        "height": h,
                        "aspect_ratio": ratio,
                        "is_vertical_9_16": is_vert,
                        "is_horizontal_16_9": (w >= h),
                        "orientation": "vertical" if is_vert else "horizontal"
                    }
        except Exception:
            pass

    return default_res


def is_video_silent(video_path: Path | str) -> bool:
    """فحص ما إذا كان ملف الفيديو صامتاً بدون مسار صوتي."""
    p = Path(video_path)
    if not p.exists() or not p.is_file():
        return False
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_type",
        "-of", "json",
        str(p)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0 and res.stdout:
            data = json.loads(res.stdout)
            streams = data.get("streams", [])
            return len(streams) == 0
    except Exception:
        pass
    return False


def merge_silent_video_with_audio(video_path: Path | str, audio_path: Path | str, output_path: Path | str) -> bool:
    """دمج ملف صوتي سريري مع فيديو صامت باستخدام FFmpeg فائق السرعة."""
    vp = Path(video_path)
    ap = Path(audio_path)
    out_p = Path(output_path)
    if not vp.exists() or not ap.exists():
        return False
    out_p.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(vp),
        "-i", str(ap),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(out_p)
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return res.returncode == 0 and out_p.exists() and out_p.stat().st_size > 0
    except Exception:
        return False


def classify_file_category(file_path: Path) -> str:
    """استنتاج التخصص الجراحي للملف بناءً على اسمه ومحتواه النصي إن وُجد."""
    name_lower = file_path.name.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}

    # فحص اسم الملف (وزن أكبر)
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in name_lower:
                scores[cat] += 6

    # فحص محتوى الملف إذا كان نصاً أو HTML
    if file_path.suffix.lower() in [".txt", ".md", ".html", ".htm", ".json"]:
        try:
            sample_text = read_resilient_text(file_path)[:4000].lower()
            for cat, kws in CATEGORY_KEYWORDS.items():
                for kw in kws:
                    count = sample_text.count(kw.lower())
                    if count > 0:
                        scores[cat] += min(count, 5)
        except Exception:
            pass

    best_cat = max(scores, key=scores.get)
    if scores[best_cat] > 0:
        return best_cat
    return "c-section"  # الافتراضي إذا لم تتطابق أي كلمة


def route_platform_text_files(files_or_dir) -> dict:
    """
    R1: موجه ومنسق ملفات النصوص لكل منصة (Platform-Specific Text Router).
    يقوم بالفحص الذكي للاسم والمحتوى لتوجيه كل ملف لمنصته المحددة بدقة 100%:
    - facebook: منشور فيسبوك
    - instagram: حزمة إنستجرام
    - tiktok: حزمة وسيناريو تيك توك
    - youtube: حزمة وسيناريو يوتيوب
    - blogger: مقال بلوجر والدليل الطبي الشامل
    - reddit: منشور ومقال ريديت / التقرير السريري الشامل
    - general: باقي النصوص العامة
    """
    if isinstance(files_or_dir, (str, Path)):
        p = Path(files_or_dir)
        if p.is_dir():
            candidates = [
                f for f in p.iterdir()
                if f.is_file() and f.suffix.lower() in [".txt", ".md"] and not f.name.startswith("PROMPTS")
            ]
            if not candidates:
                arch_candidates = []
                for candidate_root in [p.parent / "archive", p / "archive"]:
                    if candidate_root.exists() and candidate_root.is_dir():
                        for sdir in candidate_root.iterdir():
                            if sdir.is_dir():
                                arch_candidates.append(sdir)
                arch_subdirs = sorted(arch_candidates, key=lambda x: x.name, reverse=True)
                for sdir in arch_subdirs:
                    candidates = [
                        f for f in sdir.iterdir()
                        if f.is_file() and f.suffix.lower() in [".txt", ".md"] and not f.name.startswith("PROMPTS")
                    ]
                    if candidates:
                        break
        else:
            candidates = [p] if p.suffix.lower() in [".txt", ".md"] else []
    else:
        candidates = [Path(f) for f in files_or_dir if Path(f).suffix.lower() in [".txt", ".md"] and not Path(f).name.startswith("PROMPTS")]

    routed = {
        "facebook": None,
        "instagram": None,
        "tiktok": None,
        "youtube": None,
        "blogger": None,
        "reddit": None,
        "general": []
    }

    scored_candidates = []
    for f in candidates:
        name_l = f.name.lower()
        head_sample = read_resilient_text(f)[:1000].lower() if f.is_file() else ""
        scored_candidates.append((f, name_l, head_sample))

    allocated = set()

    # أنماط مطابقة أسماء الملفات (Pass 1 - Highest Precedence)
    # نستخدم حدود أحرف آمنة تدعم snake_case مثل fb_... و ig_... و yt_...
    NAME_PATTERNS = {
        "facebook": re.compile(r"(?:فيسبوك|فيس[\s_]*بوك|facebook|(?<![a-zA-Z0-9])fb(?![a-zA-Z0-9]))", re.IGNORECASE),
        "instagram": re.compile(r"(?:إنستجرام|انستجرام|إنستغرام|انستغرام|انستا|(?<![a-zA-Z0-9])insta(?![a-zA-Z0-9])|instagram|(?<![a-zA-Z0-9])ig(?![a-zA-Z0-9]))", re.IGNORECASE),
        "tiktok": re.compile(r"(?:تيك[\s_]*توك|تيكتوك|tiktok|(?<![ء-يa-zA-Z])تيك(?![ء-يa-zA-Z]))", re.IGNORECASE),
        "youtube": re.compile(r"(?:يوتيوب|يو[\s_]*تيوب|youtube|(?<![a-zA-Z0-9])yt(?![a-zA-Z0-9]))", re.IGNORECASE),
        "blogger": re.compile(r"(?:بلوجر|بلوقر|blogger|الدليل[\s_]*الطبي[\s_]*الشامل|(?<![ء-يa-zA-Z])مقال(?![ء-يa-zA-Z]))", re.IGNORECASE),
        "reddit": re.compile(r"(?:ريديت|reddit|التقرير[\s_]*السريري[\s_]*الشامل|(?<![ء-يa-zA-Z])تقرير(?![ء-يa-zA-Z]))", re.IGNORECASE),
    }

    # أنماط مطابقة الترويسات والمحتوى (Pass 2 - Platform-Specific Content Fallback)
    CONTENT_PATTERNS = {
        "facebook": re.compile(r"(?:منشور[\s_]*فيسبوك|بوست[\s_]*فيسبوك|Facebook[\s_]*Post)", re.IGNORECASE),
        "instagram": re.compile(r"(?:حزمة[\s_]*(?:إنستجرام|انستجرام|إنستغرام|انستغرام)|كابشن[\s_]*(?:إنستجرام|انستجرام|إنستغرام|انستغرام)|دليل[\s_]*الكاروسيل|سكريبت[\s_]*ريلز|Instagram[\s_]*Reel)", re.IGNORECASE),
        "tiktok": re.compile(r"(?:حزمة[\s_]*(?:تيك[\s_]*توك|تيكتوك)|سيناريو[\s_]*(?:تيك[\s_]*توك|تيكتوك)|كابشن[\s_]*(?:تيك[\s_]*توك|تيكتوك)|الهوك[\s_]*البصري|TikTok[\s_]*Script)", re.IGNORECASE),
        "youtube": re.compile(r"(?:حزمة[\s_]*سيو[\s_]*يوتيوب|سيو[\s_]*يوتيوب|سكريبت[\s_]*الفيديو[\s_]*الكامل[\s_]*16:9|العنوان[\s_]*السريري[\s_]*الجذاب|YouTube SEO Title|YouTube Tags List)", re.IGNORECASE),
        "blogger": re.compile(r"(?:الدليل[\s_]*الطبي[\s_]*الشامل|مقال[\s_]*بلوجر|الوصف[\s_]*التعريفي|Google Blogger)", re.IGNORECASE),
        "reddit": re.compile(r"(?:التقرير[\s_]*السريري[\s_]*الشامل|Reddit Post|مجتمعات[\s_]*ريديت)", re.IGNORECASE),
    }

    # المرحلة الأولى (Pass 1): مطابقة اسم الملف الصريحة لكل منصة بأعلى أولوية
    for plat in ["facebook", "instagram", "tiktok", "youtube", "blogger", "reddit"]:
        pat = NAME_PATTERNS[plat]
        for f, name_l, head in scored_candidates:
            if f in allocated:
                continue
            if plat == "blogger" and ("ريديت" in name_l or "reddit" in name_l):
                continue
            if plat == "reddit" and ("بلوجر" in name_l or "blogger" in name_l):
                continue
            if pat.search(name_l):
                routed[plat] = f
                allocated.add(f)
                break

    # المرحلة الثانية (Pass 2): فحص ترويسات ومحتوى الملفات المتبقية للمنصات التي لم يحدد لها ملف
    for plat in ["facebook", "instagram", "tiktok", "youtube", "blogger", "reddit"]:
        if routed[plat] is not None:
            continue
        c_pat = CONTENT_PATTERNS[plat]
        for f, name_l, head in scored_candidates:
            if f in allocated:
                continue
            if plat == "blogger" and ("ريديت" in name_l or "reddit" in name_l):
                continue
            if plat == "reddit" and ("بلوجر" in name_l or "blogger" in name_l):
                continue
            if c_pat.search(head):
                routed[plat] = f
                allocated.add(f)
                break

    # دعم علامة (نص المنشور الكامل) لفيسبوك فقط إذا كان فيسبوك شاغراً والملف لا يخص منصة أخرى بوضوح
    if routed["facebook"] is None:
        other_platform_names = ["instagram", "إنستجرام", "انستجرام", "tiktok", "تيك", "youtube", "يوتيوب", "blogger", "بلوجر", "reddit", "ريديت"]
        for f, name_l, head in scored_candidates:
            if f in allocated:
                continue
            if any(op in name_l for op in other_platform_names):
                continue
            if re.search(r"(?:نص[\s_]*المنشور[\s_]*الكامل|نص[\s_]*المنشور[\s_]*المباشر)", head):
                routed["facebook"] = f
                allocated.add(f)
                break

    # جمع الملفات المتبقية كملفات عامة
    for f in candidates:
        if f not in allocated:
            routed["general"].append(f)

    return routed


def extract_clean_content(file_path_or_text, platform: str = "facebook", landing_url: str = "", whatsapp_url: str = "") -> dict:
    """
    R2: مستخرج متن المحتوى السريري الفعلي (Clean Content Extractor).
    - تجاوز كافة الترويسات الفنية والبيانات الوصفية مثل (المشروع: منصة هيلينج تاتش، السيو الموجه...).
    - استخراج المتن الحقيقي الخالص للنشر.
    - دمج روابط الهبوط والواتساب بصورة نظيفة أسفل المتن الحقيقي مع الحفاظ على كود HT10 ورقم 01155803307.
    """
    if isinstance(file_path_or_text, bytes):
        for enc in ["utf-8-sig", "utf-8", "cp1256", "latin-1"]:
            try:
                raw_text = file_path_or_text.decode(enc)
                break
            except Exception:
                continue
        else:
            raw_text = file_path_or_text.decode("utf-8", errors="ignore")
    elif isinstance(file_path_or_text, (str, Path)) and (isinstance(file_path_or_text, Path) or (len(str(file_path_or_text)) < 300 and os.path.exists(str(file_path_or_text)))):
        raw_text = read_resilient_text(file_path_or_text)
    else:
        raw_text = str(file_path_or_text)

    raw_text = raw_text.strip()
    if not raw_text:
        return {"caption": "", "body": "", "hashtags": "", "title": ""}

    platform_lower = platform.lower()

    if platform_lower == "facebook":
        return _extract_clean_facebook(raw_text, landing_url, whatsapp_url)
    elif platform_lower == "instagram":
        return _extract_clean_instagram(raw_text, landing_url, whatsapp_url)
    elif platform_lower == "tiktok":
        return _extract_clean_tiktok(raw_text, landing_url, whatsapp_url)
    elif platform_lower == "youtube":
        return _extract_clean_youtube(raw_text, landing_url, whatsapp_url)
    elif platform_lower == "blogger":
        return _extract_clean_blogger(raw_text, landing_url, whatsapp_url)
    elif platform_lower == "reddit":
        return _extract_clean_reddit(raw_text, landing_url, whatsapp_url)
    else:
        return _extract_clean_facebook(raw_text, landing_url, whatsapp_url)


def _filter_technical_headers(text: str) -> str:
    """إزالة أي سطور ترويسة تقنية متبقية داخل النص بمرونة عالية، متجاوزة الرموز والأقواس والعلامات."""
    if not text:
        return ""
    header_pattern = re.compile(
        r"^[^\w\u0600-\u06FF\d\n\r]*(?:"
        r"منشور[\s_]*فيسبوك|"
        r"حزمة[\s_]*(?:إنستجرام|انستجرام|إنستغرام|انستغرام|تيك[\s_]*توك|تيكتوك|سيو[\s_]*يوتيوب|المحتوى[\s_]*الرقمي)|"
        r"تاريخ(?:[\s_]*و[\s_]*وقت)?[\s_]*الإنتاج|"
        r"المشروع|"
        r"الموضوع(?:[\s_]*السريري)?|"
        r"السيو[\s_]*الموجه|"
        r"الكلمات[\s_]*(?:المستهدفة|المفتاحية)|"
        r"العرض[\s_]*المعتمد|"
        r"الواتساب[\s_]*المباشر|"
        r"رابط[\s_]*الواتساب(?:[\s_]*المباشر)?|"
        r"كود[\s_]*(?:الخصم|المعاينة)(?:[\s_]*و[\s_]*المعاينة)?\s*:|"
        r"المنصة|"
        r"الهدف[\s_]*التسويقي|"
        r"الفئة[\s_]*المستهدفة|"
        r"نبرة[\s_]*الصوت|"
        r"Production\s*Date|"
        r"Project:|"
        r"Target\s*Keywords|"
        r"SEO\s*Title|"
        r"SEO\s*Description|"
        r"===+|---+|\*\*\*+"
        r")",
        re.IGNORECASE
    )
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue
        # استثناء سطور عروض الهدايا وكود المعاينة السريرية الموجهة للعميل (🎁)
        if stripped.startswith("🎁"):
            cleaned_lines.append(line)
            continue
        if header_pattern.search(stripped):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def _extract_clean_facebook(raw_text: str, landing_url: str = "", whatsapp_url: str = "") -> dict:
    # 1. البحث عن علامة بداية المتن الحقيقي بمرونة
    start_markers = [
        r"(?:^|\n)[^\w\u0600-\u06FF\d]*(?:نص[\s_]*المنشور[\s_]*الكامل[\s_]*للنشر[\s_]*المباشر|نص[\s_]*المنشور[\s_]*الكامل|نص[\s_]*المنشور[\s_]*المباشر|نص[\s_]*المنشور|نص[\s_]*البوست|نص[\s_]*الكابشن)\s*:?\s*",
    ]

    body_text = ""
    for marker in start_markers:
        parts = re.split(marker, raw_text, flags=re.IGNORECASE, maxsplit=1)
        if len(parts) > 1 and len(parts[1].strip()) > 50:
            body_text = parts[1].strip()
            break

    # إذا لم توجد علامة بداية، ننظف الترويسة من الأعلى
    if not body_text:
        lines = raw_text.splitlines()
        start_idx = 0
        header_line_re = re.compile(
            r"^[^\w\u0600-\u06FF\d]*(?:منشور|حزمة|تاريخ|المشروع|الموضوع|السيو|الكلمات|العرض|الواتساب|كود|المنصة|الهدف|الفئة|نبرة|❓|📌|===|---|Production|Project|Target|SEO)",
            re.IGNORECASE
        )
        for i, l in enumerate(lines):
            ls = l.strip()
            if not ls:
                continue
            if header_line_re.search(ls):
                continue
            start_idx = i
            break
        body_text = "\n".join(lines[start_idx:]).strip()

    # تنظيف أي ترويسة تقنية داخلية قد تكون موجودة
    body_text = _filter_technical_headers(body_text)

    # استخراج الهاشتاجات فقط من نهاية المنشور مع الحفاظ على عناوين الماركداون (### عنوان) في المتن
    lines = body_text.splitlines()
    tag_lines = []
    content_lines = []
    in_tail_tags = False
    for l in reversed(lines):
        ls = l.strip()
        if not ls:
            if in_tail_tags:
                continue
            else:
                content_lines.insert(0, l)
                continue
        # سطر هاشتاجات حقيقي: يبدأ بـ # متبوع بحرف أو رقم (وليس مسافة أو # أخرى مثل ### عنوان)
        if re.match(r"^#(?:[ء-يa-zA-Z0-9_]+)", ls):
            words = ls.split()
            if all(w.startswith("#") and not w.startswith("##") for w in words):
                tag_lines.insert(0, ls)
                in_tail_tags = True
                continue
        in_tail_tags = False
        content_lines.insert(0, l)

    body_text = "\n".join(content_lines).strip()
    hashtags = " ".join(tag_lines).strip()

    # استبدال نصوص الروابط المؤقتة بالروابط الحقيقية المعتمدة
    if whatsapp_url:
        body_text = re.sub(
            r"(?:^|\n)[ \t]*(?:👉|💬|📱|\*|\-)?[ \t]*رابط[\s_]*(?:الاستشارة|الواتساب)(?:[\s_]*والتفعيل)?(?:[\s_]*المباشر)?\s*:?\s*[^\n]+",
            f"\n👉 رابط الاستشارة والتفعيل المباشر عبر واتساب:\n{whatsapp_url}",
            body_text
        )

    # التأكد من وجود رابط صفحة الهبوط والواتساب بوضوح وأناقة أسفل المتن
    footer_parts = []
    if landing_url and landing_url not in body_text:
        footer_parts.append(f"━━━━━━━━━━━━━━━━━━━━━━━\n🔗 رابط الدليل السريري وحاسبة التعافي المتخصصة:\n👉 {landing_url}")
    if whatsapp_url and whatsapp_url not in body_text:
        footer_parts.append(f"💬 للتوجيه السريري المجاني والاستشارة المباشرة وتفعيل كود (HT10):\n👉 {whatsapp_url}")
    elif "01155803307" not in body_text:
        footer_parts.append("📱 للتواصل والاستشارة السريرية المجانية عبر واتساب: 01155803307 (كود المعاينة HT10)")

    footer_text = "\n\n".join(footer_parts)
    if footer_text:
        if "━━━━━━━━━━━━━━━━━━━━━━━" not in body_text:
            body_text = f"{body_text}\n\n{footer_text}"
        else:
            body_text = f"{body_text}\n{footer_text}"

    full_caption = f"{body_text}\n\n{hashtags}".strip() if hashtags else body_text

    return {
        "caption": full_caption,
        "body": body_text,
        "hashtags": hashtags,
        "title": "منشور فيسبوك السريري والإنساني"
    }


def _extract_clean_instagram(raw_text: str, landing_url: str = "", whatsapp_url: str = "") -> dict:
    carousel_guide = ""
    reels_script = ""
    caption = ""

    # تقسيم حسب الأقسام الثلاثة
    parts = re.split(r"(?:^|\n)(?:\d+\.\s*)?كابشن إنستجرام[^\n]*", raw_text, flags=re.IGNORECASE)
    if len(parts) > 1:
        caption = _filter_technical_headers(parts[1].strip())
        top_content = parts[0]
    else:
        caption = _filter_technical_headers(raw_text)
        top_content = ""

    if top_content:
        reels_parts = re.split(r"(?:^|\n)(?:\d+\.\s*)?سكريبت ريلز[^\n]*", top_content, flags=re.IGNORECASE)
        if len(reels_parts) > 1:
            reels_script = _filter_technical_headers(reels_parts[1].strip())
            carousel_guide = _filter_technical_headers(reels_parts[0].strip())
        else:
            carousel_guide = _filter_technical_headers(top_content)

    # تنظيف الترويسات من الكابشن
    caption = _filter_technical_headers(caption)

    # الهاشتاجات
    hashtags = ""
    tag_match = re.findall(r"(#[^\s#]+)", caption)
    if tag_match:
        hashtags = " ".join(tag_match)

    return {
        "caption": caption,
        "carousel_guide": carousel_guide,
        "reels_script": reels_script,
        "hashtags": hashtags,
        "title": "كابشن إنستجرام السريري"
    }


def _extract_clean_tiktok(raw_text: str, landing_url: str = "", whatsapp_url: str = "") -> dict:
    hook = ""
    script = ""
    caption = ""

    parts = re.split(r"(?:^|\n)(?:\d+\.\s*)?(?:الكابشن والهاشتاجات|كابشن تيك توك)[^\n]*", raw_text, flags=re.IGNORECASE)
    if len(parts) > 1:
        caption = _filter_technical_headers(parts[1].strip())
        top_content = parts[0]
    else:
        caption = _filter_technical_headers(raw_text)
        top_content = ""

    if top_content:
        script_parts = re.split(r"(?:^|\n)(?:\d+\.\s*)?سكريبت الفيديو الكامل[^\n]*", top_content, flags=re.IGNORECASE)
        if len(script_parts) > 1:
            script = _filter_technical_headers(script_parts[1].strip())
            hook = _filter_technical_headers(script_parts[0].strip())
        else:
            script = _filter_technical_headers(top_content)

    caption = _filter_technical_headers(caption)
    hashtags = " ".join(re.findall(r"(#[^\s#]+)", caption))

    return {
        "caption": caption,
        "script": script,
        "hook": hook,
        "hashtags": hashtags,
        "title": "سيناريو وكابشن تيك توك"
    }


def _extract_clean_youtube(raw_text: str, landing_url: str = "", whatsapp_url: str = "") -> dict:
    title = ""
    script_16x9 = ""
    shorts_script = ""
    description = ""
    tags = ""

    # العنوان
    title_match = re.search(r"(?:العنوان السريري الجذاب|YouTube SEO Title)[^\n]*\n+([^\n]+)", raw_text, flags=re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title_lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        title = title_lines[0] if title_lines else "دليل التعافي الطبي المعتمد"

    # سكريبت 16:9
    s16_match = re.search(r"(?:سكريبت الفيديو الكامل 16:9)[^\n]*\n(.*?)(?=(?:سكريبت شورتس|وصف الفيديو|قائمة التاغات|\Z))", raw_text, flags=re.DOTALL | re.IGNORECASE)
    if s16_match:
        script_16x9 = _filter_technical_headers(s16_match.group(1).strip())

    # سكريبت شورتس
    shorts_match = re.search(r"(?:سكريبت شورتس عمودي 9:16)[^\n]*\n(.*?)(?=(?:وصف الفيديو|قائمة التاغات|\Z))", raw_text, flags=re.DOTALL | re.IGNORECASE)
    if shorts_match:
        shorts_script = _filter_technical_headers(shorts_match.group(1).strip())

    # الوصف
    desc_match = re.search(r"(?:وصف الفيديو المهيأ لسيو يوتيوب مصر|SEO Description)[^\n]*\n(.*?)(?=(?:قائمة التاغات|YouTube Tags List|\Z))", raw_text, flags=re.DOTALL | re.IGNORECASE)
    if desc_match:
        description = _filter_technical_headers(desc_match.group(1).strip())
    else:
        description = _filter_technical_headers(raw_text)

    # التاغات
    tags_match = re.search(r"(?:قائمة التاغات الدلالية|YouTube Tags List)[^\n]*\n+([^\n]+)", raw_text, flags=re.IGNORECASE)
    if tags_match:
        tags = tags_match.group(1).strip()

    return {
        "title": title,
        "description": description,
        "tags": tags,
        "script_16x9": script_16x9,
        "shorts_script": shorts_script
    }


def _extract_clean_blogger(raw_text: str, landing_url: str = "", whatsapp_url: str = "") -> dict:
    raw_text = raw_text.lstrip("\ufeff").strip()
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    if not lines:
        return {"title": "", "meta_description": "", "html_content": ""}

    title = lines[0]
    title = re.sub(r"^(?:[#*\->•📌📝\s]*)(?:الدليل[\s_]*الطبي[\s_]*الشامل|مقال[\s_]*بلوجر|تقرير)\s*:?\s*", "", title, flags=re.IGNORECASE).strip().lstrip("# \t*")

    meta_desc = ""
    start_idx = 1
    if len(lines) > 1:
        m = re.match(r"^(?:[#*\->•📌📝\s]*)(?:الوصف[\s_]*التعريفي(?:\s*\(Meta\s*Description\))?)\s*:?\s*(.*)$", lines[1], re.IGNORECASE)
        if m:
            inline_desc = m.group(1).strip()
            if inline_desc:
                meta_desc = inline_desc
                start_idx = 2
            else:
                meta_desc = lines[2] if len(lines) > 2 else ""
                start_idx = 3

    html_sections = []
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        if len(table_rows) == 1:
            row_text = ", ".join(table_rows[0]) if isinstance(table_rows[0], list) else str(table_rows[0])
            html_sections.append(f'<p style="color:#334155; line-height:1.85; margin-bottom:14px;">{row_text}</p>')
        else:
            header_len = len(table_rows[0])
            tbl_html = '<div style="overflow-x:auto; margin:22px 0;"><table style="width:100%; border-collapse:collapse; font-size:0.95rem; border:1px solid #CBD5E1;">'
            tbl_html += '<tr style="background:#0D4A4D; color:#ffffff;">' + "".join([f'<th style="padding:12px; border:1px solid #CBD5E1;">{c.strip()}</th>' for c in table_rows[0]]) + '</tr>'
            for r in table_rows[1:]:
                padded_r = r + [""] * max(0, header_len - len(r))
                tbl_html += '<tr style="background:#F8FAFC;">' + "".join([f'<td style="padding:10px 12px; border:1px solid #E2E8F0; color:#334155;">{c.strip()}</td>' for c in padded_r[:header_len]]) + '</tr>'
            tbl_html += '</table></div>'
            html_sections.append(tbl_html)
        table_rows = []

    for line in lines[start_idx:]:
        stripped = line.strip()
        if not stripped:
            continue

        # فحص وتجاهل خط فاصل الجداول في الماركداون |---|---|
        if re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", stripped):
            continue

        # فحص صفوف جدول الماركداون | col1 | col2 |
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 3:
            cols = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cols) >= 2:
                table_rows.append(cols)
                continue

        # فحص صفوف الجدول بفاصل Tab (المفصول بتاب من Excel / Google Sheets)
        if "\t" in stripped and not stripped.startswith("*") and not stripped.startswith("س") and not stripped.startswith("-"):
            cols = [c.strip() for c in stripped.split("\t") if c.strip()]
            if len(cols) >= 2:
                table_rows.append(cols)
                continue

        # فحص صفوف الجدول (CSV format بمختلف الفواصل , أو ،) مع منع الخلط مع الفقرات العادية
        if ("," in stripped or "،" in stripped) and not stripped.startswith("*") and not stripped.startswith("س") and not stripped.startswith("-"):
            delimiter = "،" if "،" in stripped and stripped.count("،") >= stripped.count(",") else ","
            cols = [c.strip() for c in stripped.split(delimiter) if c.strip()]
            is_valid_row = False
            if len(cols) >= 2:
                no_sentence_period = not any(". " in c for c in cols)
                if not table_rows:
                    if len(cols) >= 3 and no_sentence_period and all(len(c) < 100 for c in cols) and not stripped.endswith("."):
                        if delimiter == "،":
                            if all(len(c) < 50 for c in cols) and (sum(len(c) for c in cols) / len(cols) < 35):
                                is_valid_row = True
                        else:
                            is_valid_row = True
                else:
                    header_count = len(table_rows[0])
                    if abs(len(cols) - header_count) <= 1 and no_sentence_period and all(len(c) < 160 for c in cols):
                        is_valid_row = True

            if is_valid_row:
                table_rows.append(cols)
                continue

        flush_table()

        # عناوين رئيسية مرقمة أو ماركداون
        if stripped.startswith("## ") or stripped.startswith("### "):
            heading_text = stripped.lstrip("#").strip()
            html_sections.append(f'<h2 style="color:#0D4A4D; font-size:1.35rem; margin-top:28px; border-right:4px solid #10B981; padding-right:12px; line-height:1.4;">{heading_text}</h2>')
        elif re.match(r"^\d+\.\s+", stripped) and len(stripped) < 120 and not stripped.endswith("."):
            html_sections.append(f'<h2 style="color:#0D4A4D; font-size:1.35rem; margin-top:28px; border-right:4px solid #10B981; padding-right:12px; line-height:1.4;">{stripped}</h2>')
        # أسئلة شائعة FAQ
        elif stripped.startswith("س") and (":" in stripped[:6] or stripped.startswith("سؤال") or "❓" in stripped[:4]):
            html_sections.append(f'<h3 style="color:#065F46; font-size:1.1rem; margin-top:20px; margin-bottom:6px;">❓ {stripped}</h3>')
        # إجابات FAQ
        elif stripped.startswith("ج:") or stripped.startswith("جواب:"):
            html_sections.append(f'<div style="background:#F0FDF4; padding:12px 16px; border-radius:10px; margin-bottom:14px; color:#166534; font-size:0.98rem; line-height:1.8;">{stripped}</div>')
        # نقاط قائمة
        elif stripped.startswith("* ") or stripped.startswith("- "):
            html_sections.append(f'<p style="color:#334155; line-height:1.8; margin:6px 0 6px 16px; padding-right:12px;">• {stripped[2:].strip()}</p>')
        else:
            html_sections.append(f'<p style="color:#334155; line-height:1.85; margin-bottom:14px;">{stripped}</p>')

    flush_table()

    cta_html = f"""
    <div style="background:linear-gradient(135deg, #0D4A4D 0%, #134E4A 100%); color:#ffffff; padding:24px; border-radius:16px; text-align:center; margin-top:35px;">
        <h4 style="margin:0 0 10px 0; font-size:1.25rem;">🩺 احصل على استشارة سريرية وتوجيه مجاني لحالتك</h4>
        <p style="margin:0 0 18px 0; color:#CCFBF1; font-size:0.95rem;">تواصل مباشرة مع أخصائية التعافي مع تفعيل كود <strong>(HT10)</strong> للشحن المجاني وحق فتح ومعاينة الشحنة قبل الاستلام.</p>
        <a href="{whatsapp_url or 'https://wa.me/201155803307'}" target="_blank" style="display:inline-block; background:#10B981; color:#ffffff; font-weight:800; font-size:1.05rem; padding:12px 28px; border-radius:30px; text-decoration:none;">محادثة واتساب الفورية (01155803307) ←</a>
    </div>
    """
    html_sections.append(cta_html)

    full_html = f"""<div dir="rtl" style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width:820px; margin:auto; background:#ffffff; padding:28px; border-radius:18px; border:1px solid #E2E8F0; color:#1E293B; line-height:1.9;">
    <h1 style="color:#0D4A4D; font-size:1.9rem; font-weight:900; line-height:1.4; margin-bottom:18px;">{title}</h1>
    {"".join(html_sections)}
</div>"""

    return {
        "title": title,
        "meta_description": meta_desc,
        "html_content": full_html
    }


def _extract_clean_reddit(raw_text: str, landing_url: str = "", whatsapp_url: str = "") -> dict:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    raw_title = lines[0] if lines else "التقرير السريري الشامل في بروتوكولات التعافي الجراحي"
    title = re.sub(r"^(?:[#*\->•📌📝\s]*)(?:التقرير[\s_]*السريري[\s_]*الشامل|منشور[\s_]*ريديت|reddit)\s*:?\s*", "", raw_title, flags=re.IGNORECASE).strip().lstrip("# \t*")
    if not title:
        title = raw_title.lstrip("# \t*")

    clean_body = _filter_technical_headers(raw_text)
    clean_lines = clean_body.splitlines()
    while clean_lines and not clean_lines[0].strip():
        clean_lines.pop(0)
    if clean_lines:
        first_clean = clean_lines[0].strip().lstrip("# \t*")
        raw_first = raw_title.lstrip("# \t*")
        if first_clean == title or first_clean == raw_first or (title and title in first_clean):
            clean_lines.pop(0)

    body_md = "\n".join(clean_lines).strip()
    markdown = f"# {title}\n\n{body_md}"

    if whatsapp_url and whatsapp_url not in markdown:
        markdown += f"\n\n---\n💬 **للتوجيه السريري المجاني والاستشارة عبر واتساب:** [اضغط هنا للتواصل]({whatsapp_url})\n"
    if landing_url and landing_url not in markdown:
        markdown += f"🌐 **رابط بوابة التعافي السريرية:** [{landing_url}]({landing_url})\n"

    return {
        "title": title,
        "markdown": markdown
    }


def scan_and_triage_manual_inbox(inbox_dir: Path) -> dict:
    """
    مسح شامل لصندوق manual_inbox وتصنيف كافة الملفات حسب التخصص ونوع الميديا،
    مع فرز دقيق لنسبة أبعاد الفيديوهات (9:16 مقابل 16:9) وتوزيع الصور المتعددة (Hero + Gallery).
    """
    results = {
        "detected_category": None,
        "matched_files": {cat: {"videos": [], "images": [], "audios": [], "texts": [], "htmls": []} for cat in CATEGORY_KEYWORDS},
        "platform_texts": {
            "facebook": None,
            "instagram": None,
            "tiktok": None,
            "youtube": None,
            "blogger": None,
            "reddit": None,
            "general": []
        },
        "media_triage": {
            "images": {
                "hero": None,
                "gallery": [],
                "all": []
            },
            "videos": {
                "vertical_9_16": [],
                "horizontal_16_9": [],
                "all": []
            },
            "audios": [],
            "silent_videos": []
        },
        "all_files_count": 0,
        "recommended_template_index": None
    }

    if not inbox_dir.exists():
        return results

    valid_files = find_active_inbox_files(inbox_dir)
    results["all_files_count"] = len(valid_files)
    if not valid_files:
        return results

    category_activity = {cat: 0 for cat in CATEGORY_KEYWORDS}

    inbox_images = []
    inbox_videos = []
    inbox_audios = []

    for f in valid_files:
        cat = classify_file_category(f)
        ext = f.suffix.lower()

        if ext in [".mp4", ".mov", ".mkv", ".webm"]:
            results["matched_files"][cat]["videos"].append(f)
            inbox_videos.append(f)
            category_activity[cat] += 4
        elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
            results["matched_files"][cat]["images"].append(f)
            inbox_images.append(f)
            category_activity[cat] += 1
        elif ext in [".m4a", ".mp3", ".wav", ".aac"]:
            results["matched_files"][cat]["audios"].append(f)
            inbox_audios.append(f)
            category_activity[cat] += 2
        elif ext in [".txt", ".md"]:
            results["matched_files"][cat]["texts"].append(f)
            category_activity[cat] += 3
        elif ext in [".html", ".htm"]:
            results["matched_files"][cat]["htmls"].append(f)
            category_activity[cat] += 3

    # توجيه ملفات المنصات (R1)
    text_files = [f for f in valid_files if f.suffix.lower() in [".txt", ".md"]]
    results["platform_texts"] = route_platform_text_files(text_files)

    # تصنيف الميديا المتعددة:
    # 1. الصور: الأولى Hero والباقي Gallery
    if inbox_images:
        results["media_triage"]["images"]["all"] = inbox_images
        results["media_triage"]["images"]["hero"] = inbox_images[0]
        results["media_triage"]["images"]["gallery"] = inbox_images[1:]

    # 2. الفيديوهات: 9:16 رأسي مقابل 16:9 أفقي وفحص الصمت
    for v in inbox_videos:
        results["media_triage"]["videos"]["all"].append(v)
        dim = probe_media_dimensions(v)
        if dim.get("is_vertical_9_16"):
            results["media_triage"]["videos"]["vertical_9_16"].append(v)
        else:
            results["media_triage"]["videos"]["horizontal_16_9"].append(v)
        if is_video_silent(v):
            results["media_triage"]["silent_videos"].append(v)

    # 3. الصوتيات
    results["media_triage"]["audios"] = inbox_audios

    # اختيار التخصص الأكثر نشاطاً من المدخلات الحالية
    most_active = max(category_activity, key=category_activity.get)
    if category_activity[most_active] > 0:
        results["detected_category"] = most_active

    return results


def archive_used_inbox_files(inbox_dir: Path, files_to_archive: list) -> int:
    """
    أرشفة الملفات المستخدمة تلقائياً في مجلد مؤرخ لحفظ نظافة الصندوق:
    media_assets/archive/YYYY-MM-DD_HHMMSS/
    تترك media_assets/manual_inbox/ نظيفة وفارغة 100%.
    """
    if not files_to_archive:
        return 0
    now_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    # توجيه الأرشيف إلى media_assets/archive/YYYY-MM-DD_HHMMSS/
    archive_folder = inbox_dir.parent / "archive" / now_str
    archive_folder.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in files_to_archive:
        try:
            if isinstance(f, (str, Path)):
                f_path = Path(f)
                if f_path.exists() and f_path.is_file():
                    # التحقق من أن الملف ينتمي لـ inbox_dir
                    try:
                        f_path.resolve().relative_to(inbox_dir.resolve())
                        is_inbox = True
                    except Exception:
                        is_inbox = (f_path.parent.resolve() == inbox_dir.resolve())

                    if is_inbox:
                        dest = archive_folder / f_path.name
                        shutil.copy2(str(f_path), str(dest))
                        try:
                            f_path.unlink()
                        except Exception:
                            pass
                        count += 1
        except Exception:
            pass
    return count
