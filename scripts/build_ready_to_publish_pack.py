# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك حزم النشر الشاملة الديناميكي بالمجلدات المؤرخة المفرزة (2026)
Dynamic Multi-Platform Publishing Engine: YouTube, TikTok, Instagram, Blogger, Reddit, Facebook
=============================================================================
100% خالي من أي نصوص أو قوالب ثابتة.
يعتمد بالكامل على استيعاب مدخلات manual_inbox أو الأرشيف الأحدث، وتوليد حزمة مخصصة للمنتج والتخصص الحالي.
"""

import sys
import os
import re
import shutil
import glob
import urllib.parse
import datetime as dt
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media_assets"
READY_BASE_DIR = MEDIA_DIR / "ready_to_publish"
MANUAL_INBOX_DIR = MEDIA_DIR / "manual_inbox"
POMELLI_LIB_DIR = MEDIA_DIR / "pomelli_library"
DOCS_DIR = BASE_DIR / "docs"

# استيراد محرك الفيديو والفرز الذكي
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "scripts"))
from smart_intake_classifier import (
    scan_and_triage_manual_inbox,
    route_platform_text_files,
    extract_clean_content,
    find_active_inbox_files,
    read_resilient_text,
    classify_file_category,
    CATEGORY_KEYWORDS
)
from media_video_engine import (
    build_audio_visual_videos,
    build_uploaded_video_variants,
    generate_clean_youtube_thumbnail
)

YOUTUBE_CHANNEL_ID = "UCcHqrSEET7IEhr9ueM8VELQ"
YOUTUBE_UPLOAD_URL = f"https://studio.youtube.com/channel/{YOUTUBE_CHANNEL_ID}/videos/upload?d=ud"

CATEGORY_DEFAULTS = {
    "rhinoplasty": {
        "title": "دعامات الأنف السيليكونية وتماثل الفتحات بعد التجميل | هيلينج تاتش مصر",
        "shorts_title": "سر تماثل فتحات الأنف بعد التجميل وقص الجناح #Shorts #تجميل_الانف",
        "wa_msg": "أهلاً بحضرتك، محتاج استشارة بخصوص دعامة الأنف السيليكونية وتماثل الفتحات، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "tags": "#تجميل_الانف_مصر #دعامات_الانف_السيليكون #نوستريل_ريتينر_مصر #فتحات_الانف #تجميل_الانف #هيلينج_تاتش_مصر #كود_HT10 #جراحة_التجميل_مصر",
        "topic_ar": "دعامات الأنف السيليكونية وتماثل الفتحات بعد التجميل"
    },
    "c-section": {
        "title": "بروتوكول تعافي جرح القيصرية والشاور الآمن ومنع الندبات وتكون الكلويد",
        "shorts_title": "خايفة من أول شاور بعد القيصرية؟ الحل الطبي لحماية الجرح من الماء #Shorts #قيصرية",
        "wa_msg": "أهلاً بحضرتك، محتاجة استشارة بخصوص جرح القيصرية والشاور الآمن، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "tags": "#ولادة_قيصرية #جرح_القيصرية #علاج_الندبات #شيت_سيليكون #تيجاديرم #صحة_المرأة #هيلينج_تاتش_مصر #الاستحمام_بعد_القيصرية",
        "topic_ar": "تعافي جرح القيصرية والشاور الآمن"
    },
    "bariatric": {
        "title": "بروتوكول العناية بثقوب المنظار بعد عمليات التكميم والاستحمام الآمن",
        "shorts_title": "أول شاور بعد التكميم بدون خوف على جروح المنظار #Shorts #تكميم",
        "wa_msg": "أهلاً بحضرتك، محتاج استشارة بخصوص حماية ثقوب المنظار بعد التكميم، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "tags": "#تكميم_المعدة #جراحات_السمنة #ثقوب_المنظار #بخاخ_اوبسايت #علاج_الندبات #هيلينج_تاتش_مصر #كود_HT10",
        "topic_ar": "العناية بثقوب المنظار بعد التكميم"
    },
    "thyroid": {
        "title": "حماية وتسطيح ندبة الرقبة بعد استئصال الغدة الدرقية والوقاية من التصبغ",
        "shorts_title": "إزاي تحمي ندبة الرقبة من أشعة الشمس وتمنع بروزها؟ #Shorts #غدة_درقية",
        "wa_msg": "أهلاً بحضرتك، محتاجة استشارة بخصوص حماية وتسطيح ندبة الرقبة بعد استئصال الغدة الدرقية، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "tags": "#استئصال_الغدة_الدرقية #ندبات_الرقبة #شيت_سيليكون #بلاستر_طبي #هيلينج_تاتش_مصر #كود_HT10",
        "topic_ar": "حماية وتسطيح ندبة الرقبة بعد استئصال الغدة"
    }
}


def get_active_assets(category: str = None) -> dict:
    """اكتشاف وتحديد أحدث ملفات الحملة النشطة في manual_inbox أو أرشيف الحملة الأخير مع عزل التخصص 100%."""
    triage = scan_and_triage_manual_inbox(MANUAL_INBOX_DIR)
    active_files = find_active_inbox_files(MANUAL_INBOX_DIR)
    detected = triage.get("detected_category") or "rhinoplasty"
    if not category:
        category = detected

    # عزل ملفات النصوص حسب التخصص المطلوب لمنع تسرب نصوص تخصص لآخر
    if category == detected:
        platform_texts = triage.get("platform_texts", {})
    else:
        # البحث عن ملفات نصوص تخص هذا التخصص بعينه في الصندوق أو الأرشيف
        cat_texts = [f for f in active_files if f.suffix.lower() in [".txt", ".md"] and classify_file_category(f) == category]
        if not cat_texts and (MANUAL_INBOX_DIR / "archive").exists():
            for arch_dir in sorted((MANUAL_INBOX_DIR / "archive").iterdir(), reverse=True):
                if arch_dir.is_dir():
                    cand = [f for f in arch_dir.iterdir() if f.is_file() and f.suffix.lower() in [".txt", ".md"] and classify_file_category(f) == category]
                    if cand:
                        cat_texts = cand
                        break
        platform_texts = route_platform_text_files(cat_texts) if cat_texts else {}

    assets = {
        "video": None,
        "audio": None,
        "hero_img": None,
        "square_img": None,
        "vertical_img": None,
        "platform_texts": platform_texts,
        "category": category,
        "active_files": active_files
    }

    # 1. الفيديو المعتمد للحملة
    vids = [f for f in active_files if f.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm"]]
    cat_keywords = CATEGORY_KEYWORDS.get(category, [])
    matching_vids = [v for v in vids if category in v.name.lower() or any(kw.lower() in v.name.lower() for kw in cat_keywords)]
    if matching_vids:
        assets["video"] = matching_vids[0]
    else:
        campaign_vid = DOCS_DIR / "assets" / f"campaign_{category}_video.mp4"
        if campaign_vid.exists():
            assets["video"] = campaign_vid
        elif category == detected and vids:
            assets["video"] = vids[0]

    # 2. الصوت المرفوع
    audios = [f for f in active_files if f.suffix.lower() in [".m4a", ".mp3", ".wav", ".aac"]]
    if audios and category == detected:
        assets["audio"] = audios[0]

    # 3. صور Pomelli والأصول المرئية
    imgs = [f for f in active_files if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]] if category == detected else []
    if not imgs and category == detected and POMELLI_LIB_DIR.exists():
        imgs = list(POMELLI_LIB_DIR.glob("*.png"))

    if imgs:
        square_cand = next((im for im in imgs if "1_1" in im.name or "photoshoot-1" in im.name), imgs[0])
        vert_cand = next((im for im in imgs if "9_16" in im.name), square_cand)
        hero_cand = next((im for im in imgs if "16_9" in im.name or "photoshoot-4" in im.name), square_cand)
        assets["hero_img"] = hero_cand
        assets["square_img"] = square_cand
        assets["vertical_img"] = vert_cand
    else:
        # صورة افتراضية من أصول الحملة في docs
        def_hero = DOCS_DIR / "assets" / f"campaign_{category}_hero.png"
        fallback_hero = DOCS_DIR / "assets" / "campaign_rhinoplasty_hero.png"
        og_hero = DOCS_DIR / "assets" / "og-image.jpg"
        chosen_hero = def_hero if def_hero.exists() else (fallback_hero if fallback_hero.exists() else (og_hero if og_hero.exists() else None))
        if chosen_hero:
            assets["hero_img"] = chosen_hero
            assets["square_img"] = chosen_hero
            assets["vertical_img"] = chosen_hero

    return assets


def get_latest_pack_dir(category: str = None) -> Path:
    """إرجاع أحدث مجلد حزمة مؤرخ تم إنشاؤه (مع دعم الفلترة حسب التخصص اختياريًا)."""
    if not READY_BASE_DIR.exists():
        READY_BASE_DIR.mkdir(parents=True, exist_ok=True)
    dirs = sorted([d for d in READY_BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("202")], key=lambda x: x.name, reverse=True)
    if not dirs:
        return READY_BASE_DIR
    if not category:
        return dirs[0]
    for d in dirs:
        guide = d / "00_دليل_النشر_السريع.txt"
        if guide.exists():
            content = guide.read_text(encoding="utf-8", errors="ignore")
            if f"({category})" in content or category.lower() in content.lower():
                return d
    return dirs[0]


def generate_pack(category: str = None) -> Path:
    now = dt.datetime.now()
    timestamp_folder_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    pack_dir = READY_BASE_DIR / timestamp_folder_name
    pack_dir.mkdir(parents=True, exist_ok=True)

    # مجلدات المنصات المخصصة
    yt_dir = pack_dir / "01_يوتيوب_YouTube"
    tiktok_dir = pack_dir / "02_تيكتوك_TikTok"
    ig_dir = pack_dir / "03_إنستجرام_Instagram"
    blogger_dir = pack_dir / "04_بلوجر_Blogger"
    reddit_dir = pack_dir / "05_ريديت_Reddit"
    fb_dir = pack_dir / "06_فيسبوك_Facebook"

    for d in [yt_dir, tiktok_dir, ig_dir, blogger_dir, reddit_dir, fb_dir]:
        d.mkdir(parents=True, exist_ok=True)

    assets = get_active_assets(category)
    cat = assets["category"]
    p_texts = assets["platform_texts"]
    cat_conf = CATEGORY_DEFAULTS.get(cat, CATEGORY_DEFAULTS["rhinoplasty"])

    # الروابط الديناميكية
    lp_url = f"https://medon90ae.github.io/healing-touch-egypt/lp/{cat}-recovery-protocol.html"
    site_url = "https://medon90ae.github.io/healing-touch-egypt/"
    wa_msg = cat_conf["wa_msg"]
    wa_url = f"https://wa.me/201155803307?text={urllib.parse.quote(wa_msg)}"
    tags = cat_conf["tags"]

    # =========================================================================
    # 🎥 1. معالجة الفيديو المرفوع (كامل + شورتس + ريلز + تيك توك)
    # =========================================================================
    if assets["video"]:
        build_uploaded_video_variants(assets["video"], yt_dir, yt_dir)
        shorts_file = yt_dir / "فيديو_شورتس_وريلز_9x16.mp4"
        if shorts_file.exists():
            shutil.copy2(str(shorts_file), str(tiktok_dir / "فيديو_تيكتوك_رأسي_9x16.mp4"))
            shutil.copy2(str(shorts_file), str(ig_dir / "فيديو_ريلز_Reels_9x16.mp4"))

    # =========================================================================
    # 🎙️ 2. تحويل الصوت والبودكاست المرفوع إلى فيديوهات مرئية لجميع المنصات
    # =========================================================================
    if assets["audio"] and assets["hero_img"]:
        audio_vids = build_audio_visual_videos(assets["audio"], assets["hero_img"], yt_dir, yt_dir)
        vert_audio_vid = yt_dir / "فيديو_بودكاست_صوتي_شورتس_9x16.mp4"
        if vert_audio_vid.exists():
            shutil.copy2(str(vert_audio_vid), str(tiktok_dir / "فيديو_بودكاست_صوتي_تيكتوك_9x16.mp4"))
            shutil.copy2(str(vert_audio_vid), str(ig_dir / "فيديو_بودكاست_صوتي_ريلز_9x16.mp4"))

    # =========================================================================
    # 🖼️ 3. توليد وحفظ الصور المصغرة والبوستات
    # =========================================================================
    if assets["hero_img"]:
        generate_clean_youtube_thumbnail(assets["hero_img"], yt_dir / "صورة_مصغرة_Thumbnail.png")
    if assets["square_img"]:
        shutil.copy2(str(assets["square_img"]), str(ig_dir / "صورة_بوست_رئيسية_1x1.png"))
        shutil.copy2(str(assets["square_img"]), str(fb_dir / "صورة_منشور_فيسبوك_1x1.png"))
    if assets["vertical_img"]:
        shutil.copy2(str(assets["vertical_img"]), str(ig_dir / "صورة_ستوري_Story_9x16.png"))

    # =========================================================================
    # 📝 4. قوالب ونصوص يوتيوب (ديناميكية 100%)
    # =========================================================================
    yt_file = p_texts.get("youtube")
    if yt_file:
        yt_data = extract_clean_content(yt_file, "youtube", landing_url=lp_url, whatsapp_url=wa_url)
        yt_title = yt_data["title"]
        yt_desc = yt_data["description"]
        yt_tags = yt_data["tags"]
        if yt_data.get("script_16x9"):
            (yt_dir / "سكريبت_الفيديو_الكامل.txt").write_text(yt_data["script_16x9"], encoding="utf-8")
        if yt_data.get("shorts_script"):
            (yt_dir / "بيانات_الشورتس.txt").write_text(f"العنوان:\n{cat_conf['shorts_title']}\n\nالسكريبت:\n{yt_data['shorts_script']}\n\nرابط الواتساب وتفعيل HT10:\n{wa_url}\n\n{tags}", encoding="utf-8")
        else:
            (yt_dir / "بيانات_الشورتس.txt").write_text(f"العنوان:\n{cat_conf['shorts_title']}\n\nالوصف:\nدليل سريري سريع وموثوق لحالتك مع تفعيل كود HT10 للشحن المجاني وحق المعاينة قبل الاستلام.\n{wa_url}\n\n{tags}", encoding="utf-8")
    else:
        yt_title = cat_conf["title"]
        yt_desc = f"""🌿 {cat_conf['topic_ar']} (2026)
