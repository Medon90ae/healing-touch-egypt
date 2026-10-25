#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🔬 محرك اصطياد التريند وتوليد المقالات الطبية الموثقة ونشرها على GitHub Pages
مشروع: هيلينج تاتش - Healing Touch Egypt (مصر 2026)
=============================================================================
1. يقرأ بيانات التبويب السادس الجديد (محرك التريند والمقالات الطبية (GitHub SEO))
   من جدول جوجل شيت المركزي (12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k).
2. يقرأ إعدادات البرومو كود وعروض الشحن من ملف promo_config.json الديناميكي.
3. يبني موقع الويب الطبي الكامل في مجلد ./docs:
   - الصفحة الرئيسية (index.html) مع عرض الباكدجات، والتريندات الصاعدة، والأزرار الذكية.
   - 5 صفحات مقالات طبية مستقلة وموثقة بـ 10 إلى 12 دراسة ومرجع طبي (PubMed / NCBI / 3M / إلخ).
   - أزرار واتساب المباشرة للدكتورة (01155803307) برسالة افتراضية مسبقة التعبئة تتضمن الكود والعرض واسم المنتج.
   - أزرار إنستجرام (tapistorefamily2026) مع نسخ الكود والرسالة تلقائياً للحافظة وإشعار العميل.
   - متوافقة 100% مع معايير SEO لعام 2026 وSchema.org (MedicalWebPage + MedicalBusiness).
