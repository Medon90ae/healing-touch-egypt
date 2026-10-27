# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك صفحات الهبوط المستقلة وحزم المصادر والأدلة السريرية (2026)
Campaign Landing Page Engine & Clinical Guidance Orchestrator
(Clinical Evidence Deep Research & Clinical Guidance Hub)
=============================================================================
"""

import os
import sys
import json
import re
import shutil
import urllib.parse
from datetime import datetime
from pathlib import Path

# ضمان ترميز UTF-8 على كافة طرفيات ويندوز لمنع أخطاء طباعة الإيموجي
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# المسارات الأساسية للمشروع
BASE_DIR = Path(r"c:\followUPSHEET\healing_touch").resolve()
DOCS_DIR = BASE_DIR / "docs"
LP_DIR = DOCS_DIR / "lp"
MEDIA_DIR = BASE_DIR / "media_assets"
MANUAL_INBOX_DIR = MEDIA_DIR / "manual_inbox"
BRANDED_DIR = MEDIA_DIR / "branded_designs"
NOTEBOOKLM_DIR = MEDIA_DIR / "notebooklm_hub"
NOTEBOOK_PIC_DIR = NOTEBOOKLM_DIR / "pic"
NOTEBOOK_ARCHIVE_DIR = NOTEBOOKLM_DIR / "daily_sources_archive"

for d in (LP_DIR, MANUAL_INBOX_DIR, BRANDED_DIR, NOTEBOOKLM_DIR, NOTEBOOK_PIC_DIR, NOTEBOOK_ARCHIVE_DIR):
    d.mkdir(parents=True, exist_ok=True)

SITE_BASE_URL = "https://medon90ae.github.io/healing-touch-egypt"
TRACKING_ENDPOINT = "https://script.google.com/macros/s/AKfycbwDYeWbB9SjUqX1RXH7DaZ8yqG6V5Ay7yAiJ9L27Du1pJ8zb-NVgXzw6oz_0wJVp8Fr/exec"
OFFICIAL_WA_PHONE = "201155803307"
OFFICIAL_PROMO_CODE = "HT10"


def load_products_data() -> list:
    reg_path = BASE_DIR / "products_registry.json"
    if reg_path.exists():
        try:
            return json.loads(reg_path.read_text(encoding="utf-8")).get("products", [])
        except Exception:
            pass
    return []


# =============================================================================
# 1️⃣ توليد حزمة المصادر والأدلة السريرية المتكاملة (Clinical Evidence & Guidance Hub)
# =============================================================================
def generate_prompts_and_sources_pack(case_data: dict, pic_files: list = None) -> dict:
    title = case_data.get("title", "بروتوكول العناية الجراحية وعلاج الندبات")
    cat = case_data.get("category", "c-section")
    story_text = case_data.get("story_text", "")
    hashtags = case_data.get("hashtags", "")

    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    date_display = now.strftime("%Y-%m-%d %I:%M %p")

    # أسماء وتصنيفات بالإنجليزية للأدلة والمشاهد السريرية
    clinical_scenarios = {
        "c-section": {
            "ar_name": "الولادة القيصرية وتأمين الشاور ومنع الكلويد",
            "en_product": "BUPY Medical Silicone Scar Sheet & 3M Tegaderm Waterproof Dressing",
            "en_prompt_square": "A commercial luxury pharmaceutical photoshoot of BUPY Medical Silicone Scar Sheet and 3M Tegaderm waterproof dressing on a clean white marble tray, soft morning sunlight through hospital window, sterile aesthetic, tiny delicate water droplets showing waterproof seal, warm medical ambiance, 8k product photography, hyper-detailed, advertising quality.",
            "en_prompt_story": "Vertical editorial commercial shot of BUPY Medical Silicone tape roll and Smith & Nephew Opsite spray, minimal pastel green and white clinical background, soft natural lighting, showing moisture barrier and sterile protection, 8k resolution, elegant maternity healthcare photography.",
            "en_prompt_hero": "Wide landscape banner shot of post-cesarean recovery essentials: 3M Tegaderm dressing, BUPY silicone scar roll, and sterile medical wipes on a luxury clinic desk, soft depth of field, high-end medical branding aesthetic."
        },
        "rhinoplasty": {
            "ar_name": "تجميل الأنف اللحمي وتفريغ تورم الأرنبة",
            "en_product": "3M Micropore Tan Surgical Tape & Silicone Nostril Retainer",
            "en_prompt_square": "High-end aesthetic clinic product photoshoot of 3M Micropore Tan Surgical Tape roll next to medical silicone nostril retainer on a frosted glass surface, soft clinical ring light, pristine sterile environment, hyper-realistic, 8k resolution.",
            "en_prompt_story": "Vertical commercial shot of 3M beige porous surgical tape, delicate medical background, soft focus, aesthetic cosmetic surgery recovery setup, professional medical photography.",
            "en_prompt_hero": "Wide cinematic shot of rhinoplasty recovery essentials: 3M beige tape and silicone nostril retainer on an aesthetic surgeon consultation tray, clean minimalist lighting."
        },
        "bariatric": {
            "ar_name": "ثقوب منظار التكميم وتحويل المسار",
            "en_product": "Smith & Nephew Opsite Spray & BUPY Silicone Strips",
            "en_prompt_square": "Studio commercial photoshoot of Smith & Nephew Opsite Spray transparent dressing can next to BUPY silicone scar strips, clean sterile clinical surface, microscopic water mist showing waterproof protection, crisp professional lighting, 8k resolution.",
            "en_prompt_story": "Vertical aesthetic commercial shot of transparent Opsite spray mist can, minimalist healthcare setting, modern surgical recovery aesthetic, 8k hyper-realistic.",
            "en_prompt_hero": "Wide landscape banner of laparoscopic recovery kit: Opsite spray and silicone patches on modern clinical surface, soft green tones, professional medical grade."
        },
        "thyroid": {
            "ar_name": "جراحة الرقبة والغدة الدرقية وحماية الندبة من الشمس",
            "en_product": "BUPY Silicone Scar Sheet & 3M Micropore Tan Tape",
            "en_prompt_square": "Luxury pharmaceutical product photography of BUPY Silicone Scar Sheet roll and 3M skin-tone tape, soft daylight, elegant neutral background, sterile clinical aesthetic, 8k resolution.",
            "en_prompt_story": "Vertical commercial editorial of silicone scar sheeting for neck scar protection, soft warm lighting, dermatology clinic setting, hyper-realistic.",
            "en_prompt_hero": "Wide landscape shot of neck and thyroid scar recovery protocol products on clean medical presentation surface."
        }
    }

    scen = clinical_scenarios.get(cat, clinical_scenarios["c-section"])

    # نص الحزمة الكامل المنسق
    pack_md = f"""# 🌿 حزمة البرومبتات والإنتاج الرقمي الموحد اليومية – هيلينج تاتش مصر
**تاريخ التوليد:** {date_display}
**الحالة المستهدفة:** {title} ({scen['ar_name']})
**كود الأولوية السريرية:** `HT10` (استشارة سريرية ومتابعة مجانية مع أخصائية التعافي + حق فتح ومعاينة الشحنة قبل الاستلام)
**رابط اللاندنج بيدج المتوقع:** `{SITE_BASE_URL}/lp/{cat}-recovery-protocol.html`

=============================================================================
🎨 [1] برومبت جلسات التوثيق والتصوير السريري للمستلزمات الطبية (Clinical Photography):
=============================================================================
💡 تعليمات إنتاج الصور السريرية المعتمدة للمنتج الحقيقي 100%:
1. ارفع صورة المنتج الطبية الحقيقية من مجلد:
   C:\\followUPSHEET\\healing_touch\\media_assets\\notebooklm_hub\\pic
2. المقاسات المعتمدة:
   • المربع لمنشورات التوعية.
   • الرأسي للقصص السريعة ومقاطع الفيديو.
   • الأفقي لغلاف الدليل السريري وصفحة التوجيه.
3. انسخ التوجيه الإنجليزي التالي المخصص لكل موضع:

--- [توجيه الصورة المربعة لمنشورات التوعية] ---
{scen['en_prompt_square']}

--- [توجيه الصورة الرأسية للقصص السريعة ومقاطع الفيديو] ---
{scen['en_prompt_story']}

--- [توجيه الغلاف الأفقي للدليل السريري وصفحة التوجيه] ---
{scen['en_prompt_hero']}

=============================================================================
🧩 [2] إرشادات وتصميم الواجهات والصفحات السريرية (Clinical Landing Design):
=============================================================================
💡 لبناء وتصميم واجهة صفحة إرشادية سريرية مخصصة:
انسخ الأمر التالي الموجه لمحرك تصميم الواجهات:

```text
Design a luxury, reassuring Arabic (RTL) medical recovery clinical guide for "Healing Touch Egypt" (هيلينج تاتش مصر).
Topic: {title} ({scen['ar_name']}).
Brand Colors: Deep Teal (#064E3B), Emerald (#059669), Mint (#10B981), Amber (#D97706), Soft White background.
Sections to include:
1. Hero Section with reassuring medical headline, trust badges (Clinical Consultation, Inspection before Acceptance, Code HT10).
2. Video & Clinical showcase section with physiological proof.
3. Interactive Comparison Table (Traditional Care vs Healing Touch Protocol).
4. Clinical Supply Cards with physiological functions and consultation CTA buttons.
5. Scientific Evidence section citing PubMed and Cochrane studies.
6. FAQ Accordion for post-op recovery queries.
7. Sticky Mobile CTA bar: "حجز استشارة مجانية بكود HT10".
All CTA buttons should trigger free recovery consultation modal.
```
💡 ملحوظة: بعد الانتهاء، ضع كود HTML في manual_inbox ليقوم المحرك بحقن بوابة التسجيل السريري فيه تلقائياً (وإذا لم تضعه، المحرك سينشئ صفحة التوجيه أوتوماتيكياً).

=============================================================================
🔬 [3] برومبت أداة Gemini Deep Research & Literature Insights (أبحاث سريرية حديثة):
الرابط المباشر: https://gemini.google.com/ (مع تفعيل خيار Deep Research)
=============================================================================
انسخ هذا الأمر للحصول على أحدث الدراسات الطبية لعام 2025/2026:

