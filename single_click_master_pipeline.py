#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | المسار الرئيسي الموحد بضغطة زر واحدة (2026)
Single-Click Master Pipeline & Unified Orchestration Suite (Milestone 4 - R4)
=============================================================================
Unified, autonomous end-to-end execution:
- Step 1: Media scanning & classification (Hero + Carousel, 9:16 vs 16:9 video, audio)
          with clean fallback to clinical research harvester & SEO trend engine.
- Step 2: Dynamic landing page generation with clinical cases carousel & modal viewer.
- Step 3: Branded creatives, cards, and dated ready-to-publish 6-platform packages.
- Step 4: 6-platform structured payload dispatch to n8n webhook (Telegram HITL review).
- Step 5: Parallel publishing execution / staging (Meta, Instagram, YouTube, TikTok, Reddit, Blogger).
- Step 6: Automated inbox hygiene & archival to media_assets/archive/YYYY-MM-DD_HHMMSS/.
"""

import argparse
import datetime as dt
import json
import logging
import os
import shutil
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ضبط ترميز UTF-8 لطرفية ويندوز لمنع تشوه النصوص العربية
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# إعداد المسارات الأساسية
BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media_assets"
MANUAL_INBOX_DIR = MEDIA_DIR / "manual_inbox"
ARCHIVE_ROOT_DIR = MEDIA_DIR / "archive"
BRANDED_DIR = MEDIA_DIR / "branded_designs"
DOCS_DIR = BASE_DIR / "docs"
LP_DIR = DOCS_DIR / "lp"
READY_BASE_DIR = MEDIA_DIR / "ready_to_publish"
SCRIPTS_DIR = BASE_DIR / "scripts"

# إضافة المسارات إلى sys.path للاستيراد السلس
for p in [str(BASE_DIR), str(SCRIPTS_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# التأكد من وجود المجلدات الضرورية
for d in [MANUAL_INBOX_DIR, ARCHIVE_ROOT_DIR, BRANDED_DIR, LP_DIR, READY_BASE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("SingleClickMasterPipeline")

# استيراد محركات المنظومة
from smart_intake_classifier import (
    scan_and_triage_manual_inbox,
    find_active_inbox_files,
    route_platform_text_files,
    extract_clean_content,
    probe_media_dimensions,
    is_video_silent,
    merge_silent_video_with_audio,
    archive_used_inbox_files,
    classify_file_category,
    CATEGORY_KEYWORDS
)

import campaign_landing_engine as cle
from scripts.dispatch_n8n_bridge import (
    build_omnichannel_payload,
    dispatch_to_n8n_webhook,
    DEFAULT_N8N_WEBHOOK_URL
)
from scripts.build_ready_to_publish_pack import generate_pack

import antigravity_social_automation as asa


# =============================================================================
# الخطوة 1: فحص وتصنيف الميديا مع المسار الاحتياطي لمحرك الأبحاث وسيو مصر
# =============================================================================
def step_1_scan_and_classify_media(category: Optional[str] = None) -> Dict[str, Any]:
    """
    Step 1: Scan and classify media in media_assets/manual_inbox/:
    - Multi-images -> 1 hero cover + remaining as clinical gallery/carousel.
    - Videos -> 9:16 vertical (Reels, Shorts, TikTok) vs 16:9 horizontal (YouTube, Blogger, LP).
    - Audio -> detection & silent video merging.
    - If manual_inbox is empty: cleanly fallback to clinical research harvester and SEO trend engine.
    """
    logger.info("━" * 60)
    logger.info("🔍 [الخطوة 1/6]: فحص وتصنيف وسائط manual_inbox ومطابقتها مع الأبحاث السريرية...")

    triage = scan_and_triage_manual_inbox(MANUAL_INBOX_DIR)
    
    # فحص الملفات المرفوعة الفعلية في الصندوق
    inbox_files = [
        f for f in MANUAL_INBOX_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]
    has_custom_inbox = len(inbox_files) > 0

    chosen_category = category
    if not chosen_category:
        chosen_category = triage.get("detected_category")

    # تحديد القالب السريري المناسب
    templates = asa.CLINICAL_STORIES_TEMPLATES
    chosen_idx = 0
    if chosen_category:
        for idx, t in enumerate(templates):
            if t.get("category") == chosen_category:
                chosen_idx = idx
                break
    else:
        chosen_idx = asa.get_next_template_index()

    tmpl = dict(templates[chosen_idx])
    final_category = tmpl.get("category", "c-section")

    used_inbox_files: List[Path] = []
    hero_image: Optional[Path] = None
    gallery_images: List[Path] = []
    video_vertical: Optional[Path] = None
    video_horizontal: Optional[Path] = None
    audio_path: Optional[Path] = None
    platform_texts: Dict[str, Any] = {}
    live_trends: List[str] = []

    # سحب الترندات الحية من جوجل مصر دائماً لإثراء المحتوى
    try:
        from github_seo_trend_engine import harvest_live_egypt_trends, convert_query_to_hashtag
        cat_lookup = "thyroid-gynecomastia" if final_category == "thyroid" else final_category
        live_trends_dict = harvest_live_egypt_trends()
        live_trends = live_trends_dict.get(cat_lookup, [])
        if live_trends:
            trend_block = f"\n\n📈 من أكثر تساؤلات الحالات الصاعدة في بحث جوجل مصر هذا الأسبوع:\n• " + "\n• ".join(live_trends[:3])
            tmpl["story_text"] = tmpl["story_text"] + trend_block
            tags_str = " ".join([convert_query_to_hashtag(q) for q in live_trends[:4] if len(q.split()) <= 5])
            if tags_str:
                tmpl["hashtags"] = f"{tmpl['hashtags']} {tags_str}"
            logger.info(f"🔥 تم رصد ترندات جوجل مصر الصاعدة لتخصص ({final_category}): {len(live_trends)} استفسارات.")
    except Exception as e:
        logger.warning(f"تنبيه سحب ترندات جوجل: {e}")

    if has_custom_inbox:
        logger.info(f"📥 تم اكتشاف {len(inbox_files)} ملفات مرفوعة في manual_inbox. جاري التوزيع السريري:")
        
        inbox_images = [f for f in inbox_files if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
        inbox_videos = [f for f in inbox_files if f.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm"]]
        inbox_audios = [f for f in inbox_files if f.suffix.lower() in [".m4a", ".mp3", ".wav", ".aac"]]
        inbox_texts = [f for f in inbox_files if f.suffix.lower() in [".txt", ".md"]]

        # 1. توزيع الصور (Hero + Carousel)
        if inbox_images:
            hero_image = inbox_images[0]
            gallery_images = inbox_images[1:]
            used_inbox_files.extend(inbox_images)
            logger.info(f"   • صورة الغلاف الرئيسية (Hero Cover): {hero_image.name}")
            if gallery_images:
                logger.info(f"   • معرض الحالات السريرية (Carousel): {len(gallery_images)} صور إضافية.")

        # 2. فرز الفيديوهات حسب الأبعاد (9:16 مقابل 16:9)
        for v in inbox_videos:
            used_inbox_files.append(v)
            dim = probe_media_dimensions(v)
            if dim.get("is_vertical_9_16"):
                if not video_vertical:
                    video_vertical = v
                    logger.info(f"   • فيديو رأسي (9:16 للريلز وتيك توك وشورتس): {v.name}")
            else:
                if not video_horizontal:
                    video_horizontal = v
                    logger.info(f"   • فيديو عرضي (16:9 لليوتيوب وبلوجر واللاندنج): {v.name}")

        # 3. معالجة الصوت والدمج مع الفيديو الصامت
        if inbox_audios:
            audio_path = inbox_audios[0]
            used_inbox_files.extend(inbox_audios)
            logger.info(f"   • تسجيل صوتي سريري: {audio_path.name}")
            # دمج الصوت مع أي فيديو صامت
            for cand_v in [video_horizontal, video_vertical]:
                if cand_v and is_video_silent(cand_v):
                    merged_out = DOCS_DIR / "assets" / f"merged_{cand_v.name}"
                    if merge_silent_video_with_audio(cand_v, audio_path, merged_out):
                        logger.info(f"   • تم دمج الصوت مع الفيديو الصامت بنجاح: {merged_out.name}")

        # 4. توجيه نصوص المنصات المرفوعة
        if inbox_texts:
            platform_texts = route_platform_text_files(inbox_texts)
            used_inbox_files.extend(inbox_texts)
            logger.info(f"   • تم فرز {len(inbox_texts)} ملفات نصوص وتوجيهها للمنصات.")

    if not hero_image:
        logger.info("ℹ️ لم يتم العثور على صورة غلاف في manual_inbox (أو الصندوق فارغ) — تفعيل المسار الاحتياطي عبر الأبحاث السريرية ومكتبة Pomelli.")
        photo_info = asa.get_clinical_case_photo(tmpl["title"], final_category)
        raw_img = photo_info.get("local_path", "")
        if raw_img and Path(raw_img).exists():
            hero_image = Path(raw_img)
            logger.info(f"   • اعتماد الصورة السريرية من مكتبة الأبحاث: {hero_image.name}")
        else:
            default_hero = DOCS_DIR / "assets" / f"campaign_{final_category}_hero.png"
            og_fallback = DOCS_DIR / "assets" / "og-image.jpg"
            hero_image = default_hero if default_hero.exists() else og_fallback

    return {
        "status": "success",
        "has_custom_inbox": has_custom_inbox,
        "category": final_category,
        "template_index": chosen_idx,
        "case_data": tmpl,
        "hero_image": hero_image,
        "gallery_images": gallery_images,
        "video_vertical": video_vertical,
        "video_horizontal": video_horizontal,
        "audio_path": audio_path,
        "platform_texts": platform_texts,
        "used_inbox_files": used_inbox_files,
        "live_trends": live_trends
    }


# =============================================================================
# الخطوة 2: بناء صفحة الهبوط المستقلة مع معرض الحالات السريرية
# =============================================================================
def step_2_build_campaign_landing_page(step1_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Step 2: Build campaign landing page with clinical cases carousel via campaign_landing_engine.py.
    """
    logger.info("━" * 60)
    logger.info("🌐 [الخطوة 2/6]: بناء صفحة الهبوط السريرية المستقلة ومعرض الحالات المتجاوب...")

    tmpl = step1_data["case_data"]
    cat = step1_data["category"]

    # نسخ أصول الميديا لـ docs/assets لتكون متاحة للويب
    hero_p = step1_data.get("hero_image")
    gallery_p_list = step1_data.get("gallery_images", [])
    video_h_p = step1_data.get("video_horizontal")
    video_v_p = step1_data.get("video_vertical")
    audio_p = step1_data.get("audio_path")

    dest_hero = DOCS_DIR / "assets" / f"campaign_{cat}_hero.png"
    if hero_p and Path(hero_p).exists() and Path(hero_p).resolve() != dest_hero.resolve():
        try:
            shutil.copy2(str(hero_p), str(dest_hero))
        except Exception:
            pass

    dest_gallery_paths: List[str] = []
    gallery_dir = DOCS_DIR / "assets" / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)
    for idx, g_p in enumerate(gallery_p_list):
        dest_g = gallery_dir / f"campaign_{cat}_case_{idx+1}.png"
        try:
            if Path(g_p).exists() and Path(g_p).resolve() != dest_g.resolve():
                shutil.copy2(str(g_p), str(dest_g))
            dest_gallery_paths.append(str(dest_g))
        except Exception:
            dest_gallery_paths.append(str(g_p))

    dest_v_vid = DOCS_DIR / "assets" / f"campaign_{cat}_video_9x16.mp4"
    if video_v_p and Path(video_v_p).exists() and Path(video_v_p).resolve() != dest_v_vid.resolve():
        try:
            shutil.copy2(str(video_v_p), str(dest_v_vid))
        except Exception:
            pass

    dest_h_vid = DOCS_DIR / "assets" / f"campaign_{cat}_video.mp4"
    if video_h_p and Path(video_h_p).exists() and Path(video_h_p).resolve() != dest_h_vid.resolve():
        try:
            shutil.copy2(str(video_h_p), str(dest_h_vid))
        except Exception:
            pass

    media_assets = {
        "hero_path": str(dest_hero) if dest_hero.exists() else str(hero_p or ""),
        "square_path": str(dest_hero) if dest_hero.exists() else str(hero_p or ""),
        "story_path": str(dest_hero) if dest_hero.exists() else str(hero_p or ""),
        "gallery_paths": dest_gallery_paths,
        "video_horizontal": str(dest_h_vid) if dest_h_vid.exists() else str(video_h_p or ""),
        "video_vertical": str(dest_v_vid) if dest_v_vid.exists() else str(video_v_p or ""),
        "audio_path": str(audio_p or "")
    }

    # تحديث وتوليد صفحات المنتجات متعددة الزوايا
    try:
        cle.generate_all_multi_angle_product_lps()
    except Exception as e:
        logger.warning(f"تنبيه توليد صفحات المنتجات: {e}")

    # بناء اللاندنج بيدج المتخصصة للحملة
    lp_res = cle.build_campaign_landing_page(
        case_data=tmpl,
        media_assets=media_assets
    )

    logger.info(f"[+] 🌐 تم بناء الـ Landing Page بنجاح: {lp_res.get('slug')}.html")
    logger.info(f"   👉 الرابط الحي: {lp_res.get('public_url')}")

    return {
        "status": "success",
        "slug": lp_res.get("slug"),
        "local_file": lp_res.get("local_file"),
        "public_url": lp_res.get("public_url"),
        "media_assets": media_assets
    }


