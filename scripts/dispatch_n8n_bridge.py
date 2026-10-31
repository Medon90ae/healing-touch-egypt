#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/dispatch_n8n_bridge.py
Omnichannel Python-to-n8n Webhook Bridge for Healing Touch Egypt.

Interface Contract:
- Target Endpoint: POST http://localhost:5678/webhook/publish-post
- Headers: {"Content-Type": "application/json; charset=utf-8"}
- Dispatches 6-platform structured JSON payload:
  * Meta Pages: Facebook Photo + Facebook Reels
  * Instagram: Reels + Carousels
  * YouTube: Shorts + Channel Video (16:9)
  * TikTok: Direct Auto-Posting / Staged Asset Package
  * Reddit: Clinical Discussion Post with Markdown Formatting
  * Blogger: Formatted Clinical Article with HTML Tables & SEO Tags
"""

import argparse
import datetime as dt
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("n8n_dispatch_bridge")

DEFAULT_N8N_WEBHOOK_URL = os.getenv("N8N_PUBLISH_WEBHOOK_URL", "http://localhost:5678/webhook/publish-post")
DEFAULT_PROMO_CODE = "HT10"
DEFAULT_PROMO_TEXT = "كود الخصم: HT10 (شحن مجاني + حق فتح ومعاينة الشحنة قبل الدفع)"


def build_omnichannel_payload(
    campaign_id: str,
    theme: str = "surgical_wound_and_scar_care",
    product_name: str = "BUPY Silicone Scar Sheets 4cm x 3m",
    promo_code: str = DEFAULT_PROMO_CODE,
    promo_text: Optional[str] = None,
    wa_link: Optional[str] = None,
    landing_url: Optional[str] = None,
    hero_image: Optional[str] = None,
    gallery_images: Optional[List[str]] = None,
    video_vertical: Optional[str] = None,
    video_horizontal: Optional[str] = None,
    copywriting: Optional[Dict[str, str]] = None,
    hashtags: Optional[str] = None,
    reddit_subreddit: str = "r/Egypt",
    blogger_labels: Optional[List[str]] = None,
    target_platforms: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Constructs the standard 6-platform structured JSON payload adhering to the
    specification in PROJECT.md and n8n omnichannel_cross_post.json.
    """
    if promo_text is None:
        promo_text = f"كود الخصم: {promo_code} (شحن مجاني + حق فتح ومعاينة الشحنة قبل الدفع)"
    if wa_link is None:
        wa_link = f"https://medon90ae.github.io/healing-touch-egypt/wa.html?case={campaign_id}"
    if landing_url is None:
        landing_url = f"https://medon90ae.github.io/healing-touch-egypt/lp/{campaign_id}.html"

    copy = copywriting or {}
    tags = hashtags or "#ولادة_قيصرية_مصر #جرح_القيصرية #علاج_الندبات #شيت_سيليكون_بوبي #ضمادات_تيجاديرم #هيلينج_تاتش_مصر"

    # Default platform texts
    fb_text = copy.get("facebook") or copy.get("text") or "بروتوكول العناية الجراحية بالندبات وتأمين الاستحمام الآمن بعد الجراحة"
    ig_text = copy.get("instagram") or copy.get("text") or "خطوات سريرية معتمدة للتعافي بعد الجراحة وتسطيح الندبات"
    tt_text = copy.get("tiktok") or f"{fb_text[:140]} #fyp #foryou #تيك_توك_مصر #تعافي_جراحي"
    yt_shorts_title = copy.get("youtube_title") or f"بروتوكول تسطيح وتجميل الندبات بعد الجراحة | هيلينج تاتش مصر #Shorts"
    if "#Shorts" not in yt_shorts_title:
        yt_shorts_title = f"{yt_shorts_title} #Shorts"
    yt_video_title = yt_shorts_title.replace("#Shorts", "").strip()
    yt_desc = copy.get("youtube_description") or f"الدليل الطبي المعتمد لتعافي الجروح والندبات الجراحية في المنزل بدون مضاعفات\n\n🎁 {promo_text}\n🩺 استشارة مجانية مع أخصائية العناية بالتعافي: {wa_link}\n\n{tags}"

    rd_title = copy.get("reddit_title") or f"الدليل السريري الموثق للتعافي بعد الجراحة والعناية بالندبات | هيلينج تاتش مصر"
    rd_md = copy.get("reddit_markdown") or f"""# الدليل السريري للتعافي الجراحي والعناية بالندبات

تعتبر فترة ما بعد العمليات الجراحية مرحلة دقيقة تتطلب الالتزام بالتوجيهات السريرية المعتمدة لضمان التئام الجرح دون مضاعفات أو تشكل ندبات متضخمة.

## الإرشادات السريرية الأساسية:
1. الحفاظ على بيئة جرح نظيفة ورطبة باستخدام ضمادات السيليكون الطبية المعتمدة فور التئام حواف الجرح.
2. تجنب تعريض الجرح للشد الميكانيكي أو أشعة الشمس المباشرة خلال الأشهر الأولى.
3. الاستعانة بالضمادات المانعة للماء لتأمين الاستحمام الصحي بدون رطوبة مباشرة على الجرح.

🎁 **{promo_text}**

🩺 **للحصول على استشارة مجانية مباشرة مع أخصائية العناية بالتعافي:**
👉 [اضغط هنا لفتح المحادثة المباشرة]({wa_link})

---
**المراجع والدراسات السريرية المعتمدة:**
- PubMed Central & International Wound Journal Standards (2024-2026)

{tags}"""

    bl_title = copy.get("blogger_title") or f"الدليل الطبي الشامل: بروتوكول التعافي والعناية بالندبات الجراحية"
    bl_html = copy.get("blogger_html") or f"""<article class="clinical-article" dir="rtl">
<h1>{bl_title}</h1>
<p class="lead-paragraph">بروتوكول سريري استرشادي متقدم يهدف لتوجيه المرضى خلال مراحل التعافي بعد العمليات الجراحية والولادة القيصرية لضمان التئام مثالي ومنع تضخم الندبات.</p>

<table border="1" cellpadding="10" style="width:100%; border-collapse:collapse; margin:20px 0; border:1px solid #d1d5db; font-family:sans-serif;">
  <thead>
    <tr style="background-color:#ecfdf5; color:#065f46;">
      <th style="text-align:right;">الفترة الزمنية للتعافي</th>
      <th style="text-align:right;">التوجيه السريري المعتمد</th>
      <th style="text-align:right;">المنتج الطبي الموصى به</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>الأسبوع 1 إلى 2</td>
      <td>تأمين الحماية الكاملة من الماء والبكتيريا أثناء الاستحمام</td>
      <td>ضمادات 3M Tegaderm +Pad الطبية المقاومة للماء</td>
    </tr>
    <tr>
      <td>الأسبوع 3 إلى 12</td>
      <td>تسطيح الندبة وتوحيد ملمس الجلد بالترطيب الهيدراتي المستمر</td>
      <td>شرائح السيليكون الطبية BUPY Silicone Scar Sheets</td>
    </tr>
  </tbody>
</table>

<div class="cta-panel" style="background:#f0fdf4; border-right:4px solid #10b981; padding:16px; border-radius:8px; margin:24px 0;">
  <h3 style="color:#047857; margin-top:0;">🎁 استشارة مجانية وعرض خاص</h3>
  <p>{promo_text}</p>
  <p><a href="{wa_link}" style="color:#059669; font-weight:bold; text-decoration:underline;">اضغطي هنا للتواصل المباشر مع أخصائية العناية بالتعافي عبر واتساب</a></p>
</div>

<footer style="margin-top:25px; padding-top:15px; border-top:1px solid #e5e7eb; font-size:0.9em; color:#4b5563;">
  <p>الكلمات الدلالية ومحركات البحث السريرية: {tags}</p>
</footer>
</article>"""

    labels = blogger_labels or ["العناية بالجروح", "ندبات القيصرية", "سيو مصر", "HT10", "هيلينج تاتش مصر"]
    hero = hero_image or "https://raw.githubusercontent.com/Medon90ae/healing-touch-egypt/main/docs/assets/og-image.jpg"
    gallery = gallery_images or [hero]
    v_vert = video_vertical or "https://medon90ae.github.io/healing-touch-egypt/assets/video_vertical.mp4"
    v_horiz = video_horizontal or "https://medon90ae.github.io/healing-touch-egypt/assets/video_horizontal.mp4"
    platforms = target_platforms or ["facebook", "instagram", "youtube", "tiktok"]
    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    idempotency_key = f"ht_{campaign_id}_{today_str}"

    payload = {
        "event": "media_pack_ready",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "idempotency_key": idempotency_key,
        "google_flow_project_url": "https://flow.google.com/project/942f62cb-f0e4-4860-bfce-2ba75998cfc7",
        "campaign_id": campaign_id,
        "theme": theme,
        "product_name": product_name,
        "promo_code": promo_code,
        "promo_text": promo_text,
        "wa_link": wa_link,
        "landing_url": landing_url,
        "target_platforms": platforms,
        "system_user_tokens": {
            "fb_page_id": os.getenv("FB_PAGE_ID", "1371809382684781").strip("'\" "),
            "ig_user_id": os.getenv("IG_USER_ID", "27911522148524499").strip("'\" "),
            "meta_permanent_token_configured": bool(os.getenv("META_PERMANENT_PAGE_TOKEN")),
            "ig_permanent_token_configured": bool(os.getenv("INSTAGRAM_ACCESS_TOKEN")),
        },
        "meta_platforms": {
            "facebook_photo": {
                "image_url_or_path": hero,
                "caption": f"{fb_text}\n\n🎁 {promo_text}\n🩺 استشيري أخصائية العناية بالتعافي مجاناً: {wa_link}\n\n{tags}"
            },
            "facebook_reels": {
                "video_url_or_path": v_vert,
                "caption": f"{fb_text}\n\n🎁 {promo_text}\n🩺 استشيري أخصائية العناية بالتعافي مجاناً: {wa_link}\n\n{tags}"
            },
            "instagram_reels": {
                "video_url_or_path": v_vert,
                "caption": f"{ig_text}\n\n🎁 {promo_text}\n🩺 استشيري أخصائية العناية بالتعافي مجاناً: الرابط في البايو أو زوري {wa_link}\n\n{tags}"
            },
            "instagram_carousel": {
                "media_urls": gallery,
                "caption": f"{ig_text}\n\n🎁 {promo_text}\n🩺 استشيري أخصائية العناية بالتعافي مجاناً: الرابط في البايو أو زوري {wa_link}\n\n{tags}"
            }
        },
        "youtube_platforms": {
            "youtube_shorts": {
                "video_path": v_vert,
                "title": yt_shorts_title,
                "description": yt_desc
            },
            "youtube_video": {
                "video_path": v_horiz,
                "title": yt_video_title,
                "description": yt_desc
            }
        },
        "tiktok_platform": {
            "video_path": v_vert,
            "caption": tt_text
        },
        "reddit_platform": {
            "subreddit": reddit_subreddit,
            "title": rd_title,
            "content_markdown": rd_md
        },
        "blogger_platform": {
            "title": bl_title,
            "content_html": bl_html,
            "labels": labels
        },
        "media": {
            "hero_image_url": hero,
            "gallery_image_urls": gallery,
            "video_vertical_url": v_vert,
            "video_horizontal_url": v_horiz,
            "video_vertical_path": "media_assets/branded_designs/latest_reel.mp4"
        },
        "copywriting": {
            "facebook": fb_text,
            "instagram": ig_text,
            "tiktok": tt_text,
            "youtube_title": yt_shorts_title,
            "youtube_description": yt_desc,
            "reddit_title": rd_title,
            "reddit_markdown": rd_md,
            "blogger_title": bl_title,
            "blogger_html": bl_html
        },
        "hashtags": tags
    }
    return payload