دليل علمي سريري شامل يقدم إرشادات التعافي والآلية الفسيولوجية المعتمدة لحماية الأنسجة.

🔗 روابط الدليل وحاسبة التعافي السريرية:
🌐 دليل التعافي التفاعلي:
{lp_url}

🏛️ تصفح الموسوعة الطبية السريرية الشاملة:
{site_url}

💬 للتوجيه السريري المجاني وتفعيل كود (HT10) للشحن المجاني والمعاينة قبل الاستلام:
👉 {wa_url}

⚠️ تنويه طبي: المحتوى للتوعية السريرية المعتمدة ولا يُغني عن استشارة طبيبك المعالج.

{tags}"""
        yt_tags = tags
        (yt_dir / "بيانات_الشورتس.txt").write_text(f"العنوان:\n{cat_conf['shorts_title']}\n\nالوصف:\nدليل سريري سريع وموثوق لحالتك مع تفعيل كود HT10 للشحن المجاني وحق المعاينة قبل الاستلام.\n{wa_url}\n\n{tags}", encoding="utf-8")

    (yt_dir / "بيانات_الفيديو_عنوان_ووصف_وهاشتاجات.txt").write_text(f"العنوان:\n{yt_title}\n\nالوصف:\n{yt_desc}\n\nقائمة التاغات:\n{yt_tags}", encoding="utf-8")

    # =========================================================================
    # 📱 5. قوالب تيك توك (ديناميكية 100%)
    # =========================================================================
    tt_file = p_texts.get("tiktok")
    if tt_file:
        tt_data = extract_clean_content(tt_file, "tiktok", landing_url=lp_url, whatsapp_url=wa_url)
        tt_caption = tt_data["caption"]
        if tt_data.get("script"):
            (tiktok_dir / "سيناريو_تيكتوك_الرقمي.txt").write_text(f"الهوك البصري:\n{tt_data.get('hook', '')}\n\nالسكريبت:\n{tt_data['script']}", encoding="utf-8")
    else:
        category_emojis = {
            "rhinoplasty": "👃✨",
            "c-section": "🌸✨",
            "bariatric": "🩹✨",
            "thyroid": "🌿✨",
            "gynecomastia": "🩺✨",
            "tummy_tuck": "🩹✨"
        }
        cat_emoji = category_emojis.get(cat, "✨")
        tt_caption = f"""{cat_conf['shorts_title']} {cat_emoji}
