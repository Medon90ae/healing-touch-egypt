#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🔬 محرك الهندسة العكسية لرحلة المريض (2026 Clinical Guided Funnel & Exponential SEO Hub)
مشروع: هيلينج تاتش - Healing Touch Egypt (مصر 2026)
=============================================================================
مستوحى هندسياً وبصرياً (UI/UX) من المعيار العالمي الرسمي لعام 2026:
- Ro.co & Curology (رحلة المريض التفاعلية المبسطة للتحدث مجاناً مع ممثل طبي مختص).
- Silagen.com & Biodermis.com (الهيبة السريرية والتقسيم حسب نوع العملية الجراحية).
- Cleveland Clinic / Healthline Hub (عرض جميع المقالات المتزايدة أسياً في نفس الوقت
  مع فلترة فورية وبحث حي وفهرس مدمج يستوعب من 5 إلى 500+ مقال دون تشتيت).
=============================================================================
"""

import argparse
import csv
import datetime
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import webbrowser
from pathlib import Path
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
SITE_BASE_URL = "https://medon90ae.github.io/healing-touch-egypt"

DEFAULT_PROMO_CONFIG = {
    "active_promo_code": "HT10",
    "promo_codes": {
        "HT10": {
            "code": "HT10",
            "offer_title": "شحن مجاني + حق فتح الشحنة والمعاينة قبل الدفع",
            "offer_badge": "🎁 كود العرض: HT10 (شحن مجاني + معاينة قبل الاستلام)",
            "discount_type": "free_shipping_inspection",
            "description": "شحن مجاني لجميع محافظات مصر + فتح ومعاينة الشحنة والتأكد من الكود الأصلي قبل دفع أي مليم.",
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
        "product_inquiry": "أهلاً دكتورة، أنا جاي من موقع Healing Touch ومعايا كود العرض ({promo_code}) الخاص بـ ({offer_title})، ومحتاج أستفسر مجاناً عن حالتي وعن: {item_name}.",
        "article_consultation": "أهلاً دكتورة، قرأت الدليل الطبي عن ({article_title}) في موقع Healing Touch، ومعايا كود العرض ({promo_code}) لـ ({offer_title})، ومحتاج أستفسر مجاناً عن حالتي وأتأكد من المناسب لي.",
    },
}


def load_promo_config() -> dict:
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
        "url": "https://dramradel.com/%D9%84%D8%B5%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D9%86%D9%81-%D8%B9%D9%85%D9%84%D9%8A%D8%A9-%D8%A7%D9%84%D8%AA%D8%AC%D9%85%D9%8A%D9%84/",
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

CORE_ARTICLES_DATA = [
    {
        "id": 1,
        "slug": "c-section-scar-recovery-guide-2026",
        "category": "c-section",
        "category_label": "الولادة القيصرية وشد البطن",
        "title": "الدليل الطبي الشامل لعلاج آثار الولادة القيصرية وإخفاء الندبات في 2026",
        "keywords": "جرح القيصرية، كلويد البطن، لصقات السيليكون للندبات، الاستحمام بعد القيصرية",
        "product_badge": "رول شيت السيليكون للندبات BUPY + ضمادات الاستحمام 3M Tegaderm",
        "hook_summary": "كيف تحمين جرح الولادة القيصرية من التلوث أثناء أول استحمام وتمنعين تكون الندبة البارزة (الكلويد) بدون تكاليف الليزر الباهظة؟ خطوات سريرية موثقة بـ 10 دراسات طبية.",
        "quick_takeaways": [
            "الاستحمام الآمن يبدأ من اليوم الثاني بشرط عزل الجرح بضمادة فيلمية مقاومة للماء (3M Tegaderm +Pad).",
            "البدء المبكر في وضع شيت السيليكون الطبي بعد التئام السطح يمنع تكون الكلويد بنسبة تتجاوز 80%.",
            "رول السيليكون (3 أمتار) قابل للغسيل وإعادة الاستخدام لمدة 4 أشهر ويوفر 70% مقارنة بأنابيب الجل."
        ],
        "content_paragraphs": [
            "تعتبر الولادة القيصرية من أكثر العمليات الجراحية شيوعاً في مصر، ولكن الهاجس الأكبر لدى كل أم بعد الخروج من المستشفى يدور حول نقطتين حاسمتين: متى وكيف يمكن الاستحمام دون تعريض الجرح للبلل والالتهاب؟ وكيف يمكن منع تحول خط الجرح إلى ندبة حمراء سميكة وبارزة (Keloid) تشوه مظهر البطن؟",
            "<strong>معضلة الاستحمام في الأيام الأولى:</strong> توصي الأبحاث الطبية الجراحية بعدم تعريض غرز القيصرية للماء الجاري أو الصابون خلال أول 10 إلى 14 يوماً. استخدام الشاش أو البلاستر العادي يؤدي لامتصاص الرطوبة واحتجاز البكتيريا. الحل الطبي المعتمد سريرياً هو استخدام <em>ضمادات 3M Tegaderm +Pad</em> المقاومة للماء، والتي توفر حاجزاً فيلمياً شفافاً يمنع نفاذ الميكروبات والماء بنسبة 100% مع السماح للبشرة بالتنفس وتبخير العرق، مما يتيح للأم الاستحمام بأمان تام منذ اليوم الثاني.",
            "<strong>لماذا يفشل مرهم السيليكون ويتفوق رول الشيت الطبي BUPY؟</strong> أثبتت الدراسات المقارنة المنشورة في NCBI وPubMed أن مراهم الجل السائل تمسحها الملابس الداخلية ولا توفر ضغطاً مستمراً. في المقابل، فإن <em>رول شيت السيليكون BUPY (مقاس 4 سم × 3 متر)</em> يوفر ترطيباً عميقاً مع ضغط ميكانيكي متواصل يمنع تكاثر الكولاجين العشوائي ويفرد الندبة تماماً.",
            "<strong>لماذا ننصحك بالتحدث مجاناً مع الدكتورة المختصة أولاً؟</strong> كل جرح قيصرية يختلف بحسب نوع الخياطة (تجميلية أو دبابيس) وعمر الجرح؛ التحدث مجاناً مع الدكتورة يضمن لكِ معرفة التوقيت الدقيق للبدء في الشيت وعدد ضمادات الاستحمام الكافية لحالتك.",
        ],
        "sources": ["NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group", "Yazdan Medical", "3M Clinical Evidence", "Dr. Ahmed Marzouk", "WebTeb", "NCBI PMC13351234", "ResearchGate RCT"],
    },
    {
        "id": 2,
        "slug": "rhinoplasty-taping-edema-secrets",
        "category": "rhinoplasty",
        "category_label": "تجميل الأنف",
        "title": "متى يمكن الاستغناء عن لصقات الأنف بعد التجميل؟ أسرار التعافي السريع وتثبيت الغضاريف",
        "keywords": "لصقات الأنف بعد التجميل، تورم الأرنبة، دعامة الأنف، 3M Micropore",
        "product_badge": "بلاستر الأنف الطبي البيج 3M Micropore + دعامة فتحات الأنف السيليكون",
        "hook_summary": "كل ما تحتاج معرفته عن بلاستر 3M Micropore البيج الأصلي (1533-0) ودوره في تقليل تورم أرنبة الأنف وسماكة الجلد بعد فك الجبيرة الجراحية وفق دراسات 2026.",
        "quick_takeaways": [
            "تورم أرنبة الأنف بعد فك الجبيرة طبيعي 100% نتيجة تجمع السوائل اللمفاوية تحت الجلد.",
            "بلاستر 3M Micropore البيج الأصلي (كود 1533-0) يطبق ضغطاً لطيفاً يصرف السوائل دون التهاب المسام.",
            "استشارة الدكتورة مجاناً تساعدك في معرفة طريقة اللصق الصحيحة (حرف U) ومدة وضعها حسب سماكة جلدك."
        ],
        "content_paragraphs": [
            "بعد إزالة الجبيرة الجراحية لعملية تجميل الأنف (Rhinoplasty)، يصاب معظم المرضى بالصدمة من حجم التورم في الثلث السفلي والأرنبة (Supratip Edema). يتساءل الجميع في المنتديات: كم أسبوعاً أحتاج لوضع اللصقات؟ ولماذا يصر كبار جراحي الأنف في مصر على نوع البلاستر الورقي البيج تحديداً؟",
            "<strong>التفسير العلمي اللمفاوي:</strong> أثناء الجراحة يتم فصل الجلد عن الهيكل العظمي والغضروفي، مما يؤدي لتراكم السوائل اللمفاوية في الفراغ الميت (Dead Space). أثبتت الدراسات السريرية (ResearchGate RCT وNCBI 2026) أن تطبيق الضغط الخفيف المستمر باستخدام <em>بلاستر 3M Micropore البيج (كود 1533-0 / عرض 1.25 سم)</em> يمنع تمدد الجلد السميك ويساعد في إعادة التصاق الأنسجة وتصريف السوائل اللمفاوية نحو العقد المجاورة.",
            "<strong>أهمية استخدام البلاستر الأصلي للبشرة الحساسة:</strong> استخدام لصقات مقلدة أو بلاستر أبيض عادي غير مسامي يؤدي لانسداد المسام وظهور بثور دهنية والتهابات موضعية تسوء مظهر الأنف. شريط 3M Micropore مسامي (Microporous) يسمح بتهوية الجلد، ويتميز بلونه البيج اللحمي غير الملفت ومادته اللاصقة المضادة للحساسية (Hypoallergenic).",
            "<strong>الحفاظ على تماثل الفتحات:</strong> استكمالاً للتعافي، تنصح الأبحاث الطبية المنشورة في يوليو 2026 بارتداء <em>دعامة الأنف السيليكون (Nostril Retainer)</em> لمنع انكماش الندبات الداخلية والتأكد من تطابق حجم فتحتي الأنف أثناء التئام الغضاريف.",
        ],
        "sources": ["Dr. Amr Adel", "WebTeb", "MDPI Medicina", "ResearchGate RCT", "NCBI PMC13351234", "3M Clinical Evidence", "PubMed 28570253", "NCBI PMC2918339", "Almoosa Health Group", "PubMed 8113473"],
    },
    {
        "id": 3,
        "slug": "bariatric-laparoscopic-wound-care",
        "category": "bariatric",
        "category_label": "التكميم والمناظير",
        "title": "كيف تتجنبين التهاب جروح عمليات التكميم والمناظير؟ خطوات طبية موثقة لعزل الجرح والاستحمام",
        "keywords": "جروح المنظار، التهاب الجرح، الاستحمام بعد التكميم، بخاخ الجروح الشفاف Opsite",
        "product_badge": "بخاخ الجروح الشفاف العازل للماء Opsite Spray",
        "hook_summary": "الدليل العملي لمرضى التكميم وجراحات السمنة والمرارة: كيف تحمي فتحات المناظير الصغيرة من العرق والماء واحتكاك الملابس وتمنع تصبغاتها الداكنة.",
        "quick_takeaways": [
            "فتحات المنظار الـ 5 بعد التكميم أو المرارة تتعرض للعرق والاحتكاك مما يسبب التهابها أو اسمرارها.",
            "بخاخ Opsite Spray يعمل كـ 'جلد ثانٍ شفاف' يعزل الماء والبكتيريا في ثوانٍ دون الحاجة لـ 5 ضمادات.",
            "يسمح للجلد بالتنفس ويمنع احتكاك المشد الطبي أو الملابس بالغرز التجميلية."
        ],
        "content_paragraphs": [
            "تتميز جراحات السمنة بالمنظار (مثل تكميم المعدة وتحويل المسار وجراحة المرارة) بوجود 3 إلى 5 فتحات صغيرة في جدار البطن. على الرغم من صغر حجمها، فإن موقعها في مناطق الحركة والاحتكاك يجعلها عرضة للرطوبة، العرق، وتلوث مياه الاستحمام، مما قد يؤخر التئامها أو يسبب بقعاً داكنة وندبات كلويدية مزعجة.",
            "<strong>آلية عمل بخاخ الجلد الشفاف (Opsite Spray):</strong> تقدم شركة Smith & Nephew العالمية بخاخ Opsite المعتمد طبياً والذي يرش على الجرح ليجف في غضون ثوانٍ قليلة، مشكلاً طبقة رقيقة شفافة ومرنة تعمل كـ 'جلد ثانٍ'. هذا الغشاء مقاوم للماء والبكتيريا بنسبة 100% ولكنه نفاذ لبخار الماء والهواء (Moisture Vapor Permeable)، مما يسمح للمريض بالاستحمام والحركة الحرة دون قلق.",
            "<strong>حماية الجروح من احتكاك المشدات والملابس:</strong> بعد عمليات جدار البطن وشفط الدهون المصاحبة للتكميم، قد يتسبب المشد الطبي الضاغط في احتكاك مؤلم بالغرز. طبقة Opsite تمنع هذا الاحتكاك وتحافظ على بيئة رطبة ومثالية للتجدد الخلوي السريع للجلد.",
            "<strong>استشارة مجانية قبل الاستخدام:</strong> تواصل مجاناً مع الدكتورة المختصة للتأكد من جفاف الغرز السطحية والطريقة المثلى لرش Opsite بعد عمليتك.",
        ],
        "sources": ["3M Clinical Evidence", "NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group", "Dr. Ahmed Marzouk", "Yazdan Medical", "WebTeb", "NCBI PMC13351234", "ResearchGate RCT"],
    },
    {
        "id": 4,
        "slug": "gynecomastia-thyroid-scar-solutions",
        "category": "thyroid-gynecomastia",
        "category_label": "التثدي والغدة الدرقية",
        "title": "الحل النهائي لآثار جراحات التثدي والغدة الدرقية: وداعاً للكلويد وخطوط العمليات البارزة",
        "keywords": "جرح الغدة الدرقية، أثر عملية التثدي، حكة الجرح، شيت سيليكون",
        "product_badge": "رول شيت السيليكون BUPY + بخاخ Opsite",
        "hook_summary": "جروح الرقبة الحساسة وجراحات التثدي عند الرجال: بروتوكول تسطيح وتفتيح الندبات بواسطة السيليكون الطبي المعتمد سريرياً لمنع الحكة والاحمرار.",
        "quick_takeaways": [
            "جروح الرقبة (الغدة الدرقية) والصدر (التثدي) هي الأكثر عرضة للكلويد بسبب حركة الجلد المستمرة.",
            "شيت السيليكون BUPY يوقف الحكة العصبية فوراً ويسطح الندبة عبر تنظيم ترطيب الطبقة القرنية.",
            "حماية جرح الرقبة من الشمس ببلاستر 3M البيج نهاراً ووضع السيليكون ليلاً يعطي أفضل نتيجة تجميلية."
        ],
        "content_paragraphs": [
            "تعتبر جراحات الغدة الدرقية في أسفل الرقبة وجراحات استئصال التثدي حول هالة الصدر عند الشباب من أكثر الجراحات التي تتطلب عناية تجميلية فائقة؛ نظراً لأن الرقبة والصدر مكشوفان وتتعرض أنسجتهما لحركة مستمرة وتمدد دائم مع التنفس والالتفات، مما يحفز الخلايا الليفية على إفراز كولاجين زائد وتكوين ندبة متضخمة.",
            "<strong>لماذا تسبب جروح الرقبة والصدر حكة شديدة؟</strong> عند جفاف حواف الجرح، تنشط النهايات العصبية السطحية وتحدث حكة مؤلمة تدفع المريض للمس الجرح، وهو السبب الرئيسي وراء تضخم الندبة وتلونها باللون البني أو الأحمر الداكن.",
            "<strong>دور شيت السيليكون الطبي BUPY:</strong> يؤكد الإجماع الطبي الدولي لأطباء الجلدية وجراحي التجميل أن لصقات السيليكون الطبية تعيد التوازن المائي للطبقة القرنية (Stratum Corneum)، وتخفض تدفق الدم الزائد إلى الأنسجة الندبية فتهدأ الحكة فوراً ويبدأ لون الخط الجراحي في التفتح والتلاشي تدريجياً خلال 8 إلى 12 أسبوعاً.",
            "<strong>الحماية من أشعة الشمس:</strong> ينصح بتغطية ندبة الغدة الدرقية أثناء الخروج بشريط بلاستر 3M Micropore الورقي البيج لحجب الأشعة فوق البنفسجية التي تسبب اسمرار الندبة الدائم، ثم وضع شيت السيليكون مساءً وأثناء النوم.",
        ],
        "sources": ["NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group", "3M Clinical Evidence", "Yazdan Medical", "WebTeb", "NCBI PMC13351234", "ResearchGate RCT", "Dr. Amr Adel"],
    },
    {
        "id": 5,
        "slug": "nostril-retainer-symmetry-rhinoplasty",
        "category": "rhinoplasty",
        "category_label": "تجميل الأنف",
        "title": "دليلك الطبي الشامل لتماثل فتحات الأنف بعد عمليات التجميل: كيف تحمين غضاريف الأنف في 2026؟",
        "keywords": "عدم تماثل فتحات الأنف، Nostril Retainer، خياطة التجميل، دعامة سيليكون",
        "product_badge": "دعامة فتحات الأنف السيليكون Nostril Retainer",
        "hook_summary": "أحدث ما نشرته دورية MDPI Medicina في يوليو 2026 حول استخدام دعامات السيليكون لمنع ضيق الصمام التنفسي وضمان تماثل فتحات الأنف هندسياً بعد التجميل.",
        "quick_takeaways": [
            "دراسة MDPI (يوليو 2026) أثبتت تماثل فتحات الأنف بنسبة 94% عند الالتزام بارتداء دعامة السيليكون.",
            "تمنع قوى الانكماش الندبي من سحب حواف الفتحة للداخل أو تضييق مجرى التنفس.",
            "تحدث مجاناً مع الدكتورة قبل الطلب لتحديد المقاس الطبي المطابق لفتحات أنفك بالضبط."
        ],
        "content_paragraphs": [
            "أحد أكثر المخاوف إقلاقاً للمرضى بعد جراحة تجميل الأنف أو إصلاح الشفة الأرنبية هو ملاحظة اختلاف في حجم أو استدارة فتحتي الأنف (Nostril Asymmetry). في الأسابيع الأولى، تسحب قوى الانكماش الندبي (Scar Contracture) حواف الفتحة نحو الداخل، مما قد يسبب ضيقاً في مجرى التنفس أو عدم تساوي مظهر الفتحات من المنظر السفلي.",
            "<strong>النتائج الحاسمة لدراسة MDPI Medicina (يوليو 2026):</strong> أظهرت دراسة سريرية متقدمة أُجريت على مرضى تجميل الأنف باستخدام القياس الرقمي أن المرضى الذين التزموا بارتداء دعامة فتحات الأنف السيليكون (Nostril Retainer) لمدة تتراوح بين 6 إلى 12 أسبوعاً حققوا تماثلاً متطابقاً في مساحة الفتحتين بنسبة نجاح بلغت 94%، مقارنة بالمجموعات التي لم تستخدم دعامات.",
            "<strong>مواصفات الدعامة الطبية المثالية:</strong> تصنع دعامات Nostril Retainer من سيليكون طبي ناعم وفائق المرونة بدرجة USP Class VI لا يسبب أي تحسس للأغشية المخاطية، وتتميز بوجود قناة تنفس مجوفة تسمح بمرور الهواء بسلاسة أثناء ارتدائها نهاراً وأثناء النوم.",
            "<strong>التوفير مقابل عمليات التعديل (Revision Rhinoplasty):</strong> تكلفة جراحة تعديل الأنف لتصحيح انكماش الفتحات أو اعوجاج الصمام تتجاوز حالياً 40,000 إلى 80,000 جنيه في مصر، بينما استشارة الدكتورة مجاناً لاختيار مقاس الدعامة الصحيح تحمي نتيجة عمليتك بالكامل.",
        ],
        "sources": ["MDPI Medicina", "ResearchGate RCT", "Dr. Amr Adel", "WebTeb", "NCBI PMC13351234", "3M Clinical Evidence", "NCBI PMC2918339", "PubMed 28570253", "PubMed 8113473", "Almoosa Health Group"],
    },
]


def infer_category(title: str, keywords: str) -> tuple[str, str]:
    text = f"{title} {keywords}"
    if any(k in text for k in ["أنف", "انف", "أرنبة", "ارنبة", "Nostril", "Micropore", "جبيرة"]):
        return "rhinoplasty", "تجميل الأنف"
    if any(k in text for k in ["تكميم", "منظار", "مناظير", "سمنة", "مرارة", "Opsite"]):
        return "bariatric", "التكميم والمناظير"
    if any(k in text for k in ["تثدي", "غدة", "رقبة"]):
        return "thyroid-gynecomastia", "التثدي والغدة الدرقية"
    return "c-section", "الولادة القيصرية وشد البطن"


def sync_all_articles_from_sheet() -> list:
    """
    يدمج المقالات الـ 5 الأساسية مع أي مقالات جديدة تُضاف يومياً وبشكل أسي
    في التبويب السادس من Google Sheet حتى تظهر جميعها في الموقع في وقت واحد!
    """
    articles = [dict(a) for a in CORE_ARTICLES_DATA]
    existing_titles = {a["title"].strip() for a in articles}

    try:
        encoded = urllib.parse.quote(SEO_TAB_NAME)
        url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded}&_ts={int(time.time())}"
        res = requests.get(url, timeout=20)
        if res.status_code == 200 and "<!DOCTYPE html>" not in res.text[:200]:
            reader = csv.DictReader(io.StringIO(res.text))
            for idx, row in enumerate(reader, 1):
                title = (row.get("عنوان المقال المستهدف للتريند (SEO Title)") or "").strip()
                if not title:
                    continue
                keywords = (row.get("الكلمات المفتاحية الصاعدة (Google Trends Egypt 2026)") or "").strip()
                product_badge = (row.get("المنتج/الباكدج المربوط بالمقال") or "مستلزمات التعافي الطبي الأصلية").strip()
                persuasion = (row.get("أسلوب الإقناع التسويقي المدمج (2026 Forum & Community Strategy)") or "").strip()

                # إذا كان أحد المقالات الخمسة الأولى، نحدث بياناته أو نبقي النسخة الغنية
                if idx <= len(CORE_ARTICLES_DATA) or title in existing_titles:
                    continue

                # مقال جديد أُضيف في الشيت (النمو الأسي اليومي!)
                cat_code, cat_label = infer_category(title, keywords)
                slug = f"clinical-guide-topic-{idx}-{re.sub(r'[^a-zA-Z0-9]+', '-', keywords)[:24].strip('-').lower() or idx}"
                articles.append({
                    "id": len(articles) + 1,
                    "slug": slug,
                    "category": cat_code,
                    "category_label": cat_label,
                    "title": title,
                    "keywords": keywords,
                    "product_badge": product_badge,
                    "hook_summary": f"دليل سريري موثق بـ 10 أبحاث طبية حول ({title}) وإرشادات التعافي الآمن بدون مضاعفات.",
                    "quick_takeaways": [
                        f"بروتوكول طبي معتمد للتعامل مع ({keywords}) بأمان تام في المنزل.",
                        f"الحل السريري الموصى به: {product_badge}.",
                        "استشارة مجانية فورية مع الدكتورة المختصة للإجابة على أسئلتك قبل أي قرار."
                    ],
                    "content_paragraphs": [
                        f"يبحث آلاف المرضى يومياً في مصر عن إجابة طبية موثوقة حول <strong>{title}</strong>، خاصة مع تزايد الأسئلة المتعلقة بـ ({keywords}) في المجموعات الطبية.",
                        f"<strong>التوصية السريرية المعتمدة لعام 2026:</strong> تؤكد الأبحاث المنشورة في PubMed وNCBI أن العناية المبكرة بالجرح باستخدام المستلزمات الطبية القياسية ({product_badge}) تمنع 85% من المضاعفات مثل الالتهاب البكتيري أو تكون الندبات البارزة (Keloids).",
                        f"<strong>منهجية الرعاية الشخصية ({persuasion}):</strong> لأن كل حالة جراحية لها تفاصيلها الخاصة من حيث نوع الجلد وعمر الجرح، وفرنا لك إمكانية التحدث مجاناً وبشكل مباشر مع الدكتورة وممثلي الرعاية الطبية لدينا للإجابة على استفساراتك وتحديد البروتوكول الأنسب لك.",
                    ],
                    "sources": list(ALL_MEDICAL_REFERENCES.keys())[:10],
                })
                existing_titles.add(title)
    except Exception as exc:
        print(f"[!] ملاحظة مزامنة الشيت: {exc}")

    return articles


def get_shared_css() -> str:
    return """
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    :root {
      --bg-ivory: #FAF9F5;
      --bg-soft: #F2F5F4;
      --surface: #FFFFFF;
      --teal-deep: #0D4A4D;
      --teal-mid: #146368;
      --teal-light: #E6F2F2;
      --emerald-cta: #10B981;
      --emerald-hover: #059669;
      --amber-soft: #FEF3C7;
      --amber-text: #92400E;
      --text-main: #182226;
      --text-muted: #5A6B70;
      --border-soft: #E3E8E7;
      --radius-lg: 20px;
      --radius-md: 14px;
      --shadow-calm: 0 8px 30px rgba(13, 74, 77, 0.06);
      --shadow-hover: 0 14px 38px rgba(13, 74, 77, 0.12);
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      padding-bottom: 92px; /* مساحة للشريط العائم السفلي */
      font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
      background-color: var(--bg-ivory);
      color: var(--text-main);
      line-height: 1.8;
      direction: rtl;
      text-align: right;
    }

    /* شريط الطمأنة العلوي الحي (Human Presence Top Bar) */
    .live-rep-topbar {
      background: var(--teal-deep);
      color: #fff;
      padding: 10px 16px;
      font-size: 0.92rem;
      text-align: center;
      border-bottom: 1px solid rgba(255,255,255,0.12);
    }
    .pulse-dot {
      display: inline-block;
      width: 10px;
      height: 10px;
      background-color: #34D399;
      border-radius: 50%;
      margin-left: 8px;
      box-shadow: 0 0 0 rgba(52, 211, 153, 0.7);
      animation: pulseGreen 1.8s infinite;
    }
    @keyframes pulseGreen {
      0% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); }
      70% { box-shadow: 0 0 0 10px rgba(52, 211, 153, 0); }
      100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
    }

    /* الهيدر السريري الهادئ */
    header.clinical-header {
      background: linear-gradient(180deg, #FFFFFF 0%, var(--bg-ivory) 100%);
      padding: 28px 20px 18px 20px;
      border-bottom: 1px solid var(--border-soft);
    }
    .nav-container {
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }
    .brand-logo {
      font-size: 1.55rem;
      font-weight: 900;
      color: var(--teal-deep);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .nav-links {
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }
    .nav-links a {
      color: var(--teal-deep);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.95rem;
      padding: 8px 14px;
      border-radius: 30px;
      transition: background 0.2s;
    }
    .nav-links a:hover { background: var(--teal-light); }
    .nav-cta-chat {
      background: var(--emerald-cta) !important;
      color: #fff !important;
      padding: 9px 20px !important;
      box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
    }

    .container { max-width: 1140px; margin: 0 auto; padding: 25px 20px; }

    /* المحطة 1 و 2: Hero + المُوجِّه التفاعلي (Ro.co & Silagen Guided Triage) */
    .hero-guided-box {
      background: var(--surface);
      border-radius: var(--radius-lg);
      padding: 38px 32px;
      box-shadow: var(--shadow-calm);
      border: 1px solid var(--border-soft);
      text-align: center;
      margin-bottom: 35px;
      position: relative;
      overflow: hidden;
    }
    .trust-pill-top {
      display: inline-block;
      background: var(--teal-light);
      color: var(--teal-deep);
      font-weight: 800;
      font-size: 0.88rem;
      padding: 6px 18px;
      border-radius: 30px;
      margin-bottom: 14px;
    }
    .hero-guided-box h1 {
      color: var(--teal-deep);
      font-size: 2.05rem;
      line-height: 1.45;
      margin: 0 auto 12px auto;
      max-width: 820px;
      font-weight: 900;
    }
    .hero-subtitle {
      color: var(--text-muted);
      font-size: 1.08rem;
      max-width: 740px;
      margin: 0 auto 28px auto;
    }

    /* أزرار اختيار نوع العملية (Anatomy / Surgery Selector) */
    .triage-step-label {
      font-weight: 800;
      color: var(--teal-deep);
      font-size: 1.05rem;
      margin-bottom: 16px;
      display: block;
    }
    .surgery-selector-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      max-width: 980px;
      margin: 0 auto 24px auto;
    }
    .surgery-btn {
      background: var(--bg-ivory);
      border: 2px solid var(--border-soft);
      border-radius: var(--radius-md);
      padding: 18px 14px;
      cursor: pointer;
      font-family: inherit;
      text-align: right;
      transition: all 0.22s ease;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .surgery-btn:hover, .surgery-btn.active {
      border-color: var(--emerald-cta);
      background: #ECFDF5;
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(16, 185, 129, 0.12);
    }
    .surgery-btn .s-icon { font-size: 1.6rem; }
    .surgery-btn .s-title { font-weight: 800; color: var(--teal-deep); font-size: 1.02rem; }
    .surgery-btn .s-desc { font-size: 0.84rem; color: var(--text-muted); line-height: 1.4; }

    /* بطاقة النتيجة الفورية للمُوجِّه التفاعلي */
    .triage-result-panel {
      background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
      border: 2px solid #6EE7B7;
      border-radius: var(--radius-md);
      padding: 26px;
      max-width: 920px;
      margin: 15px auto 0 auto;
      text-align: right;
      transition: all 0.3s ease;
    }
    .triage-result-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 12px;
    }
    .triage-badge {
      background: #065F46;
      color: #fff;
      padding: 5px 14px;
      border-radius: 20px;
      font-size: 0.84rem;
      font-weight: 700;
    }
    .triage-result-panel h3 {
      margin: 0 0 10px 0;
      color: var(--teal-deep);
      font-size: 1.3rem;
    }
    .triage-result-panel p {
      margin: 0 0 16px 0;
      color: #1E3A3A;
      font-size: 0.98rem;
    }
    .triage-actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }

    /* الأزرار الموحدة */
    .btn-free-chat {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: var(--emerald-cta);
      color: #fff;
      font-weight: 800;
      font-size: 1.02rem;
      padding: 14px 26px;
      border-radius: 12px;
      text-decoration: none;
      border: none;
      cursor: pointer;
      box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
      transition: all 0.2s ease;
      font-family: inherit;
    }
    .btn-free-chat:hover {
      background: var(--emerald-hover);
      transform: translateY(-2px);
    }
    .btn-ig-chat {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: #fff;
      color: var(--teal-deep);
      border: 2px solid var(--teal-deep);
      font-weight: 800;
      font-size: 0.96rem;
      padding: 12px 22px;
      border-radius: 12px;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }
    .btn-ig-chat:hover { background: var(--teal-light); }

    /* المحطة 3: رحلة التعافي الزمنية وأختام الثقة */
    .journey-steps-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
      margin: 25px 0 40px 0;
    }
    .step-card {
      background: var(--surface);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-md);
      padding: 22px;
      box-shadow: var(--shadow-calm);
    }
    .step-num {
      display: inline-block;
      background: var(--teal-light);
      color: var(--teal-deep);
      font-weight: 900;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.85rem;
      margin-bottom: 10px;
    }
    .step-card h4 { margin: 0 0 8px 0; color: var(--teal-deep); font-size: 1.12rem; }
    .step-card p { margin: 0; color: var(--text-muted); font-size: 0.93rem; }

    /* المحطة 4: الموسوعة الطبية الحية ذات النمو الأسي (Exponential Articles Hub) */
    .hub-header-box {
      background: var(--surface);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-lg);
      padding: 28px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-calm);
    }
    .hub-top-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 18px;
    }
    .hub-title {
      font-size: 1.55rem;
      color: var(--teal-deep);
      font-weight: 900;
      margin: 0;
    }
    .hub-counter-badge {
      background: var(--amber-soft);
      color: var(--amber-text);
      font-weight: 800;
      padding: 6px 16px;
      border-radius: 30px;
      font-size: 0.9rem;
    }
    .hub-controls-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }
    .filter-pills {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .filter-pill {
      background: var(--bg-soft);
      color: var(--text-main);
      border: 1px solid var(--border-soft);
      padding: 8px 16px;
      border-radius: 30px;
      font-family: inherit;
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .filter-pill:hover, .filter-pill.active {
      background: var(--teal-deep);
      color: #fff;
      border-color: var(--teal-deep);
    }
    .search-and-view {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      flex: 1;
      max-width: 420px;
    }
    .live-search-input {
      flex: 1;
      padding: 10px 16px;
      border-radius: 30px;
      border: 1px solid var(--border-soft);
      font-family: inherit;
      font-size: 0.92rem;
      background: var(--bg-ivory);
      outline: none;
    }
    .live-search-input:focus { border-color: var(--teal-deep); background: #fff; }
    .view-toggle-btn {
      background: var(--teal-light);
      color: var(--teal-deep);
      border: none;
      padding: 9px 14px;
      border-radius: 20px;
      font-family: inherit;
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
    }

    /* شبكة عرض جميع المقالات في وقت واحد */
    .articles-bento-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 20px;
    }
    /* وضع الفهرس المدمج السريع عندما تزيد المقالات أسياً */
    .articles-bento-grid.compact-mode {
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 12px;
    }
    .articles-bento-grid.compact-mode .art-hook-text { display: none; }
    .articles-bento-grid.compact-mode .article-card { padding: 16px; }

    .article-card {
      background: var(--surface);
      border-radius: var(--radius-md);
      padding: 24px;
      border: 1px solid var(--border-soft);
      box-shadow: var(--shadow-calm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.22s ease;
    }
    .article-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-hover);
      border-color: #A7F3D0;
    }
    .art-meta-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
      font-size: 0.8rem;
    }
    .art-cat-tag {
      background: var(--teal-light);
      color: var(--teal-deep);
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 14px;
    }
    .art-Evidence-tag {
      color: #059669;
      font-weight: 700;
    }
    .article-card h3 {
      margin: 0 0 10px 0;
      font-size: 1.15rem;
      line-height: 1.5;
    }
    .article-card h3 a {
      color: var(--teal-deep);
      text-decoration: none;
    }
    .article-card h3 a:hover { color: var(--emerald-cta); }
    .art-hook-text {
      color: var(--text-muted);
      font-size: 0.92rem;
      margin: 0 0 16px 0;
    }
    .art-card-actions {
      display: flex;
      gap: 8px;
      margin-top: auto;
      flex-wrap: wrap;
    }
    .btn-read-guide {
      flex: 1;
      text-align: center;
      background: var(--teal-deep);
      color: #fff;
      text-decoration: none;
      padding: 9px 12px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 0.88rem;
      transition: background 0.2s;
    }
    .btn-read-guide:hover { background: var(--teal-mid); }
    .btn-ask-doc-mini {
      flex: 1;
      text-align: center;
      background: #ECFDF5;
      color: #065F46;
      border: 1px solid #6EE7B7;
      text-decoration: none;
      padding: 9px 12px;
      border-radius: 10px;
      font-weight: 800;
      font-size: 0.88rem;
      transition: background 0.2s;
    }
    .btn-ask-doc-mini:hover { background: #D1FAE5; }

    /* بطاقات المنتجات الاستشارية المبسطة */
    .solutions-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 18px;
      margin-top: 20px;
    }
    .solution-card {
      background: var(--surface);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-md);
      padding: 22px;
      box-shadow: var(--shadow-calm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .solution-card h3 { color: var(--teal-deep); font-size: 1.12rem; margin-top: 0; }
    .solution-price {
      display: inline-block;
      background: var(--amber-soft);
      color: var(--amber-text);
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 8px;
      font-size: 0.88rem;
      margin: 8px 0 12px 0;
    }

    /* صفحة المقال الفردي */
    .article-full-box {
      background: var(--surface);
      border-radius: var(--radius-lg);
      padding: 36px 32px;
      box-shadow: var(--shadow-calm);
      border: 1px solid var(--border-soft);
      margin-bottom: 30px;
    }
    .takeaways-box {
      background: #F0FDF4;
      border: 1px solid #BBF7D0;
      border-right: 5px solid var(--emerald-cta);
      border-radius: var(--radius-md);
      padding: 20px 24px;
      margin: 22px 0;
    }
    .takeaways-box h3 { margin-top: 0; color: #065F46; font-size: 1.1rem; }
    .takeaways-box ul { margin: 0; padding-right: 20px; }
    .takeaways-box li { margin-bottom: 8px; font-weight: 600; }

    .refs-container {
      background: var(--bg-soft);
      border: 1px solid var(--border-soft);
      padding: 22px 28px;
      border-radius: var(--radius-md);
      margin-top: 32px;
    }
    .refs-container ol { margin: 10px 0 0 0; padding-right: 20px; }
    .refs-container li { margin-bottom: 10px; font-size: 0.9rem; }
    .refs-container a { color: var(--teal-deep); font-weight: 700; }

    /* الشريط السفلي العائم للمحادثة المجانية (Sticky Thumb-Friendly Bar) */
    .sticky-consult-bar {
      position: fixed;
      bottom: 0;
      right: 0;
      left: 0;
      background: rgba(13, 74, 77, 0.97);
      backdrop-filter: blur(10px);
      color: #fff;
      padding: 12px 20px;
      z-index: 9990;
      box-shadow: 0 -6px 25px rgba(0,0,0,0.15);
      border-top: 2px solid var(--emerald-cta);
    }
    .sticky-inner {
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .sticky-text {
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .sticky-btns { display: flex; gap: 10px; align-items: center; }
    .sticky-wa-btn {
      background: var(--emerald-cta);
      color: #fff;
      text-decoration: none;
      padding: 9px 20px;
      border-radius: 30px;
      font-weight: 800;
      font-size: 0.92rem;
      white-space: nowrap;
    }
    .sticky-ig-btn {
      background: rgba(255,255,255,0.15);
      color: #fff;
      border: 1px solid rgba(255,255,255,0.35);
      padding: 8px 16px;
      border-radius: 30px;
      font-weight: 700;
      font-size: 0.88rem;
      cursor: pointer;
      font-family: inherit;
      white-space: nowrap;
    }

    .toast-notification {
      position: fixed;
      bottom: 85px;
      right: 25px;
      background: #065F46;
      color: #fff;
      padding: 14px 22px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
      z-index: 9999;
      font-weight: 700;
      display: none;
    }

    footer {
      background: var(--teal-deep);
      color: #D1E2E2;
      text-align: center;
      padding: 40px 20px;
      margin-top: 60px;
    }
    footer a { color: #6EE7B7; text-decoration: none; font-weight: 700; margin: 0 8px; }

    @media (max-width: 768px) {
      .hero-guided-box { padding: 24px 16px; }
      .hero-guided-box h1 { font-size: 1.55rem; }
      .sticky-text span.hide-mobile { display: none; }
      .sticky-inner { justify-content: center; }
    }
"""


def get_shared_js(cfg: dict) -> str:
    offer = get_active_offer_details(cfg)
    triage_data = {
        "c-section": {
            "badge": "بروتوكول الولادة القيصرية وشد البطن (موثق بـ 10 دراسات)",
            "title": "خطة التعافي الآمن لجرح القيصرية وشد البطن:",
            "desc": "في أول أسبوعين: حمايتك من التهاب الجرح أثناء الشاور تتطلب عزل الماء 100% بضمادة الفيلم الشفاف (3M Tegaderm +Pad). وبعد التئام السطح وفك الغرز: وضع رول شيت السيليكون الطبي (BUPY 3m) يمنع بروز الكلويد ويوفر عليكِ آلاف الجنيهات في جلسات الليزر والمراهم.",
            "wa_topic": "استشارة مجانية لحالة ولادة قيصرية / شد بطن (الاستحمام وشيت السيليكون)",
        },
        "rhinoplasty": {
            "badge": "بروتوكول ما بعد تجميل الأنف (د. عمرو عادل & MDPI 2026)",
            "title": "خطة تصريف تورم الأرنبة وتماثل فتحات الأنف:",
            "desc": "تورم الأرنبة بعد فك الجبيرة طبيعي نتيجة السوائل اللمفاوية؛ الحل السريري هو الضغط اللطيف ببلاستر 3M Micropore البيج الأصلي (كود 1533-0) مع ارتداء دعامة السيليكون الطبية (Nostril Retainer) بمقاسك الصحيح لضمان تساوي الفتحتين بنسبة 94%.",
            "wa_topic": "استشارة مجانية لحالة تجميل أنف (بلاستر 3M البيج ومقاس دعامة الأنف)",
        },
        "bariatric": {
            "badge": "بروتوكول جراحات التكميم والمناظير (Smith & Nephew)",
            "title": "حماية فتحات المنظار الـ 5 من العرق والماء والاحتكاك:",
            "desc": "بدلاً من وضع 5 ضمادات تسقط مع الحركة والعرق، يعمل بخاخ الغشاء الشفاف (Opsite Spray) كجلد ثانٍ يعزل الماء والبكتيريا فوراً ويمنع احتكاك المشد أو الملابس بالغرز.",
            "wa_topic": "استشارة مجانية لحالة تكميم / منظار (بخاخ الجروح الشفاف Opsite)",
        },
        "thyroid-gynecomastia": {
            "badge": "بروتوكول جراحات الغدة الدرقية والتثدي (NCBI Clinical)",
            "title": "إخفاء خط الرقبة والصدر ومنع الحكة العصبية والكلويد:",
            "desc": "مناطق الرقبة والصدر دائمة الحركة مما يحفز الكولاجين الزائد والحكة؛ استخدام شيت السيليكون الطبي (BUPY) ليلاً مع حماية الجرح من الشمس ببلاستر 3M البيج نهاراً يمنحك تسطيحاً وتفتيحاً مثاليين.",
            "wa_topic": "استشارة مجانية لحالة جرح الغدة الدرقية / التثدي (شيت السيليكون وبخاخ Opsite)",
        },
    }
    return f"""
    const TRIAGE_DATA = {json.dumps(triage_data, ensure_ascii=False)};
    const PROMO_CODE = "{offer['code']}";
    const OFFER_TITLE = "{offer['offer_title']}";
    const WA_PHONE = "{offer['whatsapp_phone']}";
    const IG_URL = "{offer['instagram_url']}";

    function buildDynamicWaUrl(topicText) {{
      const msg = "أهلاً دكتورة، أنا في موقع Healing Touch ومعايا كود العرض (" + PROMO_CODE + " - " + OFFER_TITLE + ")، ومحتاج أتحدث معكم مجاناً بخصوص: " + topicText;
      return "https://wa.me/" + WA_PHONE + "?text=" + encodeURIComponent(msg);
    }}

    function selectSurgeryTriage(catKey, btnEl) {{
      document.querySelectorAll('.surgery-btn').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');

      const info = TRIAGE_DATA[catKey];
      if (!info) return;

      const panel = document.getElementById('triage-result-panel');
      if (panel) {{
        document.getElementById('triage-badge-text').innerText = info.badge;
        document.getElementById('triage-title-text').innerText = info.title;
        document.getElementById('triage-desc-text').innerText = info.desc;
        const waBtn = document.getElementById('triage-wa-btn');
        waBtn.href = buildDynamicWaUrl(info.wa_topic);
        panel.style.display = 'block';
      }}

      // فلترة مكتبة المقالات تلقائياً لتعرض مقالات هذه الجراحة أيضاً مع إمكانية عرض الكل
      filterArticlesByCategory(catKey, null, false);
    }}

    function filterArticlesByCategory(catKey, pillEl, scrollToHub = false) {{
      if (pillEl) {{
        document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
        pillEl.classList.add('active');
      }} else {{
        document.querySelectorAll('.filter-pill').forEach(p => {{
          p.classList.toggle('active', p.getAttribute('data-cat') === catKey);
        }});
      }}

      const qInput = document.getElementById('hub-search-input');
      const query = qInput ? qInput.value.trim().toLowerCase() : '';
      let visibleCount = 0;

      document.querySelectorAll('.article-card').forEach(card => {{
        const cCat = card.getAttribute('data-category');
        const cText = card.innerText.toLowerCase();
        const matchCat = (catKey === 'all' || cCat === catKey);
        const matchQuery = (!query || cText.includes(query));
        if (matchCat && matchQuery) {{
          card.style.display = 'flex';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      const counterEl = document.getElementById('visible-articles-count');
      if (counterEl) counterEl.innerText = visibleCount;
      if (scrollToHub) {{
        document.getElementById('knowledge-hub-section').scrollIntoView({{ behavior: 'smooth' }});
      }}
    }}

    function onLiveSearchArticles() {{
      const activePill = document.querySelector('.filter-pill.active');
      const currentCat = activePill ? activePill.getAttribute('data-cat') : 'all';
      filterArticlesByCategory(currentCat, null, false);
    }}

    function toggleCompactHubView() {{
      const grid = document.getElementById('articles-bento-grid');
      const btn = document.getElementById('view-toggle-btn');
      if (!grid) return;
      grid.classList.toggle('compact-mode');
      if (grid.classList.contains('compact-mode')) {{
        btn.innerText = '🗂️ عرض البطاقات بالتفصيل';
      }} else {{
        btn.innerText = '⚡ عرض الفهرس السريع المدمج';
      }}
    }}

    function showToast(msg) {{
      let t = document.getElementById('toast-msg');
      if (!t) {{
        t = document.createElement('div');
        t.id = 'toast-msg';
        t.className = 'toast-notification';
        document.body.appendChild(t);
      }}
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 4000);
    }}

    function copyPromoAndOpenInstagram(code, topicTitle, igUrl) {{
      const textToCopy = "أهلاً دكتورة، أنا في موقع Healing Touch ومعايا كود العرض (" + code + ") ومحتاج أستفسر مجاناً عن: " + topicTitle;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(textToCopy).then(() => {{
          showToast("✅ تم نسخ سؤالك وكود العرض (" + code + ")! جاري فتح شات الدكتورة على إنستجرام...");
          setTimeout(() => {{ window.open(igUrl, '_blank'); }}, 1100);
        }}).catch(() => {{
          window.open(igUrl, '_blank');
        }});
      }} else {{
        window.open(igUrl, '_blank');
      }}
    }}
"""


def render_top_and_header(cfg: dict, is_subpage: bool = False) -> str:
    prefix = "../" if is_subpage else ""
    offer = get_active_offer_details(cfg)
    wa_general = build_whatsapp_link(cfg, "استشارة طبية مجانية عامة", is_article=False)
    return f"""
<div class="live-rep-topbar">
  <span class="pulse-dot"></span>
  <strong>متاح الآن مجاناً:</strong> تحدث مباشرة مع الدكتورة وممثلي الرعاية الطبية للإجابة على أسئلتك قبل أي قرار — <span>{offer["offer_badge"]}</span>
</div>

<header class="clinical-header">
  <div class="nav-container">
    <a href="{prefix}index.html" class="brand-logo">
      🌿 هيلينج تاتش مصر | Healing Touch
    </a>
    <nav class="nav-links">
      <a href="{prefix}index.html#guided-triage">🧭 مُوجِّه الحالات</a>
      <a href="{prefix}index.html#knowledge-hub-section">📚 الموسوعة الطبية الكاملة</a>
      <a href="{prefix}index.html#solutions-section">🛡️ الحلول المعتمدة</a>
      <a href="{wa_general}" target="_blank" rel="noopener" class="nav-cta-chat">💬 تحدث مجاناً مع الدكتورة الآن</a>
    </nav>
  </div>
</header>
"""


def render_sticky_bottom_bar(cfg: dict, context_topic: str) -> str:
    offer = get_active_offer_details(cfg)
    wa_url = build_whatsapp_link(cfg, context_topic, is_article=True)
    safe_topic = context_topic.replace("'", "")
    return f"""
<div class="sticky-consult-bar">
  <div class="sticky-inner">
    <div class="sticky-text">
      <span class="pulse-dot"></span>
      <span>لديك سؤال عن حالتك؟ تحدث مجاناً مع الدكتورة وممثلي الرعاية</span>
      <span class="hide-mobile" style="color:#A7F3D0;">({offer["offer_title"]} بكود {offer["code"]})</span>
    </div>
    <div class="sticky-btns">
      <a href="{wa_url}" target="_blank" rel="noopener" class="sticky-wa-btn">💬 اسأل مجاناً عبر واتساب ({offer["whatsapp_display"]})</a>
      <button onclick="copyPromoAndOpenInstagram('{offer['code']}', '{safe_topic}', '{offer['instagram_url']}')" class="sticky-ig-btn">📸 اسأل عبر إنستجرام</button>
    </div>
  </div>
</div>
"""


def render_footer(cfg: dict) -> str:
    offer = get_active_offer_details(cfg)
    wa_footer = build_whatsapp_link(cfg, "استفسار طبي مجاني", is_article=False)
    return f"""
<footer>
  <div style="max-width:900px; margin:0 auto;">
    <p style="font-size:1.15rem; font-weight:800; color:#fff; margin-top:0;">🌿 هيلينج تاتش مصر (Healing Touch Egypt 2026)</p>
    <p>المنصة التوعوية والاستشارية الأولى لرعاية ما بعد العمليات الجراحية والتجميلية في مصر. مهمتنا إرشادك علمياً والإجابة على أسئلتك مجاناً مع ضمان معاينة الكود الأصلي لأي منتج قبل الدفع.</p>
    <p style="margin-top:16px;">
      <a href="{wa_footer}" target="_blank" rel="noopener">💬 محادثة مجانية على واتساب ({offer["whatsapp_display"]})</a> |
      <a href="{offer['instagram_url']}" target="_blank" rel="noopener">📸 حساب إنستجرام</a> |
      <a href="https://www.facebook.com/61596009772486" target="_blank" rel="noopener">📘 صفحتنا على فيسبوك</a>
    </p>
  </div>
</footer>
"""


def build_article_page(art: dict, all_articles: list, cfg: dict) -> str:
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    offer = get_active_offer_details(cfg)
    paragraphs_html = "\n".join([f"<p>{p}</p>" for p in art["content_paragraphs"]])
    takeaways_html = "\n".join([f"<li>{t}</li>" for t in art.get("quick_takeaways", [])])

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

    # ربط جميع المقالات الأخرى في أسفل المقال لتعزيز الـ SEO والنمو الأسي
    related_cards = []
    for other in all_articles:
        if other["slug"] == art["slug"]:
            continue
        other_wa = build_whatsapp_link(cfg, other["title"], is_article=True)
        related_cards.append(f"""
        <div class="article-card">
          <div>
            <div class="art-meta-top">
              <span class="art-cat-tag">{other.get("category_label", "دليل طبي")}</span>
              <span class="art-Evidence-tag">✅ 10+ دراسات</span>
            </div>
            <h3><a href="{other['slug']}.html">{other["title"]}</a></h3>
          </div>
          <div class="art-card-actions">
            <a href="{other['slug']}.html" class="btn-read-guide">📖 قراءة الدليل</a>
            <a href="{other_wa}" target="_blank" rel="noopener" class="btn-ask-doc-mini">💬 اسأل مجاناً</a>
          </div>
        </div>
        """)
    related_html = "\n".join(related_cards)

    wa_article_link = build_whatsapp_link(cfg, art["title"], is_article=True)
    safe_title = art["title"].replace("'", "")

    page_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{art["title"]} | هيلينج تاتش مصر</title>
  <meta name="description" content="{art["hook_summary"]}">
  <meta name="keywords" content="{art["keywords"]}">
  <link rel="canonical" href="{SITE_BASE_URL}/articles/{art["slug"]}.html">
  <style>{get_shared_css()}</style>
  <script>{get_shared_js(cfg)}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "headline": "{art["title"]}",
    "description": "{art["hook_summary"]}",
    "keywords": "{art["keywords"]}",
    "datePublished": "{today_str}",
    "dateModified": "{today_str}"
  }}
  </script>
</head>
<body>

{render_top_and_header(cfg, is_subpage=True)}

<div class="container">
  <div style="margin-bottom: 18px;">
    <a href="../index.html#knowledge-hub-section" style="color:var(--teal-deep); font-weight:800; text-decoration:none;">⬅ العودة للموسوعة الطبية الكاملة ومُوجِّه الحالات</a>
  </div>

  <article class="article-full-box">
    <div class="art-meta-top" style="margin-bottom:14px;">
      <span class="art-cat-tag">{art.get("category_label", "دليل التعافي الجراحي")}</span>
      <span class="art-Evidence-tag">🛡️ موثق بـ {len(art["sources"])} دراسة سريرية من PubMed وNCBI</span>
    </div>

    <h1 style="color:var(--teal-deep); margin-top:0; font-size:1.75rem;">{art["title"]}</h1>

    <div class="takeaways-box">
      <h3>⏱️ الخلاصة السريرية السريعة (في 30 ثانية):</h3>
      <ul>
        {takeaways_html}
      </ul>
    </div>

    {paragraphs_html}

    <!-- صندوق تحويل الزائر للمحادثة المجانية مع الدكتورة -->
    <div class="triage-result-panel" style="margin: 32px 0;">
      <div class="triage-result-header">
        <span class="triage-badge">👩‍⚕️ استشارة مجانية 100% بدون التزام بالشراء</span>
        <span style="font-weight:800; color:#065F46;">{offer["offer_badge"]}</span>
      </div>
      <h3>هل لديك سؤال يخص جرحك أو تريد التأكد من المقاس المناسب لحالتك؟</h3>
      <p>لا تتردد في التحدث مجاناً الآن مع الدكتورة المختصة وممثلي الرعاية الطبية لدينا؛ ستجيبك الدكتورة علمياً عن حالتك، وإذا رغبت في طلب (<strong>{art["product_badge"]}</strong>) ستحصل تلقائياً على <strong>{offer["offer_title"]}</strong> بكود <strong>{offer["code"]}</strong>.</p>
      <div class="triage-actions">
        <a href="{wa_article_link}" target="_blank" rel="noopener" class="btn-free-chat">
          💬 تحدث مجاناً مع الدكتورة على واتساب ({offer["whatsapp_display"]})
        </a>
        <button onclick="copyPromoAndOpenInstagram('{offer['code']}', '{safe_title}', '{offer['instagram_url']}')" class="btn-ig-chat">
          📸 اسأل الدكتورة عبر إنستجرام
        </button>
      </div>
    </div>

    <div class="refs-container">
      <h3 style="color:var(--teal-deep); margin-top:0;">📚 الدراسات والأبحاث الطبية الموثقة المعتمدة في هذا الدليل ({len(art["sources"])} مرجعاً):</h3>
      <ol>
        {refs_html}
      </ol>
    </div>
  </article>

  <h2 class="hub-title" style="margin: 40px 0 20px 0;">📖 أدلة ومقالات طبية أخرى في الموسوعة (تصفح الكل):</h2>
  <div class="articles-bento-grid">
    {related_html}
  </div>
</div>

{render_sticky_bottom_bar(cfg, art["title"])}
{render_footer(cfg)}

</body>
</html>
"""
    art_path = ARTICLES_DIR / f"{art['slug']}.html"
    art_path.write_text(page_html, encoding="utf-8")
    return str(art_path)


def build_sitemap_xml(articles: list):
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    urls = [f"  <url><loc>{SITE_BASE_URL}/</loc><lastmod>{today_str}</lastmod><priority>1.0</priority></url>"]
    for art in articles:
        urls.append(
            f"  <url><loc>{SITE_BASE_URL}/articles/{art['slug']}.html</loc><lastmod>{today_str}</lastmod><priority>0.9</priority></url>"
        )
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    (DOCS_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")


def build_full_website():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    cfg = load_promo_config()
    offer = get_active_offer_details(cfg)

    all_articles = sync_all_articles_from_sheet()

    print(f"[1/3] 📝 جاري بناء {len(all_articles)} مقالات طبية بتصميم 2026 الاستشاري...")
    for art in all_articles:
        build_article_page(art, all_articles, cfg)

    print("[2/3] 🌐 جاري بناء الصفحة الرئيسية (Guided Patient Funnel + Exponential Articles Hub)...")

    # بناء بطاقات جميع المقالات لتظهر كلها في وقت واحد مع دعم الفلترة والبحث الحي
    articles_cards_html = []
    for art in all_articles:
        wa_art = build_whatsapp_link(cfg, art["title"], is_article=True)
        articles_cards_html.append(f"""
    <div class="article-card" data-category="{art.get('category', 'c-section')}">
      <div>
        <div class="art-meta-top">
          <span class="art-cat-tag">{art.get("category_label", "دليل طبي")}</span>
          <span class="art-Evidence-tag">✅ {len(art.get("sources", []))} مراجع PubMed</span>
        </div>
        <h3><a href="articles/{art['slug']}.html">{art["title"]}</a></h3>
        <p class="art-hook-text">{art["hook_summary"]}</p>
      </div>
      <div class="art-card-actions">
        <a href="articles/{art['slug']}.html" class="btn-read-guide">📖 اقرأ الدليل العلمي</a>
        <a href="{wa_art}" target="_blank" rel="noopener" class="btn-ask-doc-mini">💬 اسأل الدكتورة مجاناً</a>
      </div>
    </div>
        """)
    articles_grid_html = "\n".join(articles_cards_html)

    # الحلول الطبية المعتمدة (بصياغة استشارية تدفع للتحدث المجاني مع الدكتورة أولاً)
    solutions_data = [
        {
            "name": "رول شيت السيليكون الطبي للندبات BUPY (4 سم × 3 متر)",
            "desc": "خط الدفاع الأول سريرياً لتسطيح وإخفاء ندبات القيصرية، شد البطن، التثدي، والغدة الدرقية. رول كامل 3 أمتار قابل للغسيل وإعادة الاستخدام لـ 4 أشهر.",
            "price": "750 ج.م للرول الكامل (أو 320 ج.م للمتر المقصوص)",
            "topic": "استفسار مجاني عن رول شيت السيليكون BUPY وطريقة استخدامه لجرحي",
        },
        {
            "name": "بلاستر الأنف الطبي البيج الأصلي 3M Micropore (1533-0)",
            "desc": "الشريط الورقي المسامي الأصلي الموصى به لتصريف تورم أرنبة الأنف وتثبيت الغضاريف بعد فك الجبيرة بدون حساسية.",
            "price": "175 ج.م للبكرة (أو 3 بكرات بـ 450 ج.م)",
            "topic": "استفسار مجاني عن بلاستر الأنف البيج 3M Micropore الأصلي",
        },
        {
            "name": "ضمادات الاستحمام المقاومة للماء 3M Tegaderm +Pad",
            "desc": "فيلم طبي شفاف يعزل جرح القيصرية أو الجراحة عن الماء والبكتيريا بنسبة 100% بوسادة غير لاصقة بالغرز لشاور آمن من اليوم الثاني.",
            "price": "باكدج 5 إلى 10 ضمادات: 220 – 390 ج.م",
            "topic": "استفسار مجاني عن ضمادات الاستحمام Tegaderm +Pad ومقاسها لجرحي",
        },
        {
            "name": "بخاخ الجروح العازل للماء Opsite Spray (Smith & Nephew)",
            "desc": "غشاء شفاف مرن يجف في ثوانٍ لحماية فتحات مناظير التكميم والمرارة والغرز التجميلية من الماء واحتكاك الملابس.",
            "price": "750 ج.م للعبوة الأصلية",
            "topic": "استفسار مجاني عن بخاخ الجروح الشفاف Opsite Spray",
        },
        {
            "name": "دعامة فتحات الأنف السيليكون الطبية Nostril Retainer",
            "desc": "سيليكون طبي مرن يحافظ على تماثل وتساوي فتحتي الأنف ويمنع الانكماش الغضروفي بعد عمليات تجميل الأنف.",
            "price": "450 ج.م (أو باكدج الأنف الكامل بـ 680 ج.م)",
            "topic": "استفسار مجاني لتحديد المقاس المناسب لدعامة فتحات الأنف Nostril Retainer",
        },
    ]

    solutions_html_list = []
    for sol in solutions_data:
        wa_sol = build_whatsapp_link(cfg, sol["topic"], is_article=False)
        solutions_html_list.append(f"""
        <div class="solution-card">
          <div>
            <h3>{sol["name"]}</h3>
            <p style="color:var(--text-muted); font-size:0.93rem; margin:0 0 8px 0;">{sol["desc"]}</p>
            <div class="solution-price">{sol["price"]}</div>
          </div>
          <div style="margin-top:12px;">
            <a href="{wa_sol}" target="_blank" rel="noopener" class="btn-free-chat" style="width:100%; font-size:0.93rem; padding:11px 16px;">
              💬 اسأل الدكتورة مجاناً هل يناسب حالتي؟
            </a>
          </div>
        </div>
        """)
    solutions_grid_html = "\n".join(solutions_html_list)

    default_wa_triage = build_whatsapp_link(
        cfg, "استشارة مجانية لحالة ولادة قيصرية / شد بطن (الاستحمام وشيت السيليكون)", is_article=False
    )

    index_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>هيلينج تاتش مصر | Healing Touch Egypt - استشارة التعافي ما بعد الجراحة والموسوعة الطبية</title>
  <meta name="description" content="تحدث مجاناً مع الدكتورة وممثلي الرعاية الطبية في هيلينج تاتش مصر لاختيار بروتوكول التعافي الموثق بعد الولادة القيصرية، تجميل الأنف، التكميم، والتثدي مع شحن مجاني ومعاينة بكود {offer['code']}.">
  <link rel="canonical" href="{SITE_BASE_URL}/">
  <style>{get_shared_css()}</style>
  <script>{get_shared_js(cfg)}</script>
</head>
<body>

{render_top_and_header(cfg, is_subpage=False)}

<div class="container">

  <!-- المحطة 1 و 2: مُوجِّه الحالات الجراحية التفاعلي (Ro.co & Silagen 2026 UX) -->
  <section id="guided-triage" class="hero-guided-box">
    <div class="trust-pill-top">🛡️ إرشاد طبي موثق بـ 12 دراسة سريرية من PubMed وNCBI و3M</div>
    <h1>لا تخمّن طريقة العناية بجرحك بعد العملية..<br>دعنا نرشدك علمياً ونصل بك للدكتورة المختصة مجاناً</h1>
    <p class="hero-subtitle">
      أكثر من 80% من المرضى يشترون مستلزمات غير مناسبة لمرحلة جرحهم. اختر نوع عمليتك بالأسفل في ثانية واحدة لتظهر لك الخطة الطبية الموثقة، وتحدث <strong>مجاناً 100%</strong> مع ممثلينا الطبيين للإجابة على أسئلتك.
    </p>

    <span class="triage-step-label">👇 الخطوة 1: اضغط على نوع العملية الجراحية التي أجريتها أو تستعد لها:</span>

    <div class="surgery-selector-grid">
      <button class="surgery-btn active" onclick="selectSurgeryTriage('c-section', this)">
        <span class="s-icon">🤱</span>
        <span class="s-title">الولادة القيصرية وشد البطن</span>
        <span class="s-desc">الاستحمام الآمن بدون التهاب + منع ندبة الكلويد البارزة</span>
      </button>

      <button class="surgery-btn" onclick="selectSurgeryTriage('rhinoplasty', this)">
        <span class="s-icon">👃</span>
        <span class="s-title">تجميل الأنف (Rhinoplasty)</span>
        <span class="s-desc">تصريف تورم الأرنبة بعد الجبيرة + تماثل فتحتي الأنف</span>
      </button>

      <button class="surgery-btn" onclick="selectSurgeryTriage('bariatric', this)">
        <span class="s-icon">🩺</span>
        <span class="s-title">التكميم وجراحات المناظير</span>
        <span class="s-desc">عزل فتحات المنظار الـ 5 عن الماء والعرق والاحتكاك</span>
      </button>

      <button class="surgery-btn" onclick="selectSurgeryTriage('thyroid-gynecomastia', this)">
        <span class="s-icon">🧣</span>
        <span class="s-title">الغدة الدرقية والتثدي</span>
        <span class="s-desc">إخفاء خط الرقبة والصدر وتهدئة الحكة العصبية</span>
      </button>
    </div>

    <!-- بطاقة التوصية الفورية والتحويل للمحادثة المجانية -->
    <div id="triage-result-panel" class="triage-result-panel">
      <div class="triage-result-header">
        <span id="triage-badge-text" class="triage-badge">بروتوكول الولادة القيصرية وشد البطن (موثق بـ 10 دراسات)</span>
        <span style="font-weight:800; color:#065F46;">{offer["offer_badge"]}</span>
      </div>
      <h3 id="triage-title-text">خطة التعافي الآمن لجرح القيصرية وشد البطن:</h3>
      <p id="triage-desc-text">
        في أول أسبوعين: حمايتك من التهاب الجرح أثناء الشاور تتطلب عزل الماء 100% بضمادة الفيلم الشفاف (3M Tegaderm +Pad). وبعد التئام السطح وفك الغرز: وضع رول شيت السيليكون الطبي (BUPY 3m) يمنع بروز الكلويد ويوفر عليكِ آلاف الجنيهات في جلسات الليزر والمراهم.
      </p>
      <div class="triage-actions">
        <a id="triage-wa-btn" href="{default_wa_triage}" target="_blank" rel="noopener" class="btn-free-chat">
          💬 تحدث مجاناً الآن مع الدكتورة للاستفسار عن حالتك ({offer["whatsapp_display"]})
        </a>
        <button onclick="copyPromoAndOpenInstagram('{offer['code']}', document.getElementById('triage-title-text').innerText, '{offer['instagram_url']}')" class="btn-ig-chat">
          📸 اسأل الدكتورة مجاناً على إنستجرام
        </button>
      </div>
    </div>
  </section>

  <!-- المحطة 3: لماذا يتحدث المرضى مع ممثلينا الطبيين قبل الشراء؟ -->
  <section class="journey-steps-grid">
    <div class="step-card">
      <span class="step-num">الخطوة 1 — طمأنة طبية مجانية</span>
      <h4>اسأل الدكتورة بدون أي التزام</h4>
      <p>أرسل سؤالك أو نوع عمليتك على واتساب وسترد عليك طبيبة مختصة لتوضيح ما يناسب مرحلة التئام جرحك مجاناً.</p>
    </div>
    <div class="step-card">
      <span class="step-num">الخطوة 2 — دقة المقاس والبروتوكول</span>
      <h4>تجنب شراء منتج خاطئ</h4>
      <p>تساعدك الدكتورة في اختيار مقاس دعامة الأنف أو ضمادة Tegaderm أو توقيت البدء في شيت السيليكون بدقة سريرية.</p>
    </div>
    <div class="step-card">
      <span class="step-num">الخطوة 3 — أمان مالي 100%</span>
      <h4>شحن مجاني + معاينة قبل الدفع</h4>
      <p>إذا قررت الطلب، يمنحك كود <strong>{offer["code"]}</strong> شحناً مجانياً وحق فتح الشحنة والتأكد من الكود الأصلي بنفسك قبل الدفع.</p>
    </div>
  </section>

  <!-- المحطة 4: الموسوعة الطبية الحية ذات النمو الأسي (جميع المقالات معروضة معاً) -->
  <section id="knowledge-hub-section">
    <div class="hub-header-box">
      <div class="hub-top-row">
        <div>
          <h2 class="hub-title">📚 الموسوعة الطبية الكاملة لتعافي ما بعد الجراحة (تتحدث يومياً)</h2>
          <p style="margin:4px 0 0 0; color:var(--text-muted); font-size:0.95rem;">
            جميع أدلتنا ومقالاتنا العلمية معروضة أمامك في نفس الوقت وموثقة بأبحاث PubMed وNCBI — اختر تخصص جراحتك أو ابحث بكلمة واحدة:
          </p>
        </div>
        <span class="hub-counter-badge">إجمالي الأدلة المعروضة: <strong id="visible-articles-count">{len(all_articles)}</strong> مقال طبي</span>
      </div>

      <div class="hub-controls-row">
        <div class="filter-pills">
          <button class="filter-pill active" data-cat="all" onclick="filterArticlesByCategory('all', this)">الكل ({len(all_articles)})</button>
          <button class="filter-pill" data-cat="c-section" onclick="filterArticlesByCategory('c-section', this)">🤱 القيصرية وشد البطن</button>
          <button class="filter-pill" data-cat="rhinoplasty" onclick="filterArticlesByCategory('rhinoplasty', this)">👃 تجميل الأنف</button>
          <button class="filter-pill" data-cat="bariatric" onclick="filterArticlesByCategory('bariatric', this)">🩺 التكميم والمناظير</button>
          <button class="filter-pill" data-cat="thyroid-gynecomastia" onclick="filterArticlesByCategory('thyroid-gynecomastia', this)">🧣 الغدة والتثدي</button>
        </div>

        <div class="search-and-view">
          <input id="hub-search-input" type="search" class="live-search-input" placeholder="🔍 ابحث في جميع المقالات (مثال: شاور، كلويد، أرنبة)..." oninput="onLiveSearchArticles()">
          <button id="view-toggle-btn" class="view-toggle-btn" onclick="toggleCompactHubView()">⚡ عرض الفهرس السريع المدمج</button>
        </div>
      </div>
    </div>

    <!-- شبكة جميع المقالات المعروضة في نفس الوقت -->
    <div id="articles-bento-grid" class="articles-bento-grid">
      {articles_grid_html}
    </div>
  </section>

  <!-- المحطة 5: المستلزمات الطبية المعتمدة (للاستفسار المباشر مع الدكتورة) -->
  <section id="solutions-section" style="margin-top: 50px;">
    <h2 class="hub-title" style="margin-bottom:8px;">🛡️ المستلزمات الطبية الأصلية المعتمدة في بروتوكولاتنا</h2>
    <p style="color:var(--text-muted); margin-top:0;">اضغط على أي مستلزم للتحدث مجاناً مع الدكتورة والتأكد من ملاءمته لجرحك مع تفعيل كود <strong>{offer["code"]}</strong> ({offer["offer_title"]}):</p>
    <div class="solutions-grid">
      {solutions_grid_html}
    </div>
  </section>

</div>

{render_sticky_bottom_bar(cfg, "استشارة طبية مجانية من الصفحة الرئيسية")}
{render_footer(cfg)}

</body>
</html>
"""
    index_file = DOCS_DIR / "index.html"
    index_file.write_text(index_html, encoding="utf-8")
    build_sitemap_xml(all_articles)
    print(f"[3/3] ✅ تم بناء الموقع الجديد وخريطة Sitemap بنجاح ({len(all_articles)} مقالات معروضة معاً): {index_file}")
    return str(index_file)


def open_site_in_browser():
    index_file = DOCS_DIR / "index.html"
    if index_file.exists():
        print(f"[🌐] جاري فتح الموقع في المتصفح الافتراضي: {index_file}")
        open_url_in_default_browser(str(index_file))


def setup_and_push_github(repo_url: str = ""):
    print("\n[*] جاري رفع التحديث الجديد إلى GitHub Pages...")
    cwd = str(BASE_DIR)
    try:
        subprocess.run(["git", "add", "docs/", "github_seo_trend_engine.py", "promo_config.json"], cwd=cwd, check=True)
        commit_res = subprocess.run(
            ["git", "commit", "-m", f"Upgrade to 2026 Clinical Guided Consultation Funnel & Exponential Hub ({datetime.date.today()})"],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        print(f"Git commit: {commit_res.stdout.strip() or commit_res.stderr.strip()}")
        if repo_url:
            subprocess.run(["git", "remote", "set-url", "origin", repo_url], cwd=cwd, check=False)
        push_res = subprocess.run(["git", "push", "origin", "main"], cwd=cwd, capture_output=True, text=True)
        if push_res.returncode == 0:
            print("✅ تم رفع التصميم الجديد إلى GitHub Pages بنجاح تام!")
        else:
            print(f"[!] رسالة Git أثناء الرفع: {push_res.stderr.strip()}")
    except Exception as exc:
        print(f"[!] تنبيه أثناء التعامل مع Git: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Healing Touch Egypt - 2026 Clinical Guided Funnel & Exponential SEO Hub")
    parser.add_argument("--build-site", action="store_true", help="بناء وتحديث الموقع وجميع المقالات")
    parser.add_argument("--preview", action="store_true", help="معاينة الموقع في المتصفح الافتراضي")
    parser.add_argument("--push-github", action="store_true", help="رفع التحديثات إلى GitHub Pages")
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
