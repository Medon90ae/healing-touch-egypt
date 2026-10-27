# -*- coding: utf-8 -*-
"""
Fix antigravity_social_automation.py:
1. Prevent export_notebooklm_master_source from blocking Option 1 (auto-daily).
2. Move manual_inbox intake to the very top of run_unified_studio_and_publish.
3. Support Arabic-named MP4 videos, M4A audios, Pomelli images, and clinical text files.
4. Ensure Facebook and Instagram receive the full caption containing landing page and WhatsApp links.
5. Archive ALL processed files in manual_inbox so it becomes 100% clean.
"""

import sys
import os
import re
from pathlib import Path

BASE_DIR = Path(r"c:\followUPSHEET\healing_touch").resolve()
SOCIAL_FILE = BASE_DIR / "antigravity_social_automation.py"

content = SOCIAL_FILE.read_text(encoding="utf-8")

# 1. In export_notebooklm_master_source:
# Only prompt user for selection if explicitly called or when interactive flag is set,
# NEVER prompt when running in automated batch mode or when called without product_choice
old_export_head = '''def export_notebooklm_master_source(product_choice: str = None) -> str:
    """تجهيز ملف المعرفة والبرومبت الموحد الشامل الجاهز للرفع المباشر في Google NotebookLM مع برومبتات Pomelli و Deep Research."""
    if product_choice is None:
        # إذا كنا في طرفية تفاعلية، نطلب الاختيار من المستخدم
        if sys.stdin and sys.stdin.isatty():
            product_choice = prompt_user_for_product_selection()
        else:
            product_choice = "1"'''

new_export_head = '''def export_notebooklm_master_source(product_choice: str = None, interactive: bool = False) -> str:
    """تجهيز ملف المعرفة والبرومبت الموحد الشامل الجاهز للرفع المباشر في Google NotebookLM مع برومبتات Pomelli و Deep Research."""
    if product_choice is None:
        if interactive and sys.stdin and sys.stdin.isatty():
            product_choice = prompt_user_for_product_selection()
        else:
            product_choice = "1"'''

if old_export_head in content:
    content = content.replace(old_export_head, new_export_head)
    print("[+] Updated export_notebooklm_master_source signature with interactive flag")

# In main(): when mode == "notebooklm", set interactive=True
old_mode_nlm = '''    if args.mode == "notebooklm":
        src_path = export_notebooklm_master_source(product_choice=args.product)'''

new_mode_nlm = '''    if args.mode == "notebooklm":
        src_path = export_notebooklm_master_source(product_choice=args.product, interactive=True)'''

if old_mode_nlm in content:
    content = content.replace(old_mode_nlm, new_mode_nlm)
    print("[+] Set interactive=True for mode notebooklm in main()")

# 2. In run_unified_studio_and_publish:
# Remove notebook_file = export_notebooklm_master_source() or replace with non-interactive call
content = content.replace(
    'notebook_file = export_notebooklm_master_source()',
    'notebook_file = str(NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md")'
)