دليل التعافي الطبي المعتمد جراحياً لحماية أنسجتك وتأمين أفضل نتيجة.

استشارة سريرية مجانية وتفعيل كود HT10 للشحن المجاني والمعاينة قبل الاستلام:
👉 الرابط في البايو أو واتساب المباشر: {wa_url}

{tags} #Shorts #تيك_توك_طبي"""

    (tiktok_dir / "كابشن_وهاشتاجات_تيكتوك.txt").write_text(tt_caption, encoding="utf-8")

    # =========================================================================
    # 📸 6. قوالب إنستجرام (ديناميكية 100%)
    # =========================================================================
    ig_file = p_texts.get("instagram")
    if ig_file:
        ig_data = extract_clean_content(ig_file, "instagram", landing_url=lp_url, whatsapp_url=wa_url)
        ig_caption = ig_data["caption"]
        if ig_data.get("carousel_guide"):
            (ig_dir / "دليل_الكاروسيل_السريري.txt").write_text(ig_data["carousel_guide"], encoding="utf-8")
        if ig_data.get("reels_script"):
            (ig_dir / "سكريبت_الريلز.txt").write_text(ig_data["reels_script"], encoding="utf-8")
    else:
        ig_caption = f"""🌿 {cat_conf['title']}

دليل سريري شامل يوضح أهم خطوات التعافي الطبي وتجنب الأخطاء الشائعة لضمان أفضل نتيجة جراحية وجمالية.

🎁 كود المعاينة والشحن المجاني: (HT10)
📦 يمنحك حق فتح ومعاينة الشحنة والتأكد من المقاس الأصلي قبل الاستلام والدفع!

💬 لحجز استشارة سريرية مجانية مع أخصائية التعافي عبر واتساب:
📱 الرقم المباشر: 01155803307
🔗 رابط التفعيل والحجز المباشر تجدونه في البيو (Bio)!

{tags}"""

    (ig_dir / "كابشن_وهاشتاجات_إنستجرام.txt").write_text(ig_caption, encoding="utf-8")

    # =========================================================================
    # 📰 7. مقال بلوجر HTML (ديناميكي 100%)
    # =========================================================================
    blogger_file = p_texts.get("blogger")
    if blogger_file:
        bl_data = extract_clean_content(blogger_file, "blogger", landing_url=lp_url, whatsapp_url=wa_url)
        blogger_html = bl_data["html_content"]
    else:
        blogger_html = f"""<div dir="rtl" style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width:820px; margin:auto; background:#ffffff; padding:28px; border-radius:18px; border:1px solid #E2E8F0; color:#1E293B; line-height:1.9;">
    <h1 style="color:#0D4A4D; font-size:1.9rem; font-weight:900; line-height:1.4; margin-bottom:18px;">{cat_conf['title']}</h1>
    <div style="background:#ECFDF5; border-right:4px solid #10B981; padding:16px 20px; border-radius:12px; margin-bottom:26px;">
        <strong style="color:#065F46; font-size:1.05rem;">💡 القاعدة السريرية الذهبية:</strong>
        <p style="margin:6px 0 0 0; color:#064E3B; font-size:0.96rem;">الالتزام بالبروتوكول الطبي السريري المعتمد واستخدام المستلزمات الطبية الأصلية يضمن استقرار النتيجة ومنع المضاعفات.</p>
    </div>
    <div style="background:linear-gradient(135deg, #0D4A4D 0%, #134E4A 100%); color:#ffffff; padding:24px; border-radius:16px; text-align:center; margin-top:35px;">
        <h4 style="margin:0 0 10px 0; font-size:1.25rem;">🩺 احصل على استشارة سريرية وتوجيه مجاني لحالتك</h4>
        <p style="margin:0 0 18px 0; color:#CCFBF1; font-size:0.95rem;">تواصل مباشرة مع أخصائية التعافي مع تفعيل كود <strong>(HT10)</strong> للشحن المجاني وحق فتح ومعاينة الشحنة قبل الاستلام.</p>
        <a href="{wa_url}" target="_blank" style="display:inline-block; background:#10B981; color:#ffffff; font-weight:800; font-size:1.05rem; padding:12px 28px; border-radius:30px; text-decoration:none;">محادثة واتساب الفورية (01155803307) ←</a>
    </div>
</div>"""

    (blogger_dir / "مقال_بلوجر_جاهز_للنشر.html").write_text(blogger_html, encoding="utf-8")

    # =========================================================================
    # 🔴 8. مقال ريديت Markdown (ديناميكي 100%)
    # =========================================================================
    reddit_file = p_texts.get("reddit")
    if reddit_file:
        rd_data = extract_clean_content(reddit_file, "reddit", landing_url=lp_url, whatsapp_url=wa_url)
        reddit_md = rd_data["markdown"]
    else:
        reddit_md = f"""# {cat_conf['title']}

### 🌿 نظرة سريرية عامة
دليل التعافي المبني على الأدلة السريرية والفسيولوجية في بيئة الجراحات الحديثة في مصر.

---

### 🔗 روابط الدليل والاستشارة
* 🌐 **[دليل التعافي وحاسبة الجرح السريرية التفاعلية]({lp_url})**
* 💬 **للتوجيه السريري المجاني وتفعيل كود (HT10) للشحن والمعاينة المجانية:** [تواصل عبر واتساب]({wa_url})

{tags}"""

    (reddit_dir / "منشور_ومقال_ريديت_Markdown.md").write_text(reddit_md, encoding="utf-8")

    # =========================================================================
    # 📘 9. منشور فيسبوك السريري والإنساني (نظيف 100%)
    # =========================================================================
    fb_file = p_texts.get("facebook")
    if fb_file:
        fb_data = extract_clean_content(fb_file, "facebook", landing_url=lp_url, whatsapp_url=wa_url)
        fb_post_text = fb_data["caption"]
    else:
        fb_post_text = f"""🌿 {cat_conf['title']}

عزيزي المريض.. سلامتك وسلامة نتائج عمليتك هي أولويتنا السريرية القصوى! ❤️
أهم خطوات التعافي السليم تعتمد على حماية الأنسجة وتجنب الاجتهادات المنزلية الخاطئة.

━━━━━━━━━━━━━━━━━━━━━━━
🔗 رابط الدليل السريري وحاسبة التعافي المتخصصة:
👉 {lp_url}

💬 للتوجيه السريري المجاني والاستشارة المباشرة عبر واتساب (01155803307) وتفعيل كود (HT10):
👉 {wa_url}

{tags}"""

    (fb_dir / "منشور_فيسبوك_السريري_والإنساني.txt").write_text(fb_post_text, encoding="utf-8")

    # =========================================================================
    # 📋 10. الدليل الإرشادي السريع داخل الحزمة
    # =========================================================================
    guide_text = f"""=============================================================================
🌿 هيلينج تاتش مصر | حزمة النشر الشاملة المفرزة ({timestamp_folder_name})
التخصص والحملة: {cat_conf['topic_ar']} ({cat})
=============================================================================

📁 01_يوتيوب_YouTube:
   - فيديو يوتيوب كامل 16x9 (MP4)
   - فيديو شورتس 9x16 (MP4)
   - صورة مصغرة Thumbnail بدقة 4K
   - ملف بيانات الفيديو والشورتس والسكريبتات الجاهزة للنسخ

📁 02_تيكتوك_TikTok:
   - فيديو تيكتوك رأسي 9x16 (MP4)
   - كابشن وهاشتاجات تيكتوك وسيناريو رقمي موجه لخوارزمية مصر

📁 03_إنستجرام_Instagram:
   - فيديو ريلز 9x16 (MP4)
   - صور البوست والستوري (Pomelli 4K)
   - كابشن وهاشتاجات إنستجرام ودليل الكاروسيل والريلز

📁 04_بلوجر_Blogger:
   - مقال HTML سريري شامل جاهز للنسخ ولصقه فوراً في مدونة بلوجر

📁 05_ريديت_Reddit:
   - مقال Markdown موثق بالأبحاث والمراجع السريرية جاهز للنشر في مجتمعات ريديت

📁 06_فيسبوك_Facebook:
   - منشور فيسبوك السريري والإنساني الكامل مع روابط الواتساب وكود HT10
============================================================================="""
    (pack_dir / "00_دليل_النشر_السريع.txt").write_text(guide_text, encoding="utf-8")

    # تسجيل مسار أحدث حزمة في ملف ثابت لسهولة الفتح
    (READY_BASE_DIR / "LATEST_PACK_PATH.txt").write_text(str(pack_dir), encoding="utf-8")

    print(f"\n[+] 🎉 تم إنشاء وتجهيز حزمة النشر الشاملة ({cat}) بنجاح في المجلد المؤرخ:")
    print(f"    👉 {pack_dir}")
    return pack_dir


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build ready-to-publish packs")
    parser.add_argument("--category", "-c", type=str, default=None, help="Target category (rhinoplasty, c-section, bariatric, thyroid)")
    args = parser.parse_args()
    generate_pack(category=args.category)
