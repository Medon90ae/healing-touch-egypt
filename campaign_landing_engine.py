# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك صفحات الهبوط المستقلة وحزم البرومبتات الذكية (2026)
Campaign Landing Page Engine & Multi-Tool Prompt Orchestrator
(Google Pomelli + Google Stitch + Gemini Deep Research + Google NotebookLM)
=============================================================================
"""

import os
import sys
import json
import re
import shutil
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
# 1️⃣ توليد حزمة البرومبتات المتكاملة (Pomelli + Stitch + Deep Research + NotebookLM)
# =============================================================================
def generate_prompts_and_sources_pack(case_data: dict, pic_files: list = None) -> dict:
    title = case_data.get("title", "بروتوكول العناية الجراحية وعلاج الندبات")
    cat = case_data.get("category", "c-section")
    story_text = case_data.get("story_text", "")
    hashtags = case_data.get("hashtags", "")

    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    date_display = now.strftime("%Y-%m-%d %I:%M %p")

    # أسماء وتصنيفات بالإنجليزية لأداة Pomelli
    pomelli_scenarios = {
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

    scen = pomelli_scenarios.get(cat, pomelli_scenarios["c-section"])

    # نص الحزمة الكامل المنسق
    pack_md = f"""# 🌿 حزمة البرومبتات والإنتاج الرقمي الموحد اليومية – هيلينج تاتش مصر
**تاريخ التوليد:** {date_display}
**الحالة المستهدفة:** {title} ({scen['ar_name']})
**كود الخصم المعتمد:** `HT10` (شحن مجاني لكافة المحافظات + حق فتح ومعاينة الشحنة قبل الدفع)
**رابط اللاندنج بيدج المتوقع:** `{SITE_BASE_URL}/lp/{cat}-recovery-protocol.html`

=============================================================================
🎨 [1] برومبت أداة Google Pomelli (جلسات التصوير الإعلاني الفاخرة Photoshoot & Campaigns):
الرابط المباشر: https://labs.google.com/pomelli/campaigns
=============================================================================
💡 تعليمات الاستخدام في Pomelli للحصول على صور استوديو عالمية بالمنتج الحقيقي 100%:
1. اضغط على زر [Product] في واجهة Pomelli وارفع صورة المنتج الحقيقية من مجلد:
   C:\\followUPSHEET\\healing_touch\\media_assets\\notebooklm_hub\\pic
2. اختر مقاس العرض [Aspect Ratio]:
   • اختر 1:1 لبوست فيسبوك وإنستجرام.
   • اختر 9:16 لكارت الستوري وتيك توك.
   • اختر 16:9 لغلاف اللاندنج بيدج وبلوجر.
3. انسخ البرومبت الإنجليزي التالي والصقه في مربع الوصف:

--- [برومبت الصورة المربعة 1:1 لبوست فيسبوك وإنستجرام] ---
{scen['en_prompt_square']}

--- [برومبت الصورة الرأسية 9:16 لاستوري إنستجرام وتيك توك] ---
{scen['en_prompt_story']}

--- [برومبت الغلاف الأفقي 16:9 للاندنج بيدج والمدونة] ---
{scen['en_prompt_hero']}

=============================================================================
🧩 [2] برومبت أداة Google Stitch (تصميم واجهات وصفحات الهبوط AI):
الرابط المباشر: https://stitch.withgoogle.com/
=============================================================================
💡 لإنشاء واجهة لاندنج بيدج مخصصة بالذكاء الاصطناعي على Stitch:
انسخ الأمر التالي والصقه في شات Stitch:

```text
Design a luxury, high-converting Arabic (RTL) medical recovery landing page for "Healing Touch Egypt" (هيلينج تاتش مصر).
Topic: {title} ({scen['ar_name']}).
Brand Colors: Deep Teal (#064E3B), Emerald (#059669), Mint (#10B981), Amber (#D97706), Soft White background.
Sections to include:
1. Hero Section with reassuring medical headline, trust badges (Free Shipping Egypt, Inspection before Payment, Code HT10).
2. Video & Photoshoot showcase section with clinical proof.
3. Interactive Comparison Table (Traditional Care vs Healing Touch Protocol).
4. Product Cards with real prices in EGP and CTA buttons.
5. Scientific Evidence section citing PubMed and Cochrane studies.
6. FAQ Accordion for post-op recovery queries.
7. Sticky Mobile CTA bar: "حجز استشارة مجانية بكود HT10".
All CTA buttons should trigger free recovery consultation modal.
```
💡 ملحوظة: بعد الانتهاء اضغط Export ونزّل كود HTML وضعه في manual_inbox ليقوم المحرك بحقن بوابة التسجيل فيه تلقائياً! (وإذا لم تضعه، المحرك سينشئ اللاندنج بيدج أوتوماتيكياً).

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
1. 🎬 [فيديو شارح]: شغل أداة (Video Overview) في الاستوديو لإنشاء فيديو شارح تفاعلي لبيولوجيا التعافي بعد {scen['ar_name']} باستخدام مستلزمات BUPY و 3M و Opsite مع التنويه لكود الخصم HT10 ورقم الواتساب 01155803307.
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
        "pomelli_prompt": scen["en_prompt_square"],
        "title": title,
        "category": cat
    }