```text
قم بإجراء بحث سريري وطبي متعمق (Deep Clinical Research) حول أحدث بروتوكولات العناية بالتعافي ومنع الندبات الجراحية بعد {scen['ar_name']}.
المطلوب:
1. تحليل أوراق بحثية وتجارب سريرية من PubMed و Cochrane Library و NCBI من 2023 حتى 2026.
2. مقارنة علمية دقيقة بين: استخدام شرائح السيليكون الطبي (Silicone Gel Sheeting) وبخاخ أوبسايت العازل وضماات 3M تيجاديرم، مقابل الشاش العادي والمراهم التقليدية.
3. تقديم جدول مقارنة علمي يوضح: نسب منع الكلويد، معدل عزل الماء والبكتيريا، والراحة السريرية.
4. توثيق المراجع بأرقام وتواريخ النشر وروابط PubMed الرسمية.
الصياغة: تقرير علمي موثق وموجز قابل للإدراج في الدليل السريري لمنصة هيلينج تاتش مصر.
```

=============================================================================
🎙️ [4] برومبت Google NotebookLM الاستوديو (الفيديو الشارح + نصوص السوشيال):
الرابط المباشر: https://notebooklm.google.com/
=============================================================================
انسخ هذا الأمر في شات NotebookLM (بعد رفع ملف المصدر المحدث):