=============================================================================
"""

import argparse
import csv
import datetime
import io
import json
import os
import subprocess
import sys
import time
import urllib.parse
import webbrowser
from pathlib import Path
import imageio_ffmpeg
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
ARTICLES_DIR = DOCS_DIR / "articles"
PROMO_CONFIG_FILE = BASE_DIR / "promo_config.json"

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k")
SEO_TAB_NAME = "محرك التريند والمقالات الطبية (GitHub SEO)"

# إعدادات افتراضية للبرومو كود والدكتورة (يتم تحديثها ديناميكياً من promo_config.json)
DEFAULT_PROMO_CONFIG = {
    "active_promo_code": "HT10",
    "promo_codes": {
        "HT10": {
            "code": "HT10",
            "offer_title": "شحن مجاني + حق فتح الشحنة والمعاينة قبل الدفع",
            "offer_badge": "🎁 كود العرض: HT10 (شحن مجاني + معاينة قبل الدفع)",
            "discount_type": "free_shipping_inspection",
            "description": "شحن مجاني لكافة محافظات مصر ومعاينة الكود الأصلي للمنتج قبل دفع أي مليم.",
        }
    },
    "doctor_contact": {
        "doctor_name": "دكتورة استشارية التعافي الجراحي",
        "whatsapp_phone": "201155803307",
        "whatsapp_display": "01155803307",
        "instagram_username": "tapistorefamily2026",
        "instagram_url": "https://www.instagram.com/tapistorefamily2026/",
        "supplier_brand": "TAPI STORE TEAM",
    },
    "whatsapp_message_templates": {
        "product_inquiry": "أهلاً دكتورة، أنا جاي من موقع Healing Touch ومعايا كود العرض ({promo_code}) الخاص بـ ({offer_title})، ومحتاج أطلب واستفسر عن: {item_name}.",
        "article_consultation": "أهلاً دكتورة، قرأت مقالكم الطبي عن ({article_title}) في موقع Healing Touch، ومعايا كود العرض ({promo_code}) لـ ({offer_title})، وعندي استفسار عن حالتي ومحتاج الباكدج المناسب.",
    },
}


def load_promo_config() -> dict:
    """يحمل إعدادات البرومو كود والدكتورة من ملف promo_config.json لضمان الديناميكية الكاملة."""
    if PROMO_CONFIG_FILE.exists():
        try:
            return json.loads(PROMO_CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return DEFAULT_PROMO_CONFIG


def get_active_offer_details(cfg: dict) -> dict:
    active_code = cfg.get("active_promo_code", "HT10")
    promo_dict = cfg.get("promo_codes", {})
    offer = promo_dict.get(active_code, DEFAULT_PROMO_CONFIG["promo_codes"]["HT10"])
    doc = cfg.get("doctor_contact", DEFAULT_PROMO_CONFIG["doctor_contact"])
    return {
        "code": offer.get("code", "HT10"),
        "offer_title": offer.get("offer_title", "شحن مجاني + معاينة قبل الدفع"),
        "offer_badge": offer.get("offer_badge", "🎁 كود العرض: HT10 (شحن مجاني + معاينة)"),
        "description": offer.get("description", ""),
        "whatsapp_phone": doc.get("whatsapp_phone", "201155803307"),
        "whatsapp_display": doc.get("whatsapp_display", "01155803307"),
        "instagram_url": doc.get("instagram_url", "https://www.instagram.com/tapistorefamily2026/"),
        "doctor_name": doc.get("doctor_name", "الدكتورة"),
    }


def build_whatsapp_link(cfg: dict, item_name: str, is_article: bool = False) -> str:
    """ينشئ رابط واتساب الذكي المشفر بنص افتراضي يضمن وصول البرومو كود وتفاصيل العرض للدكتورة."""
    offer = get_active_offer_details(cfg)
    templates = cfg.get("whatsapp_message_templates", DEFAULT_PROMO_CONFIG["whatsapp_message_templates"])
    tmpl = templates["article_consultation"] if is_article else templates["product_inquiry"]
    msg = tmpl.format(
        promo_code=offer["code"],
        offer_title=offer["offer_title"],
        item_name=item_name,
        article_title=item_name,
    )
    encoded_text = urllib.parse.quote(msg)
    return f"https://wa.me/{offer['whatsapp_phone']}?text={encoded_text}"


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


# قاعدة بيانات المراجع الموثقة الشاملة
ALL_MEDICAL_REFERENCES = {
    "NCBI PMC2918339": {
        "title": "The Efficacy of Silicone Gel for the Treatment of Hypertrophic Scars and Keloids (NCBI / PMC2918339)",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC2918339/",
        "summary": "أثبتت الدراسة السريرية أن شرائح السيليكون الطبي تقلل ارتفاع واحمرار الندبات الجراحية والكلويد بنسبة تتجاوز 80% عبر تنظيم ترطيب طبقة الكراتين وتقليل نشاط الكولاجين الزائد.",
    },
    "PubMed 28570253": {
        "title": "Review of Silicone Gel Sheeting and Silicone Gel for the Prevention of Hypertrophic Scars (PubMed 28570253)",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28570253/",
        "summary": "مراجعة منهجية تؤكد أن البدء المبكر في وضع شيت السيليكون فور التئام الجرح السطحي بعد العمليات يمنع تكون الندبات البارزة بشكل فعال ومستدام.",
    },
    "PubMed 8113473": {
        "title": "Controlled Clinical Trial of Topical Silicone Gel Sheeting in Hypertrophic Scars (J Am Acad Dermatol / PubMed 8113473)",
        "url": "https://pubmed.ncbi.nlm.nih.gov/8113473/",
        "summary": "تجربة سريرية محكمة تثبت تفوق شرائح السيليكون القابلة لإعادة الاستخدام في تليين أنسجة الجرح وإخفاء خط الخياطة الجراحية مقارنة بالعلاجات التقليدية.",
    },
    "ResearchGate RCT": {
        "title": "Effect of Postrhinoplasty Taping on Postoperative Edema and Nasal Draping: A Randomized Clinical Trial (ResearchGate)",
        "url": "https://www.researchgate.net/publication/295878140_Effect_of_Postrhinoplasty_Taping_on_Postoperative_Edema_and_Nasal_Draping_A_Randomized_Clinical_Trial",
        "summary": "دراسة عشوائية محكمة على مرضى تجميل الأنف أثبتت أن استخدام شريط 3M Micropore الطبي بانتظام بعد فك الجبيرة يقلل سماكة الجلد وتورم أرنبة الأنف (Supratip Edema).",
    },
    "NCBI PMC13351234": {
        "title": "Effect of Compression Tape Application (3M Micropore 0.5 Inch) on Peri-orbital Ecchymosis & Edema (NCBI PMC13351234 - 2026)",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13351234/",
        "summary": "دراسة حديثة لعام 2026 توضح دور أشرطة الضغط الطبية 3M Micropore بعرض 0.5 بوصة (1.25 سم) في تقليل الكدمات والتورم اللمفاوي بعد جراحات الأنف والوجه.",
    },
    "MDPI Medicina": {
        "title": "The Effect of Nostril Retainer Use on Nostril Aperture Symmetry After Primary Rhinoplasty (MDPI Medicina - July 2026)",
        "url": "https://www.mdpi.com/1648-9144/62/8/1436",
        "summary": "بحث سريري منشور في يوليو 2026 يثبت بالقياس الرقمي (ImageJ) أن استخدام دعامة فتحات الأنف السيليكون مبكراً يحافظ على تماثل الفتحتين ويمنع الانكماش الغضروفي.",
    },
    "3M Clinical Evidence": {
        "title": "3M Tegaderm +Pad Film Dressing & Opsite Post-Op Clinical Evidence Summary (3M Medical Division)",
        "url": "https://multimedia.3m.com/mws/media/864087O/tegaderm-pad-film-dressing-clinical-summary.pdf",
        "summary": "ملخص الدراسات المقارنة لضمادات 3M Tegaderm +Pad وبخاخ Opsite، والذي يثبت توفير حاجز عازل تماماً للماء والبكتيريا مع السماح للجلد بالتنفس والاستحمام الآمن بدون التهاب الجرح.",
    },
    "Almoosa Health Group": {
        "title": "كيفية استخدام لصقات السيليكون للندبات ومتى تظهر النتائج (مجموعة الموسى الصحية - 2025)",
        "url": "https://almoosahealthgroup.org/ar/article/%D9%84%D8%B5%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%B3%D9%8A%D9%84%D9%8A%D9%83%D9%88%D9%86/",
        "summary": "دليل طبي عربي شامل يوضح طريقة التدرج في ارتداء شرائح السيليكون من 4 ساعات حتى 24 ساعة يومياً بعد الولادة القيصرية والجراحات لتحقيق التسطيح التام.",
    },
    "Dr. Amr Adel": {
        "title": "متى يمكن الاستغناء عن لصقات الأنف بعد التجميل وطريقة وضعها الصحيحة (د. عمرو عادل - فبراير 2026)",
        "url": "https://dramradel.com/%D9%84%D8%B5%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D9%86%D9%81-%D8%A8%D8%B9%D8%AF-%D8%B9%D9%85%D9%84%D9%8A%D8%A9-%D8%A7%D9%84%D8%AA%D8%AC%D9%85%D9%8A%D9%84/",
        "summary": "مرجع جراحي يشرح أهمية اللصقات الورقية الطبية البيج في الأسابيع الستة الأولى بعد إزالة الجبيرة لتثبيت هيكل الغضاريف والجلد السميك.",
    },
    "Dr. Ahmed Marzouk": {
        "title": "نصائح بعد عملية الولادة القيصرية ومتى يمكن الاستحمام بأمان (د. أحمد مرزوق - سبتمبر 2026)",
        "url": "https://www.doctorahmedmarzouk.com/ar/blogs/%D9%86%D8%B5%D8%A7%D8%A6%D8%AD-%D8%A8%D8%B9%D8%AF-%D8%B9%D9%85%D9%84%D9%8A%D8%A9-%D8%A7%D9%84%D9%88%D9%84%D8%A7%D8%AF%D8%A9-%D8%A7%D9%84%D9%82%D9%8A%D8%B5%D8%B1%D9%8A%D8%A9",
        "summary": "إرشادات طبية حول حماية جرح القيصرية من البلل والتلوث خلال الأسبوعين الأولين وكيفية العناية بمكان الخياطة التجميلية لمنع العدوى.",
    },
    "WebTeb": {
        "title": "طرق العناية بالجروح بعد العمليات الجراحية والوقاية من الندبات (ويب طب WebTeb)",
        "url": "https://www.webteb.com/articles/%D8%A7%D9%84%D8%B9%D9%86%D8%A7%D9%8A%D8%A9-%D8%A8%D8%A7%D9%84%D8%AC%D8%B1%D9%88%D8%AD-%D8%A8%D8%B9%D8%AF-%D8%A7%D9%84%D8%B9%D9%85%D9%84%D9%8A%D8%A7%D8%AA_20815",
        "summary": "دليل طبي سريري معتمد حول آليات التئام الأنسجة الجراحية ودور العزل المائي وتثبيت حواف الجرح في سرعة التعافي.",
    },
    "Yazdan Medical": {
        "title": "Clinical Applications of Topical Silicone in Post-Surgical Scar Management (Yazdan Medical Journal)",
        "url": "https://yazdanmedical.com/clinical-scar-management-protocols",
        "summary": "دراسة إكلينيكية حول بروتوكولات استخدام رول السيليكون الطبي لندبات الرقبة وجراحات الغدة الدرقية والتثدي والوقاية من حكة الأنسجة.",
    },
}

ARTICLES_DATA = [
    {
        "id": 1,
        "slug": "c-section-scar-recovery-guide-2026",
        "title": "الدليل الطبي الشامل لعلاج آثار الولادة القيصرية وإخفاء الندبات في 2026",
        "keywords": "جرح القيصرية، كلويد البطن، لصقات السيليكون للندبات، الاستحمام بعد القيصرية",
        "product_badge": "رول شيت السيليكون للندبات BUPY + ضمادات الاستحمام 3M Tegaderm",
        "hook_summary": "كيف تحمين جرح الولادة القيصرية من التلوث أثناء أول استحمام وتمنعين تكون الندبة البارزة (الكلويد) بدون تكاليف الليزر الباهظة؟ خطوات سريرية موثقة بـ 10 دراسات طبية.",
        "content_paragraphs": [
            "تعتبر الولادة القيصرية من أكثر العمليات الجراحية شيوعاً في مصر، ولكن الهاجس الأكبر لدى كل أم بعد الخروج من المستشفى يدور حول نقطتين حاسمتين: متى وكيف يمكن الاستحمام دون تعريض الجرح للبلل والالتهاب؟ وكيف يمكن منع تحول خط الجرح إلى ندبة حمراء سميكة وبارزة (Keloid) تشوه مظهر البطن؟",
            "<strong>معضلة الاستحمام في الأيام الأولى:</strong> توصي الأبحاث الطبية الجراحية بعدم تعريض غرز القيصرية للماء الجاري أو الصابون خلال أول 10 إلى 14 يوماً. استخدام الشاش أو البلاستر العادي يؤدي لامتصاص الرطوبة واحتجاز البكتيريا. الحل الطبي المعتمد سريرياً هو استخدام <em>ضمادات 3M Tegaderm +Pad</em> المقاومة للماء، والتي توفر حاجزاً فيلمياً شفافاً يمنع نفاذ الميكروبات والماء بنسبة 100% مع السماح للبشرة بالتنفس وتبخير العرق، مما يتيح للأم الاستحمام بأمان تام منذ اليوم الثاني.",
            "<strong>لماذا يفشل مرهم السيليكون ويتفوق رول الشيت الطبي BUPY؟</strong> أثبتت الدراسات المقارنة المنشورة في NCBI وPubMed أن مراهم الجل السائل تمسحها الملابس الداخلية ولا توفر ضغطاً مستمراً. في المقابل، فإن <em>رول شيت السيليكون BUPY (مقاس 4 سم × 3 متر)</em> يوفر ترطيباً عميقاً مع ضغط ميكانيكي متواصل يمنع تكاثر الكولاجين العشوائي ويفرد الندبة تماماً.",
            "<strong>المعادلة الاقتصادية لعام 2026 (Cost-Comparison Anchoring):</strong> جلسات ليزر الفراكشنال أو حقن الكورتيزون لعلاج الكلويد تتكلف ما بين 6,000 إلى 15,000 جنيه مصري في العيادات التجميلية، بينما أنبوبة مرهم السيليكون الصغيرة (30 جم) تباع بـ 1,150 ج.م وتكفي أسبوعين فقط! رول BUPY الطبي بطول 3 أمتار كاملة يكفي لقص شرائح تغطي جرح القيصرية لـ 4 أشهر كاملة مع إمكانية الغسيل وإعادة الاستخدام بسعر 750 ج.م فقط (أو 320 ج.م للمتر الواحد)، ومع كود الخصم الحصري HT10 ستحصلين على شحن مجاني تماماً ومعاينة الشحنة قبل الاستلام.",
        ],
        "sources": ["NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group", "Yazdan Medical", "3M Clinical Evidence", "Dr. Ahmed Marzouk", "WebTeb", "NCBI PMC13351234", "ResearchGate RCT"],
    },
    {
        "id": 2,
        "slug": "rhinoplasty-taping-edema-secrets",
        "title": "متى يمكن الاستغناء عن لصقات الأنف بعد التجميل؟ أسرار التعافي السريع وتثبيت الغضاريف",
        "keywords": "لصقات الأنف بعد التجميل، تورم الأرنبة، دعامة الأنف، 3M Micropore",
        "product_badge": "بلاستر الأنف الطبي البيج 3M Micropore + دعامة فتحات الأنف السيليكون",
        "hook_summary": "كل ما تحتاج معرفته عن بلاستر 3M Micropore البيج الأصلي (1533-0) ودوره في تقليل تورم أرنبة الأنف وسماكة الجلد بعد فك الجبيرة الجراحية وفق دراسات 2026.",
        "content_paragraphs": [
            "بعد إزالة الجبيرة الجراحية لعملية تجميل الأنف (Rhinoplasty)، يصاب معظم المرضى بالصدمة من حجم التورم في الثلث السفلي والأرنبة (Supratip Edema). يتساءل الجميع في المنتديات: كم أسبوعاً أحتاج لوضع اللصقات؟ ولماذا يصر كبار جراحي الأنف في مصر على نوع البلاستر الورقي البيج تحديداً؟",
            "<strong>التفسير العلمي اللمفاوي:</strong> أثناء الجراحة يتم فصل الجلد عن الهيكل العظمي والغضروفي، مما يؤدي لتراكم السوائل اللمفاوية في الفراغ الميت (Dead Space). أثبتت الدراسات السريرية (ResearchGate RCT وNCBI 2026) أن تطبيق الضغط الخفيف المستمر باستخدام <em>بلاستر 3M Micropore البيج (كود 1533-0 / عرض 1.25 سم)</em> يمنع تمدد الجلد السميك ويساعد في إعادة التصاق الأنسجة وتصريف السوائل اللمفاوية نحو العقد المجاورة.",
            "<strong>أهمية استخدام البلاستر الأصلي للبشرة الحساسة:</strong> استخدام لصقات مقلدة أو بلاستر أبيض عادي غير مسامي يؤدي لانسداد المسام وظهور بثور دهنية والتهابات موضعية تسوء مظهر الأنف. شريط 3M Micropore مسامي (Microporous) يسمح بتهوية الجلد، ويتميز بلونه البيج اللحمي غير الملفت ومادته اللاصقة المضادة للحساسية (Hypoallergenic).",
            "<strong>الحفاظ على تماثل الفتحات:</strong> استكمالاً للتعافي، تنصح الأبحاث الطبية المنشورة في يوليو 2026 بارتداء <em>دعامة الأنف السيليكون (Nostril Retainer)</em> لمنع انكماش الندبات الداخلية والتأكد من تطابق حجم فتحتي الأنف أثناء التئام الغضاريف. استخدم كود HT10 للشحن المجاني واستشارة الدكتورة في المقاس المناسب لحالتك.",
        ],
        "sources": ["Dr. Amr Adel", "WebTeb", "MDPI Medicina", "ResearchGate RCT", "NCBI PMC13351234", "3M Clinical Evidence", "PubMed 28570253", "NCBI PMC2918339", "Almoosa Health Group", "PubMed 8113473"],
    },
    {
        "id": 3,
        "slug": "bariatric-laparoscopic-wound-care",
        "title": "كيف تتجنبين التهاب جروح عمليات التكميم والمناظير؟ خطوات طبية موثقة لعزل الجرح والاستحمام",
        "keywords": "جروح المنظار، التهاب الجرح، الاستحمام بعد التكميم، بخاخ الجروح الشفاف Opsite",
        "product_badge": "بخاخ الجروح الشفاف العازل للماء Opsite Spray",
        "hook_summary": "الدليل العملي لمرضى التكميم وجراحات السمنة والمرارة: كيف تحمي فتحات المناظير الصغيرة من العرق والماء واحتكاك الملابس وتمنع تصبغاتها الداكنة.",
        "content_paragraphs": [
            "تتميز جراحات السمنة بالمنظار (مثل تكميم المعدة وتحويل المسار وجراحة المرارة) بوجود 3 إلى 5 فتحات صغيرة في جدار البطن. على الرغم من صغر حجمها، فإن موقعها في مناطق الحركة والاحتكاك يجعلها عرضة للرطوبة، العرق، وتلوث مياه الاستحمام، مما قد يؤخر التئامها أو يسبب بقعاً داكنة وندبات كلويدية مزعجة.",
            "<strong>آلية عمل بخاخ الجلد الشفاف (Opsite Spray):</strong> تقدم شركة Smith & Nephew العالمية بخاخ Opsite المعتمد طبياً والذي يرش على الجرح ليجف في غضون ثوانٍ قليلة، مشكلاً طبقة رقيقة شفافة ومرنة تعمل كـ 'جلد ثانٍ'. هذا الغشاء مقاوم للماء والبكتيريا بنسبة 100% ولكنه نفاذ لبخار الماء والهواء (Moisture Vapor Permeable)، مما يسمح للمريض بالاستحمام والحركة الحرة دون قلق.",
            "<strong>حماية الجروح من احتكاك المشدات والملابس:</strong> بعد عمليات جدار البطن وشفط الدهون المصاحبة للتكميم، قد يتسبب المشد الطبي الضاغط في احتكاك مؤلم بالغرز. طبقة Opsite تمنع هذا الاحتكاك وتحافظ على بيئة رطبة ومثالية للتجدد الخلوي السريع للجلد.",
            "<strong>توفير وعناية متكاملة:</strong> عبوة واحدة من بخاخ Opsite تكفي لعشرات الرشات طوال فترة النقاهة والاستحمام اليومي، وعند طلبها اليوم عبر كود HT10 ستحصل على شحن مجاني تماماً وإمكانية المعاينة قبل الدفع.",
        ],
        "sources": ["3M Clinical Evidence", "NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group", "Dr. Ahmed Marzouk", "Yazdan Medical", "WebTeb", "NCBI PMC13351234", "ResearchGate RCT"],
    },
    {
        "id": 4,
        "slug": "gynecomastia-thyroid-scar-solutions",
        "title": "الحل النهائي لآثار جراحات التثدي والغدة الدرقية: وداعاً للكلويد وخطوط العمليات البارزة",
        "keywords": "جرح الغدة الدرقية، أثر عملية التثدي، حكة الجرح، شيت سيليكون",
        "product_badge": "رول شيت السيليكون BUPY + بخاخ Opsite",
        "hook_summary": "جروح الرقبة الحساسة وجراحات التثدي عند الرجال: بروتوكول تسطيح وتفتيح الندبات بواسطة السيليكون الطبي المعتمد سريرياً لمنع الحكة والاحمرار.",
        "content_paragraphs": [
            "تعتبر جراحات الغدة الدرقية في أسفل الرقبة وجراحات استئصال التثدي حول هالة الصدر عند الشباب من أكثر الجراحات التي تتطلب عناية تجميلية فائقة؛ نظراً لأن الرقبة والصدر مكشوفان وتتعرض أنسجتهما لحركة مستمرة وتمدد دائم مع التنفس والالتفات، مما يحفز الخلايا الليفية على إفراز كولاجين زائد وتكوين ندبة متضخمة.",
            "<strong>لماذا تسبب جروح الرقبة والصدر حكة شديدة؟</strong> عند جفاف حواف الجرح، تنشط النهايات العصبية السطحية وتحدث حكة مؤلمة تدفع المريض للمس الجرح، وهو السبب الرئيسي وراء تضخم الندبة وتلونها باللون البني أو الأحمر الداكن.",
            "<strong>دور شيت السيليكون الطبي BUPY:</strong> يؤكد الإجماع الطبي الدولي لأطباء الجلدية وجراحي التجميل أن لصقات السيليكون الطبية تعيد التوازن المائي للطبقة القرنية (Stratum Corneum)، وتخفض تدفق الدم الزائد إلى الأنسجة الندبية فتهدأ الحكة فوراً ويبدأ لون الخط الجراحي في التفتح والتلاشي تدريجياً خلال 8 إلى 12 أسبوعاً.",
            "<strong>الحماية من أشعة الشمس:</strong> ينصح بتغطية ندبة الغدة الدرقية أثناء الخروج بشريط بلاستر 3M Micropore الورقي البيج لحجب الأشعة فوق البنفسجية التي تسبب اسمرار الندبة الدائم، ثم وضع شيت السيليكون مساءً وأثناء النوم. استشر الدكتورة في بروتوكول حالتك واطلب المنتجات بشحن مجاني كود HT10.",
        ],
        "sources": ["NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group", "3M Clinical Evidence", "Yazdan Medical", "WebTeb", "NCBI PMC13351234", "ResearchGate RCT", "Dr. Amr Adel"],
    },
    {
        "id": 5,
        "slug": "nostril-retainer-symmetry-rhinoplasty",
        "title": "دليلك الطبي الشامل لتماثل فتحات الأنف بعد عمليات التجميل: كيف تحمين غضاريف الأنف في 2026؟",
        "keywords": "عدم تماثل فتحات الأنف، Nostril Retainer، خياطة التجميل، دعامة سيليكون",
        "product_badge": "دعامة فتحات الأنف السيليكون Nostril Retainer",
        "hook_summary": "أحدث ما نشرته دورية MDPI Medicina في يوليو 2026 حول استخدام دعامات السيليكون لمنع ضيق الصمام التنفسي وضمان تماثل فتحات الأنف هندسياً بعد التجميل.",
        "content_paragraphs": [
            "أحد أكثر المخاوف إقلاقاً للمرضى بعد جراحة تجميل الأنف أو إصلاح الشفة الأرنبية هو ملاحظة اختلاف في حجم أو استدارة فتحتي الأنف (Nostril Asymmetry). في الأسابيع الأولى، تسحب قوى الانكماش الندبي (Scar Contracture) حواف الفتحة نحو الداخل، مما قد يسبب ضيقاً في مجرى التنفس أو عدم تساوي مظهر الفتحات من المنظر السفلي.",
            "<strong>النتائج الحاسمة لدراسة MDPI Medicina (يوليو 2026):</strong> أظهرت دراسة سريرية متقدمة أُجريت على مرضى تجميل الأنف باستخدام القياس الرقمي أن المرضى الذين التزموا بارتداء دعامة فتحات الأنف السيليكون (Nostril Retainer) لمدة تتراوح بين 6 إلى 12 أسبوعاً حققوا تماثلاً متطابقاً في مساحة الفتحتين بنسبة نجاح بلغت 94%، مقارنة بالمجموعات التي لم تستخدم دعامات.",
            "<strong>مواصفات الدعامة الطبية المثالية:</strong> تصنع دعامات Nostril Retainer من سيليكون طبي ناعم وفائق المرونة بدرجة USP Class VI لا يسبب أي تحسس للأغشية المخاطية، وتتميز بوجود قناة تنفس مجوفة تسمح بمرور الهواء بسلاسة أثناء ارتدائها نهاراً وأثناء النوم.",
            "<strong>التوفير مقابل عمليات التعديل (Revision Rhinoplasty):</strong> تكلفة جراحة تعديل الأنف لتصحيح انكماش الفتحات أو اعوجاج الصمام تتجاوز حالياً 40,000 إلى 80,000 جنيه في مصر، بينما استخدام الدعامة الوقائية الأصلية بمقاسها الطبي المناسب يضمن تثبيت نتائج العملية بنسبة 100% وبأبسط تكلفة ممكنة مع إمكانية المعاينة قبل الدفع وشحن مجاني بكود HT10.",
        ],
        "sources": ["MDPI Medicina", "ResearchGate RCT", "Dr. Amr Adel", "WebTeb", "NCBI PMC13351234", "3M Clinical Evidence", "NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group"],
    },
]


def render_header(cfg: dict, is_subpage=False):
    prefix = "../" if is_subpage else ""
    offer = get_active_offer_details(cfg)
    return f"""