def dispatch_to_n8n_webhook(
    payload: Dict[str, Any],
    webhook_url: str = DEFAULT_N8N_WEBHOOK_URL,
    timeout: int = 30
) -> Tuple[bool, Dict[str, Any]]:
    """
    Sends the formatted omnichannel clinical pack to the n8n orchestrator webhook.
    Returns (success: bool, response_dict: dict).
    """
    logger.info("Dispatching 6-platform omnichannel payload to n8n: %s", webhook_url)
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=timeout
        )
        if response.status_code == 200:
            try:
                res_json = response.json()
            except Exception:
                res_json = {"raw": response.text}
            logger.info("n8n webhook responded 200 OK: %s", res_json.get("event", "success"))
            return True, res_json
        logger.warning("n8n webhook returned HTTP %d: %s", response.status_code, response.text[:200])
        return False, {"error": f"HTTP {response.status_code}", "body": response.text}
    except requests.exceptions.ConnectionError as ce:
        logger.error("Failed to connect to n8n webhook at %s: %s", webhook_url, ce)
        return False, {"error": "ConnectionError", "details": str(ce)}
    except requests.exceptions.Timeout as te:
        logger.error("Timeout dispatching to n8n webhook after %ds: %s", timeout, te)
        return False, {"error": "Timeout", "details": str(te)}
    except Exception as e:
        logger.error("Unexpected error during n8n dispatch: %s", e)
        return False, {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Dispatch Omnichannel Pack to n8n Webhook")
    parser.add_argument("--campaign", default="post_op_care", help="Campaign ID (e.g. csection_care, rhinoplasty)")
    parser.add_argument("--product", default="BUPY Silicone Scar Sheets 4cm x 3m", help="Product Name")
    parser.add_argument("--url", default=DEFAULT_N8N_WEBHOOK_URL, help="n8n Webhook URL")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without network request")
    args = parser.parse_args()

    payload = build_omnichannel_payload(
        campaign_id=args.campaign,
        product_name=args.product
    )

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(0)

    ok, res = dispatch_to_n8n_webhook(payload, webhook_url=args.url)
    print(f"Dispatch status: {'SUCCESS' if ok else 'FAILED'}")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