```text
بصفتك رئيس قطاع المحتوى الطبي الرقمي في (هيلينج تاتش مصر)، وبالاعتماد على ملف المصدر (Healing_Touch_Brief) فقط:
1. 🎬 [فيديو شارح]: شغل أداة (Video Overview) في الاستوديو لإنشاء فيديو شارح تفاعلي لبيولوجيا التعافي بعد {scen['ar_name']} باستخدام مستلزمات BUPY و 3M و Opsite مع التنويه لأولوية المتابعة السريرية المجانية بكود HT10 ورقم الواتساب 01155803307.
2. 📝 [النصوص والمقالات]: اكتب المنشور الكامل لفيسبوك (Clinical Storytelling)، بوست واستوري إنستجرام، مقال سيو كامل لمدونة بلوجر بجدول مقارنة، وسكربت ريلز وتيك توك، ومنشور مناقشة ريديت.
3. احفظ الفيديو (.mp4) والنصوص (.txt) في مجلد:
   C:\\followUPSHEET\\healing_touch\\media_assets\\manual_inbox
```
"""

    # حفظ في مجلد الوارد manual_inbox
    pack_txt_file = MANUAL_INBOX_DIR / "PROMPTS_PACK_TODAY.txt"
    pack_md_file = MANUAL_INBOX_DIR / "PROMPTS_PACK_TODAY.md"
    pack_txt_file.write_text(pack_md, encoding="utf-8")
    pack_md_file.write_text(pack_md, encoding="utf-8")

    # حفظ في أرشيف النوت بوك
    archive_pack = NOTEBOOK_ARCHIVE_DIR / f"Prompts_Pack_{timestamp_str}.md"
    archive_pack.write_text(pack_md, encoding="utf-8")

    # تحديث الملف الدائم في notebooklm_hub
    (NOTEBOOKLM_DIR / "PROMPTS_PACK_TODAY.md").write_text(pack_md, encoding="utf-8")

    return {
        "txt_path": str(pack_txt_file),
        "md_path": str(pack_md_file),
        "clinical_prompt": scen["en_prompt_square"],
        "title": title,
        "category": cat
    }


# =============================================================================
# 2️⃣ بناء وتوليد Landing Page مستقلة فائقة التحويل (مع بوابة التسجيل الإجبارية)
# =============================================================================
def build_campaign_landing_page(case_data: dict, media_assets: dict = None, custom_template_html: str = "", **kwargs) -> dict:
    if not custom_template_html and kwargs:
        for val in kwargs.values():
            if isinstance(val, str) and len(val.strip()) > 50:
                custom_template_html = val
                break
    cat = case_data.get("category", "c-section")
    title = case_data.get("title", "بروتوكول العناية الجراحية المتكامل وعلاج الندبات")
    story_text = case_data.get("story_text", "")
    hashtags = case_data.get("hashtags", "")
    date_slug = datetime.now().strftime("%Y-%m-%d")

    slug = f"{cat}-recovery-protocol"
    lp_file = LP_DIR / f"{slug}.html"
    page_public_url = f"{SITE_BASE_URL}/lp/{slug}.html"

    # البحث عن أحدث فيديو وصور في manual_inbox أو branded_designs
    video_rel_path = ""
    # فحص manual_inbox أولاً
    mp4_inbox = sorted(list(MANUAL_INBOX_DIR.glob("*.mp4")), key=lambda x: x.stat().st_mtime, reverse=True)
    if mp4_inbox:
        # نسخ الفيديو إلى docs/assets/ لدعمه على GitHub Pages
        dest_video = DOCS_DIR / "assets" / f"campaign_{cat}_video.mp4"
        try:
            shutil.copy2(mp4_inbox[0], dest_video)
            video_rel_path = f"../assets/{dest_video.name}"
        except Exception:
            pass

    # فحص الصور
    image_rel_path = "../assets/og-image.jpg"
    square_pic = media_assets.get("square_path") if media_assets else ""
    if square_pic and os.path.isfile(square_pic):
        dest_img = DOCS_DIR / "assets" / f"campaign_{cat}_hero.png"
        try:
            shutil.copy2(square_pic, dest_img)
            image_rel_path = f"../assets/{dest_img.name}"
        except Exception:
            pass

    # إذا وفّر المستخدم كود HTML مخصص
    if custom_template_html and len(custom_template_html.strip()) > 200:
        print("[*] 🧩 تم اكتشاف تصميم واجهة مخصص! جاري حقن بوابة التسجيل الإجبارية وأكواد السيو...")
        augmented_html = _inject_gate_and_tracking_into_html(custom_template_html, title, cat, page_public_url)
        lp_file.write_text(augmented_html, encoding="utf-8")
        _register_page_in_sitemap(slug)
        return {"slug": slug, "local_file": str(lp_file), "public_url": page_public_url, "title": title}

    # بناء اللاندنج بيدج الأصلية الكاملة عالية التحويل (Zero-Friction Native LP)
    products = load_products_data()
    recommended_prods = [p for p in products if cat in p.get("category", "") or cat in p.get("secondary_category", "")]
    if not recommended_prods:
        recommended_prods = products[:3]

    products_cards_html = []
    for p in recommended_prods:
        products_cards_html.append(f"""
        <div class="product-lp-card">
          <div class="prod-badge">{p.get('badge', 'مستلزم معتمد')}</div>
          <h3>{p.get('name_ar')}</h3>
          <p class="prod-desc">{p.get('short_summary', p.get('clinical_summary', ''))[:160]}...</p>
          <div class="prod-clinical-role" style="margin-bottom: 16px; padding: 10px 0; border-top: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9;">
            <span class="clinical-badge" style="font-size: 0.88rem; font-weight: 800; color: var(--teal-deep);">🌿 مستلزم طبي معتمد سريرياً</span>
          </div>
          <button class="btn-consult-prod" onclick="openPromoDrawer('{p.get('name_ar')}', 'whatsapp'); return false;">
            💬 استشيري أخصائية التعافي مجاناً عبر واتساب
          </button>
        </div>
        """)

    # فحص وجود فيديو
    video_block = ""
    if not video_rel_path:
        for ext in [".mp4", ".mov", ".webm"]:
            cand_v = DOCS_DIR / "assets" / f"campaign_{cat}_video{ext}"
            if cand_v.exists():
                video_rel_path = f"../assets/{cand_v.name}"
                break

    if video_rel_path:
        video_block = f"""
        <div class="video-container-card">
          <div class="video-header-tag">🎬 فيديو الشرح السريري العملي التفاعلي</div>
          <video controls autoplay muted loop playsinline class="lp-video-player">
            <source src="{video_rel_path}" type="video/mp4">
            متصفحك لا يدعم تشغيل الفيديو المباشر.
          </video>
          <p class="video-caption">شرح تفاعلي لبيولوجيا التعافي، مراحل تنظيم الكولاجين، وطريقة استخدام المستلزمات الطبية المعتمدة للوقاية من تضخم الندبات.</p>
        </div>
        """

    # فحص وجود تعليق صوتي وبودكاست سريري
    audio_rel_path = ""
    for ext in [".m4a", ".mp3", ".wav"]:
        cand_a = DOCS_DIR / "assets" / f"campaign_{cat}_audio{ext}"
        if cand_a.exists():
            audio_rel_path = f"../assets/{cand_a.name}"
            break

    audio_block = ""
    if audio_rel_path:
        audio_block = f"""
        <div class="audio-container-card" style="background:#F0FDF4; border:1px solid #A7F3D0; border-radius:14px; padding:20px; margin:24px 0;">
          <div style="font-weight:800; color:#065F46; margin-bottom:10px; font-size:1.05rem;">🎙️ استمع إلى الشرح والبودكاست السريري لحالة اليوم (Audio Overview):</div>
          <audio controls style="width:100%; border-radius:30px;">
            <source src="{audio_rel_path}" type="audio/mp4">
            متصفحك لا يدعم تشغيل الصوت المباشر.
          </audio>
          <p style="font-size:0.88rem; color:#475569; margin-top:8px;">حوار سريري توضيحي حول فيزيولوجيا التئام الأنسجة، ترطيب الكولاجين، وطريقة الوقاية من تضخم الندبات والكلويد.</p>
        </div>
        """

    # أسئلة شائعة مطابقة لترندات بحث جوجل مصر
    faq_items = [
        ("هو ينفع أستحمى بأمان بعد الجراحة بدون ما الجرح يلتهب؟", "نعم، باستخدام الضمادات شبه المنفذة مثل 3M Tegaderm أو بخاخ أوبسايت العازل Smith & Nephew Opsite، يتم عزل الماء بنسبة 100% مع السماح للجلد بالتنفس وطرد بخار العرق، مما يتيح لك الاستحمام بحرية تامة دون رطوبة متبقية على خط الخياطة."),
        ("ليه حاسة بخط ناشف ومكلكع تحت مكان الجرح بعد أسبوعين؟", "هذا تكتل طبيعي ناتج عن إفراز مكثف وعشوائي لألياف الكولاجين خلال مرحلة الالتئام. تطبيق رول السيليكون الطبي BUPY يمارس ضغطاً ميكانيكياً خفيفاً ويحبس الرطوبة الفسيولوجية، مما يعيد ترتيب ألياف الكولاجين في مسار مسطح وناعم ويمنع تحول الخط إلى كلويد دائم."),
        ("كيف أحصل على التوجيه والاستشارة السريرية المجانية لمرحلة تعافي جرحي؟", "يمكنك التواصل المباشر مع استشاري العناية بالتعافي عبر واتساب من خلال الرابط أو الزر المباشر بالصفحة؛ لتحصل على إرشادات علمية دقيقة تناسب نوع عمليتك وتاريخ إجرائها ومعدل التئام الأنسجة لديك.")
    ]

    faq_html = "\n".join([f"""
    <details class="faq-accordion-item">
      <summary class="faq-question">❓ {q}</summary>
      <div class="faq-answer">{a}</div>
    </details>
    """ for q, a in faq_items])

    full_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | هيلينج تاتش مصر</title>
  <meta name="description" content="الدليل السريري وحملة التعافي المعتمدة لحالة {title}. اكتشف بروتوكول العزل المائي وتسطيح الندبات بكود HT10 واستشارة مجانية مع أخصائية التعافي.">
  <link rel="canonical" href="{page_public_url}">
  
  <!-- Open Graph / Facebook / WhatsApp -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | هيلينج تاتش مصر">
  <meta property="og:description" content="بروتوكول علمي متكامل لمنع تضخم الندبات وتأمين الاستحمام مع استشارة سريرية مجانية وأولوية المتابعة بكود HT10.">
  <meta property="og:image" content="{image_rel_path}">
  <meta property="og:url" content="{page_public_url}">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "name": "{title}",
    "url": "{page_public_url}",
    "description": "{title} - بروتوكول التعافي بعد العمليات الجراحية وعلاج الندبات",
    "publisher": {{
      "@type": "Organization",
      "name": "Healing Touch Egypt - هيلينج تاتش مصر",
      "url": "{SITE_BASE_URL}"
    }}
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <script src="../assets/whatsapp-triage.js"></script>

  <style>
    :root {{
      --teal-deep: #064E3B;
      --teal-dark: #065F46;
      --emerald: #059669;
      --mint: #10B981;
      --mint-light: #ECFDF5;
      --amber: #D97706;
      --amber-light: #FEF3C7;
      --surface: #FFFFFF;
      --bg-soft: #F8FAFC;
      --border: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #475569;
      --radius: 16px;
      --shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.08), 0 8px 10px -6px rgba(6, 78, 59, 0.04);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }}
    body {{ background: var(--bg-soft); color: var(--text-main); line-height: 1.75; direction: rtl; padding-bottom: 90px; }}
    
    /* الهيدر والشريط العلوي */
    .top-banner {{ background: var(--teal-deep); color: #fff; text-align: center; font-size: 0.88rem; font-weight: 700; padding: 10px 16px; display: flex; justify-content: center; align-items: center; gap: 8px; flex-wrap: wrap; }}
    .top-banner .code-pill {{ background: var(--amber); color: #fff; padding: 3px 10px; border-radius: 20px; font-weight: 800; letter-spacing: 0.5px; }}
    
    .nav-bar {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto; }}
    .nav-logo {{ font-size: 1.35rem; font-weight: 900; color: var(--teal-deep); text-decoration: none; display: flex; align-items: center; gap: 8px; }}
    .btn-nav-wa {{ background: var(--teal-dark); color: #fff; padding: 9px 18px; border-radius: 10px; font-weight: 700; font-size: 0.9rem; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: 0.2s; cursor: pointer; border: none; }}
    .btn-nav-wa:hover {{ background: var(--emerald); }}

    /* حاوية المحتوى الرئيسي */
    .container {{ max-width: 980px; margin: 32px auto; padding: 0 20px; }}

    /* سكشن الهيرو */
    .hero-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 36px; box-shadow: var(--shadow); margin-bottom: 32px; }}
    .category-tag {{ display: inline-block; background: var(--mint-light); color: var(--teal-deep); font-weight: 800; font-size: 0.88rem; padding: 6px 14px; border-radius: 20px; margin-bottom: 16px; border: 1px solid #A7F3D0; }}
    .hero-title {{ font-size: 2rem; font-weight: 900; color: var(--teal-deep); line-height: 1.35; margin-bottom: 16px; }}
    .hero-lead {{ font-size: 1.15rem; color: var(--text-muted); margin-bottom: 24px; }}
    
    .trust-badges-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 28px; }}
    .trust-badge-item {{ background: #F1F5F9; border-radius: 10px; padding: 12px 14px; font-weight: 700; font-size: 0.88rem; color: #1E293B; display: flex; align-items: center; gap: 8px; }}
    
    .hero-cta-row {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .btn-hero-primary {{ flex: 1; min-width: 260px; background: #059669; color: #fff; padding: 14px 24px; border-radius: 12px; font-size: 1.05rem; font-weight: 800; text-align: center; border: none; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25); }}
    .btn-hero-primary:hover {{ background: #047857; transform: translateY(-2px); }}
    .btn-hero-secondary {{ flex: 1; min-width: 220px; background: #F8FAFC; color: var(--teal-deep); border: 2px solid var(--border); padding: 14px 20px; border-radius: 12px; font-size: 1rem; font-weight: 800; text-align: center; text-decoration: none; display: flex; justify-content: center; align-items: center; }}
    .btn-hero-secondary:hover {{ background: #F1F5F9; }}

    /* مشغل الفيديو والوسائط */
    .video-container-card {{ background: #0F172A; border-radius: var(--radius); padding: 20px; margin-bottom: 32px; color: #fff; }}
    .video-header-tag {{ color: #6EE7B7; font-weight: 800; font-size: 0.95rem; margin-bottom: 12px; }}
    .lp-video-player {{ width: 100%; max-height: 480px; border-radius: 12px; background: #000; outline: none; }}
    .video-caption {{ font-size: 0.88rem; color: #94A3B8; margin-top: 10px; }}

    /* السرد الطبي السريري */
    .clinical-narrative-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; margin-bottom: 32px; box-shadow: var(--shadow); }}
    .clinical-narrative-card h2 {{ font-size: 1.45rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 16px; }}
    .narrative-body {{ font-size: 1.05rem; line-height: 1.85; color: #334155; white-space: pre-line; margin-bottom: 24px; }}

    /* بطاقات المنتجات */
    .products-section-title {{ font-size: 1.5rem; font-weight: 900; color: var(--teal-deep); margin-bottom: 20px; }}
    .products-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 36px; }}
    .product-lp-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow); transition: 0.2s; }}
    .product-lp-card:hover {{ border-color: var(--mint); transform: translateY(-3px); }}
    .prod-badge {{ display: inline-block; background: var(--mint-light); color: var(--teal-deep); font-weight: 800; font-size: 0.8rem; padding: 4px 10px; border-radius: 8px; margin-bottom: 12px; align-self: flex-start; }}
    .product-lp-card h3 {{ font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 10px; }}
    .prod-desc {{ font-size: 0.92rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px; }}
    .prod-clinical-role {{ margin-bottom: 16px; padding: 10px 0; border-top: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9; }}
    .clinical-badge {{ font-size: 0.88rem; font-weight: 800; color: var(--teal-deep); }}
    .btn-consult-prod {{ width: 100%; background: var(--teal-dark); color: #fff; border: none; padding: 12px; border-radius: 10px; font-weight: 800; font-size: 0.95rem; cursor: pointer; transition: 0.2s; }}
    .btn-consult-prod:hover {{ background: var(--emerald); }}

    /* الأسئلة الشائعة Accordion */
    .faq-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; margin-bottom: 32px; box-shadow: var(--shadow); }}
    .faq-title {{ font-size: 1.45rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 20px; }}
    .faq-accordion-item {{ border: 1px solid var(--border); border-radius: 10px; margin-bottom: 12px; overflow: hidden; }}
    .faq-question {{ font-weight: 800; font-size: 1.05rem; padding: 14px 18px; cursor: pointer; background: #F8FAFC; color: #1E293B; }}
    .faq-answer {{ padding: 16px 18px; font-size: 0.98rem; color: #334155; line-height: 1.7; background: #fff; }}

    /* الشريط السفلي الثابت للهواتف */
    .sticky-bottom-bar {{ position: fixed; bottom: 0; left: 0; right: 0; background: rgba(255, 255, 255, 0.96); backdrop-filter: blur(10px); border-top: 1px solid var(--border); padding: 12px 20px; z-index: 1000; box-shadow: 0 -4px 15px rgba(0, 0, 0, 0.06); }}
    .sticky-inner {{ max-width: 980px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 12px; }}
    .sticky-promo-info {{ font-weight: 800; font-size: 0.88rem; color: var(--teal-deep); }}
    .btn-sticky-cta {{ background: #059669; color: #fff; border: none; padding: 12px 24px; border-radius: 10px; font-weight: 800; font-size: 0.95rem; cursor: pointer; }}

    /* مودال تسجيل العميل الإجباري Zero-Bypass */
    #promo-lead-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(6, 78, 59, 0.65); backdrop-filter: blur(4px); z-index: 99999; justify-content: center; align-items: center; padding: 16px; direction: rtl; }}
    .lead-modal-card {{ background: #fff; border-radius: 20px; max-width: 460px; width: 100%; padding: 28px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); border: 2px solid #6EE7B7; text-align: center; position: relative; }}
    .lead-modal-card h3 {{ color: var(--teal-deep); font-size: 1.35rem; font-weight: 900; margin-bottom: 8px; }}
    .lead-modal-desc {{ font-size: 0.92rem; color: var(--text-muted); margin-bottom: 20px; line-height: 1.5; }}
    .input-group {{ text-align: right; margin-bottom: 16px; }}
    .input-group label {{ display: block; font-weight: 800; font-size: 0.88rem; color: #1E293B; margin-bottom: 6px; }}
    .input-group input {{ width: 100%; padding: 12px 14px; border-radius: 10px; border: 1.5px solid var(--border); font-size: 1rem; outline: none; }}
    .input-group input:focus {{ border-color: var(--emerald); }}
    .lead-err-msg {{ color: #DC2626; font-size: 0.85rem; font-weight: 700; margin-bottom: 14px; display: none; text-align: right; }}
    .btn-confirm-lead {{ width: 100%; background: #059669; color: #fff; border: none; padding: 14px; border-radius: 12px; font-size: 1.05rem; font-weight: 800; cursor: pointer; margin-bottom: 10px; }}
    .btn-close-lead {{ background: transparent; border: none; color: #94A3B8; font-weight: 700; font-size: 0.88rem; cursor: pointer; }}
  </style>
</head>
<body>

  <!-- شريط العرض العلوي -->
  <div class="top-banner">
    <span>🌿 كود الأولوية السريرية المعتمد:</span>
    <span class="code-pill">HT10</span>
    <span>(استشارة ومتابعة سريرية مجانية عبر واتساب مع أخصائية التعافي)</span>
  </div>

  <!-- الناف بار -->
  <header class="nav-bar">
    <a href="{SITE_BASE_URL}/" class="nav-logo">
      <span>🌿</span>
      <span>هيلينج تاتش مصر</span>
    </a>
    <button class="btn-nav-wa" onclick="openPromoDrawer('{title}', 'whatsapp'); return false;">
      💬 استشارة مجانية مع أخصائية التعافي
    </button>
  </header>

  <main class="container">
    
    <!-- كارت الهيرو الرئيسي -->
    <section class="hero-card">
      <span class="category-tag">✨ بروتوكول سريري معتمد للتعافي الجراحي والعناية بالندبات</span>
      <h1 class="hero-title">{title}</h1>
      <p class="hero-lead">الدليل السريري المعتمد للوقاية من تضخم الندبات (الكلويد)، عزل الماء 100% أثناء الاستحمام، وتنظيم بناء ألياف الكولاجين بعد العمليات الجراحية.</p>

      <div class="trust-badges-grid">
        <div class="trust-badge-item">🌿 بروتوكول سريري معتمد دولياً</div>
        <div class="trust-badge-item">🔬 مبني على توصيات PubMed وCochrane</div>
        <div class="trust-badge-item">🛡️ مستلزمات طبية أصلية 100%</div>
        <div class="trust-badge-item">🩺 استشارة ومتابعة سريرية مجانية</div>
      </div>

      <div class="hero-cta-row">
        <button class="btn-hero-primary" onclick="openPromoDrawer('{title}', 'whatsapp'); return false;">
          💬 استشيري أخصائية التعافي مجاناً بكود HT10
        </button>
        <a href="#products-section" class="btn-hero-secondary">
          📦 استعرض المستلزمات الطبية المعتمدة
        </a>
      </div>
    </section>

    <!-- مشغل الفيديو الشارح إن وجد -->
    {video_block}
    {audio_block}

    <!-- السرد الإكلينيكي وحل المشكلة -->
    <section class="clinical-narrative-card">
      <h2>🧬 التحليل الطبي وبيولوجيا التئام الأنسجة:</h2>
      <div class="narrative-body">{story_text}</div>
      <button class="btn-hero-primary" onclick="openPromoDrawer('استشارة سريرية بخصوص: {title}', 'whatsapp'); return false;">
        🩺 اسأل أخصائية التعافي عن حالتك بالتحديد مجاناً
      </button>
    </section>

    <!-- قائمة المستلزمات الطبية المعتمدة ودورها السريري -->
    <section id="products-section">
      <h2 class="products-section-title">📦 المستلزمات الطبية المعتمدة ودورها السريري في البروتوكول:</h2>
      <div class="products-grid">
        {"".join(products_cards_html)}
      </div>
    </section>

    <!-- الأسئلة الشائعة -->
    <section class="faq-card">
      <h2 class="faq-title">❓ أهم التساؤلات واستفسارات المرضى الأكثر بحثاً في مصر:</h2>
      {faq_html}
    </section>

  </main>

  <!-- الشريط السفلي الثابت للهواتف -->
  <aside class="sticky-bottom-bar">
    <div class="sticky-inner">
      <div class="sticky-promo-info">
        <span>كود الأولوية السريرية <strong>HT10</strong> مفعل</span>
        <br><small style="color: #64748B;">استشارة ومتابعة سريرية مجانية عبر واتساب</small>
      </div>
      <button class="btn-sticky-cta" onclick="openPromoDrawer('{title}', 'whatsapp'); return false;">
        💬 حجز استشارة مجانية
      </button>
    </div>
  </aside>

  <!-- نافذة تسجيل العميل الإلزامية Zero-Bypass Modal -->
  <div id="promo-lead-modal" onclick="if(event.target.id === 'promo-lead-modal') this.style.display = 'none';">
    <div class="lead-modal-card">
      <h3>🩺 استشارة سريرية مجانية</h3>
      <p class="lead-modal-desc">أهلاً بكِ في هيلينج تاتش مصر. لتسجيل ملفك وتفعيل أولوية الاستشارة السريرية بكود <strong>HT10</strong>، يرجى إدخال اسمك ورقم الموبايل للمتابعة:</p>
      
      <div class="input-group">
        <label for="lead-patient-name">اسم المريض / العميل الكريم:</label>
        <input type="text" id="lead-patient-name" placeholder="مثال: سارة أحمد" autocomplete="name">
      </div>

      <div class="input-group">
        <label for="lead-patient-phone">رقم الموبايل / واتساب (11 رقماً):</label>
        <input type="tel" id="lead-patient-phone" placeholder="مثال: 01012345678" autocomplete="tel">
      </div>

      <div id="lead-form-error" class="lead-err-msg"></div>

      <button class="btn-confirm-lead" onclick="executeProceedToConsultation();">
        💬 تأكيد الاستشارة وبدء المحادثة عبر واتساب
      </button>

      <button class="btn-close-lead" onclick="document.getElementById('promo-lead-modal').style.display = 'none';">
        إلغاء
      </button>
    </div>
  </div>

  <script>
    const PROMO_CODE = "{OFFICIAL_PROMO_CODE}";
    const WA_PHONE = "{OFFICIAL_WA_PHONE}";
    const TRACKING_ENDPOINT = "{TRACKING_ENDPOINT}";
    let currentTopic = "{title}";

    function openPromoDrawer(topic, channel) {{
      currentTopic = topic || document.title;
      const modal = document.getElementById('promo-lead-modal');
      if (modal) {{
        modal.style.display = 'flex';
        const nameInput = document.getElementById('lead-patient-name');
        if (nameInput) setTimeout(() => nameInput.focus(), 150);
      }}
    }}

    function executeProceedToConsultation() {{
      const nameInput = document.getElementById('lead-patient-name');
      const phoneInput = document.getElementById('lead-patient-phone');
      const errEl = document.getElementById('lead-form-error');

      const pName = nameInput ? nameInput.value.trim() : '';
      const pPhone = phoneInput ? phoneInput.value.trim().replace(/\\s+/g, '') : '';

      if (!pName || pName.length < 2) {{
        errEl.innerText = "⚠️ يرجى إدخال اسمك الكريم (حرفين على الأقل) لتسجيل ملف الاستشارة وتأكيد الطلب.";
        errEl.style.display = 'block';
        if (nameInput) nameInput.focus();
        return;
      }}

      const egyptPhoneRegex = /^01[0125][0-9]{{8}}$/;
      if (!pPhone || !egyptPhoneRegex.test(pPhone)) {{
        errEl.innerText = "⚠️ يرجى إدخال رقم موبايل/واتساب صحيح مكون من 11 رقماً يبدأ بـ 01 لتأكيد الاستشارة السريرية.";
        errEl.style.display = 'block';
        if (phoneInput) phoneInput.focus();
        return;
      }}

      errEl.style.display = 'none';

      // إرسال البيانات فوراً لجدول جوجل شيت المركزي
      try {{
        fetch(TRACKING_ENDPOINT, {{
          method: 'POST',
          mode: 'no-cors',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            timestamp: new Date().toISOString(),
            channel: 'whatsapp',
            patient_name: pName,
            client_name: pName,
            name: pName,
            patient_phone: pPhone,
            client_phone: pPhone,
            phone: pPhone,
            context_topic: currentTopic,
            topic: currentTopic,
            promo_code: PROMO_CODE,
            page_url: window.location.href
          }})
        }}).catch(() => {{}});
      }} catch(e) {{}}

      document.getElementById('promo-lead-modal').style.display = 'none';

      const waMsg = "أهلاً بكِ، أنا (" + pName + ") مسجل في موقع هيلينج تاتش بكود الأولوية السريرية (HT10)، ومحتاج استشارة سريرية مجانية بخصوص: " + currentTopic;
      const waUrl = "https://wa.me/" + WA_PHONE + "?text=" + encodeURIComponent(waMsg);
      setTimeout(() => {{ window.open(waUrl, '_blank'); }}, 250);
    }}
  </script>
</body>
</html>"""

    lp_file.write_text(full_html, encoding="utf-8")
    print(f"[+] 🌐 تم بناء الـ Landing Page المستقلة بنجاح: {lp_file.name}")
    print(f"   • الرابط الحي: {page_public_url}")

    _register_page_in_sitemap(slug)
    return {"slug": slug, "local_file": str(lp_file), "public_url": page_public_url, "title": title}


