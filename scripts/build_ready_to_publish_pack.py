# -*- coding: utf-8 -*-
"""
مولد حزم النشر الجاهزة اليدوية السريعة لريديت وجوجل بلوجر
Generates 1-click ready-to-copy/import publication packs for Reddit and Blogger.
Fully compliant with Zero-Commerce, clinical reassurance, and live GitHub Pages asset links.
"""

import sys
import os
import datetime as dt
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
READY_DIR = BASE_DIR / "media_assets" / "ready_to_publish"
READY_DIR.mkdir(parents=True, exist_ok=True)

def generate_pack():
    date_str = dt.datetime.now().strftime("%Y-%m-%d")
    
    # 1. بيانات الحالة والتريندات السريرية الحالية
    title = "بروتوكول تعافي جرح القيصرية والشاور وإدارة الندبات الجراحية (الدليل السريري المعتمد 2026)"
    reddit_title = "دليل تعافي جرح القيصرية والشاور الآمن: كيف يمنع السيليكون الطبي تشوه الندبات وتكون الكلويد؟"
    
    hero_img_url = "https://medon90ae.github.io/healing-touch-egypt/assets/campaign_c-section_hero.png"
    video_url = "https://medon90ae.github.io/healing-touch-egypt/assets/campaign_c-section_video.mp4"
    audio_url = "https://medon90ae.github.io/healing-touch-egypt/assets/campaign_c-section_audio.m4a"
    lp_url = "https://medon90ae.github.io/healing-touch-egypt/lp/c-section-recovery-protocol.html"
    wa_url = "https://wa.me/201155803307?text=%D8%A3%D9%87%D9%84%D8%A7%D9%8B%20%D8%A8%D9%83%D9%90%D8%8C%20%D8%A3%D9%88%D8%AF%20%D8%A7%D8%B3%D8%AA%D8%B4%D8%A7%D8%B1%D8%A9%20%D8%B3%D8%B1%D9%8A%D8%B1%D9%8A%D8%A9%20%D9%85%D8%AC%D8%A7%D9%86%D9%8A%D8%A9%20%D8%AD%D9%88%D9%84%20%D9%85%D8%B1%D8%AD%D9%84%D8%A9%20%D8%AA%D8%B9%D8%A7%D9%81%D9%8A%20%D8%AC%D8%B1%D8%AD%D9%8A"
    
    labels = "ولادة قيصرية, جرح القيصرية, علاج الندبات, شيت سيليكون, ضمادات تيجاديرم, صحة المرأة, رعاية بعد الجراحة"
    
    # =========================================================================
    # 🔴 ملف قالب REDDIT
    # =========================================================================
    reddit_content = f"""# {reddit_title}

### 🌿 نظرة سريرية عامة
يُعد جرح الولادة القيصرية من أكثر الجروح الجراحية التي تتطلب عناية دقيقة تجمع بين الأمان الفسيولوجي والراحة النفسية للأم في الأيام والأسابيع الأولى. إن الهاجس الأكبر الذي تواجهه معظم الأمهات يتمثل في:
1. **الخوف من الاستحمام (الشاور)** وملامسة المياه للجرح خلال أول أسبوعين.
2. **الخوف من تحول خط الجرح إلى ندبة متضخمة أو كلويد بارز وداكن** يسبب الحكة أو الألم المشدود.

---

### 🧬 الآلية البيولوجية لالتئام الأنسجة (Physiology of Tissue Healing)
يمر التئام جدار البطن بعد القيصرية بثلاث مراحل بيولوجية متتابعة:
- **مرحلة الالتهاب الدفاعي (Inflammatory Phase):** في الأيام الأولى، تتدفق الخلايا المناعية لإغلاق الشعيرات الدموية ومنع العدوى.
- **مرحلة إعادة البناء والترميم (Proliferative Phase):** تبدأ الخلايا الليفية بتصنيع الكولاجين العشوائي. إذا تعرض الجرح للجفاف أو الاحتكاك المستمر، يفرز الجسم كولاجين مفرطاً ينتج عنه الكلويد.
- **مرحلة النضج وإعادة التشكيل (Remodeling Phase):** تستمر من 6 أشهر إلى سنة، وهي المرحلة الحاسمة التي يتدخل فيها السيليكون الطبي لتنظيم ألياف الكولاجين لتصبح مسطحة ومطابقة للون الجلد الطبيعي.

---

### 🛡️ بروتوكول التعافي المعتمد (الخطوة بخطوة)

#### ١. تأمين الشاور العازل للماء (Waterproof Protection)
* يُوصى باستخدام الضمادات الشفافة العازلة (مثل **3M Tegaderm Film**) بعد استقرار الجرح، حيث توفر غشاءً شبه نفاذ يعزل الماء والبكتيريا تماماً ويسمح للجلد بالتنفس وطرد بخار العرق.
* يتيح للأم أخذ شاور كامل بكل راحة دون القلق من تبلل الجرح أو الحاجة لغيار يومي مؤلم.

#### ٢. التحكم بالترطيب ومنع الندبة البارزة (Silicone Hydration)
* بمجرد إغلاق الجرح والتئام القشرة السطحية (عادة بعد أسبوعين إلى 3 أسابيع)، يُعد **شيت السيليكون الطبي (Medical Silicone Sheet)** المعيار الذهبي المعتمد عالمياً (Gold Standard).
* يعمل السيليكون على حبس الرطوبة الفسيولوجية (Transepidermal Water Loss Control)، مما يرسل إشارة بيولوجية للخلايا الليفية بالتوقف عن إنتاج الكولاجين الزائد، مانعاً بذلك بروز الندبة وتصلبها.

---

### 🎬 المحاضرة المرئية والشرح الصوتي الموثق
* **فيديو التئام الأنسجة السريري:** [مشاهدة الفيديو الموثق]({video_url})
* **التسجيل الصوتي التحليلي:** [الاستماع للشرح السريري الكامل]({audio_url})

---

### 📚 مصادر وتوجيه سريري إضافي
* 🔗 **[دليل التعافي السريري التفاعلي وحاسبة الجرح]({lp_url})**
* 💬 **للتوجيه السريري المجاني والاستفسارات الطبية:** [تواصل مع أخصائية الرعاية عبر واتساب]({wa_url})

#ولادة_قيصرية #علاج_الندبات #جرح_القيصرية #شيت_سيليكون #تيجاديرم #صحة_المرأة
"""

    reddit_file = READY_DIR / "[قالب_ريديت_Reddit]_جاهز_للنشر.md"
    reddit_file.write_text(reddit_content, encoding="utf-8")

    # =========================================================================
    # 📝 ملف قالب BLOGGER (HTML نظيف ومرتب للنسخ واللصق)
    # =========================================================================
    blogger_html = f"""<!-- 
=============================================================================
🌿 هيلينج تاتش مصر | قالب مقال مدونة جوجل (Google Blogger) المنسق
طريقة النشر في 15 ثانية:
1. افتح لوحة تحكم بلوجر: https://draft.blogger.com/blog/posts/6258225961862592152
2. اضغط "مشاركة جديدة" (New Post).
3. ضع في خانة العنوان (Title):
   {title}
4. في محرر المقال، اضغط على أيقونة القلم أعلى اليسار واختر "عرض HTML" (<>).
5. انسخ كل الكود الموجود أسفل هذا الصندوق والصقه بالكامل، ثم اضغط "نشر" (Publish)!
=============================================================================
-->

<div dir="rtl" style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width:820px; margin:auto; background:#ffffff; padding:28px; border-radius:18px; border:1px solid #E2E8F0; color:#1E293B; line-height:1.9;">

    <!-- صورة الغلاف السريرية عالية الدقة من خادم GitHub Pages -->
    <div style="text-align:center; margin-bottom:28px;">
        <img src="{hero_img_url}" alt="{title}" style="max-width:100%; height:auto; border-radius:16px; box-shadow:0 10px 25px rgba(0,0,0,0.06);" />
    </div>

    <h1 style="color:#065F46; font-size:1.85rem; font-weight:700; border-bottom:3px solid #10B981; padding-bottom:14px; margin-bottom:24px;">
        {title}
    </h1>

    <div style="background:#F0FDF4; border-right:5px solid #10B981; padding:18px 22px; border-radius:12px; margin-bottom:28px;">
        <p style="margin:0; font-size:1.08rem; color:#064E3B; font-weight:500;">
            <strong>🌿 إرشاد وتوجيه سريري معتمد:</strong> صُمم هذا البروتوكول للإجابة عن التساؤلات الأكثر شيوعاً للأمهات حول حماية جرح القيصرية أثناء الاستحمام والوقاية المبكرة من الندبات المتضخمة والكلويد وفق أحدث الدراسات الطبية المنشورة (2024–2026).
        </p>
    </div>

    <!-- مشغل الفيديو الطبي والشرح الصوتي -->
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:16px; padding:20px; margin:28px 0; text-align:center;">
        <h3 style="color:#1E293B; margin-top:0; margin-bottom:14px; font-size:1.2rem;">🎬 الفيديو التوضيحي السريري: فسيولوجيا التئام جدار البطن</h3>
        <video controls style="max-width:100%; width:720px; border-radius:12px; outline:none; background:#000;">
            <source src="{video_url}" type="video/mp4">
            متصفحك لا يدعم مشغل الفيديو المباشر.
        </video>
        
        <div style="margin-top:20px; padding-top:16px; border-top:1px dashed #CBD5E1;">
            <p style="margin:0 0 10px 0; font-weight:600; color:#475569;">🎙️ الاستماع للشرح الصوتي الكامل (آلية عمل السيليكون الطبي لمنع تشوه الندبات):</p>
            <audio controls style="width:100%; max-width:600px;">
                <source src="{audio_url}" type="audio/mp4">
                متصفحك لا يدعم مشغل الصوت المباشر.
            </audio>
        </div>
    </div>

    <h2 style="color:#047857; font-size:1.45rem; margin-top:32px;">🧬 بيولوجيا التئام الجروح: لماذا تتكون الندبة البارزة بعد القيصرية؟</h2>
    <p style="font-size:1.05rem; color:#334155;">
        الجلد هو خط الدفاع الأول للجسم، وعند إجراء الشق الجراحي في الولادة القيصرية، يبدأ الجسم فسيولوجياً في تكوين نسيج ليفي رابط لسد الفجوة بأسرع ما يمكن. ورغم أهمية هذه الاستجابة لحماية الجسم من العدوى، إلا أن فقدان الجلد للرطوبة وتوتر الأنسجة يؤديان غالباً إلى <strong>إفراز مفرط لبروتين الكولاجين</strong>، مما يحول خط الجرح الناعم إلى ندبة متضخمة حمراء (Hypertrophic Scar) أو كلويد بارز ومتيبس.
    </p>

    <h2 style="color:#047857; font-size:1.45rem; margin-top:32px;">🛡️ المعايير الطبية المعتمدة للتعافي الجراحي الآمن</h2>
    
    <div style="margin:20px 0;">
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; margin-bottom:16px; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
            <h3 style="color:#0D9488; margin:0 0 8px 0; font-size:1.18rem;">1. تأمين شاور الاستحمام الآمن (عزل الماء والبكتيريا)</h3>
            <p style="margin:0; color:#475569; font-size:1rem;">
                الاستحمام دون حماية قد يعرض الجرح للبلل والعدوى، بينما الضمادات القطنية التقليدية تحبس الرطوبة وتزيد الاحتكاك. استخدام الضمادات الشفافة العازلة للماء تماماً (مثل <strong>3M Tegaderm</strong>) يسمح للأم بالشاور المريح مع بقاء الجرح جافاً ومحمياً بنسبة 100%.
            </p>
        </div>

        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; margin-bottom:16px; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
            <h3 style="color:#0D9488; margin:0 0 8px 0; font-size:1.18rem;">2. إدارة الندبات بشرائح السيليكون الطبي (Medical Silicone)</h3>
            <p style="margin:0; color:#475569; font-size:1rem;">
                يُجمع جراحو التجميل والنساء والولادة عالمياً على أن <strong>شرائح السيليكون الطبي</strong> هي الخط الأول غير الجراحي لإعادة تسطيح وتنعيم الندبات؛ حيث تقوم بحفظ التوازن الرطوبي للأنسجة وإيقاف النشاط المفرط للخلايا الليفية.
            </p>
        </div>
    </div>

    <!-- صندوق التوجيه والاستشارة السريرية المجانية -->
    <div style="background:linear-gradient(135deg, #065F46 0%, #047857 100%); color:#ffffff; border-radius:16px; padding:30px 24px; text-align:center; margin-top:40px; box-shadow:0 12px 30px rgba(6,95,70,0.2);">
        <h3 style="margin:0 0 10px 0; font-size:1.4rem; color:#FFFFFF;">هل لديك استفسار أو قلق بخصوص مظهر أو مرحلة التئام جرحك؟</h3>
        <p style="margin:0 0 24px 0; font-size:1.05rem; opacity:0.92; max-width:620px; margin-left:auto; margin-right:auto;">
            فريق التوجيه السريري متاح لتقديم الإرشاد الطبي المجاني والموثوق لمساعدتك في اختيار الخطوة الأمثل للتعافي براحة وطمأنينة.
        </p>
        <div style="display:flex; justify-content:center; gap:14px; flex-wrap:wrap;">
            <a href="{lp_url}" target="_blank" style="background:#FFFFFF; color:#065F46; padding:14px 26px; border-radius:12px; font-weight:700; text-decoration:none; display:inline-block; font-size:1rem;">
                🌐 زيارة دليل التعافي وحاسبة الجرح
            </a>
            <a href="{wa_url}" target="_blank" style="background:#25D366; color:#FFFFFF; padding:14px 26px; border-radius:12px; font-weight:700; text-decoration:none; display:inline-block; font-size:1rem;">
                💬 استشارة سريرية مجانية عبر واتساب
            </a>
        </div>
    </div>

    <!-- تصنيفات المقال السريرية -->
    <div style="margin-top:24px; padding-top:14px; border-top:1px solid #E2E8F0; font-size:0.9rem; color:#64748B;">
        <strong>التصنيفات الموصى بها في بلوجر (Labels):</strong> {labels}
    </div>
</div>
"""

    blogger_file = READY_DIR / "[قالب_بلوجر_Blogger]_جاهز_للنشر.html"
    blogger_file.write_text(blogger_html, encoding="utf-8")

    # =========================================================================
    # 📦 ملف استيراد بلوجر الآلي (Atom XML)
    # =========================================================================
    now_iso = dt.datetime.now(dt.timezone.utc).isoformat()
    escaped_html = (
        blogger_html
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    categories_xml = "\n".join([f'<category scheme="http://www.blogger.com/atom/ns#" term="{t.strip()}" />' for t in labels.split(",")])

    atom_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title type="text">مدونة هيلينج تاتش مصر للتعافي الجراحي</title>
  <subtitle type="text">الدليل السريري الموثق للعناية بالجروح وإدارة الندبات</subtitle>
  <updated>{now_iso}</updated>
  <entry>
    <id>tag:blogger.com,1999:post-csection-recovery-protocol</id>
    <published>{now_iso}</published>
    <updated>{now_iso}</updated>
    <title type="text">{title}</title>
    <content type="html">{escaped_html}</content>
    {categories_xml}
  </entry>
</feed>
"""
    xml_file = READY_DIR / "[استيراد_بلوجر_XML]_blogger_import.xml"
    xml_file.write_text(atom_xml, encoding="utf-8")

    # =========================================================================
    # 📘 دليل النشر السريع (Quick Guide)
    # =========================================================================
    guide_txt = f"""=============================================================================
🌿 هيلينج تاتش مصر | دليل النشر اليدوي السريع في 30 ثانية (ريديت وبلوجر)
=============================================================================

أهلاً بك! لقد تم تجهيز قوالب اليوم الموثقة بالكامل لضمان النشر السريع الخالي من الأخطاء:

-----------------------------------------------------------------------------
🔴 [1] طريقة نشر مقال REDDIT في 15 ثانية:
-----------------------------------------------------------------------------
1. افتح صفحة إنشاء المنشور على حسابك في Reddit:
   👉 https://www.reddit.com/r/u_Dull-Nectarine4963/submit
   (أو افتح أي مجتمع طبي /subreddit ترغب بالنشر فيه)
2. افتح الملف:
   📄 [قالب_ريديت_Reddit]_جاهز_للنشر.md
3. انسخ السطر الأول وضعه في خانة "Title".
4. انسخ باقي النص وضعه في خانة "Post (Text)".
5. اضغط على زر "Post" وسيكون مقالك منشوراً فورياً بنسبة 100%!

-----------------------------------------------------------------------------
📝 [2] طريقة نشر مقال BLOGGER في 15 ثانية:
-----------------------------------------------------------------------------
الطريقة (أ) - النسخ واللصق المباشر (الأسهل والأسرع):
1. افتح لوحة تحكم مدونتك:
   👉 https://draft.blogger.com/blog/posts/6258225961862592152
2. اضغط على زر "مشاركة جديدة" (+ New Post).
3. ضع في العنوان:
   {title}
4. من شريط الأدوات بأعلى اليمين، اضغط على أيقونة القلم واختر: "عرض HTML" (<>).
5. افتح الملف:
   📄 [قالب_بلوجر_Blogger]_جاهز_للنشر.html
   وانسخ محتواه بالكامل والصقه في المحرر.
6. في القائمة الجانبية (Labels / التصنيفات)، الصق:
   {labels}
7. اضغط على زر "نشر" (Publish) البرتقالي!

الطريقة (ب) - الاستيراد التلقائي بضغطة زر:
1. من لوحة Blogger، ادخل على "الإعدادات" (Settings) -> "إدارة المدونة" (Manage blog).
2. اختر "استيراد المحتوى" (Import content).
3. ارفع الملف الجاهز:
   📦 [استيراد_بلوجر_XML]_blogger_import.xml
   وسيتم إنشاء المقال بجميع وسومه وبياناته تلقائياً!

-----------------------------------------------------------------------------
🌟 جميع الملفات جاهزة ومحفوظة في مجلدك:
{READY_DIR.resolve()}
=============================================================================
"""
    guide_file = READY_DIR / "00_دليل_النشر_السريع.txt"
    guide_file.write_text(guide_txt, encoding="utf-8")

    print("[+] 🎉 تم إنشاء وتجهيز حزمة النشر الجاهزة بنجاح في:")
    print(f"    {READY_DIR.resolve()}")
    return True

if __name__ == "__main__":
    generate_pack()