# =============================================================================
# 2️⃣ بناء وتوليد Landing Page مستقلة فائقة التحويل (مع بوابة التسجيل الإجبارية)
# =============================================================================
def build_campaign_landing_page(case_data: dict, media_assets: dict = None, custom_stitch_html: str = "") -> dict:
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

    # إذا وفّر المستخدم كود HTML مخصص من Google Stitch
    if custom_stitch_html and len(custom_stitch_html.strip()) > 200:
        print("[*] 🧩 تم اكتشاف تصميم واجهة مخصص من Google Stitch! جاري حقن بوابة التسجيل الإجبارية وأكواد السيو...")
        augmented_html = _inject_gate_and_tracking_into_stitch_html(custom_stitch_html, title, cat, page_public_url)
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
          <div class="prod-price-row">
            <span class="live-price">{p.get('price_display', 'السعر سارٍ')}</span>
            <span class="promo-pill">شحن مجاني بكود HT10</span>
          </div>
          <button class="btn-order-prod" onclick="openPromoDrawer('{p.get('name_ar')}', 'whatsapp'); return false;">
            🩺 اطلب الآن واستشر الأخصائية مجاناً
          </button>
        </div>
        """)

    video_block = ""
    if video_rel_path:
        video_block = f"""
        <div class="video-container-card">
          <div class="video-header-tag">🎬 فيديو الشرح السريري التوضيحي (Google NotebookLM Studio)</div>
          <video controls autoplay muted loop playsinline class="lp-video-player">
            <source src="{video_rel_path}" type="video/mp4">
            متصفحك لا يدعم تشغيل الفيديو المباشر.
          </video>
          <p class="video-caption">شرح تفاعلي لبيولوجيا التعافي، مراحل تنظيم الكولاجين، وطريقة استخدام المستلزمات الطبية المعتمدة للوقاية من تضخم الندبات.</p>
        </div>
        """

    # أسئلة شائعة مطابقة لترندات بحث جوجل مصر
    faq_items = [
        ("هو ينفع أستحمى بأمان بعد الجراحة بدون ما الجرح يلتهب؟", "نعم، باستخدام الضمادات شبه المنفذة مثل 3M Tegaderm أو بخاخ أوبسايت العازل Smith & Nephew Opsite، يتم عزل الماء بنسبة 100% مع السماح للجلد بالتنفس وطرد بخار العرق، مما يتيح لك الاستحمام بحرية تامة دون رطوبة متبقية على خط الخياطة."),
        ("ليه حاسة بخط ناشف ومكلكع تحت مكان الجرح بعد أسبوعين؟", "هذا تكتل طبيعي ناتج عن إفراز مكثف وعشوائي لألياف الكولاجين خلال مرحلة الالتئام. تطبيق رول السيليكون الطبي BUPY يمارس ضغطاً ميكانيكياً خفيفاً ويحبس الرطوبة الفسيولوجية، مما يعيد ترتيب ألياف الكولاجين في مسار مسطح وناعم ويمنع تحول الخط إلى كلويد دائم."),
        ("ما هي مميزات كود الخصم HT10 وكيف أحصل على الاستشارة؟", "كود HT10 يمنحك شحناً مجانياً لكافة محافظات مصر مع ميزة فتح ومعاينة الشحنة قبل الدفع للتأكد من أصلية المستلزمات الطبية وتاريخ الصلاحية، بالإضافة لمتابعة سريرية مجانية عبر واتساب مع أخصائية العناية بالتعافي.")
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
  <meta property="og:description" content="بروتوكول علمي متكامل لمنع تضخم الندبات وتأمين الاستحمام مع كود الخصم HT10 وشحن مجاني ومعاينة قبل الدفع.">
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
    .prod-price-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding: 10px 0; border-top: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9; }}
    .live-price {{ font-size: 1.25rem; font-weight: 900; color: var(--teal-deep); }}
    .promo-pill {{ font-size: 0.78rem; background: var(--amber-light); color: #B45309; padding: 3px 8px; border-radius: 6px; font-weight: 800; }}
    .btn-order-prod {{ width: 100%; background: var(--teal-dark); color: #fff; border: none; padding: 12px; border-radius: 10px; font-weight: 800; font-size: 0.95rem; cursor: pointer; transition: 0.2s; }}
    .btn-order-prod:hover {{ background: var(--emerald); }}

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
    <span>🌿 كود الخصم الحصري المعتمد لليوم:</span>
    <span class="code-pill">HT10</span>
    <span>(شحن مجاني لكافة محافظات مصر + حق فتح ومعاينة الشحنة قبل الدفع)</span>
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
        <div class="trust-badge-item">🚚 شحن مجاني لكافة محافظات مصر</div>
        <div class="trust-badge-item">📦 حق فتح وفحص الشحنة قبل الدفع</div>
        <div class="trust-badge-item">🛡️ مستلزمات طبية أصلية 100%</div>
        <div class="trust-badge-item">🩺 متابعة مستمرة مع أخصائية التعافي</div>
      </div>

      <div class="hero-cta-row">
        <button class="btn-hero-primary" onclick="openPromoDrawer('{title}', 'whatsapp'); return false;">
          💬 احجز استشارة مجانية الآن وفعّل كود HT10
        </button>
        <a href="#products-section" class="btn-hero-secondary">
          📦 استعرض المستلزمات الطبية والأسعار
        </a>
      </div>
    </section>

    <!-- مشغل الفيديو الشارح إن وجد -->
    {video_block}

    <!-- السرد الإكلينيكي وحل المشكلة -->
    <section class="clinical-narrative-card">
      <h2>🧬 التحليل الطبي وبيولوجيا التئام الأنسجة:</h2>
      <div class="narrative-body">{story_text}</div>
      <button class="btn-hero-primary" onclick="openPromoDrawer('استشارة سريرية بخصوص: {title}', 'whatsapp'); return false;">
        🩺 اسأل أخصائية التعافي عن حالتك بالتحديد مجاناً
      </button>
    </section>

    <!-- قائمة المستلزمات الطبية المعتمدة بأسعارها الحية -->
    <section id="products-section">
      <h2 class="products-section-title">📦 المستلزمات الطبية المعتمدة للبروتوكول السريري (بأسعارها الرسمية):</h2>
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
        <span>كود الخصم <strong>HT10</strong> مفعل تلقائياً</span>
        <br><small style="color: #64748B;">شحن مجاني ومعاينة قبل الدفع</small>
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
      <p class="lead-modal-desc">أهلاً بكِ في هيلينج تاتش مصر. لتسجيل ملفك وتفعيل كود الخصم <strong>HT10</strong> (شحن مجاني + حق المعاينة قبل الدفع)، يرجى إدخال اسمك ورقم الموبايل للمتابعة:</p>
      
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
        💬 تفعيل الخصم وبدء المحادثة عبر واتساب
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
        errEl.innerText = "⚠️ يرجى إدخال اسمك الكريم (حرفين على الأقل) لتسجيل ملف الاستشارة وتفعيل الخصم.";
        errEl.style.display = 'block';
        if (nameInput) nameInput.focus();
        return;
      }}

      const egyptPhoneRegex = /^01[0125][0-9]{{8}}$/;
      if (!pPhone || !egyptPhoneRegex.test(pPhone)) {{
        errEl.innerText = "⚠️ يرجى إدخال رقم موبايل/واتساب صحيح مكون من 11 رقماً يبدأ بـ 01 لتفعيل كود الخصم.";
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
            topic: currentTopic,
            promo_code: PROMO_CODE,
            page_url: window.location.href,
            client_name: pName,
            client_phone: pPhone
          }})
        }}).catch(() => {{}});
      }} catch(e) {{}}

      document.getElementById('promo-lead-modal').style.display = 'none';

      const waMsg = "أهلاً بكِ، أنا (" + pName + ") مسجل في موقع هيلينج تاتش بكود الخصم (HT10 - شحن مجاني لكافة المحافظات ومعاينة قبل الدفع)، ومحتاج استشارة مجانية بخصوص: " + currentTopic;
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


def _inject_gate_and_tracking_into_stitch_html(raw_html: str, title: str, category: str, page_url: str) -> str:
    """حقن بوابة تسجيل البيانات الإلزامية في أي كود HTML مصدّر من Google Stitch لمنع أي تجاوز للواتساب."""
    gate_script_and_modal = f"""
    <!-- Zero-Bypass Lead Drawer Injected by Healing Touch Engine -->
    <div id="promo-lead-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(6,78,59,0.7); backdrop-filter:blur(4px); z-index:999999; justify-content:center; align-items:center; padding:16px; direction:rtl; font-family:'Cairo',sans-serif;">
      <div style="background:#fff; border-radius:20px; max-width:460px; width:100%; padding:28px; box-shadow:0 20px 40px rgba(0,0,0,0.25); border:2px solid #6EE7B7; text-align:center;">
        <h3 style="color:#064E3B; font-size:1.35rem; font-weight:900; margin-bottom:8px;">🩺 استشارة سريرية مجانية</h3>
        <p style="font-size:0.92rem; color:#475569; margin-bottom:20px; line-height:1.5;">لتسجيل ملفك وتفعيل كود الخصم <strong>{OFFICIAL_PROMO_CODE}</strong> (شحن مجاني + معاينة قبل الدفع)، يرجى إدخال اسمك ورقم الموبايل:</p>
        <div style="text-align:right; margin-bottom:14px;">
          <label style="display:block; font-weight:800; font-size:0.88rem; color:#1E293B; margin-bottom:6px;">اسم العميل الكريم:</label>
          <input type="text" id="stitch-lead-name" placeholder="مثال: سارة أحمد" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #CBD5E1; font-size:1rem; outline:none; box-sizing:border-box;">
        </div>
        <div style="text-align:right; margin-bottom:16px;">
          <label style="display:block; font-weight:800; font-size:0.88rem; color:#1E293B; margin-bottom:6px;">رقم الموبايل / واتساب (11 رقماً):</label>
          <input type="tel" id="stitch-lead-phone" placeholder="مثال: 01012345678" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #CBD5E1; font-size:1rem; outline:none; box-sizing:border-box;">
        </div>
        <div id="stitch-lead-error" style="color:#DC2626; font-size:0.85rem; font-weight:700; margin-bottom:12px; display:none; text-align:right;"></div>
        <button onclick="confirmStitchLead();" style="width:100%; background:#059669; color:#fff; border:none; padding:14px; border-radius:12px; font-size:1.05rem; font-weight:800; cursor:pointer;">
          💬 تفعيل الخصم وبدء المحادثة عبر واتساب
        </button>
        <button onclick="document.getElementById('promo-lead-modal').style.display='none';" style="background:transparent; border:none; color:#94A3B8; font-weight:700; font-size:0.88rem; cursor:pointer; margin-top:10px;">إلغاء</button>
      </div>
    </div>

    <script>
      function openPromoDrawer(topic, channel) {{
        const m = document.getElementById('promo-lead-modal');
        if (m) {{ m.style.display = 'flex'; document.getElementById('stitch-lead-name').focus(); }}
      }}
      function confirmStitchLead() {{
        const n = document.getElementById('stitch-lead-name').value.trim();
        const p = document.getElementById('stitch-lead-phone').value.trim().replace(/\\s+/g, '');
        const err = document.getElementById('stitch-lead-error');
        if (!n || n.length < 2) {{ err.innerText = "يرجى كتابة الاسم الكريم أولاً"; err.style.display='block'; return; }}
        if (!/^01[0125][0-9]{{8}}$/.test(p)) {{ err.innerText = "يرجى كتابة رقم موبايل صحيح (11 رقماً)"; err.style.display='block'; return; }}
        err.style.display='none';
        try {{
          fetch('{TRACKING_ENDPOINT}', {{
            method: 'POST', mode: 'no-cors',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ timestamp: new Date().toISOString(), channel: 'whatsapp', topic: '{title}', promo_code: '{OFFICIAL_PROMO_CODE}', page_url: '{page_url}', client_name: n, client_phone: p }})
          }}).catch(() => {{}});
        }} catch(e) {{}}
        document.getElementById('promo-lead-modal').style.display='none';
        const msg = "أهلاً بكِ، أنا (" + n + ") مسجل في موقع هيلينج تاتش بكود الخصم (HT10)، ومحتاج استشارة بخصوص: {title}";
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
    new_url_entry = f"  <url><loc>{SITE_BASE_URL}/lp/{slug}.html</loc><lastmod>{today_str}</lastmod><priority>0.92</priority></url>"
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