# 3. Clean manual_inbox intake logic in run_unified_studio_and_publish
# Let's inspect run_unified_studio_and_publish around lines 1440-1550
# We want to scan manual_inbox, pick the user's video, audio, image, and text BEFORE doing generation
old_intake_start = '''    photo_info = get_clinical_case_photo(tmpl["title"], tmpl["category"])
    raw_img = photo_info.get("local_path", "")
    print(f"[*] 📸 الصورة المختارة: {Path(raw_img).name if raw_img else 'افتراضية'} (المصدر: {photo_info.get('source')})")

    cards = generate_branded_card(tmpl, raw_img) if raw_img else {"square_path": "", "story_path": ""}
    square_img_path = cards.get("square_path", "") or raw_img
    story_img_path = cards.get("story_path", "")

    video_path = generate_tiktok_reel_video(story_img_path, duration_sec=8) if story_img_path else ""
    export_canva_bulk_csv(CLINICAL_STORIES_TEMPLATES)

    blogger_post = format_clinical_case_for_blogger(tmpl, photo_info)
    generate_blogger_atom_xml([blogger_post])
    notebook_file = str(NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md")

    # اختيار الوسائط المرفوعة بناءً على تصنيف التخصص الجراحي الدقيق (Smart Matching)
    cat_matched = inbox_triage["matched_files"].get(tmpl["category"], {"videos": [], "images": [], "audios": [], "texts": [], "htmls": []})

    # 1. الصوت
    if cat_matched.get("audios"):
        aud_f = cat_matched["audios"][0]
        dest_aud = NOTEBOOK_AUDIO_DIR / aud_f.name
        if not dest_aud.exists():
            shutil.copy2(str(aud_f), str(dest_aud))
        used_inbox_files.append(aud_f)
        print(f"[+] 🎙️ [المصنف الذكي]: تم التقاط ملف صوتي مطابق للتخصص ({aud_f.name})!")

    # 2. النص والمقال
    if cat_matched.get("texts"):
        chosen_txt = cat_matched["texts"][0]
        custom_text = read_resilient_text(chosen_txt).strip()
        if custom_text and len(custom_text) > 50:
            if len(custom_text) > 1500:
                truncated = custom_text[:1500]
                last_space = truncated.rfind(" ")
                custom_text = (truncated[:last_space] if last_space > 1200 else truncated) + "..."
            tmpl["story_text"] = custom_text
            used_inbox_files.append(chosen_txt)
            print(f"[+] 📝 [المصنف الذكي]: تم دمج نص سريري مطابق لحالة اليوم ({chosen_txt.name}) [{len(custom_text)} حرف]!")

    # 3. الصورة والتصميم
    if cat_matched.get("images"):
        square_img_path = str(cat_matched["images"][0])
        story_img_path = str(cat_matched["images"][0])
        used_inbox_files.append(cat_matched["images"][0])
        print(f"[+] 🎨 [المصنف الذكي]: تم اعتماد تصميم مطابق للحالة من manual_inbox ({Path(square_img_path).name})!")
    else:
        square_img_path = str(BASE_DIR / "docs" / "assets" / "og-image.jpg")
        story_img_path = square_img_path

    # 4. الفيديو
    if cat_matched.get("videos"):
        video_path = str(cat_matched["videos"][0])
        used_inbox_files.append(cat_matched["videos"][0])
        print(f"[+] 🎬 [المصنف الذكي]: تم اعتماد فيديو مطابق لحالة اليوم ({Path(video_path).name})!")'''