def _inject_gate_and_tracking_into_html(raw_html: str, title: str, category: str, page_url: str) -> str:
    """حقن بوابة تسجيل البيانات الإلزامية في أي كود HTML مصدّر لمنع أي تجاوز للواتساب."""
    gate_script_and_modal = f"""
    <!-- Zero-Bypass Lead Drawer Injected by Healing Touch Engine -->
    <div id="promo-lead-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(6,78,59,0.7); backdrop-filter:blur(4px); z-index:999999; justify-content:center; align-items:center; padding:16px; direction:rtl; font-family:'Cairo',sans-serif;">
      <div style="background:#fff; border-radius:20px; max-width:460px; width:100%; padding:28px; box-shadow:0 20px 40px rgba(0,0,0,0.25); border:2px solid #6EE7B7; text-align:center;">
        <h3 style="color:#064E3B; font-size:1.35rem; font-weight:900; margin-bottom:8px;">🩺 استشارة سريرية مجانية</h3>
        <p style="font-size:0.92rem; color:#475569; margin-bottom:20px; line-height:1.5;">لتسجيل ملفك وتفعيل أولوية الاستشارة السريرية بكود <strong>{OFFICIAL_PROMO_CODE}</strong>، يرجى إدخال اسمك ورقم الموبايل:</p>
        <div style="text-align:right; margin-bottom:14px;">
          <label style="display:block; font-weight:800; font-size:0.88rem; color:#1E293B; margin-bottom:6px;">اسم العميل الكريم:</label>
          <input type="text" id="consult-lead-name" placeholder="مثال: سارة أحمد" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #CBD5E1; font-size:1rem; outline:none; box-sizing:border-box;">
        </div>
        <div style="text-align:right; margin-bottom:16px;">
          <label style="display:block; font-weight:800; font-size:0.88rem; color:#1E293B; margin-bottom:6px;">رقم الموبايل / واتساب (11 رقماً):</label>
          <input type="tel" id="consult-lead-phone" placeholder="مثال: 01012345678" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #CBD5E1; font-size:1rem; outline:none; box-sizing:border-box;">
        </div>
        <div id="consult-lead-error" style="color:#DC2626; font-size:0.85rem; font-weight:700; margin-bottom:12px; display:none; text-align:right;"></div>
        <button onclick="confirmConsultLead();" style="width:100%; background:#059669; color:#fff; border:none; padding:14px; border-radius:12px; font-size:1.05rem; font-weight:800; cursor:pointer;">
          💬 تأكيد الاستشارة وبدء المحادثة عبر واتساب
        </button>
        <button onclick="document.getElementById('promo-lead-modal').style.display='none';" style="background:transparent; border:none; color:#94A3B8; font-weight:700; font-size:0.88rem; cursor:pointer; margin-top:10px;">إلغاء</button>
      </div>
    </div>

    <script>
      function openPromoDrawer(topic, channel) {{
        if (typeof window.HEALING_TOUCH_WHATSAPP !== 'undefined' && window.HEALING_TOUCH_WHATSAPP.showModal) {{
          window.HEALING_TOUCH_WHATSAPP.showModal(topic || '{title}');
          return;
        }}
        const m = document.getElementById('promo-lead-modal');
        if (m) {{ m.style.display = 'flex'; document.getElementById('consult-lead-name').focus(); }}
      }}
      function confirmConsultLead() {{
        const n = document.getElementById('consult-lead-name').value.trim();
        const p = document.getElementById('consult-lead-phone').value.trim().replace(/\\s+/g, '');
        const err = document.getElementById('consult-lead-error');
        if (!n || n.length < 2) {{ err.innerText = "يرجى كتابة الاسم الكريم أولاً"; err.style.display='block'; return; }}
        if (!/^01[0125][0-9]{{8}}$/.test(p)) {{ err.innerText = "يرجى كتابة رقم موبايل صحيح (11 رقماً)"; err.style.display='block'; return; }}
        err.style.display='none';
        try {{
          fetch('{TRACKING_ENDPOINT}', {{
            method: 'POST', mode: 'no-cors',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
              timestamp: new Date().toISOString(),
              channel: 'whatsapp',
              patient_name: n,
              client_name: n,
              name: n,
              patient_phone: p,
              client_phone: p,
              phone: p,
              context_topic: '{title}',
              topic: '{title}',
              promo_code: '{OFFICIAL_PROMO_CODE}',
              page_url: '{page_url}'
            }})
          }}).catch(() => {{}});
        }} catch(e) {{}}
        document.getElementById('promo-lead-modal').style.display='none';
        const msg = "أهلاً بكِ، أنا (" + n + ") مسجل في موقع هيلينج تاتش بكود الأولوية السريرية (HT10)، ومحتاج استشارة بخصوص: {title}";
        setTimeout(() => {{ window.open("https://wa.me/{OFFICIAL_WA_PHONE}?text=" + encodeURIComponent(msg), '_blank'); }}, 250);
      }}
      document.addEventListener("DOMContentLoaded", function() {{
        document.querySelectorAll("button, a").forEach(function(el) {{
          if (el.innerText.includes("استشارة") || el.innerText.includes("طلب") || el.innerText.includes("واتساب") || el.href.includes("wa.me") || el.href.includes("#")) {{
            el.onclick = function(e) {{ e.preventDefault(); openPromoDrawer('{title}', 'whatsapp'); return false; }};
          }}
        }});
      }});
    </script>
    """
    if "</body>" in raw_html:
        return raw_html.replace("</body>", f"{gate_script_and_modal}\n</body>")
    return raw_html + gate_script_and_modal