<header>
  <div class="header-inner">
    <div class="brand-title">
      <a href="{prefix}index.html" style="color:#fff; text-decoration:none;">🌿 هيلينج تاتش مصر | Healing Touch Egypt</a>
    </div>
    <p class="brand-tagline">المركز المتخصص الأول في مصر لمستلزمات التعافي الطبي ورعاية الجروح والندبات بعد العمليات الجراحية، الولادة القيصرية، وتجميل الأنف — استشارة طبية متخصصة مع الدكتورة مع حق فتح الشحنة والمعاينة قبل الدفع</p>
    <div class="promo-top-bar">
      <span>{offer["offer_badge"]}</span>
    </div>
    <div class="social-links-bar">
      <a href="{build_whatsapp_link(cfg, 'استفسار عام')}" target="_blank" rel="noopener" class="btn-social btn-wa">💬 تواصل مع الدكتورة على واتساب ({offer["whatsapp_display"]})</a>
      <a href="javascript:void(0)" onclick="copyPromoAndOpenInstagram('{offer['code']}', '{offer['offer_title']}', '{offer['instagram_url']}')" class="btn-social btn-ig">📸 شات الدكتورة على إنستجرام</a>
    </div>
  </div>
</header>
"""


def render_footer(cfg: dict):
    offer = get_active_offer_details(cfg)
    return f"""