new_intake_start = '''    # 📥 فحص واستيعاب كافة ملفات manual_inbox فورياً وتوجيهها للمشروع
    inbox_files = [f for f in MANUAL_INBOX_DIR.iterdir() if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]]
    
    inbox_videos = [f for f in inbox_files if f.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm"]]
    inbox_audios = [f for f in inbox_files if f.suffix.lower() in [".m4a", ".mp3", ".wav", ".aac"]]
    inbox_images = [f for f in inbox_files if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
    inbox_texts = [f for f in inbox_files if f.suffix.lower() in [".txt", ".md"]]
    inbox_htmls = [f for f in inbox_files if f.suffix.lower() in [".html", ".htm"]]

    # 1. معالجة الفيديو المرفوع
    uploaded_video_rel = ""
    if inbox_videos:
        chosen_vid = inbox_videos[0]
        used_inbox_files.append(chosen_vid)
        dest_vid = BASE_DIR / "docs" / "assets" / f"campaign_{tmpl['category']}_video.mp4"
        dest_portal_vid = BASE_DIR / "portal_app" / "public" / "assets" / f"campaign_{tmpl['category']}_video.mp4"
        dest_docs_portal_vid = BASE_DIR / "docs" / "portal" / "assets" / f"campaign_{tmpl['category']}_video.mp4"
        try:
            shutil.copy2(str(chosen_vid), str(dest_vid))
            dest_portal_vid.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(chosen_vid), str(dest_portal_vid))
            dest_docs_portal_vid.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(chosen_vid), str(dest_docs_portal_vid))
            video_path = str(dest_vid)
            uploaded_video_rel = f"../assets/{dest_vid.name}"
            print(f"[+] 🎬 تم اعتماد ونشر الفيديو المرفوع: {chosen_vid.name} ({chosen_vid.stat().st_size / (1024*1024):.1f} MB)")
        except Exception as e:
            print(f"[!] تنبيه نسخ الفيديو: {e}")
            video_path = str(chosen_vid)
    else:
        video_path = ""

    # 2. معالجة الصوت المرفوع
    if inbox_audios:
        chosen_aud = inbox_audios[0]
        used_inbox_files.append(chosen_aud)
        dest_aud = NOTEBOOK_AUDIO_DIR / chosen_aud.name
        dest_docs_aud = BASE_DIR / "docs" / "assets" / f"campaign_{tmpl['category']}_audio{chosen_aud.suffix}"
        try:
            shutil.copy2(str(chosen_aud), str(dest_aud))
            shutil.copy2(str(chosen_aud), str(dest_docs_aud))
            print(f"[+] 🎙️ تم اعتماد ونشر التعليق الصوتي المرفوع: {chosen_aud.name}")
        except Exception as e:
            print(f"[!] تنبيه نسخ الصوت: {e}")

    # 3. معالجة النص والمقال السريري المرفوع
    if inbox_texts:
        chosen_txt = inbox_texts[0]
        used_inbox_files.append(chosen_txt)
        custom_raw = read_resilient_text(chosen_txt).strip()
        if custom_raw and len(custom_raw) > 50:
            # استخراج ملخص سريري غني يوضح المشكلة والحل بدون بتر عشوائي
            paragraphs = [p.strip() for p in custom_raw.split("\\n") if len(p.strip()) > 30 and not p.strip().startswith("#")]
            if paragraphs:
                top_paragraphs = []
                current_len = 0
                for p in paragraphs[:4]:
                    if current_len + len(p) < 1400:
                        top_paragraphs.append(p)
                        current_len += len(p)
                if top_paragraphs:
                    tmpl["story_text"] = "\\n\\n".join(top_paragraphs)
            print(f"[+] 📝 تم استيعاب وصياغة التقرير السريري المرفوع ({chosen_txt.name})!")

    # 4. معالجة الصور المرفوعة من Pomelli
    if inbox_images:
        # تفضيل الصور ذات الحجم الأنسب للويب (مثل 1-2 ميجابايت بدلاً من 20 ميجابايت)
        sorted_imgs = sorted(inbox_images, key=lambda x: (abs(x.stat().st_size - 1.5 * 1024 * 1024)))
        chosen_img = sorted_imgs[0]
        for img in inbox_images:
            used_inbox_files.append(img)
            
        dest_hero_img = BASE_DIR / "docs" / "assets" / f"campaign_{tmpl['category']}_hero.png"
        try:
            shutil.copy2(str(chosen_img), str(dest_hero_img))
            square_img_path = str(dest_hero_img)
            story_img_path = str(dest_hero_img)
            print(f"[+] 🎨 تم اعتماد صور Pomelli السريرية المرفوعة ({chosen_img.name})!")
        except Exception:
            square_img_path = str(chosen_img)
            story_img_path = str(chosen_img)
    else:
        photo_info = get_clinical_case_photo(tmpl["title"], tmpl["category"])
        raw_img = photo_info.get("local_path", "")
        cards = generate_branded_card(tmpl, raw_img) if raw_img else {"square_path": "", "story_path": ""}
        square_img_path = cards.get("square_path", "") or raw_img
        story_img_path = cards.get("story_path", "")

    # إذا لم يكن هناك فيديو مرفوع، ننشئ فيديو ريلز من الصورة
    if not video_path and story_img_path:
        video_path = generate_tiktok_reel_video(story_img_path, duration_sec=8)

    export_canva_bulk_csv(CLINICAL_STORIES_TEMPLATES)
    blogger_post = format_clinical_case_for_blogger(tmpl, {"image_url": "../assets/og-image.jpg"})
    generate_blogger_atom_xml([blogger_post])
    notebook_file = str(NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md")'''

if old_intake_start in content:
    content = content.replace(old_intake_start, new_intake_start)
    print("[+] Successfully refactored manual_inbox intake to happen FIRST and handle all asset types")

