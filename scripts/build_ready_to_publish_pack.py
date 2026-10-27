# -*- coding: utf-8 -*-
"""
=============================================================================
🌿 هيلينج تاتش مصر | محرك حزم النشر الشاملة بالمجلدات المؤرخة المفرزة (2026)
YouTube, TikTok, Instagram, Blogger, and Reddit Multi-Platform Suite
=============================================================================
"""

import sys
import os
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

# استيراد محرك الفيديو والبودكاست السريري
sys.path.append(str(BASE_DIR / "scripts"))
from media_video_engine import build_audio_visual_videos, build_uploaded_video_variants, generate_clean_youtube_thumbnail

YOUTUBE_CHANNEL_ID = "UCcHqrSEET7IEhr9ueM8VELQ"
YOUTUBE_UPLOAD_URL = f"https://studio.youtube.com/channel/{YOUTUBE_CHANNEL_ID}/videos/upload?d=ud"


def get_active_assets() -> dict:
    """اكتشاف وتحديد أحدث ملفات الحملة النشطة في manual_inbox أو pomelli_library."""
    assets = {
        "video": None,
        "audio": None,
        "hero_img": None,
        "square_img": None,
        "vertical_img": None,
        "text": None,
        "category": "c-section"
    }

    # 1. الفيديو المرفوع
    vids = list(MANUAL_INBOX_DIR.glob("*.mp4"))
    if vids:
        assets["video"] = vids[0]

    # 2. الصوت المرفوع
    audios = list(MANUAL_INBOX_DIR.glob("*.m4a")) + list(MANUAL_INBOX_DIR.glob("*.mp3"))
    if audios:
        assets["audio"] = audios[0]

    # 3. صور Pomelli
    imgs = list(MANUAL_INBOX_DIR.glob("*pomelli*.png")) + list(MANUAL_INBOX_DIR.glob("*.png"))
    if not imgs and POMELLI_LIB_DIR.exists():
        imgs = list(POMELLI_LIB_DIR.glob("*.png"))

    if imgs:
        hero = next((im for im in imgs if "photoshoot-4" in im.name), imgs[0])
        assets["hero_img"] = hero
        assets["square_img"] = next((im for im in imgs if "1_1" in im.name or "photoshoot-1" in im.name), hero)
        assets["vertical_img"] = next((im for im in imgs if "9_16" in im.name), hero)

    # 4. النص السريري المرفوع
    texts = [f for f in MANUAL_INBOX_DIR.glob("*.txt") if not f.name.startswith("PROMPTS")]
    if texts:
        assets["text"] = texts[0]

    return assets


def get_latest_pack_dir() -> Path:
    """إرجاع أحدث مجلد حزمة مؤرخ تم إنشاؤه."""
    if not READY_BASE_DIR.exists():
        READY_BASE_DIR.mkdir(parents=True, exist_ok=True)
    dirs = sorted([d for d in READY_BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("202")], key=lambda x: x.name, reverse=True)
    if dirs:
        return dirs[0]
    return READY_BASE_DIR