def _register_page_in_sitemap(slug: str):
    """تحديث خريطة الموقع sitemap.xml بإضافة صفحة الهبوط الجديدة فورياً."""
    sitemap_file = DOCS_DIR / "sitemap.xml"
    today_str = datetime.now().strftime("%Y-%m-%d")
    new_url_entry = f"  <url><loc>{SITE_BASE_URL}/lp/{slug}.html</loc><lastmod>{today_str}</lastmod><priority>0.90</priority></url>"
    if sitemap_file.exists():
        try:
            content = sitemap_file.read_text(encoding="utf-8")
            if f"/lp/{slug}.html" not in content:
                content = content.replace("</urlset>", f"{new_url_entry}\n</urlset>")
                sitemap_file.write_text(content, encoding="utf-8")
                print(f"[+] 🗺️ تم إضافة رابط الـ Landing Page إلى sitemap.xml بنجاح!")
        except Exception:
            pass


def archive_manual_inbox_processed():
    """أرشفة ملفات manual_inbox المستخدمة إلى مجلد أرشيف زمني حتى يظل الصندوق نظيفاً للحملة التالية."""
    archive_dir = MANUAL_INBOX_DIR / "archive" / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_dir.mkdir(parents=True, exist_ok=True)
    moved_count = 0
    for f in MANUAL_INBOX_DIR.iterdir():
        if f.is_file() and f.name != "PROMPTS_PACK_TODAY.txt" and f.name != "PROMPTS_PACK_TODAY.md":
            try:
                shutil.move(str(f), str(archive_dir / f.name))
                moved_count += 1
            except Exception:
                pass
    if moved_count > 0:
        print(f"[+] 🗄️ تم نقل {moved_count} ملفات تمت معالجتها من manual_inbox إلى الأرشيف النظيف: {archive_dir.name}")


if __name__ == "__main__":
    sample_case = {
        "title": "بروتوكول العناية الجراحية المتكامل وعلاج الندبات بعد القيصرية",
        "category": "c-section",
        "story_text": "بروتوكول سريري متكامل للعناية بالندبات وتأمين الاستحمام بعد الولادة القيصرية.",
        "hashtags": "#ولادة_قيصرية #ندبات_الولادة #هيلينج_تاتش"
    }
    pack = generate_prompts_and_sources_pack(sample_case)
    print(f"[+] 🎯 تم تجهيز حزمة البرومبتات السريرية:\n   👉 {pack['txt_path']}")


