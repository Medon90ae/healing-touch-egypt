#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | استوديو التصميم الآلي (Auto-Canva Graphic & Reel Studio)
توليد تصاميم طبية احترافية وفيديوهات ريلز/تيك توك وتصدير ملفات Canva Bulk مجاناً
=============================================================================
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "media_assets" / "branded_designs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BULK_CSV_PATH = BASE_DIR / "media_assets" / "canva_bulk_import.csv"


def build_card_html(title: str, category_badge: str, key_tip: str, bg_image_uri: str, format_type: str = "square") -> str:
    """توليد كود HTML للتصميم بتنسيق طبي جذاب وأنيق يشبه قوالب كانفا بريميوم."""
    is_story = format_type == "story"
    width = 1080
    height = 1920 if is_story else 1080

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: {width}px;
      height: {height}px;
      overflow: hidden;
      font-family: 'Cairo', sans-serif;
      position: relative;
      background: #064E3B;
      color: #FFFFFF;
    }}
    .bg-img {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover;
      filter: brightness(0.68) contrast(1.1);
    }}
    .gradient-overlay {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: linear-gradient(180deg, 
        rgba(6, 78, 59, 0.92) 0%, 
        rgba(6, 78, 59, 0.4) 35%, 
        rgba(15, 23, 42, 0.75) 65%, 
        rgba(6, 78, 59, 0.96) 100%);
    }}
    .card-content {{
      position: relative;
      z-index: 10;
      width: 100%;
      height: 100%;
      padding: { '100px 70px' if is_story else '70px' };
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand-pill {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(12px);
      border: 1.5px solid rgba(255, 255, 255, 0.3);
      padding: 10px 24px;
      border-radius: 40px;
    }}
    .brand-icon {{
      width: 42px;
      height: 42px;
      background: #10B981;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }}
    .brand-text {{
      font-size: 26px;
      font-weight: 800;
      letter-spacing: 0.5px;
    }}
    .category-badge {{
      background: #F59E0B;
      color: #78350F;
      font-size: 22px;
      font-weight: 900;
      padding: 10px 24px;
      border-radius: 30px;
      box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }}
    .center-box {{
      margin: auto 0;
    }}
    .medical-sub {{
      color: #34D399;
      font-size: 26px;
      font-weight: 700;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .main-title {{
      font-size: { '56px' if is_story else '48px' };
      font-weight: 900;
      line-height: 1.3;
      margin-bottom: 24px;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }}
    .key-tip-box {{
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(16px);
      border-right: 6px solid #10B981;
      padding: 24px 28px;
      border-radius: 16px;
      font-size: 26px;
      line-height: 1.5;
      font-weight: 600;
      color: #F1F5F9;
    }}
    .footer-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
    }}
    .promo-card {{
      background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
      color: #92400E;
      padding: 16px 26px;
      border-radius: 20px;
      font-size: 24px;
      font-weight: 800;
      border: 2px dashed #D97706;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }}
    .cta-button {{
      background: #25D366;
      color: #FFFFFF;
      padding: 18px 36px;
      border-radius: 20px;
      font-size: 26px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
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
      <div class="key-tip-box">
        💡 <strong>القاعدة السريرية:</strong> {key_tip}
      </div>
    </div>
    
    <div class="footer-bar">
      <div class="promo-card">
        🎁 كود: <strong>HT10</strong> (شحن مجاني + حق المعاينة)
      </div>
      <div class="cta-button">
        💬 استشارة مجانية: 01155803307
      </div>
    </div>
  </div>
</body>
</html>"""


async def render_image_with_playwright(html_code: str, output_path: Path, width: int = 1080, height: int = 1080):
    """التقاط صورة التصميم بجودة فائقة وخط عربي منسق عبر محرك المتصفح."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        await page.set_content(html_code, wait_until="networkidle")
        await page.screenshot(path=str(output_path), full_page=True)
        await browser.close()


def generate_branded_card(case_info: dict, raw_img_path: str) -> dict:
    """
    توليد بطاقة التصميم المربعة وبطاقة الستوري الاحترافية.
    """
    title = case_info.get("title", "بروتوكول العناية الجراحية")
    cat = case_info.get("category", "c-section")
    
    cat_badges = {
        "c-section": "الولادة القيصرية",
        "rhinoplasty": "تجميل الأنف",
        "bariatric": "جراحات السمنة",
        "thyroid": "جراحة الغدة والرقبة",
        "general": "عناية ما بعد الجراحة"
    }
    badge = cat_badges.get(cat, "عناية طبية متخصصة")

    tips_map = {
        "c-section": "عزل الماء 100% بضمادات Tegaderm + تسطيح الندبة بشيت السيليكون BUPY.",
        "rhinoplasty": "تفريغ تورم الأرنبة ببلاستر 3M البيج المسامي وتماثل الفتحات بدعامة السيليكون.",
        "bariatric": "حماية ثقوب المنظار من بكتيريا الاستحمام فوراً بطبقة بخاخ Opsite الشفافة.",
        "thyroid": "حماية ندبة الرقبة من أشعة الشمس بـ 3M وترطيبها بـ BUPY لمنع التصبغ الداكن.",
        "general": "الالتزام بالبروتوكول السريري يقلل فترة التئام الجروح بنسبة تفوق 75%."
    }
    key_tip = tips_map.get(cat, tips_map["general"])

    # تجهيز مسار الصورة كـ URI
    raw_path = Path(raw_img_path).resolve()
    bg_uri = raw_path.as_uri()

    slug = f"branded_{cat}_{raw_path.stem}"
    square_png = OUTPUT_DIR / f"{slug}_square.png"
    story_png = OUTPUT_DIR / f"{slug}_story.png"

    print(f"[*] 🎨 جاري تصميم بوست احترافي (نمط كانفا) للموضوع: {title}...")

    # 1. المربع (1080x1080) لفيسبوك وإنستجرام
    square_html = build_card_html(title, badge, key_tip, bg_uri, "square")
    asyncio.run(render_image_with_playwright(square_html, square_png, 1080, 1080))
    print(f"[+] ✅ تم حفظ بوست فيسبوك وإنستجرام: {square_png.name}")

    # 2. الطولي (1080x1920) لستوري وإنستجرام ريلز وتيك توك
    story_html = build_card_html(title, badge, key_tip, bg_uri, "story")
    asyncio.run(render_image_with_playwright(story_html, story_png, 1080, 1920))
    print(f"[+] ✅ تم حفظ بطاقة تيك توك والستوري: {story_png.name}")

    return {
        "square_path": str(square_png),
        "story_path": str(story_png),
        "title": title,
        "badge": badge,
        "key_tip": key_tip
    }


def generate_tiktok_reel_video(story_card_path: str, duration_sec: int = 7) -> str:
    """
    تحويل بطاقة التصميم إلى فيديو MP4 متحرك عالي الجودة (1080x1920) لـ TikTok و Instagram Reels.
    """
    in_path = Path(story_card_path).resolve()
    out_mp4 = OUTPUT_DIR / f"{in_path.stem}_reel.mp4"

    print(f"[*] 🎬 جاري تحويل البطاقة إلى فيديو Reels/TikTok متحرك ({duration_sec} ثوانٍ)...")
    
    # تأثير تقريب بطيء سينمائي (Ken Burns Zoom) مع جودة 60fps و x264
    vf_filter = (
        f"zoompan=z='min(zoom+0.0012,1.15)':d={duration_sec}*25:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,"
        f"format=yuv420p"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", str(in_path),
        "-vf", vf_filter,
        "-t", str(duration_sec),
        "-c:v", "libx264",
        "-preset", "faster",
        "-pix_fmt", "yuv420p",
        str(out_mp4)
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if out_mp4.exists():
            print(f"[+] 🚀 تم إنشاء فيديو TikTok/Reels بنجاح: {out_mp4.name} ({out_mp4.stat().st_size} بايت)")
            return str(out_mp4)
    except Exception as e:
        print(f"[!] تنبيه في إنشاء الفيديو: {e}")
    return ""


def export_canva_bulk_csv(cases_list: list):
    """تصدير ملف CSV متوافق مباشرة مع ميزة Canva Bulk Create."""
    lines = ["Title,CategoryBadge,KeyTip,PromoCode,WhatsAppContact,TrackingLink"]
    for c in cases_list:
        title = c.get("title", "").replace(",", " ")
        cat = c.get("category", "c-section")
        tip = c.get("key_tip", "استشارة مجانية مع أخصائية التعافي").replace(",", " ")
        code = "HT10"
        wa = "201155803307"
        link = f"https://medon90ae.github.io/healing-touch-egypt/wa.html?case={cat}&code={code}"
        lines.append(f'"{title}","{cat}","{tip}","{code}","{wa}","{link}"')

    BULK_CSV_PATH.write_text("\n".join(lines), encoding="utf-8-sig")
    print(f"[+] 📁 تم تحديث ملف Canva Bulk Create: {BULK_CSV_PATH.name}")


if __name__ == "__main__":
    # تجربة سريعة
    from clinical_image_engine import get_clinical_case_photo
    test_case = {
        "title": "حالة جرح القيصرية والشاور والندبة البارزة",
        "category": "c-section"
    }
    img_info = get_clinical_case_photo(test_case["title"], test_case["category"])
    raw_img = img_info.get("local_path", "")
    if raw_img:
        cards = generate_branded_card(test_case, raw_img)
        video_path = generate_tiktok_reel_video(cards["story_path"])
        print("\n🎉 تم انتهاء تشغيل الاستوديو بنجاح!")