def generate_pack() -> Path:
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

    for d in [yt_dir, tiktok_dir, ig_dir, blogger_dir, reddit_dir]:
        d.mkdir(parents=True, exist_ok=True)

    assets = get_active_assets()

    # نصوص وروابط الحملة السريرية المعتمدة
    title = "بروتوكول تعافي جرح القيصرية والشاور الآمن ومنع الندبات وتكون الكلويد"
    shorts_title = "خايفة من أول شاور بعد القيصرية؟ الحل الطبي لحماية الجرح من الماء #Shorts #قيصرية"
    lp_url = "https://medon90ae.github.io/healing-touch-egypt/lp/c-section-recovery-protocol.html"
    site_url = "https://medon90ae.github.io/healing-touch-egypt/"
    wa_msg = "أهلاً بحضرتك، محتاجة استشارة بخصوص جرح القيصرية والشاور الآمن، وتفعيل كود (HT10) للشحن المجاني وحق معاينة الشحنة قبل الاستلام."
    wa_url = f"https://wa.me/201155803307?text={urllib.parse.quote(wa_msg)}"
    tags = "#ولادة_قيصرية #جرح_القيصرية #علاج_الندبات #شيت_سيليكون #تيجاديرم #صحة_المرأة #هيلينج_تاتش_مصر #الاستحمام_بعد_القيصرية"

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
        shutil.copy2(str(assets["hero_img"]), str(ig_dir / "صورة_بوست_رئيسية_1x1.png"))
        if assets["vertical_img"]:
            shutil.copy2(str(assets["vertical_img"]), str(ig_dir / "صورة_ستوري_Story_9x16.png"))

    # =========================================================================
    # 📝 4. قوالب نصوص يوتيوب
    # =========================================================================
    yt_desc = f"""🌿 بروتوكول التعافي السريري لجرح القيصرية والشاور الآمن ومنع تشوه الندبات الجراحية (2026)
دليل علمي شامل يشرح للأمهات كيفية حماية جرح القيصرية أثناء الاستحمام، والآلية البيولوجية لتدخل السيليكون الطبي لمنع تكون الكلويد والندبات المتضخمة.

⏱️ الفواصل الزمنية (Timestamps):
00:00 مقدمة: هواجس التعافي بعد الولادة القيصرية
00:45 بيولوجيا التئام جدار البطن ومراحل تشكل النسيج الرابط
02:15 لماذا تتكون الندبة البارزة ومتى يفرز الجسم كولاجين مفرط؟
04:00 بروتوكول الاستحمام الآمن: عزل الماء والبكتيريا بواسطة Tegaderm
05:30 المعيار الذهبي: كيف يُنظم شيت السيليكون الطبي فقدان الماء (TEWL)؟
07:15 إرشادات العناية اليومية ونمط الحياة الآمن لتعافي الأنسجة
08:30 التوجيه والاستشارة السريرية المجانية وتفعيل كود HT10

🔗 روابط الدليل وحاسبة التعافي السريرية:
🌐 دليل التعافي وحاسبة الجرح التفاعلية:
{lp_url}

🏛️ تصفح الموسوعة الطبية السريرية الشاملة:
{site_url}

💬 للتوجيه السريري المجاني وتفعيل كود (HT10) للشحن المجاني والمعاينة قبل الاستلام:
👉 {wa_url}

⚠️ تنويه طبي: المحتوى للتوعية السريرية المعتمدة ولا يُغني عن استشارة طبيبك المعالج.

{tags}"""

    (yt_dir / "بيانات_الفيديو_عنوان_ووصف_وهاشتاجات.txt").write_text(f"العنوان:\n{title}\n\nالوصف:\n{yt_desc}", encoding="utf-8")
    (yt_dir / "بيانات_الشورتس.txt").write_text(f"العنوان:\n{shorts_title}\n\nالوصف:\nاستحمام آمن بعد القيصرية بدون خوف من الماء! عزل كامل بضمادة تيجاديرم وحماية خط الجرح بشيت السيليكون الطبي.\nللتفاصيل وتفعيل كود HT10 للشحن المجاني:\n{wa_url}\n\n{tags}", encoding="utf-8")

    # =========================================================================
    # 📱 5. قوالب تيك توك وإنستجرام
    # =========================================================================
    tiktok_caption = f"""خايفة من أول شاور بعد الولادة القيصرية؟ 🚿
الحل الطبي السريري: عزل تام للماء والبكتيريا بالضمادات الشفافة المعتمدة، ثم حماية الجرح بشيت السيليكون الطبي لمنع الندبة البارزة والكلويد.

استشارة سريرية مجانية وتفعيل كود HT10 للشحن المجاني والمعاينة قبل الاستلام:
👉 الرابط في البايو أو واتساب المباشر: {wa_url}

{tags} #Shorts #تيك_توك_طبي"""
    (tiktok_dir / "كابشن_وهاشتاجات_تيكتوك.txt").write_text(tiktok_caption, encoding="utf-8")
    (ig_dir / "كابشن_وهاشتاجات_إنستجرام.txt").write_text(f"🌿 {title}\n\n{tiktok_caption}", encoding="utf-8")

    # =========================================================================
    # 📰 6. قالب مقال بلوجر HTML
    # =========================================================================
    hero_rel_url = f"https://medon90ae.github.io/healing-touch-egypt/assets/campaign_c-section_hero.png"
    blogger_html = f"""<div dir="rtl" style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width:820px; margin:auto; background:#ffffff; padding:28px; border-radius:18px; border:1px solid #E2E8F0; color:#1E293B; line-height:1.9;">
    <div style="text-align:center; margin-bottom:28px;">
        <img src="{hero_rel_url}" alt="{title}" style="max-width:100%; height:auto; border-radius:16px; box-shadow:0 10px 25px rgba(0,0,0,0.06);" />
    </div>
    <h1 style="color:#0D4A4D; font-size:1.9rem; font-weight:900; line-height:1.4; margin-bottom:18px;">{title}</h1>
    <div style="background:#ECFDF5; border-right:4px solid #10B981; padding:16px 20px; border-radius:12px; margin-bottom:26px;">
        <strong style="color:#065F46; font-size:1.05rem;">💡 القاعدة السريرية الذهبية:</strong>
        <p style="margin:6px 0 0 0; color:#064E3B; font-size:0.96rem;">الاستحمام بعد القيصرية آمن تماماً عند عزل الجرح بضمادات شفافة عازلة شبه نفاذة. والوقاية من الندبة البارزة تبدأ بعد التئام السطح باستخدام شيت السيليكون الطبي كمعيار ذهبي معتمد عالمياً.</p>
    </div>
    <h3 style="color:#134E4A; font-size:1.35rem; margin-top:28px;">البروتوكول السريري المتكامل (خطوة بخطوة):</h3>
    <ol style="padding-right:24px; font-size:1rem; color:#334155;">
        <li style="margin-bottom:12px;"><strong>تأمين أول شاور:</strong> وضع ضمادة 3M Tegaderm المقاومة للماء لعزل بكتيريا الاستحمام والسماح للجلد بطرد بخار العرق.</li>
        <li style="margin-bottom:12px;"><strong>تسطيح الندبة:</strong> بعد سقوط القشرة السطحية والتئام الجرح (الأسبوع الثاني إلى الثالث)، يبدأ تطبيق شيت السيليكون الطبي BUPY يومياً لمدة 12-16 ساعة لفرملة الكولاجين العشوائي.</li>
        <li style="margin-bottom:12px;"><strong>حماية اللون:</strong> تجنب التعرض المباشر للشمس لحماية خط الجرح من التصبغ الداكن.</li>
    </ol>
    <div style="background:linear-gradient(135deg, #0D4A4D 0%, #134E4A 100%); color:#ffffff; padding:24px; border-radius:16px; text-align:center; margin-top:35px;">
        <h4 style="margin:0 0 10px 0; font-size:1.25rem;">🩺 احصلي على استشارة سريرية وتوجيه مجاني لحالتك</h4>
        <p style="margin:0 0 18px 0; color:#CCFBF1; font-size:0.95rem;">تواصلِ مباشرة مع أخصائية التعافي مع تفعيل كود <strong>(HT10)</strong> للشحن المجاني وحق فتح ومعاينة الشحنة قبل الاستلام.</p>
        <a href="{wa_url}" target="_blank" style="display:inline-block; background:#10B981; color:#ffffff; font-weight:800; font-size:1.05rem; padding:12px 28px; border-radius:30px; text-decoration:none;">محادثة واتساب الفورية ←</a>
    </div>
</div>"""
    (blogger_dir / "مقال_بلوجر_جاهز_للنشر.html").write_text(blogger_html, encoding="utf-8")

    # =========================================================================
    # 🔴 7. قالب مقال ريديت Markdown
    # =========================================================================
    reddit_md = f"""# {title}

### 🌿 نظرة سريرية عامة
يُعد جرح الولادة القيصرية من أكثر الجروح الجراحية التي تتطلب عناية دقيقة تجمع بين الأمان الفسيولوجي والراحة النفسية للأم في الأسابيع الأولى:
1. **الخوف من الاستحمام (الشاور)** وتلوث الجرح بمياه الاستحمام.
2. **الخوف من تحول خط الجرح إلى ندبة متضخمة أو كلويد بارز وداكن.**

---

### 🧬 الآلية البيولوجية لالتئام الأنسجة (Physiology of Tissue Healing)
- **مرحلة الالتهاب الدفاعي (Inflammatory Phase):** إغلاق الشعيرات ومنع العدوى البكتيرية.
- **مرحلة إعادة البناء (Proliferative Phase):** الخلايا الليفية تصنع كولاجين. إذا جف الجرح أو تعرض للاحتكاك، ينتج الجسم كولاجين مفرطاً يشكل الكلويد.
- **مرحلة النضج (Remodeling Phase):** يتدخل السيليكون الطبي لتنظيم ألياف الكولاجين لتصبح مسطحة ومطابقة للجلد الطبيعي.

---

### 🛡️ بروتوكول التعافي المعتمد
1. **الشاور العازل للماء:** ضمادات Tegaderm العازلة بنسبة 100% للماء والبكتيريا.
2. **شيت السيليكون الطبي:** شيت BUPY الطبي لتنظيم فقدان الماء السطحي (TEWL) وحبس الرطوبة الفسيولوجية.

---

### 🔗 روابط الدليل والاستشارة
* 🌐 **[دليل التعافي وحاسبة الجرح السريرية التفاعلية]({lp_url})**
* 💬 **للتوجيه السريري المجاني وتفعيل كود (HT10) للشحن والمعاينة المجانية:** [تواصل عبر واتساب]({wa_url})

{tags}"""
    (reddit_dir / "منشور_ومقال_ريديت_Markdown.md").write_text(reddit_md, encoding="utf-8")

    # =========================================================================
    # 📋 8. الدليل الإرشادي السريع داخل الحزمة
    # =========================================================================
    guide_text = f"""=============================================================================
🌿 هيلينج تاتش مصر | حزمة النشر الشاملة المفرزة ({timestamp_folder_name})
=============================================================================

📁 01_يوتيوب_YouTube:
   - فيديو يوتيوب كامل 16x9 (MP4)
   - فيديو شورتس 9x16 (MP4)
   - فيديو بودكاست صوتي مرئي 16x9 (MP4)
   - فيديو بودكاست صوتي شورتس 9x16 (MP4)
   - صورة مصغرة Thumbnail بدقة 4K
   - ملف بيانات الفيديو والشورتس الجاهزة للنسخ

📁 02_تيكتوك_TikTok:
   - فيديو تيكتوك رأسي 9x16 (MP4)
   - فيديو بودكاست صوتي تيكتوك 9x16 (MP4)
   - كابشن وهاشتاجات تيكتوك

📁 03_إنستجرام_Instagram:
   - فيديو ريلز 9x16 (MP4)
   - فيديو بودكاست صوتي ريلز 9x16 (MP4)
   - صور البوست والستوري (Pomelli 4K)
   - كابشن وهاشتاجات إنستجرام

📁 04_بلوجر_Blogger:
   - مقال HTML جاهز للنسخ ولصقه فوراً في بلوجر

📁 05_ريديت_Reddit:
   - مقال Markdown جاهز للنشر في مجتمعات ريديت
============================================================================="""
    (pack_dir / "00_دليل_النشر_السريع.txt").write_text(guide_text, encoding="utf-8")

    # تسجيل مسار أحدث حزمة في ملف ثابت لسهولة الفتح
    (READY_BASE_DIR / "LATEST_PACK_PATH.txt").write_text(str(pack_dir), encoding="utf-8")

    print(f"\n[+] 🎉 تم إنشاء وتجهيز حزمة النشر الشاملة بنجاح في المجلد المؤرخ:")
    print(f"    👉 {pack_dir}")
    return pack_dir


if __name__ == "__main__":
    generate_pack()