# =============================================================================
# 3️⃣ محرك بناء صفحات الهبوط المتعددة للمنتج نفسه (Multi-Angle Product LPs)
# =============================================================================
MULTI_ANGLE_LANDING_PAGES_SPEC = {
    "bupy-silicone-scar-sheet": [
        {
            "slug": "bupy-silicone-scar-flattening",
            "title": "علاج تليف وبروز جرح القيصرية وتسطيح الندبة بشيت السيليكون الطبي BUPY",
            "category": "c-section",
            "lead": "كيف تعمل شيتات السيليكون الطبي المتطورة على فرملة إنتاج الكولاجين العشوائي وتنعيم الكتل الصلبة الناتجة عن ندبات القيصرية وجراحات شد البطن.",
            "narrative": """تعتبر مرحلة إعادة تشكيل الأنسجة (Remodeling Phase) المرحلة الأكثر حساسية بعد جراحات البطن والقيصرية. عندما تجف أنسجة الجرح وتفقد رطوبتها الطبيعية، تتكاثر خلايا الفايبروبلاست وتنتج ألياف كولاجين كثيفة غير منتظمة تظهر في صورة بروز جراحي أو كتلة قاسية تحت الجلد.
            
أثبتت المراجعات السريرية أن شيتات السيليكون الطبي BUPY توفر بيئة إغلاق ميكروسكوبية تحاكي الطبقة القرنية للبشرة، مما يخفف التوتر الشعيري ويقلل فقدان السوائل عبر البشرة (TEWL). هذا الترطيب العميق يرسل إشارات بيولوجية للخلايا الليفية لتنظيم ألياف الكولاجين بصورة أفقية مسطحة، مما يؤدي لاستواء الندبة وتراجع بروزها بنسبة تتجاوز 85% خلال 8 إلى 12 أسبوعاً.""",
            "faqs": [
                ("متى ألاحظ بداية استواء الندبة وتراجع الكتلة المتليفة؟", "تبدأ الملاحظات السريرية الأولية في تحسن ملمس ومرونة الندبة وتلاشي الحكة خلال أول أسبوعين إلى 3 أسابيع، بينما يكتمل التسطيح واستعادة لون الجلد الطبيعي تدريجياً بين الشهر الثاني والثالث من الالتزام اليومي."),
                ("هل يصلح شيت السيليكون لندبات القيصرية القديمة؟", "نعم، أثبتت الدراسات فعالية السيليكون الطبي الموضعي في تحسين الندبات المتليفة حتى عمر سنتين، مع التوصية بالاستمرار لمدة لا تقل عن 12 أسبوعاً للحصول على أفضل استواء سريري.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        },
        {
            "slug": "bupy-silicone-timeline-keloid-prevention",
            "title": "التوقيت الطبي الصحيح لبدء استخدام السيليكون بعد فك الغرز والوقاية من الكيلويد",
            "category": "c-section",
            "lead": "الدليل الإكلينيكي لتحديد الموعد الآمن لبدء وضع لصقات السيليكون بعد اكتمال انغلاق البشرة، والجدول التدريجي لساعات الارتداء اليومي.",
            "narrative": """أحد أكثر الأخطاء شيوعاً التي تسبب انتكاسة في التئام الجروح هو التسرع بوضع لصقات السيليكون قبل اكتمال انغلاق طبقة البشرة السطحية. القاعدة الطبية المعتمدة من الجمعية الدولية لجراحي التجميل (ISAPS) تؤكد: لا توضع لصقات السيليكون أبداً فوق جرح مفتوح أو رطب أو يحتوي على إفرازات.
            
الموعد الطبي السليم يبدأ عادة بعد أسبوعين إلى 3 أسابيع من الجراحة، وفور سقوط القشور الجافة والتأكد من التئام الحواف تماماً. يبدأ المريض بجدول تدريجي: 4 ساعات يومياً في أول يومين، ثم زيادة ساعتين يومياً حتى الوصول إلى 12 - 20 ساعة يومياً، مما يمنع حدوث أي تعرق مفرط أو حساسية ويمنع تشكل الكيلويد مبكراً.""",
            "faqs": [
                ("ماذا أفعل إذا شعرت بحكة أو احمرار خفيف في بداية الاستخدام؟", "هذا مؤشر على الحاجة للتدرج اللطيف؛ قومي بنزع الشيت وغسل المنطقة بماء فاتر وتجفيفها، ثم تقليل ساعات الارتداء اليومي إلى 4-6 ساعات لعدة أيام حتى تتأقلم البشرة، مع التأكد من نظافة الشيت وغسله يومياً."),
                ("هل يقي شيت السيليكون من تحول الجرح إلى ندبة سميكة داكنة؟", "نعم، العزل والضغط الميكانيكي المستمر يمنعان اتساع خط الجراحة ويقللان التروية الدموية المفرطة للشعيرات السطحية، مما يحافظ على خط خياطة رفيع فاتح اللون.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        },
        {
            "slug": "bupy-silicone-daily-care-washing-guide",
            "title": "روتين الغسيل اليومي وإعادة استخدام شيت السيليكون BUPY وتجنب الحساسية",
            "category": "c-section",
            "lead": "كيف تغسلين وتحافظين على شيت السيليكون الطبي ليدوم معك حتى 25 يوماً للقطعة الواحدة بكفاءة التصاق وترطيب كاملة.",
            "narrative": """يتميز رول شيت السيليكون BUPY بقابلية الغسيل وإعادة الاستخدام المتكرر، مما يجعله الخيار الاقتصادي والسريري الأوفر والأنسب لعلاج الندبات الطويلة كجروح القيصرية وشد البطن.
            
للحفاظ على كفاءة الالتصاق والطبقة العلاجية: يتم غسل الشيت يومياً بماء فاتر وصابون لطيف خالٍ من الزيوت أو العطور، ثم يُشطف جيداً بالماء ويُترك على سطح نظيف ليجف تلقائياً في الهواء دون استخدام مناديل ورقية قد تترك وبراً على السيليكون. بعد الجفاف، يستعيد الشيت قدرته الطبيعية على الالتصاق ويوضع مجدداً فوق الجلد النظيف والجاف.""",
            "faqs": [
                ("كم يوماً تدوم قطعة الشيت الواحدة بعد قصها؟", "تدوم القطعة الواحدة من 20 إلى 25 يوماً مع الغسيل اليومي السليم، ويمكن قص الرول كاملاً إلى قطع متتالية تكفي كورس العلاج لعدة أشهر."),
                ("هل يمكن وضع كريمات مرطبة تحت شيت السيليكون؟", "لا، يجب أن يوضع شيت السيليكون مباشرة فوق جلد نظيف وجاف تماماً؛ وضع أي زيوت أو كريمات يقلل التصاق الشيت ويسبب انسداد المسام وظهور حبوب دهنية.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        }
    ],
    "3m-tegaderm-plus-pad": [
        {
            "slug": "tegaderm-showering-waterproof-protection",
            "title": "فوبيا الاستحمام بعد الولادة القيصرية وعزل الجرح بلصقة 3M Tegaderm + Pad",
            "category": "c-section",
            "lead": "كيف تضمنين الاستحمام اليومي بأمان تام دون تسرب قطرة ماء واحدة لخط الخياطة، مع وسادة معقمة ممتصة للإفرازات.",
            "narrative": """تشعر الأمهات بعد الجراحة بالقلق الشديد من ملامسة ماء الاستحمام للجرح خوفاً من انتقال الميكروبات أو تفكك الغرز. تم تصميم لصقة 3M Tegaderm + Pad الطبية بغشاء بولي يوريثان شفاف فائق الرقة ومقاوم بنسبة 100% لنفاذ الماء والبكتيريا والفيروسات.
            
تتيح اللصقة للأم الاستحمام الطبيعي بماء دافئ وصابون بحرية تامة دون الحاجة لتغطية الجرح بأكياس بلاستيكية مزعجة. وتحتوي في مركزها على وسادة معقمة عالية الامتصاص مغطاة بطبقة خاصة تمنع التصاقها بخط الجراحة، مما يجعل نزعها بعد الاستحمام أو بعد عدة أيام أمراً سهلاً وخالياً تماماً من الألم.""",
            "faqs": [
                ("هل يمكن الاستحمام فور وضع اللصقة في المستشفى أو المنزل؟", "نعم، فور تثبيت اللصقة والتأكد من التصاق حوافها الشفافة بالجلد الجاف بشكل محكم، توفر عزلاً مائياً فورياً بنسبة 100% يسمح بالاستحمام الآمن."),
                ("كم يوماً يمكن ترك لصقة 3M Tegaderm على الجرح؟", "يمكن ترك اللصقة على الجرح من 4 إلى 7 أيام طالما ظلت الحواف ملتصقة والوسادة المركزية نظيفة، ويتم تغييرها عند تشبع الوسادة أو تراخي الحواف.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        },
        {
            "slug": "tegaderm-sterile-dressing-change-guide",
            "title": "بروتوكول تغيير اللصقة المعقمة بعد فك الضمادة الأولى دون شد الجلد",
            "category": "c-section",
            "lead": "الخطوات السريرية السليمة لنزع واستبدال ضمادة الجراحة المعقمة دون إجهاد خط الخياطة أو التسبب في تهيج الجلد.",
            "narrative": """تغيير الغيار الجراحي الأول في المنزل يتطلب عناية دقيقة لتجنب فتح الغرز أو نقل العدوى. الخطأ الأبرز هو نزع اللصقة بشكل عمودي للأعلى، وهو ما يسبب شداً مفاجئاً على حواف الجرح.
            
البروتوكول الطبي المعتمد: اغسلي يديك جيداً بالماء والصابون، ثم ابدئي بنزع أطراف اللصقة الشفافة بهدوء وموازاة مع سطح الجلد باتجاه نمو الشعر. جففي الجلد المحيط بشاش معقم، ثم ثبتي لصقة 3M Tegaderm + Pad الجديدة من المنتصف باتجاه الأطراف مع الضغط الخفيف على الحواف لضمان إحكام العزل.""",
            "faqs": [
                ("هل أحتاج لوضع مطهر بيتادين أو كحول قبل وضع اللصقة الجديدة؟", "لا ينصح بوضع الكحول أو البيتادين المركز مباشرة وتركه رطباً؛ بل يُنصح بتنظيف الجلد المحيط بمحلول ملحي وتركه ليجف تماماً قبل تثبيت اللصقة المعقمة."),
                ("ما هي علامات التحذير التي تستوجب مراجعة الطبيب؟", "إذا لاحظتِ احمراراً متزايداً يتجاوز 2 سم حول الجرح، أو سخونة موضعية شديدة، أو خروج إفرازات ذات رائحة غير معتادة، يجب استشارة الفريق الطبي فوراً.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        }
    ],
    "3m-micropore-tan-tape-1533-0": [
        {
            "slug": "3m-micropore-rhinoplasty-taping-protocol",
            "title": "تثبيت الأنف بعد إزالة الجبيرة ومنع التورم ببلاستر 3M Micropore Tan البيج",
            "category": "rhinoplasty",
            "lead": "كيف يفرغ الضغط المتوازن للبلاستر الطبي البيج 1533-0 الوذمة التورمية ويحافظ على التصاق الجلد بالهيكل الغضروفي الجديد.",
            "narrative": """بعد رفع الجبيرة البلاستيكية أو الجبسية عن الأنف بعد عملية التجميل، يميل الجلد والأنسجة الرخوة للتورم السريع وتجمع السوائل اللمفاوية (Supratip Edema). يمثل بلاستر 3M Micropore Tan 1533-0 الأداة السريرية الأساسية لضبط التعافي في هذه المرحلة.
            
يتميز البلاستر البيج الأصلي بأنه شريط ورقي مسامي خفيف يسمح بتنفس مسام البشرة ويفرغ الضغط بالتساوي فوق جسر الأنف وأرنبته، مما يجبر الجلد على الانكماش والتطابق مع الهيكل العظمي والغضروفي الجديد، ويمنع تشكل الأنسجة الميتة المتليفة مع لون بيج طبيعي وغير لافت.""",
            "faqs": [
                ("كم ساعة يجب وضع البلاستر يومياً بعد إزالة الجبيرة؟", "يوصي معظم جراحي التجميل بوضع البلاستر طوال اليوم (24 ساعة) خلال أول أسبوعين إلى 3 أسابيع، ثم الاكتفاء بوضعه أثناء النوم لمدة شهرين إلى 3 أشهر إضافية."),
                ("كيف أزيل البلاستر دون إيذاء جلد الأنف؟", "بللي البلاستر بالماء الدافئ أثناء الاستحمام حتى يرتخي الصمغ، ثم اسحبيه برفق شديد بمحاذاة الجلد في اتجاه الأرنبة دون شد للأعلى.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        },
        {
            "slug": "3m-micropore-thyroid-neck-sun-protection",
            "title": "حماية ندبة الرقبة وتجميل الصدر من أشعة الشمس والتصبغ بالبلاستر المسامي",
            "category": "thyroid",
            "lead": "الدور الوقائي لبلاستر 3M Micropore كحاجز فيزيائي آمن يمنع وصول الأشعة الضارة لندبات استئصال الغدة الدرقية وجراحات الرقبة.",
            "narrative": """تتعرض ندبات جراحات الرقبة وأعلى الصدر لأشعة الشمس اليومية أثناء الخروج والقيادة، مما يحفز الخلايا الصبغية (Melanocytes) لإنتاج تصبغات بنية داكنة يصعب علاجها لاحقاً.
            
يعمل شريط 3M Micropore Tan كدرع فيزيائي آمن يعكس الأشعة فوق البنفسجية ويمنع وصولها للندبة الحديثة، وفي الوقت نفسه يخفف قوى الشد الحركي الناتجة عن التفاف الرقبة، مما يضمن التئام الجرح في صورة خط أبيض رفيع للغاية وغير ملحوظ.""",
            "faqs": [
                ("هل يسبب بلاستر 3M Micropore حساسية لجلد الرقبة الحساس؟", "صُنع الشريط من ألياف ورقية غير منسوجة مع صمغ أكريليكي خالٍ تماماً من مادة اللاتكس، مما يجعله مضاداً للحساسية ومناسباً للبشرة الحساسة لشهور طويلة."),
                ("متى يمكن البدء بوضع الشريط على ندبة الرقبة؟", "يبدأ استخدامه بعد سقوط خيوط الجراحة والتئام خط الخياطة التام، ويُغير كل 2-3 أيام بعد الاستحمام.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        }
    ],
    "silicone-nostril-retainer": [
        {
            "slug": "silicone-nostril-retainer-symmetry-care",
            "title": "دعامة فتحات الأنف السيليكونية الطبية والحفاظ على تماثل الفتحتين بعد التجميل",
            "category": "rhinoplasty",
            "lead": "كيف تمنع الدعامة السيليكونية انكماش مجرى الهواء الداخلي وتحافظ على فتحات أنف متناسقة ومتماثلة بعد جراحات التجميل وإصلاح الحاجز.",
            "narrative": """تعتبر قوى الانكماش الندبي الداخلي (Cicatricial Contraction) من أكبر التحديات بعد جراحات تجميل الأنف وإصلاح الشفة الأرنبية، حيث تميل الأنسجة الداخلية للتضييق غير المتماثل مما قد يشوه مظهر الفتحات أو يسبب صعوبة في التنفس.
            
تعمل دعامة الأنف السيليكونية (Silicone Nostril Retainer) كدعامة تشريحية مرنة تحافظ على الشكل البيضاوي المتناسق للفتحتين وتمنع التصاق الأنسجة أو انكماش صمام الأنف الداخلي، مع خامة سيليكون طبي فائق النعومة لا يضغط على الغضاريف أو يسبب تقرحات.""",
            "faqs": [
                ("هل تعيق دعامة الأنف التنفس الطبيعي أثناء ارتدائها؟", "لا، الدعامة مزودة بقنوات هوائية واسعة تتيح مرور تيار الهواء بسلاسة والتنفس الطبيعي حتى أثناء النوم."),
                ("كيف يتم اختيار المقاس الصحيح للدعامة؟", "يتم اختيار المقاس بدقة من المقاسات المعتمدة (0 إلى 6) بما يطابق حجم فتحة الأنف دون تمديد زائد للأنسجة، وتحت إشراف أخصائي الرعاية أو الجراح المعالج.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        }
    ],
    "smith-nephew-opsite-spray": [
        {
            "slug": "opsite-spray-bariatric-trocar-protection",
            "title": "حماية منافذ عمليات التكميم ومناظير البطن من العرق والاحتكاك ببخاخ Smith & Nephew Opsite",
            "category": "bariatric",
            "lead": "كيف يشكل بخاخ العزل الجراحي الشفاف طبقة مرنة تحمي فتحات التروكار من العرق وثنيات البطن واحتكاك الملابس اليومي.",
            "narrative": """في جراحات السمنة كالتكميم وتحويل المسار وجراحات المرارة بالمنظار، تتوزع منافذ المنظار الدقيقة على جدار البطن وتتعرض باستمرار للاحتكاك مع حزام البنطال أو العرق المتجمع في ثنيات الجلد.
            
يشكل بخاخ Smith & Nephew Opsite Spray غشاءً مطاطياً شفافاً وفائق الرقة يجف خلال ثوانٍ معدودة بعد الرش، ليوفر حاجزاً فيزيائياً عازلاً يمنع تسرب العرق أو البكتيريا للجروح، مع نفاذية ممتازة للأكسجين تسمح للجلد بالتنفس الطبيعي وتمنع التحسس الناتج عن اللصقات التقليدية.""",
            "faqs": [
                ("هل يتيح بخاخ Opsite الاستحمام اليومي دون قلق؟", "نعم، الطبقة الشفافة مقاومة للماء وتتيح الاستحمام بماء دافئ بلطف، مع تجفيف الجلد بطريقة التربيت الخفيف دون فرك."),
                ("كيف تتم إزالة طبقة البخاخ العازل عن الجلد؟", "لا تحتاج الطبقة لأي نزع أو شد؛ فهي تتلاشى تلقائياً وبشكل تدريجي مع تجدد خلايا البشرة الطبيعي وسقوط القشور.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        }
    ]
}


def generate_all_multi_angle_product_lps() -> list:
    """
    توليد مصفوفة صفحات الهبوط المتعددة والشاملة لكافة المنتجات الطبية (R2-R6).
    """
    created_pages = []
    products = load_products_data()

    for prod_id, specs in MULTI_ANGLE_LANDING_PAGES_SPEC.items():
        matched_prod = next((p for p in products if p.get("id") == prod_id), None)
        prod_title = matched_prod.get("name_ar", "مستلزم طبي معتمد") if matched_prod else "مستلزم طبي معتمد"

        for spec in specs:
            slug = spec["slug"]
            lp_file = LP_DIR / f"{slug}.html"
            page_public_url = f"{SITE_BASE_URL}/lp/{slug}.html"

            # استدعاء الفيديو المخصص إن وجد في docs/assets
            video_rel_path = ""
            video_name = spec.get("video_fallback", "")
            if video_name and (DOCS_DIR / "assets" / video_name).exists():
                video_rel_path = f"../assets/{video_name}"

            # إنشاء بطاقات المنتجات الموصى بها سريرياً
            recommended_prods = [p for p in products if p.get("id") == prod_id]
            if not recommended_prods:
                recommended_prods = products[:2]

            prods_cards_html = []
            for p in recommended_prods:
                prods_cards_html.append(f"""
                <div class="product-lp-card">
                  <div class="prod-badge">{p.get('badge', 'مستلزم طبي معتمد')}</div>
                  <h3>{p.get('name_ar')}</h3>
                  <p class="prod-desc">{p.get('short_summary', p.get('clinical_summary', ''))[:160]}...</p>
                  <div class="prod-clinical-role" style="margin-bottom: 16px; padding: 10px 0; border-top: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9;">
                    <span class="clinical-badge" style="font-size: 0.88rem; font-weight: 800; color: var(--teal-deep);">🛡️ وظيفته: دعم التعافي السريري الآمن</span>
                  </div>
                  <a href="{SITE_BASE_URL}/wa.html?case={spec['category']}&code=HT10&topic={urllib.parse.quote(p.get('name_ar'))}" target="_blank" rel="noopener" class="btn-hero-primary" style="display:block; text-align:center; text-decoration:none; padding:12px 18px; border-radius:10px; font-weight:800;">
                    💬 استشارة سريرية مجانية حول المنتج
                  </a>
                </div>
                """)

            faq_html = "\n".join([f"""
            <details class="faq-accordion-item">
              <summary class="faq-question">❓ {q}</summary>
              <div class="faq-answer">{a}</div>
            </details>
            """ for q, a in spec["faqs"]])

            video_block = ""
            if video_rel_path:
                video_block = f"""
                <div class="video-container-card">
                  <div class="video-header-tag">🎬 فيديو الشرح السريري التطبيقي المعتمد</div>
                  <video controls autoplay muted loop playsinline class="lp-video-player">
                    <source src="{video_rel_path}" type="video/mp4">
                    متصفحك لا يدعم تشغيل الفيديو المباشر.
                  </video>
                  <p class="video-caption">شرح إكلينيكي مفصل لخطوات التطبيق الصحيح وتجنب الأخطاء الشائعة أثناء مرحلة التعافي.</p>
                </div>
                """

            audio_block = ""
            audio_name = spec.get("audio_fallback", "")
            if not audio_name and spec.get("category"):
                audio_name = f"campaign_{spec['category']}_audio.m4a"
            if audio_name and (DOCS_DIR / "assets" / audio_name).exists():
                audio_rel_path = f"../assets/{audio_name}"
                audio_block = f'''
                <div style="background:#0F172A; border-radius:var(--radius); padding:20px; margin-bottom:32px; color:#fff; text-align:center;">
                  <div style="color:#6EE7B7; font-weight:800; font-size:0.95rem; margin-bottom:12px;">🎙️ الشرح الصوتي السريري المعتمد</div>
                  <audio controls style="width:100%; max-width:600px;">
                    <source src="{audio_rel_path}" type="audio/mp4">
                    متصفحك لا يدعم تشغيل الصوت المباشر.
                  </audio>
                </div>
                '''

            wa_direct_link = f"https://wa.me/{OFFICIAL_WA_PHONE}?text={urllib.parse.quote(f'أهلاً بكِ، قرأت الدليل السريري حول ({spec["title"]}) في موقع هيلينج تاتش، وأود استشارة سريرية مجانية حول حالتي للتعافي (كود المتابعة: {OFFICIAL_PROMO_CODE}).')}"

            html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{spec['title']} | هيلينج تاتش مصر</title>
  <meta name="description" content="{spec['lead']}">
  <link rel="canonical" href="{page_public_url}">
  
  <meta property="og:type" content="article">
  <meta property="og:title" content="{spec['title']} | هيلينج تاتش مصر">
  <meta property="og:description" content="{spec['lead']}">
  <meta property="og:image" content="../assets/og-image.jpg">
  <meta property="og:url" content="{page_public_url}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <script src="../assets/whatsapp-triage.js"></script>

  <style>
    :root {{
      --teal-deep: #064E3B;
      --teal-dark: #065F46;
      --emerald: #059669;
      --mint: #10B981;
      --mint-light: #ECFDF5;
      --amber: #D97706;
      --amber-light: #FEF3C7;
      --surface: #FFFFFF;
      --bg-soft: #F8FAFC;
      --border: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #475569;
      --radius: 16px;
      --shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.08), 0 8px 10px -6px rgba(6, 78, 59, 0.04);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }}
    body {{ background: var(--bg-soft); color: var(--text-main); line-height: 1.75; direction: rtl; padding-bottom: 90px; }}
    
    .top-banner {{ background: var(--teal-deep); color: #fff; text-align: center; font-size: 0.88rem; font-weight: 700; padding: 10px 16px; display: flex; justify-content: center; align-items: center; gap: 8px; flex-wrap: wrap; }}
    .top-banner .code-pill {{ background: var(--amber); color: #fff; padding: 3px 10px; border-radius: 20px; font-weight: 800; letter-spacing: 0.5px; }}
    
    .nav-bar {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto; }}
    .nav-logo {{ font-size: 1.35rem; font-weight: 900; color: var(--teal-deep); text-decoration: none; display: flex; align-items: center; gap: 8px; }}
    .btn-nav-wa {{ background: var(--teal-dark); color: #fff; padding: 9px 18px; border-radius: 10px; font-weight: 700; font-size: 0.9rem; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: 0.2s; cursor: pointer; border: none; }}
    .btn-nav-wa:hover {{ background: var(--emerald); }}

    .container {{ max-width: 980px; margin: 32px auto; padding: 0 20px; }}

    .hero-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 36px; box-shadow: var(--shadow); margin-bottom: 32px; }}
    .category-tag {{ display: inline-block; background: var(--mint-light); color: var(--teal-deep); font-weight: 800; font-size: 0.88rem; padding: 6px 14px; border-radius: 20px; margin-bottom: 16px; border: 1px solid #A7F3D0; }}
    .hero-title {{ font-size: 1.95rem; font-weight: 900; color: var(--teal-deep); line-height: 1.35; margin-bottom: 16px; }}
    .hero-lead {{ font-size: 1.12rem; color: var(--text-muted); margin-bottom: 24px; }}
    
    .trust-badges-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 28px; }}
    .trust-badge-item {{ background: #F1F5F9; border-radius: 10px; padding: 12px 14px; font-weight: 700; font-size: 0.88rem; color: #1E293B; display: flex; align-items: center; gap: 8px; }}
    
    .hero-cta-row {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .btn-hero-primary {{ flex: 1; min-width: 260px; background: #059669; color: #fff; padding: 14px 24px; border-radius: 12px; font-size: 1.05rem; font-weight: 800; text-align: center; border: none; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25); text-decoration: none; display: inline-block; }}
    .btn-hero-primary:hover {{ background: #047857; transform: translateY(-2px); }}
    .btn-hero-secondary {{ flex: 1; min-width: 220px; background: #F8FAFC; color: var(--teal-deep); border: 2px solid var(--border); padding: 14px 20px; border-radius: 12px; font-size: 1rem; font-weight: 800; text-align: center; text-decoration: none; display: flex; justify-content: center; align-items: center; }}
    .btn-hero-secondary:hover {{ background: #F1F5F9; }}

    .video-container-card {{ background: #0F172A; border-radius: var(--radius); padding: 20px; margin-bottom: 32px; color: #fff; }}
    .video-header-tag {{ color: #6EE7B7; font-weight: 800; font-size: 0.95rem; margin-bottom: 12px; }}
    .lp-video-player {{ width: 100%; max-height: 480px; border-radius: 12px; background: #000; outline: none; }}
    .video-caption {{ font-size: 0.88rem; color: #94A3B8; margin-top: 10px; }}

    .clinical-narrative-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; margin-bottom: 32px; box-shadow: var(--shadow); }}
    .clinical-narrative-card h2 {{ font-size: 1.45rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 16px; }}
    .narrative-body {{ font-size: 1.05rem; line-height: 1.85; color: #334155; white-space: pre-line; margin-bottom: 24px; }}

    .products-section-title {{ font-size: 1.5rem; font-weight: 900; color: var(--teal-deep); margin-bottom: 20px; }}
    .products-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-bottom: 36px; }}
    .product-lp-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); display: flex; flex-direction: column; justify-content: space-between; }}
    .product-lp-card h3 {{ font-size: 1.25rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 8px; }}
    .prod-desc {{ font-size: 0.92rem; color: var(--text-muted); margin-bottom: 16px; line-height: 1.6; }}

    .faq-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; box-shadow: var(--shadow); margin-bottom: 36px; }}
    .faq-title {{ font-size: 1.45rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 20px; }}
    .faq-accordion-item {{ border-bottom: 1px solid var(--border); padding: 16px 0; }}
    .faq-accordion-item:last-child {{ border-bottom: none; }}
    .faq-question {{ font-weight: 700; font-size: 1.05rem; color: var(--teal-dark); cursor: pointer; outline: none; }}
    .faq-answer {{ margin-top: 10px; font-size: 0.95rem; color: var(--text-muted); line-height: 1.7; padding-right: 20px; }}

    .footer-bar {{ background: var(--teal-deep); color: #E2E8F0; text-align: center; padding: 28px 20px; font-size: 0.88rem; }}
    .footer-bar a {{ color: #A7F3D0; text-decoration: none; margin: 0 8px; font-weight: 700; }}

    .sticky-mobile-cta {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--surface); border-top: 1px solid var(--border); padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 -4px 16px rgba(0,0,0,0.06); z-index: 999; }}
    .btn-sticky-wa {{ background: #25D366; color: #fff; padding: 10px 20px; border-radius: 10px; font-weight: 800; text-decoration: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; }}

    @media (max-width: 640px) {{
      .hero-card {{ padding: 24px; }}
      .hero-title {{ font-size: 1.55rem; }}
    }}
  </style>
</head>
<body>

  <div class="top-banner">
    <span>🛡️ دليل إرشادي سريري مستقل موثق بالدراسات — كود الاستشارة والمتابعة المجانية:</span>
    <span class="code-pill">{OFFICIAL_PROMO_CODE}</span>
  </div>

  <header class="nav-bar">
    <a href="{SITE_BASE_URL}/" class="nav-logo">
      <span>🛡️ هيلينج تاتش مصر | Healing Touch</span>
    </a>
    <a href="{wa_direct_link}" target="_blank" rel="noopener" class="btn-nav-wa">
      💬 تواصل واتساب مجاناً
    </a>
  </header>

  <main class="container">
    <section class="hero-card">
      <div class="category-tag">دليل التعافي السريري والحلول الطبية</div>
      <h1 class="hero-title">{spec['title']}</h1>
      <p class="hero-lead">{spec['lead']}</p>
      
      <div class="trust-badges-grid">
        <div class="trust-badge-item">✅ موثق بدراسات PubMed & Cochrane</div>
        <div class="trust-badge-item">🛡️ مستلزمات طبية أصلية ومعتمدة 100%</div>
        <div class="trust-badge-item">💬 استشارة سريرية وتوجيه مجاني على واتساب</div>
      </div>

      <div class="hero-cta-row">
        <a href="{wa_direct_link}" target="_blank" rel="noopener" class="btn-hero-primary">
          💬 استشارة سريرية مجانية عبر واتساب
        </a>
        <a href="{SITE_BASE_URL}/portal/" class="btn-hero-secondary">
          🩺 دليلك التفاعلي وحاسبة التعافي
        </a>
      </div>
    </section>

    {video_block}
    {audio_block}

    <section class="clinical-narrative-card">
      <h2>📖 الشرح السريري والآلية العلمية للتعافي</h2>
      <div class="narrative-body">{spec['narrative']}</div>
      <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:12px; padding:16px 20px;">
        <span style="font-weight:800; color:#065F46;">💡 نصيحة سريرية:</span>
        <span style="color:#166534; font-size:0.95rem;"> احرصي على استشارة أخصائي الرعاية السريرية قبل البدء لتحديد المقاس والبروتوكول الملائم تماماً لتاريخ عمليتك.</span>
      </div>
    </section>

    <section>
      <h2 class="products-section-title">🛡️ المستلزم الطبي الموصى به لهذه المرحلة</h2>
      <div class="products-grid">
        {"".join(prods_cards_html)}
      </div>
    </section>

    <section class="faq-card">
      <h2 class="faq-title">❓ الأسئلة الشائعة والأخطاء الحرجة</h2>
      {faq_html}
    </section>
  </main>

  <footer class="footer-bar">
    <p>جميع الحقوق محفوظة © 2026 هيلينج تاتش مصر | محتوى إرشادي توجيهي غير تجاري</p>
    <p style="margin-top:8px;">
      <a href="{SITE_BASE_URL}/">الصفحة الرئيسية</a> |
      <a href="{SITE_BASE_URL}/portal/">البوابة التفاعلية</a> |
      <a href="{wa_direct_link}" target="_blank" rel="noopener">استشارة واتساب مجانية</a>
    </p>
  </footer>

  <div class="sticky-mobile-cta">
    <div>
      <span style="font-size:0.85rem; font-weight:800; color:var(--teal-deep); display:block;">استشارة ومتابعة سريرية</span>
      <span style="font-size:0.75rem; color:var(--text-muted);">كود الدعم: {OFFICIAL_PROMO_CODE}</span>
    </div>
    <a href="{wa_direct_link}" target="_blank" rel="noopener" class="btn-sticky-wa">
      💬 استشارة واتساب مجانية
    </a>
  </div>

</body>
</html>
"""
            lp_file.write_text(html_content, encoding="utf-8")
            created_pages.append({
                "slug": slug,
                "local_file": str(lp_file),
                "public_url": page_public_url,
                "title": spec["title"],
                "category": spec["category"]
            })

    print(f"[+] تم بناء وتحديث {len(created_pages)} صفحة هبوط مستقلة ومتخصصة لكل منتج طبي في docs/lp/!")
    return created_pages
