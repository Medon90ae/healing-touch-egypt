#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | Healing Touch Egypt
محرك الفرز والتصنيف الذكي التلقائي للمدخلات (Smart Intake & Auto-Classifier)
=============================================================================
يتيح للمستخدم رمي أي ملف (فيديو، صورة، نص، صوت) في manual_inbox دون أي فرز يدوياً.
يقوم المحرك تلقائياً بقراءة المحتوى والاسم واستنتاج التخصص الجراحي المناسب ونوع الميديا،
وتوجيهه للحملة المطابقة وأرشفة الملفات بعد الاستخدام تلقائياً.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# الكلمات الدلالية السريرية لكل تخصص جراحي (عربي + إنجليزي)
CATEGORY_KEYWORDS = {
    "c-section": [
        "قيصر", "قيصرية", "كلويد", "شاور", "استحمام", "ولادة", "ندبة", "ندبات",
        "tegaderm", "bupy", "تيجاديرم", "بوبي", "شيت", "سيليكون", "csection",
        "c-section", "سيكاتريكس", "جرح الولادة", "فرد الندبة"
    ],
    "bariatric": [
        "تكميم", "سمنة", "منظار", "ثقوب", "ثقب", "تحويل مسار", "قص معدة",
        "opsite", "أوبسايت", "اوبسايت", "بخاخ", "رشاش", "bariatric", "sleeve"
    ],
    "rhinoplasty": [
        "أنف", "الانف", "تجميل أنف", "أرنبة", "دعامة", "دعامات", "خياشيم",
        "غضروف", "rhino", "rhinoplasty", "retainer", "nostril", "فتحات الأنف"
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


def classify_file_category(file_path: Path) -> str:
    """استنتاج التخصص الجراحي للملف بناءً على اسمه ومحتواه النصي إن وُجد."""
    name_lower = file_path.name.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}

    # فحص اسم الملف
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in name_lower:
                scores[cat] += 4

    # فحص محتوى الملف إذا كان نصاً أو HTML
    if file_path.suffix.lower() in [".txt", ".md", ".html", ".htm", ".json"]:
        try:
            sample_text = file_path.read_text(encoding="utf-8", errors="ignore")[:3000].lower()
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


def scan_and_triage_manual_inbox(inbox_dir: Path) -> dict:
    """
    مسح شامل لصندوق manual_inbox وتصنيف كافة الملفات حسب التخصص والنوع تلقائياً.
    يعيد قاموساً به الملفات المفروزة مع التخصص الأكثر نشاطاً اليوم.
    """
    results = {
        "detected_category": None,
        "matched_files": {cat: {"videos": [], "images": [], "audios": [], "texts": [], "htmls": []} for cat in CATEGORY_KEYWORDS},
        "all_files_count": 0,
        "recommended_template_index": None
    }

    if not inbox_dir.exists():
        return results

    valid_files = [
        f for f in inbox_dir.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]
    results["all_files_count"] = len(valid_files)
    if not valid_files:
        return results

    category_activity = {cat: 0 for cat in CATEGORY_KEYWORDS}

    for f in valid_files:
        cat = classify_file_category(f)
        ext = f.suffix.lower()

        if ext in [".mp4", ".mov", ".mkv", ".webm"]:
            results["matched_files"][cat]["videos"].append(f)
            category_activity[cat] += 3
        elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
            results["matched_files"][cat]["images"].append(f)
            category_activity[cat] += 1
        elif ext in [".m4a", ".mp3", ".wav", ".aac"]:
            results["matched_files"][cat]["audios"].append(f)
            category_activity[cat] += 2
        elif ext in [".txt", ".md"]:
            results["matched_files"][cat]["texts"].append(f)
            category_activity[cat] += 2
        elif ext in [".html", ".htm"]:
            results["matched_files"][cat]["htmls"].append(f)
            category_activity[cat] += 3

    # اختيار التخصص الأكثر نشاطاً من المدخلات الجديدة
    most_active = max(category_activity, key=category_activity.get)
    if category_activity[most_active] > 0:
        results["detected_category"] = most_active

    return results


def archive_used_inbox_files(inbox_dir: Path, files_to_archive: list) -> int:
    """أرشفة الملفات المستخدمة تلقائياً في مجلد مؤرخ لحفظ نظافة الصندوق."""
    if not files_to_archive:
        return 0
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_folder = inbox_dir / "archive" / now_str
    archive_folder.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in files_to_archive:
        try:
            if isinstance(f, (str, Path)):
                f_path = Path(f)
                if f_path.exists() and f_path.is_file() and f_path.parent.resolve() == inbox_dir.resolve():
                    dest = archive_folder / f_path.name
                    shutil.copy2(str(f_path), str(dest))
                    count += 1
        except Exception:
            pass
    return count
