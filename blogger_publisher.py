#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك النشر على مدونات جوجل (Google Blogger Publisher)
تحويل المقالات والحالات السريرية إلى منشورات بلوجر متوافقة مع SEO والأرشفة الفورية
=============================================================================
"""

import os
import sys
import json
import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
BLOGGER_EXPORT_DIR = BASE_DIR / "media_assets" / "blogger_posts"
BLOGGER_EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def format_clinical_case_for_blogger(case_data: dict, photo_info: dict, branded_img_path: str = "") -> dict:
    """
    تحويل بيانات الحالة السريرية إلى مقال بلوجر فائق التنسيق مع وسم H1/H2/H3 وروابط الـ SEO.
    """
    title = case_data.get("title", "بروتوكول العناية الجراحية")
    cat = case_data.get("category", "c-section")
    raw_story = case_data.get("story_text", "")
    hashtags = case_data.get("hashtags", "")

    # استخراج الوسوم للمدونة (Labels)
    tags_list = [t.replace("#", "").strip() for t in hashtags.split() if t.startswith("#")]
    labels_str = ", ".join(tags_list[:6])

    # تحويل النص لفقرات HTML منسقة
    paragraphs = raw_story.split("\n\n")
    html_paragraphs = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        if p_clean.startswith("١.") or p_clean.startswith("٢.") or p_clean.startswith("٣.") or p_clean.startswith("٤."):
            lines = p_clean.split("\n")
            header = lines[0]
            body = "<br>".join(lines[1:])
            html_paragraphs.append(f"""
            <div style="background:#F0FDF4; border-right:5px solid #10B981; padding:16px 20px; border-radius:10px; margin:16px 0;">
                <h3 style="color:#065F46; margin:0 0 8px 0; font-size:1.15rem;">{header}</h3>
                <p style="color:#1E293B; margin:0; line-height:1.7;">{body}</p>
            </div>
            """)
        elif "واتساب:" in p_clean or "كود" in p_clean:
            continue
        else:
            html_paragraphs.append(f'<p style="color:#334155; font-size:1.05rem; line-height:1.8; margin-bottom:16px;">{p_clean.replace(chr(10), "<br>")}</p>')

    body_html = "\n".join(html_paragraphs)
    tracking_link = f"https://medon90ae.github.io/healing-touch-egypt/wa.html?case={cat}&code=HT10"
    img_tag = f'<div style="text-align:center; margin:24px 0;"><img src="{photo_info.get("image_url", "")}" alt="{title}" style="max-width:100%; border-radius:14px; box-shadow:0 8px 24px rgba(0,0,0,0.12);" /></div>' if photo_info.get("image_url") else ""

    full_html = f"""
    <div dir="rtl" style="font-family:'Cairo', Arial, sans-serif; max-width:800px; margin:auto; background:#ffffff; padding:24px; border-radius:16px; border:1px solid #E2E8F0;">
        <div style="background:#FEF3C7; border:1px dashed #D97706; color:#92400E; padding:8px 18px; border-radius:30px; font-weight:bold; display:inline-block; margin-bottom:16px;">
            🩺 دراسة حالة سريرية | هيلينج تاتش مصر
        </div>
        
        <h1 style="color:#065F46; font-size:1.8rem; line-height:1.4; margin-bottom:20px;">{title}</h1>
        
        {img_tag}
        
        <div class="article-content" style="margin-top:20px;">
            {body_html}
        </div>

        <div style="background:linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border:2px solid #10B981; border-radius:16px; padding:24px; text-align:center; margin-top:32px;">
            <h3 style="color:#065F46; margin-top:0;">هل تحتاجين لاستشارة طبية متخصصة لحالتك؟</h3>
            <p style="color:#047857; margin-bottom:18px;">تواصل الآن مباشرة مع أخصائية العناية بالتعافي للحصول على استشارة مجانية مع تفعيل كود الخصم الحصري <strong>HT10</strong></p>
            <a href="{tracking_link}" target="_blank" style="background:#25D366; color:#ffffff; padding:14px 28px; text-decoration:none; border-radius:12px; font-weight:bold; font-size:1.1rem; display:inline-block; box-shadow:0 4px 14px rgba(37,211,102,0.35);">
                💬 تواصل معنا عبر واتساب الآن
            </a>
            <div style="margin-top:12px; font-size:0.88rem; color:#065F46;">
                🎁 كود HT10 يضمن لك: شحن مجاني لكافة محافظات مصر + حق فتح ومعاينة الشحنة قبل الدفع.
            </div>
        </div>
    </div>
    """

    slug = f"blogger_{cat}_{int(datetime.datetime.now().timestamp())}"
    html_file = BLOGGER_EXPORT_DIR / f"{slug}.html"
    html_file.write_text(full_html, encoding="utf-8")

    return {
        "title": title,
        "labels": labels_str,
        "html_content": full_html,
        "file_path": str(html_file),
        "tracking_link": tracking_link
    }


def generate_blogger_atom_xml(posts_list: list) -> str:
    """توليد ملف Atom XML رسمي يمكن استيراده مباشرة بضغطة زر واحدة داخل لوحة تحكم Blogger."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    entries = []
    for i, p in enumerate(posts_list):
        escaped_content = p["html_content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        labels_xml = "\n".join([f'<category scheme="http://www.blogger.com/atom/ns#" term="{tag.strip()}" />' for tag in p["labels"].split(",") if tag.strip()])
        
        entry = f"""
        <entry>
            <id>tag:blogger.com,1999:blog-healingtouch.post-{i+1}</id>
            <published>{now_iso}</published>
            <updated>{now_iso}</updated>
            <title type="text">{p['title']}</title>
            <content type="html">{escaped_content}</content>
            <author>
                <name>Healing Touch Egypt</name>
                <email>healingtouch@gmail.com</email>
            </author>
            {labels_xml}
        </entry>
        """
        entries.append(entry)

    atom_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>مدونة هيلينج تاتش مصر | Healing Touch Egypt Blog</title>
    <subtitle>دليل التعافي الطبي بعد الجراحات وعلاج الندبات</subtitle>
    <updated>{now_iso}</updated>
    {"".join(entries)}
</feed>
"""
    xml_path = BLOGGER_EXPORT_DIR / "blogger_import_feed.xml"
    xml_path.write_text(atom_xml, encoding="utf-8")
    print(f"[+] 📝 تم إنشاء ملف استيراد بلوجر الرسمي (XML): {xml_path.name}")
    return str(xml_path)


if __name__ == "__main__":
    from clinical_story_publisher import CLINICAL_STORIES_TEMPLATES
    posts = []
    for tmpl in CLINICAL_STORIES_TEMPLATES[:3]:
        post_info = format_clinical_case_for_blogger(tmpl, {"image_url": "https://images.pexels.com/photos/7588659/pexels-photo-7588659.jpeg"})
        posts.append(post_info)
    generate_blogger_atom_xml(posts)
    print("🎉 تم تجهيز مقالات مدونة جوجل بنجاح!")