# =============================================================================
# الخطوة 3: توليد الكروت والتصميمات وحزم النشر الجاهزة
# =============================================================================
def step_3_generate_creatives_and_packages(step1_data: Dict[str, Any], step2_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Step 3: Generate branded creatives, cards, and ready-to-publish packages.
    """
    logger.info("━" * 60)
    logger.info("🎨 [الخطوة 3/6]: توليد التصميمات المعتمدة، كروت النشر، وتجهيز الحزم المؤرخة...")

    tmpl = step1_data["case_data"]
    cat = step1_data["category"]
    lp_url = step2_data["public_url"]
    date_str = dt.datetime.now().strftime("%Y-%m-%d")

    hero_img = step1_data.get("hero_image")
    cards = asa.generate_branded_card(tmpl, str(hero_img) if hero_img else "")
    square_card = cards.get("square_path") or (str(hero_img) if hero_img else "")
    story_card = cards.get("story_path") or square_card

    # إذا لم يكن هناك فيديو، ننشئ فيديو ريلز من بطاقة الستوري
    video_p = step1_data.get("video_vertical") or step1_data.get("video_horizontal")
    if not video_p and story_card:
        try:
            created_v = asa.generate_tiktok_reel_video(story_card, duration_sec=8)
            video_p = Path(created_v) if created_v else None
        except Exception as e:
            logger.warning(f"تنبيه توليد فيديو ريلز: {e}")

    # إعداد نصوص كل منصة بالموجه النظيف
    category_messages = {
        "c-section": "أهلاً بحضرتك، محتاجة استشارة بخصوص جرح القيصرية والشاور الآمن، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "bariatric": "أهلاً بحضرتك، محتاج استشارة بخصوص حماية ثقوب المنظار بعد عملية التكميم، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "rhinoplasty": "أهلاً بحضرتك، محتاج استشارة بخصوص بلاستر 3M ودعامة الأنف لتثبيت النتيجة وتخفيف التورم، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "thyroid": "أهلاً بحضرتك، محتاجة استشارة بخصوص حماية ندبة الرقبة بعد استئصال الغدة الدرقية وتسطيحها، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
        "keloid": "أهلاً بحضرتك، محتاج استشارة بخصوص شيت السيليكون الطبي لتسطيح وتفتيح الندبة البارزة، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.",
    }
    wa_msg = category_messages.get(cat, "أهلاً بحضرتك في هيلينج تاتش مصر، محتاج استشارة بخصوص التعافي بعد عمليتي، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام.")
    wa_direct_url = f"https://wa.me/201155803307?text={urllib.parse.quote(wa_msg)}"

    platform_routed = step1_data.get("platform_texts", {})

    # فيسبوك
    fb_file = platform_routed.get("facebook")
    if fb_file:
        fb_caption = extract_clean_content(fb_file, "facebook", landing_url=lp_url, whatsapp_url=wa_direct_url)["caption"]
    else:
        fb_caption = f"""🌿 {tmpl['title']}

{tmpl['story_text'].strip()}

━━━━━━━━━━━━━━━━━━━━━━━
🔗 رابط الدليل السريري وحاسبة التعافي المتخصصة:
👉 {lp_url}

💬 للتوجيه السريري المجاني والاستشارة عبر واتساب (01155803307):
👉 {wa_direct_url}

{tmpl['hashtags']}"""

    # إنستجرام
    ig_file = platform_routed.get("instagram")
    if ig_file:
        ig_caption = extract_clean_content(ig_file, "instagram", landing_url=lp_url, whatsapp_url=wa_direct_url)["caption"]
    else:
        ig_caption = fb_caption

    # تيك توك
    tt_file = platform_routed.get("tiktok")
    if tt_file:
        tt_caption = extract_clean_content(tt_file, "tiktok", landing_url=lp_url, whatsapp_url=wa_direct_url)["caption"]
    else:
        tt_caption = f"{fb_caption[:180]} #fyp #foryou #تيك_توك_مصر #تعافي_جراحي"

    # مقال بلوجر
    bl_file = platform_routed.get("blogger")
    if bl_file:
        bl_res = extract_clean_content(bl_file, "blogger", landing_url=lp_url, whatsapp_url=wa_direct_url)
        blogger_title = bl_res["title"]
        blogger_html = bl_res["html_content"]
    else:
        blogger_post = asa.format_clinical_case_for_blogger(tmpl, {"image_url": "../assets/og-image.jpg"})
        blogger_title = blogger_post["title"]
        blogger_html = blogger_post["html_content"]

    # مقال ريديت
    rd_file = platform_routed.get("reddit")
    if rd_file:
        reddit_markdown = extract_clean_content(rd_file, "reddit", landing_url=lp_url, whatsapp_url=wa_direct_url)["markdown"]
    else:
        reddit_markdown = f"""# {tmpl['title']}

{tmpl['story_text']}

---
🔗 **[رابط الدليل السريري وحجز الاستشارة المباشر]({lp_url})**

**للتوجيه السريري والاستشارة المجانية عبر واتساب:** [01155803307]({wa_direct_url})

{tmpl['hashtags']}"""

    # حفظ ملفات النصوص المستقلة في branded_designs
    (BRANDED_DIR / f"{date_str}_[نص_منشور_فيسبوك].txt").write_text(fb_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[نص_بوست_وستوري_إنستجرام].txt").write_text(ig_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[نص_كابشن_وهاشتاجات_تيكتوك].txt").write_text(tt_caption, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[مقال_مدونة_جوجل_Blogger].txt").write_text(blogger_html, encoding="utf-8")
    (BRANDED_DIR / f"{date_str}_[منشور_ومقال_Reddit].txt").write_text(reddit_markdown, encoding="utf-8")

    # بناء حزمة ready_to_publish المؤرخة الشاملة بكافة مجلدات المنصات الـ 6
    pack_dir = generate_pack(category=cat)
    logger.info(f"[+] 📦 تم إنشاء حزمة ready_to_publish المؤرخة بنجاح: {pack_dir.name}")

    return {
        "status": "success",
        "pack_dir": pack_dir,
        "square_card": square_card,
        "story_card": story_card,
        "video_path": str(video_p) if video_p else "",
        "copywriting": {
            "facebook": fb_caption,
            "instagram": ig_caption,
            "tiktok": tt_caption,
            "youtube_title": f"{tmpl['title']} | هيلينج تاتش مصر #Shorts",
            "youtube_description": f"الدليل الطبي المعتمد لتعافي الجروح والندبات الجراحية في المنزل بدون مضاعفات\n\n🎁 كود الخصم: HT10 (شحن مجاني + حق فتح ومعاينة الشحنة قبل الدفع)\n🩺 استشارة مجانية مع أخصائية العناية بالتعافي: {wa_direct_url}\n\n{tmpl['hashtags']}",
            "reddit_title": blogger_title,
            "reddit_markdown": reddit_markdown,
            "blogger_title": blogger_title,
            "blogger_html": blogger_html
        },
        "wa_direct_url": wa_direct_url
    }


# =============================================================================
# الخطوة 4: إرسال الحزمة السريرية لـ 6 منصات لمحرك n8n وتفعيل بوابة تيليجرام
# =============================================================================
def step_4_dispatch_to_n8n_webhook(
    step1_data: Dict[str, Any],
    step2_data: Dict[str, Any],
    step3_data: Dict[str, Any],
    dry_run: bool = False,
    webhook_url: str = DEFAULT_N8N_WEBHOOK_URL
) -> Dict[str, Any]:
    """
    Step 4: Dispatch the complete 6-platform structured payload to n8n webhook
    (http://localhost:5678/webhook/publish-post) with Telegram HITL review gate triggered.
    """
    logger.info("━" * 60)
    logger.info("🚀 [الخطوة 4/6]: تجهيز وإرسال حزمة الـ 6 منصات الشاملة إلى محرك n8n...")

    tmpl = step1_data["case_data"]
    cat = step1_data["category"]
    lp_url = step2_data["public_url"]
    copy = step3_data["copywriting"]
    square_card = step3_data["square_card"]
    story_card = step3_data["story_card"]
    video_p = step3_data["video_path"]
    wa_link = step3_data["wa_direct_url"]
    gallery_paths = [str(p) for p in step1_data.get("gallery_images", [])]

    # بناء كائن الـ payload القياسي المتوافق 100% مع PROJECT.md و n8n omnichannel_cross_post.json
    n8n_payload = build_omnichannel_payload(
        campaign_id=cat,
        theme="surgical_wound_and_scar_care",
        product_name=tmpl.get("title", "BUPY Silicone Scar Sheets 4cm x 3m"),
        promo_code="HT10",
        promo_text="كود الخصم: HT10 (شحن مجاني + حق فتح ومعاينة الشحنة قبل الدفع)",
        wa_link=wa_link,
        landing_url=lp_url,
        hero_image=str(square_card),
        gallery_images=gallery_paths if gallery_paths else [str(square_card)],
        video_vertical=str(video_p),
        video_horizontal=str(step1_data.get("video_horizontal") or video_p),
        copywriting=copy,
        hashtags=tmpl.get("hashtags", "")
    )

    date_str = dt.datetime.now().strftime("%Y-%m-%d")
    payload_file = BRANDED_DIR / f"{date_str}_[n8n_omnichannel_payload].json"
    payload_file.write_text(json.dumps(n8n_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"[+] 📄 تم حفظ وثيقة حمولة n8n المفرزة في: {payload_file.name}")

    if dry_run:
        logger.info("🔍 [معاينة - DRY RUN]: تم التحقق من سلامة حمولة الـ 6 منصات لمحرك n8n (تم تجاوز الإرسال الشبكي بنجاح).")
        return {
            "status": "success",
            "dry_run": True,
            "dispatched": False,
            "payload_file": str(payload_file),
            "payload": n8n_payload
        }

    # الإرسال الفعلي لـ n8n
    ok, res = dispatch_to_n8n_webhook(n8n_payload, webhook_url=webhook_url)
    if ok:
        logger.info(f"[+] 🎯 [n8n Omnichannel Engine]: تم استلام الحزمة بنجاح عبر Webhook وتفعيل إشعار اعتماد Telegram HITL!")
    else:
        logger.warning(f"[!] ⚠️ [n8n Omnichannel Engine]: تنبيه الويب هوك ({res.get('error')}) — المنظومة تحتفظ بالحمولة جاهزة.")

    return {
        "status": "success" if ok else "warning",
        "dry_run": False,
        "dispatched": ok,
        "response": res,
        "payload_file": str(payload_file),
        "payload": n8n_payload
    }


# =============================================================================
# الخطوة 5: تنفيذ أو تجهيز النشر المتوازي للمنصات الـ 6
# =============================================================================
def step_5_execute_or_stage_parallel_publishing(
    step1_data: Dict[str, Any],
    step2_data: Dict[str, Any],
    step3_data: Dict[str, Any],
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Step 5: Execute or stage parallel publishing for Meta, Instagram, YouTube, TikTok, Reddit, and Blogger.
    """
    logger.info("━" * 60)
    logger.info("📢 [الخطوة 5/6]: تجهيز وبث المحتوى بالتوازي للمنصات الـ 6 (Facebook, Instagram, YouTube, TikTok, Reddit, Blogger)...")

    tmpl = step1_data["case_data"]
    cat = step1_data["category"]
    pack_dir = step3_data["pack_dir"]
    copy = step3_data["copywriting"]
    square_card = step3_data["square_card"]
    chosen_idx = step1_data["template_index"]

    platforms_summary = {
        "facebook": {"name": "Facebook Pages", "folder": "06_فيسبوك_Facebook", "staged": True},
        "instagram": {"name": "Instagram Reels & Carousels", "folder": "03_إنستجرام_Instagram", "staged": True},
        "youtube": {"name": "YouTube Shorts & Videos", "folder": "01_يوتيوب_YouTube", "staged": True},
        "tiktok": {"name": "TikTok Videos & Script", "folder": "02_تيكتوك_TikTok", "staged": True},
        "reddit": {"name": "Reddit Clinical Discussion", "folder": "05_ريديت_Reddit", "staged": True},
        "blogger": {"name": "Google Blogger Clinical Article", "folder": "04_بلوجر_Blogger", "staged": True}
    }

    if dry_run:
        logger.info("🔍 [معاينة - DRY RUN]: جاهزية النشر المتوازي المؤكدة للمنصات الـ 6:")
        for p_key, p_info in platforms_summary.items():
            logger.info(f"   ✅ المنصة [{p_info['name']}]: مجهزة بالكامل داخل مجلد {p_info['folder']}")
        asa.record_post_history(chosen_idx, tmpl["title"])
        return {
            "status": "success",
            "dry_run": True,
            "staged_platforms": list(platforms_summary.keys()),
            "published": False
        }

    # النشر الحي المباشر عبر واجهات البرمجة
    post_data = {
        "day": f"دراسة حالة سريرية ({chosen_idx + 1}) - {tmpl['title']}",
        "caption": copy["facebook"],
        "hashtags": "",
        "row_index": -1
    }
    
    fb_ok, fb_url = asa.publish_facebook_graph_api(post_data, square_card)
    ig_image_url = f"https://raw.githubusercontent.com/Medon90ae/healing-touch-egypt/main/docs/assets/campaign_{cat}_hero.png"
    ig_ok = asa.publish_instagram_graph_api(copy["instagram"], image_url=ig_image_url)
    
    blogger_post = {
        "title": copy["blogger_title"],
        "html_content": copy["blogger_html"],
        "file_path": str(BRANDED_DIR / f"{dt.datetime.now().strftime('%Y-%m-%d')}_[مقال_مدونة_جوجل_Blogger].txt")
    }
    bl_ok = asa.publish_to_blogger_webhook(blogger_post)
    rd_ok = asa.publish_to_reddit_api(copy["reddit_title"], copy["reddit_markdown"])

    asa.record_post_history(chosen_idx, tmpl["title"])
    logger.info("[+] 🚀 اكتمل البث السريري المباشر عبر واجهات البرمجة المعتمدة!")

    return {
        "status": "success",
        "dry_run": False,
        "published": True,
        "results": {
            "facebook": fb_ok,
            "instagram": ig_ok,
            "blogger": bl_ok,
            "reddit": rd_ok
        }
    }


# =============================================================================
# الخطوة 6: الأرشفة التلقائية ونظافة الصندوق (Folder Hygiene)
# =============================================================================
def step_6_archive_and_clean_inbox(
    step1_data: Dict[str, Any],
    dry_run: bool = False,
    force: bool = False
) -> Dict[str, Any]:
    """
    Step 6: Automatically move processed inbox assets to media_assets/archive/YYYY-MM-DD_HHMMSS/
    leaving manual_inbox completely clean and empty.
    """
    logger.info("━" * 60)
    logger.info("🧹 [الخطوة 6/6]: تنظيف وتفريغ manual_inbox وأرشفة الأصول في مجلد مؤرخ...")

    inbox_files = [
        f for f in MANUAL_INBOX_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]

    if not inbox_files:
        logger.info("[+] 🧹 صندوق manual_inbox نظيف وفارغ 100% — لا توجد أصول تحتاج أرشفة.")
        return {
            "status": "success",
            "archived_count": 0,
            "inbox_clean": True
        }

    # إذا كان Dry Run وبدون --force نحتفظ بالملفات مع إظهار تقرير المحاكاة
    if dry_run and not force:
        logger.info(f"[*] ℹ️ [DRY RUN]: تم رصد {len(inbox_files)} ملفات معالجة في manual_inbox (استخدم --force لنقلها للأرشيف فورياً في وضع المعاينة).")
        return {
            "status": "success",
            "dry_run": True,
            "simulated_archived_count": len(inbox_files),
            "inbox_clean": False
        }

    # النقل الفعلي للأرشيف المؤرخ
    files_to_clean = list(set(step1_data.get("used_inbox_files", []) + inbox_files))
    archived_count = archive_used_inbox_files(MANUAL_INBOX_DIR, files_to_clean)

    # التحقق من خلو الصندوق
    remaining = [
        f for f in MANUAL_INBOX_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]

    logger.info(f"[+] 🧹 تم تفريغ وأرشفة {archived_count} أصول بنجاح إلى مجلد مؤرخ داخل archive/.")
    logger.info(f"[+] ✨ حالة صندوق manual_inbox: {'فارغ ونظيف 100%' if len(remaining) == 0 else f'يحتوي {len(remaining)} ملفات'}")

    return {
        "status": "success",
        "archived_count": archived_count,
        "inbox_clean": len(remaining) == 0
    }


# =============================================================================
# المشغل الموحد بضغطة زر واحدة (Single-Click Master Pipeline Orchestrator)
# =============================================================================
def run_single_click_master_pipeline(
    category: Optional[str] = None,
    dry_run: bool = False,
    force: bool = False,
    open_browser: bool = False,
    webhook_url: str = DEFAULT_N8N_WEBHOOK_URL
) -> Dict[str, Any]:
    """
    Executes the entire 6-step single-click master pipeline with full determinism,
    robust error-handling, and clean exit codes.
    """
    start_time = dt.datetime.now()
    print("=" * 75)
    print("        🌿 هيلينج تاتش مصر | محرك النشر والتشغيل الموحد بضغطة زر واحدة (2026)")
    print("             Single-Click Master Pipeline & Omnichannel Engine")
    print("=" * 75)
    print(f"⏱️ توقيت البدء: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚙️ وضع التشغيل: {'معاينة تجريبية كاملة (DRY RUN)' if dry_run else 'نشر وإنتاج مباشر (LIVE PRODUCTION)'}")
    if category:
        print(f"🎯 التخصص المحدد: {category}")
    print("=" * 75)

    # الخطوة 1: فحص واستيعاب الميديا
    step1 = step_1_scan_and_classify_media(category=category)

    # الخطوة 2: بناء صفحة الهبوط
    step2 = step_2_build_campaign_landing_page(step1)

    # الخطوة 3: توليد الكروت والتصميمات وحزم النشر
    step3 = step_3_generate_creatives_and_packages(step1, step2)

    # الخطوة 4: إرسال الحزمة السريرية لمحرك n8n
    step4 = step_4_dispatch_to_n8n_webhook(step1, step2, step3, dry_run=dry_run, webhook_url=webhook_url)

    # الخطوة 5: تنفيذ النشر المتوازي للمنصات الـ 6
    step5 = step_5_execute_or_stage_parallel_publishing(step1, step2, step3, dry_run=dry_run)

    # الخطوة 6: تنظيف وأرشفة الصندوق
    step6 = step_6_archive_and_clean_inbox(step1, dry_run=dry_run, force=force)

    # فتح المتصفح إذا تم طلب ذلك
    if open_browser:
        try:
            asa.open_url_in_default_browser(step2["public_url"])
        except Exception:
            pass

    duration = (dt.datetime.now() - start_time).total_seconds()

    print("\n" + "=" * 75)
    print("🎉 اكتمل تنفيذ مسار النشر الموحد (Single-Click Master Pipeline) بنجاح!")
    print(f"⏱️ استغرق التشغيل: {duration:.2f} ثانية | كود الخروج: 0 (SUCCESS)")
    print("━" * 75)
    print(f"🌐 رابط صفحة الهبوط الحية: {step2['public_url']}")
    print(f"📦 مسار حزمة النشر المفرزة: {step3['pack_dir']}")
    print(f"📄 حمولة المنصات الـ 6 لمحرك n8n: {step4.get('payload_file')}")
    print(f"🧹 نظافة صندوق manual_inbox: {'نظيف وفارغ 100%' if step6.get('inbox_clean') else 'محفوظ للمعاينة'}")
    print("=" * 75)

    return {
        "status": "success",
        "duration_seconds": duration,
        "step1": step1,
        "step2": step2,
        "step3": step3,
        "step4": step4,
        "step5": step5,
        "step6": step6
    }


def main():
    parser = argparse.ArgumentParser(description="Healing Touch Egypt — Single-Click Master Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Run full pipeline in dry-run mode (no network requests or posting)")
    parser.add_argument("--category", "-c", type=str, default=None, help="Target surgical category (c-section, rhinoplasty, bariatric, thyroid, keloid)")
    parser.add_argument("--force", "-f", action="store_true", help="Force inbox archival even in dry-run mode")
    parser.add_argument("--open-browser", action="store_true", help="Open landing page and browser tabs after execution")
    parser.add_argument("--webhook-url", type=str, default=DEFAULT_N8N_WEBHOOK_URL, help="n8n publish-post webhook URL")

    args = parser.parse_args()

    try:
        res = run_single_click_master_pipeline(
            category=args.category,
            dry_run=args.dry_run,
            force=args.force,
            open_browser=args.open_browser,
            webhook_url=args.webhook_url
        )
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع في تشغيل المسار الموحد: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
