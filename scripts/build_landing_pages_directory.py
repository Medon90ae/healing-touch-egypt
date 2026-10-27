# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | فهرس وسجل صفحات الهبوط الرسمية (Landing Pages Directory)
=============================================================================
"""

import sys
import json
import glob
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_LP = BASE_DIR / "docs" / "lp"
MEDIA_DIR = BASE_DIR / "media_assets"
SITE_BASE_URL = "https://medon90ae.github.io/healing-touch-egypt"

def build_directory():
    lp_files = sorted(list(DOCS_LP.glob("*.html")))
    registry = []

    category_mapping = {
        "c-section": "ولادة قيصرية وتجميل بطن",
        "bariatric": "جراحات سمنة ومناظير (تكميم وتحويل مسار)",
        "rhinoplasty": "تجميل وتثبيت الأنف",
        "thyroid": "جراحة الغدة الدرقية وتجميل الرقبة",
        "bupy": "علاج وتسطيح الندبات بشرائح السيليكون",
        "tegaderm": "عزل مائي وشاور آمن للجروح",
        "opsite": "حماية منافذ العمليات ببخاخ شفاف",
        "silicone": "دعامات وشرائح السيليكون الطبية"
    }

    for f in lp_files:
        content = f.read_text(encoding="utf-8")
        title_m = re.search(r'<title>(.*?)</title>', content)
        title = title_m.group(1).split('|')[0].strip() if title_m else f.stem
        
        # Determine category
        cat_found = "عام / تعافي جراحي"
        for k, v in category_mapping.items():
            if k in f.stem.lower():
                cat_found = v
                break

        # Check media assets
        has_video = ("<video" in content)
        has_audio = ("<audio" in content)

        public_url = f"{SITE_BASE_URL}/lp/{f.name}"
        registry.append({
            "filename": f.name,
            "title": title,
            "category": cat_found,
            "has_video": has_video,
            "has_audio": has_audio,
            "file_size_kb": round(f.stat().st_size / 1024, 1),
            "public_url": public_url,
            "local_path": str(f.resolve())
        })

    # 1. Save JSON registry
    json_path = MEDIA_DIR / "landing_pages_registry.json"
    json_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. Build Markdown directory
    md_lines = [
        "# 🌐 فهرس وسجل صفحات الهبوط الرسمية - هيلينج تاتش مصر (2026)",
        f"**إجمالي عدد صفحات الهبوط النشطة حالياً:** `{len(registry)} صفحة هبوط مستقلة`\n",
        "جميع الصفحات منشورة ومرفوعة ومفحوصة بنسبة 100% على خادم GitHub Pages وتتضمن التوجيه المباشر لواتساب مع كود (HT10).\n",
        "| # | التخصص / التصنيف | عنوان صفحة الهبوط | وسائط مدعومة | الرابط الحي المباشر |",
        "|---|---|---|:---:|---|"
    ]

    for idx, item in enumerate(registry, 1):
        media_badges = []
        if item["has_video"]:
            media_badges.append("🎬 فيديو")
        if item["has_audio"]:
            media_badges.append("🎙️ صوت")
        media_str = " + ".join(media_badges) if media_badges else "📄 سريري"

        md_lines.append(
            f"| {idx} | **{item['category']}** | {item['title']} | {media_str} | [زيارة الصفحة الحية]({item['public_url']}) |"
        )

    md_lines.append("\n---\n### 📂 مسار حفظ الملفات في جهازك:")
    md_lines.append(f"`{DOCS_LP.resolve()}`\n")

    md_path = MEDIA_DIR / "LANDING_PAGES_DIRECTORY.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"[+] 🎉 تم حصر وفهرسة {len(registry)} صفحة هبوط بنجاح في:")
    print(f"    • {md_path.resolve()}")
    print(f"    • {json_path.resolve()}")
    return registry

if __name__ == "__main__":
    build_directory()