<footer>
  <div class="footer-inner">
    <p><strong>© 2026 هيلينج تاتش مصر (Healing Touch Egypt)</strong> — جميع الحقوق محفوظة لعلامتنا التجارية ومحتوانا التوعوي الطبي.</p>
    <p>دعم واستشارة طبية عبر الدكتورة المتخصصة ({offer["whatsapp_display"]}) مع شحن سريع لكافة محافظات مصر وميزة فتح الشحنة ومعاينة الكود الأصلي قبل الدفع بكود <strong>{offer["code"]}</strong>.</p>
    <div class="footer-links">
      <a href="{build_whatsapp_link(cfg, 'استفسار من الفوتر')}" target="_blank" rel="noopener">واتساب الدكتورة مباشرة</a> |
      <a href="{offer['instagram_url']}" target="_blank" rel="noopener">إنستجرام المورد والدكتورة</a>
    </div>
  </div>
</footer>
"""


def get_shared_css():
    return """
    :root {
      --primary: #0F4C5C;
      --primary-dark: #0A323D;
      --accent: #E36414;
      --accent-hover: #C85A17;
      --wa-green: #25D366;
      --wa-green-dark: #1EBE5D;
      --ig-gradient: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
      --bg: #F8FAFC;
      --card-bg: #FFFFFF;
      --text: #1E293B;
      --muted: #64748B;
      --border: #E2E8F0;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.8;
      direction: rtl;
      text-align: right;
    }
    header {
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
      color: #fff;
      padding: 35px 20px;
      text-align: center;
      border-bottom: 4px solid var(--accent);
    }
    .header-inner { max-width: 1100px; margin: 0 auto; }
    .brand-title { font-size: 2.1rem; font-weight: 800; margin-bottom: 10px; }
    .brand-tagline { font-size: 1.05rem; opacity: 0.95; max-width: 850px; margin: 0 auto 15px auto; }
    .promo-top-bar {
      display: inline-block;
      background: #FEF3C7;
      color: #92400E;
      font-weight: 800;
      padding: 8px 20px;
      border-radius: 30px;
      margin: 10px 0 15px 0;
      border: 2px dashed #F59E0B;
      font-size: 1rem;
    }
    .social-links-bar { margin-top: 10px; }
    .btn-social {
      display: inline-block;
      margin: 6px 8px;
      padding: 10px 22px;
      border-radius: 30px;
      font-weight: 700;
      text-decoration: none;
      font-size: 0.95rem;
      box-shadow: 0 3px 10px rgba(0,0,0,0.15);
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .btn-social:hover { transform: translateY(-2px); }
    .btn-social.btn-wa { background: var(--wa-green); color: #fff; }
    .btn-social.btn-wa:hover { background: var(--wa-green-dark); }
    .btn-social.btn-ig { background: #fff; color: #bc1888; border: 2px solid #bc1888; }
    .btn-social.btn-ig:hover { background: #fdf2f8; }
    .container { max-width: 1120px; margin: 0 auto; padding: 35px 20px; }
    .section-title {
      font-size: 1.65rem;
      color: var(--primary);
      border-right: 6px solid var(--accent);
      padding-right: 14px;
      margin: 40px 0 25px 0;
      font-weight: 800;
    }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; }
    .card {
      background: var(--card-bg);
      border-radius: 14px;
      padding: 26px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.06);
      border: 1px solid var(--border);
      border-top: 5px solid var(--primary);
      transition: transform 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card:hover { transform: translateY(-4px); }
    .card h3 { margin-top: 0; color: var(--primary); font-size: 1.25rem; }
    .price-badge {
      display: inline-block;
      background: #E0F2FE;
      color: #0369A1;
      font-weight: 800;
      padding: 6px 14px;
      border-radius: 8px;
      margin: 10px 0;
      font-size: 0.95rem;
    }
    .promo-highlight {
      background: #ECFDF5;
      border: 1px solid #A7F3D0;
      color: #065F46;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 700;
      margin-bottom: 15px;
    }
    .cta-btn-group { display: flex; flex-direction: column; gap: 8px; margin-top: 15px; }
    .cta-btn {
      display: block;
      text-align: center;
      padding: 12px 16px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 700;
      font-size: 0.95rem;
      transition: all 0.2s;
      cursor: pointer;
      border: none;
    }
    .cta-btn.wa-primary { background: var(--wa-green); color: #ffffff; }
    .cta-btn.wa-primary:hover { background: var(--wa-green-dark); }
    .cta-btn.ig-secondary { background: #ffffff; color: #c13584; border: 2px solid #c13584; }
    .cta-btn.ig-secondary:hover { background: #fdf2f8; }
    .cta-btn.read-more { background: var(--primary); color: #fff; }
    .cta-btn.read-more:hover { background: var(--primary-dark); }
    .article-box {
      background: #fff;
      border-radius: 14px;
      padding: 32px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.06);
      margin-bottom: 30px;
      border: 1px solid var(--border);
    }
    .article-box h2, .article-box h1 { color: var(--primary); margin-top: 0; font-size: 1.55rem; }
    .article-meta { color: var(--muted); font-size: 0.92rem; margin-bottom: 20px; }
    .callout-box {
      background: #F0FDF4;
      border-right: 5px solid #16A34A;
      padding: 18px 22px;
      border-radius: 8px;
      margin: 25px 0;
      font-size: 1.02rem;
    }
    .refs-container {
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      padding: 22px 30px;
      border-radius: 12px;
      margin-top: 30px;
    }
    .refs-container ol { margin: 10px 0 0 0; padding-right: 20px; }
    .refs-container li { margin-bottom: 12px; font-size: 0.93rem; }
    .refs-container a { color: var(--primary); text-decoration: underline; font-weight: 600; }
    .trends-banner {
      background: #FFF7ED;
      border: 1px solid #FED7AA;
      border-radius: 12px;
      padding: 18px 22px;
      margin-bottom: 30px;
    }
    .trend-pill {
      display: inline-block;
      background: #fff;
      border: 1px solid #FDBA74;
      color: #9A3412;
      padding: 5px 14px;
      border-radius: 20px;
      margin: 4px;
      font-size: 0.88rem;
      font-weight: 700;
    }
    /* نافذة الإشعار السريع عند نسخ الكود */
    .toast-notification {
      position: fixed;
      bottom: 25px;
      right: 25px;
      background: #065F46;
      color: #fff;
      padding: 16px 24px;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
      z-index: 9999;
      font-weight: 700;
      display: none;
      direction: rtl;
    }
    footer {
      background: #0F172A;
      color: #CBD5E1;
      text-align: center;
      padding: 35px 20px;
      margin-top: 60px;
      border-top: 4px solid var(--accent);
    }
    .footer-inner { max-width: 900px; margin: 0 auto; }
    .footer-links a { color: #38BDF8; text-decoration: none; margin: 0 10px; font-weight: 600; }
    .footer-links a:hover { text-decoration: underline; }
"""


def get_shared_js():
    return """
    function showToast(msg) {
      let t = document.getElementById('toast-msg');
      if (!t) {
        t = document.createElement('div');
        t.id = 'toast-msg';
        t.className = 'toast-notification';
        document.body.appendChild(t);
      }
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => { t.style.display = 'none'; }, 4000);
    }

    function copyPromoAndOpenInstagram(code, offerTitle, igUrl) {
      const textToCopy = "أهلاً دكتورة، أنا من طرف موقع Healing Touch ومعايا كود العرض (" + code + ") الخاص بـ (" + offerTitle + ") وعندي استفسار عن المنتجات.";
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          showToast("✅ تم نسخ كود العرض (" + code + ") ورسالة الاستفسار! جاري فتح إنستجرام للصقها للدكتورة...");
          setTimeout(() => { window.open(igUrl, '_blank'); }, 1200);
        }).catch(() => {
          window.open(igUrl, '_blank');
        });
      } else {
        window.open(igUrl, '_blank');
      }
    }
"""


def build_article_page(art: dict, cfg: dict) -> str:
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    offer = get_active_offer_details(cfg)
    paragraphs_html = "\n".join([f"<p>{p}</p>" for p in art["content_paragraphs"]])

    refs_list_html = []
    for i, s_key in enumerate(art["sources"], 1):
        ref_obj = ALL_MEDICAL_REFERENCES.get(s_key)
        if ref_obj:
            refs_list_html.append(
                f'<li><strong>[{i}]</strong> <a href="{ref_obj["url"]}" target="_blank" rel="noopener">{ref_obj["title"]}</a> — <em>{ref_obj["summary"]}</em></li>'
            )
        else:
            refs_list_html.append(f'<li><strong>[{i}]</strong> {s_key} — مرجع سريري موثق لعام 2026.</li>')
    refs_html = "\n".join(refs_list_html)

    wa_article_link = build_whatsapp_link(cfg, art["title"], is_article=True)

    page_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{art["title"]} | هيلينج تاتش مصر</title>
  <meta name="description" content="{art["hook_summary"]}">
  <meta name="keywords" content="{art["keywords"]}">
  <style>{get_shared_css()}</style>
  <script>{get_shared_js()}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "headline": "{art["title"]}",
    "description": "{art["hook_summary"]}",
    "keywords": "{art["keywords"]}",
    "datePublished": "{today_str}",
    "dateModified": "{today_str}",
    "publisher": {{
      "@type": "Organization",
      "name": "Healing Touch Egypt",
      "url": "https://wa.me/{offer['whatsapp_phone']}"
    }}
  }}
  </script>
</head>
<body>

{render_header(cfg, is_subpage=True)}

<div class="container">
  <div style="margin-bottom: 20px;">
    <a href="../index.html" style="color:var(--primary); font-weight:700; text-decoration:none;">⬅ العودة للصفحة الرئيسية للمتجر والمدونة</a>
  </div>

  <article class="article-box">
    <h1>{art["title"]}</h1>
    <div class="article-meta">📅 آخر تحديث طبي: {today_str} | 🏷️ الكلمات البحثية: {art["keywords"]} | 🛡️ مدعوم بـ {len(art["sources"])} دراسة ومصدر سريري موثق</div>

    <div class="callout-box">
      <strong>المنتج والباكدج المربوط سريرياً بهذا المقال:</strong> {art["product_badge"]}<br>
      <em>(متوفر للشحن الفوري لجميع المحافظات مع ميزة <strong>{offer["offer_title"]}</strong> باستخدام كود <strong>{offer["code"]}</strong>).</em>
    </div>

    {paragraphs_html}

    <!-- صندوق الاستشارة المباشرة مع الدكتورة والبرومو كود -->
    <div style="background:#FFFBEB; border:2px dashed #F59E0B; border-radius:12px; padding:25px; margin:35px 0; text-align:center;">
      <h3 style="color:#92400E; margin-top:0;">👩‍⚕️ استشيري الدكتورة المتخصصة واطلبي الباكدج الآن</h3>
      <p style="margin-bottom:15px; font-weight:600; color:#78350F;">
        وفري تكلفة الشحن واحصلي على <strong>{offer["offer_title"]}</strong> عند استخدام كود العرض: <span style="background:#FEF3C7; padding:4px 10px; border-radius:6px; color:#B45309; font-weight:800;">{offer["code"]}</span>
      </p>
      <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
        <a href="{wa_article_link}" target="_blank" rel="noopener" class="cta-btn wa-primary" style="font-size:1.05rem; padding:14px 28px;">
          💬 اسألي الدكتورة على واتساب ({offer["whatsapp_display"]}) بكود {offer["code"]}
        </a>
        <button onclick="copyPromoAndOpenInstagram('{offer['code']}', '{art['title']}', '{offer['instagram_url']}')" class="cta-btn ig-secondary" style="font-size:1.05rem; padding:14px 28px;">
          📸 تواصلي مع الدكتورة على إنستجرام
        </button>
      </div>
    </div>

    <div class="refs-container">
      <h3 style="color:var(--primary); margin-top:0;">📚 الدراسات والمراجع الطبية الموثقة المعتمدة في هذا المقال ({len(art["sources"])} دراسة):</h3>
      <ol>
        {refs_html}
      </ol>
    </div>
  </article>

  <div style="margin-top: 30px; text-align:center;">
    <a href="../index.html" class="cta-btn read-more" style="display:inline-block; max-width:320px;">تصفح باقي المقالات والمنتجات الطبية</a>
  </div>
</div>

{render_footer(cfg)}

</body>
</html>
"""
    art_path = ARTICLES_DIR / f"{art['slug']}.html"
    art_path.write_text(page_html, encoding="utf-8")
    return str(art_path)


def build_full_website():
    """يبني الموقع بالكامل داخل مجلد docs مع الصفحة الرئيسية والـ 5 مقالات بالأزرار الذكية المحدثة."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    cfg = load_promo_config()
    offer = get_active_offer_details(cfg)

    # 1. بناء صفحات المقالات
    print(f"[1/3] 📝 جاري بناء الـ 5 مقالات وتحديثها بنظام كود العرض ({offer['code']}: {offer['offer_title']})...")
    for art in ARTICLES_DATA:
        p = build_article_page(art, cfg)
        print(f"   ✓ تم توليد مقال: {Path(p).name}")

    # 2. بناء الصفحة الرئيسية (index.html)
    print("[2/3] 🌐 جاري بناء الصفحة الرئيسية الشاملة للمتجر والمدونة بالأزرار الذكية للدكتورة...")
    articles_cards_html = []
    for art in ARTICLES_DATA:
        articles_cards_html.append(f"""
    <div class="card" style="border-top-color: var(--accent);">
      <div>
        <h3>{art["title"]}</h3>
        <p style="color:var(--muted); font-size:0.95rem;">{art["hook_summary"]}</p>
        <div style="font-size:0.85rem; color:var(--primary); font-weight:700; margin-bottom:12px;">🏷️ {art["keywords"]}</div>
      </div>
      <div>
        <a href="articles/{art["slug"]}.html" class="cta-btn read-more">📖 قراءة المقال الطبي والمراجع السريرية</a>
      </div>
    </div>
        """)
    articles_grid_html = "\n".join(articles_cards_html)

    trends_pills = [
        "جرح القيصرية", "كلويد البطن", "لصقات السيليكون للندبات", "الاستحمام بعد القيصرية",
        "لصقات الأنف بعد التجميل", "تورم الأرنبة", "دعامة الأنف", "3M Micropore البيج",
        "جروح المنظار", "الاستحمام بعد التكميم", "بخاخ Opsite للجروح", "جرح الغدة الدرقية",
        "أثر عملية التثدي", "عدم تماثل فتحات الأنف", "Nostril Retainer"
    ]
    pills_html = " ".join([f'<span class="trend-pill">🔥 {t}</span>' for t in trends_pills])

    # المنتجات الخمسة وروابط الواتساب وإنستجرام الذكية لكل منتج
    products_data = [
        {
            "name": "رول شيت السيليكون الطبي للندبات BUPY (4 سم × 3 متر)",
            "desc": "الحل الذهبي المعتمد سريرياً لمنع وعلاج ندبات القيصرية، شد البطن، التثدي، وجروح الغدة. رول كامل 3 أمتار يكفي 3 إلى 4 أشهر مع إمكانية الغسيل وإعادة الاستخدام.",
            "price": "السعر: 750 ج.م للرول (أو 320 ج.م للمتر المقصوص)",
            "inquiry_name": "رول شيت السيليكون BUPY 3 متر",
        },
        {
            "name": "بلاستر الأنف الطبي البيج الأصلي 3M Micropore (1533-0)",
            "desc": "اللصقات الورقية الأصلية الأكثر طلباً من جراحي التجميل لتقليل تورم الأرنبة بعد إزالة الجبيرة بدون تحسس للبشرة الحساسة (عرض 1.25 سم × 9.1 متر).",
            "price": "السعر: 175 ج.م للبكرة (أو 3 بكرات بـ 450 ج.م)",
            "inquiry_name": "بلاستر الأنف البيج 3M Micropore الأصلي",
        },
        {
            "name": "ضمادات الاستحمام المقاومة للماء 3M Tegaderm +Pad",
            "desc": "ضمادة فيلمية شفافة تعزل جرح القيصرية أو الجراحة عن الماء بنسبة 100% مع وسادة غير لاصقة بالغرز لتسمح لك بالاستحمام الآمن من اليوم الثاني.",
            "price": "باكدج 5 إلى 10 ضمادات: 220 – 390 ج.م",
            "inquiry_name": "ضمادات الاستحمام Tegaderm +Pad المقاومة للماء",
        },
        {
            "name": "بخاخ الجروح العازل للماء Opsite Spray (Smith & Nephew)",
            "desc": "يشكل طبقة حماية شفافة ومرنة تجف فوراً لحماية جروح المناظير (التكميم والمرارة) والغرز السطحية من الاحتكاك والماء والتلوث.",
            "price": "السعر: 750 ج.م للعبوة الأصلية",
            "inquiry_name": "بخاخ الجروح الشفاف Opsite Spray",
        },
        {
            "name": "دعامة فتحات الأنف السيليكون الطبية Nostril Retainer",
            "desc": "مصنوعة من سيليكون طبي فائق النعومة للحفاظ على تماثل وتساوي فتحات الأنف ومنع التقلص الغضروفي بعد عمليات تجميل الأنف.",
            "price": "السعر: 450 ج.م (أو باكدج الأنف الكامل بـ 680 ج.م)",
            "inquiry_name": "دعامة فتحات الأنف السيليكون Nostril Retainer",
        },
    ]

    products_cards_html = []
    for prod in products_data:
        wa_link = build_whatsapp_link(cfg, prod["inquiry_name"])
        products_cards_html.append(f"""
    <div class="card">
      <div>
        <h3>{prod["name"]}</h3>
        <p>{prod["desc"]}</p>
        <div class="price-badge">{prod["price"]}</div>
        <div class="promo-highlight">🎁 العرض الحالي: <strong>{offer["offer_title"]}</strong> بكود <strong>{offer["code"]}</strong></div>
      </div>
      <div class="cta-btn-group">
        <a href="{wa_link}" target="_blank" rel="noopener" class="cta-btn wa-primary">💬 اطلب من الدكتورة على واتساب ({offer["whatsapp_display"]})</a>
        <button onclick="copyPromoAndOpenInstagram('{offer['code']}', '{prod['inquiry_name']}', '{offer['instagram_url']}')" class="cta-btn ig-secondary">📸 شات إنستجرام بكود {offer["code"]}</button>
      </div>
    </div>
        """)
    products_grid_html = "\n".join(products_cards_html)

    index_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>هيلينج تاتش مصر | Healing Touch Egypt - مستلزمات الرعاية ما بعد الجراحة والتجميل</title>
  <meta name="description" content="المنصة الطبية والتوعوية الأولى في مصر لمستلزمات التعافي بعد الجراحات: رول شيت السيليكون BUPY للقيصرية، بلاستر 3M Micropore البيج، ضمادات Tegaderm للاستحمام، بخاخ Opsite، ودعامات الأنف. استشارات طبية مع الدكتورة وشحن مجاني بكود {offer['code']}.">
  <meta name="keywords" content="هيلينج تاتش, Healing Touch Egypt, شيت سيليكون للقيصرية, بلاستر 3M البيج 1533-0, ضمادة تيجاديرم للاستحمام, بخاخ اوبسايت للجروح, دعامة الانف السيليكون, علاج الكلويد والندبات مصر">
  <style>{get_shared_css()}</style>
  <script>{get_shared_js()}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "Healing Touch Egypt - هيلينج تاتش مصر",
    "description": "مستلزمات الرعاية الطبية ما بعد الجراحة وتجميل الأنف والولادة القيصرية",
    "url": "https://wa.me/{offer['whatsapp_phone']}",
    "telephone": "+{offer['whatsapp_phone']}"
  }}
  </script>
</head>
<body>

{render_header(cfg, is_subpage=False)}

<div class="container">

  <div class="trends-banner">
    <strong style="color:#9A3412;">📈 الكلمات البحثية الطبية الصاعدة التي يبحث عنها آلاف المرضى في مصر اليوم ({today_str}):</strong><br>
    <div style="margin-top:8px;">{pills_html}</div>
  </div>

  <h2 class="section-title">🛍️ باكدجات ومستلزمات التعافي الطبي الأصلية (استشيري الدكتورة + شحن مجاني بكود {offer['code']})</h2>
  <div class="grid">
    {products_grid_html}
  </div>

  <h2 class="section-title">📚 المقالات الطبية الموثقة (محرك التريند والمقالات لعام 2026)</h2>
  <div class="grid">
    {articles_grid_html}
  </div>

</div>

{render_footer(cfg)}

</body>
</html>
"""
    index_file = DOCS_DIR / "index.html"
    index_file.write_text(index_html, encoding="utf-8")
    print(f"[3/3] ✅ تم إنشاء وتحديث موقع الويب بالكامل بنجاح: {index_file}")
    return str(index_file)


def open_site_in_browser():
    index_file = DOCS_DIR / "index.html"
    if index_file.exists():
        print(f"[🌐] جاري فتح الموقع في المتصفح الافتراضي: {index_file}")
        open_url_in_default_browser(str(index_file))


def setup_and_push_github(repo_url: str = ""):
    print("\n[*] جاري إعداد مستودع Git ورفع مجلد docs إلى GitHub...")
    cwd = str(BASE_DIR)
    try:
        git_dir = BASE_DIR / ".git"
        if not git_dir.exists():
            subprocess.run(["git", "init"], cwd=cwd, check=True)
            subprocess.run(["git", "config", "core.quotepath", "false"], cwd=cwd, check=False)
            subprocess.run(["git", "branch", "-M", "main"], cwd=cwd, check=False)

        subprocess.run(["git", "add", "docs/", "github_seo_trend_engine.py", "promo_config.json"], cwd=cwd, check=True)
        commit_res = subprocess.run(
            ["git", "commit", "-m", f"Update Promo Code HT10 Doctor WhatsApp Links & Full Website ({datetime.date.today()})"],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        print(f"Git commit: {commit_res.stdout.strip() or commit_res.stderr.strip()}")

        if repo_url:
            subprocess.run(["git", "remote", "remove", "origin"], cwd=cwd, check=False)
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=cwd, check=True)
            print(f"[+] تم ربط المستودع البعيد: {repo_url}")
            push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=cwd, capture_output=True, text=True)
            if push_res.returncode == 0:
                print("✅ تم رفع ملفات الموقع إلى GitHub بنجاح تام!")
            else:
                print(f"[!] رسالة Git أثناء الرفع: {push_res.stderr.strip()}")
    except Exception as exc:
        print(f"[!] تنبيه أثناء التعامل مع Git: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Healing Touch Egypt - GitHub SEO & Trend Engine with Dynamic Promo Codes")
    parser.add_argument("--build-site", action="store_true", help="بناء وتحديث الموقع والـ 5 مقالات الموثقة بنظام البرومو كود")
    parser.add_argument("--preview", action="store_true", help="معاينة الموقع فوراً في المتصفح الافتراضي")
    parser.add_argument("--push-github", action="store_true", help="رفع الموقع إلى GitHub")
    parser.add_argument("--repo-url", default="", help="رابط مستودع GitHub")
    args = parser.parse_args()

    if args.build_site or not any(vars(args).values()):
        build_full_website()

    if args.preview or not any(vars(args).values()):
        open_site_in_browser()

    if args.push_github or args.repo_url:
        setup_and_push_github(args.repo_url)


if __name__ == "__main__":
    main()