# 4. Fix full_caption and post_data["caption"] to guarantee Landing Page URL and WhatsApp link are included
old_caption_block = '''    # تجهيز نصوص المنصات بتاريخ اليوم مدمجاً برابط صفحة الهبوط الجديدة
    date_str = datetime.now().strftime("%Y-%m-%d")
    full_caption = f"{tmpl['story_text']}\\n\\n🔗 رابط الدليل السريري وحجز الاستشارة:\\n{lp_url}\\n\\n{tmpl['hashtags']}"
    if len(full_caption) > 2200:
        max_story_len = max(100, 2200 - len(tmpl['hashtags']) - len(lp_url) - 45)
        tmpl['story_text'] = tmpl['story_text'][:max_story_len].rsplit(" ", 1)[0] + "..."
        full_caption = f"{tmpl['story_text']}\\n\\n🔗 رابط الدليل السريري وحجز الاستشارة:\\n{lp_url}\\n\\n{tmpl['hashtags']}"'''

new_caption_block = '''    # تجهيز نصوص المنصات بتاريخ اليوم مدمجاً برابط صفحة الهبوط الجديدة ورابط واتساب المباشر
    date_str = datetime.now().strftime("%Y-%m-%d")
    wa_direct_url = f"https://wa.me/201155803307?text={urllib.parse.quote('أهلاً بكِ، أود استشارة سريرية مجانية حول مرحلة تعافي جرحي')}"
    
    clean_story_text = tmpl['story_text'].strip()
    if len(clean_story_text) > 1200:
        clean_story_text = clean_story_text[:1200].rsplit(" ", 1)[0] + "..."
        
    full_caption = f"""🌿 {tmpl['title']}

{clean_story_text}

━━━━━━━━━━━━━━━━━━━━━━━
🔗 رابط الدليل السريري وحاسبة التعافي المتخصصة:
👉 {lp_url}

💬 للتوجيه السريري المجاني والاستشارة عبر واتساب (01155803307):
👉 {wa_direct_url}

{tmpl['hashtags']}"""'''

if old_caption_block in content:
    content = content.replace(old_caption_block, new_caption_block)
    print("[+] Successfully enhanced full_caption with WhatsApp and Landing page links")

# Also ensure post_data["caption"] uses full_caption!
old_post_data = '''    post_data = {
        "day": f"دراسة حالة سريرية ({chosen_idx + 1}) - {tmpl['title']}",
        "caption": tmpl["story_text"],
        "hashtags": tmpl["hashtags"],
        "row_index": -1,
    }'''

new_post_data = '''    post_data = {
        "day": f"دراسة حالة سريرية ({chosen_idx + 1}) - {tmpl['title']}",
        "caption": full_caption,
        "hashtags": "",
        "row_index": -1,
    }'''

if old_post_data in content:
    content = content.replace(old_post_data, new_post_data)
    print("[+] Set post_data['caption'] to full_caption so Facebook receives complete text and links")

# 5. Archive ALL processed files in manual_inbox
old_archive_block = '''    # أرشفة الملفات المعالجة من manual_inbox
    cle.archive_manual_inbox_processed()
    if used_inbox_files:
        archived_count = archive_used_inbox_files(MANUAL_INBOX_DIR, used_inbox_files)
        if archived_count > 0:
            print(f"[+] 🗄️ [المصنف الذكي]: تم أرشفة وتفريغ {archived_count} ملفات مستخدمة بنجاح!")'''

new_archive_block = '''    # 🧹 تفريغ وأرشفة كافة الملفات المعالجة من manual_inbox لحفظ نظافة الصندوق بالكامل
    all_inbox_remaining = [
        f for f in MANUAL_INBOX_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name not in ["PROMPTS_PACK_TODAY.txt", "PROMPTS_PACK_TODAY.md"]
    ]
    files_to_clean = list(set(used_inbox_files + all_inbox_remaining))
    if files_to_clean:
        archived_count = archive_used_inbox_files(MANUAL_INBOX_DIR, files_to_clean)
        if archived_count > 0:
            print(f"\\n[+] 🧹 [تفريغ الصندوق]: تم تنظيف وأرشفة {archived_count} ملفات من manual_inbox إلى archive/ بنجاح!")'''

if old_archive_block in content:
    content = content.replace(old_archive_block, new_archive_block)
    print("[+] Upgraded archive block to clean ALL remaining processed files from manual_inbox")

SOCIAL_FILE.write_text(content, encoding="utf-8")
print("[+] Finished patching antigravity_social_automation.py")
