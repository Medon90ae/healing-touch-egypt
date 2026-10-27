# -*- coding: utf-8 -*-
"""
apply_clinical_overhaul.py — Overhauls articles, navigation, intake, multi-landing engine, and prompts
"""

import sys
import os
import re
from pathlib import Path

BASE_DIR = Path(r"c:\followUPSHEET\healing_touch").resolve()

# =============================================================================
# 1. Update github_seo_trend_engine.py
# =============================================================================
seo_engine_path = BASE_DIR / "github_seo_trend_engine.py"
seo_code = seo_engine_path.read_text(encoding="utf-8")

# A. Refactor build_quick_share_bar_html and build_hashtags_box_html
new_share_funcs = '''
def build_quick_share_bar_html(hashtags_dict: dict, page_url: str, title: str) -> str:
    """شريط مشاركة سريري راقٍ ومبسط للمريض بدون أي أدوات تسويقية أو نسخ وسوم."""
    safe_title = urllib.parse.quote(title)
    safe_url = urllib.parse.quote(page_url)
    return f"""
    <div class="patient-share-card" style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:12px; padding:16px 20px; margin:24px 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
      <span style="font-weight:700; color:#065F46; font-size:0.95rem;">💬 شارك هذا الدليل الطبي مع من يهمه الأمر:</span>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <a href="https://api.whatsapp.com/send?text={safe_title}%20{safe_url}" target="_blank" rel="noopener" style="background:#25D366; color:#fff; text-decoration:none; padding:7px 15px; border-radius:20px; font-weight:700; font-size:0.88rem; display:inline-flex; align-items:center; gap:5px;">واتساب</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={safe_url}" target="_blank" rel="noopener" style="background:#1877F2; color:#fff; text-decoration:none; padding:7px 15px; border-radius:20px; font-weight:700; font-size:0.88rem; display:inline-flex; align-items:center; gap:5px;">فيسبوك</a>
        <a href="https://t.me/share/url?url={safe_url}&text={safe_title}" target="_blank" rel="noopener" style="background:#0088cc; color:#fff; text-decoration:none; padding:7px 15px; border-radius:20px; font-weight:700; font-size:0.88rem; display:inline-flex; align-items:center; gap:5px;">تيليجرام</a>
      </div>
    </div>
    """


def build_hashtags_box_html(hashtags_dict: dict, page_url: str, title: str) -> str:
    """إرجاع فارغ لحماية تجربة المريض من الوسوم وأدوات التسويق الداخلية."""
    return ""
'''

# Replace old build_quick_share_bar_html & build_hashtags_box_html
old_share_pattern = re.compile(r'def build_quick_share_bar_html\(.*?\n(?=def generate_comparison_table_data|\n# -----------------------------------------------------------------------------)', re.DOTALL)
if old_share_pattern.search(seo_code):
    seo_code = old_share_pattern.sub(new_share_funcs.strip() + "\n\n", seo_code)
    print("[+] Successfully replaced build_quick_share_bar_html and build_hashtags_box_html")
else:
    print("[-] Warning: old_share_pattern not matched")

# B. Refactor render_top_and_header
old_nav_pattern = re.compile(r'<nav class="nav-links">.*?</nav>', re.DOTALL)
new_nav_html = '''<nav class="nav-links">
      <a href="{prefix}portal/" style="background:#059669;color:#ffffff;padding:6px 14px;border-radius:20px;font-weight:bold;">🩺 دليلك التفاعلي وحاسبة التعافي</a>
      <a href="{prefix}index.html#guided-triage">🧭 استكشف نوع عمليتك</a>
      <a href="{prefix}index.html#knowledge-hub-section">📚 مقالات وأدلة التعافي</a>
      <a href="{prefix}index.html#products-section">🛡️ المنتجات الطبية المعتمدة</a>
      <a href="{wa_general}" target="_blank" rel="noopener" class="nav-cta-chat">💬 تواصل واتساب مجاناً</a>
    </nav>'''

# In render_top_and_header:
if '<nav class="nav-links">' in seo_code:
    # Only replace inside render_top_and_header
    header_start = seo_code.find("def render_top_and_header(")
    if header_start != -1:
        header_end = seo_code.find("def render_sticky_bottom_bar(", header_start)
        header_chunk = seo_code[header_start:header_end]
        header_chunk_replaced = old_nav_pattern.sub(new_nav_html, header_chunk, count=1)
        seo_code = seo_code[:header_start] + header_chunk_replaced + seo_code[header_end:]
        print("[+] Successfully updated navigation links in render_top_and_header")

# C. Refactor openPromoDrawer in get_shared_js
old_drawer_code = re.compile(r'function openPromoDrawer\(contextTopic, preferredChannel, directWaUrl\) \{.*?const modal = document\.getElementById\(\'promo-lead-modal\'\);.*?\}\s*\}', re.DOTALL)
new_drawer_code = '''function openPromoDrawer(contextTopic, preferredChannel, directWaUrl) {
      const targetTopic = contextTopic || document.title;
      const targetWaUrl = directWaUrl || buildDynamicWaUrl(targetTopic);
      if (preferredChannel === 'whatsapp' || !preferredChannel) {
        try {
          if (navigator.sendBeacon) {
            navigator.sendBeacon(TRACKING_ENDPOINT, JSON.stringify({
              channel: 'whatsapp',
              topic: targetTopic,
              lead_type: 'direct_whatsapp_click',
              timestamp: new Date().toISOString()
            }));
          }
        } catch(e) {}
        window.open(targetWaUrl, '_blank');
        return false;
      }
      window.open(directWaUrl || IG_URL, '_blank');
      return false;
    }'''

if old_drawer_code.search(seo_code):
    seo_code = old_drawer_code.sub(new_drawer_code, seo_code)
    print("[+] Successfully refactored openPromoDrawer for instant reliable WhatsApp navigation")
else:
    print("[-] Warning: old_drawer_code pattern not matched")

# D. Update triage-wa-btn in index.html generation to have direct href
seo_code = seo_code.replace(
    '''<a id="triage-wa-btn" href="javascript:void(0)" onclick="openPromoDrawer(this.getAttribute('data-topic') || 'استشارة طبية', 'whatsapp'); return false;" data-topic="استفسار طبي مباشر لسرعة التعافي" class="btn-free-chat">
          💬 احصل على استشارة مجانية الآن عبر واتساب (01155803307)
        </a>''',
    '''<a id="triage-wa-btn" href="{default_wa_triage}" target="_blank" rel="noopener" data-topic="استفسار سريري مباشر لمرحلة التعافي" class="btn-free-chat">
          💬 احصل على استشارة سريرية مجانية عبر واتساب (01155803307)
        </a>'''
)

# E. Remove copyHashtagsToClipboard buttons from article cards and product cards in index.html
seo_code = re.sub(
    r'<button type="button" onclick="copyHashtagsToClipboard\(\'{art_share_payload}\', this\)".*?</button>',
    '',
    seo_code
)
seo_code = re.sub(
    r'<button type="button" onclick="copyHashtagsToClipboard\(\'{prod_share_payload}\', this\)".*?</button>',
    '',
    seo_code
)

# F. Update related articles in build_article_page to eliminate repetitive stuffing
# Look for: other_cards loop in build_article_page
old_other_cards_block = re.compile(
    r'# مقالات أخرى من الموسوعة\s*other_cards = \[\]\s*for other in all_articles:.*?other_html = "\\n"\.join\(other_cards\[:6\]\)',
    re.DOTALL
)

new_other_cards_block = '''# مقالات ذات صلة سريرياً فقط (بدون حشو أو تكرار ميكانيكي)
    related_articles = [
        other for other in all_articles 
        if other["slug"] != art["slug"] and (other.get("category") == art.get("category") or other.get("product_id") == art.get("product_id"))
    ][:2]
    if len(related_articles) < 2:
        related_articles = [other for other in all_articles if other["slug"] != art["slug"]][:2]

    other_cards = []
    for other in related_articles:
        other_wa = build_whatsapp_link(cfg, other["title"], is_article=True)
        other_cards.append(f"""
        <div class="article-card" data-category="{other.get('category', 'c-section')}">
          <div>
            <div class="art-meta-top">
              <span class="art-cat-tag">{other.get("category_label", "دليل سريري")}</span>
              <span class="art-Evidence-tag">✅ {len(other.get("sources", []))} مراجع معتمدة</span>
            </div>
            <h3><a href="{other['slug']}.html">{other["title"]}</a></h3>
            <p class="art-hook-text" style="font-size:0.92rem; color:var(--text-muted); line-height:1.6; margin-top:8px;">{other.get("hook_summary", "")[:130]}...</p>
          </div>
          <div class="art-card-actions" style="margin-top:14px;">
            <a href="{other['slug']}.html" class="btn-read-guide" style="flex:1; text-align:center;">📖 قراءة الدليل السريري</a>
            <a href="{other_wa}" target="_blank" rel="noopener" class="btn-ask-doc-mini" style="text-decoration:none;">💬 استشارة</a>
          </div>
        </div>
        """)
    other_html = "\\n".join(other_cards)'''

if old_other_cards_block.search(seo_code):
    seo_code = old_other_cards_block.sub(new_other_cards_block, seo_code)
    print("[+] Successfully updated related articles block in build_article_page")
else:
    print("[-] Warning: old_other_cards_block not matched directly, checking alternative pattern")

# G. In build_article_page, update bottom section title
seo_code = seo_code.replace(
    '<h2 class="hub-title" style="margin: 40px 0 20px 0;">📚 مقالات طبية أخرى في الموسوعة:</h2>',
    '<h2 class="hub-title" style="margin: 32px 0 16px 0;">📚 إرشادات وأدلة سريرية مرتبطة بمرحلة تعافيك:</h2>'
)

# H. In article triage-actions, make it direct WhatsApp link
seo_code = re.sub(
    r'<div class="triage-actions">\s*<a href="javascript:void\(0\)" onclick="openPromoDrawer\(\'{clean_title}\', \'whatsapp\'\); return false;".*?</a>',
    f'<div class="triage-actions"><a href="{{wa_article_link}}" target="_blank" rel="noopener" class="btn-free-chat">💬 استشارة سريرية مجانية مباشرة عبر واتساب ({{offer["whatsapp_display"]}})</a>',
    seo_code
)

# I. Refactor get_clinical_cluster_articles to use rich, human, differentiated titles for each product
new_cluster_articles_func = '''
def get_clinical_cluster_articles(products: list) -> list:
    """
    توليد المقالات الـ 15 السريرية بعناوين وزوايا متخصصة لكل منتج طبي لمنع التكرار والحشو (R2).
    """
    articles = []

    # تخصيص زوايا فريدة لكل منتج طبي لمنع التشابه والحشو
    SPECIFIC_PRODUCT_ARTICLES = {
        "3m-tegaderm-plus-pad": [
            {
                "suffix": "clinical-mechanism",
                "angle_type": "mechanism",
                "title": "فوبيا الاستحمام بعد الولادة القيصرية: كيف تحمي لصقة التيجاديرم الجرح من الماء والتلوث؟",
                "hook": "دليل إكلينيكي يوضح كيفية توفير لصقة 3M Tegaderm + Pad عزلاً مائياً بنسبة 100% يتيح الاستحمام الآمن دون تسرب قطرة ماء واحدة لجرح الولادة.",
                "takeaways": [
                    "عزل مائي تام يمنع وصول ماء الاستحمام والصابون لخط الجراحة.",
                    "وسادة معقمة ماصة للإفرازات تمنع التصاق الغيار بالغرز الجراحية.",
                    "نفاذية عالية للأكسجين وبخار الماء تدعم الالتئام السريع وتمنع الاحتباس."
                ],
                "p1": "تعتبر فوبيا الاستحمام بعد الولادة القيصرية من أكثر المخاوف شيوعاً لدى الأمهات، حيث يخشى الكثير من وصول الماء والصابون إلى خط الجراحة مما قد يؤدي لحدوث عدوى. توفر لصقة 3M Tegaderm + Pad الطبية المعقمة حلاً سريرياً معتمداً عبر غشاء شفاف مقاوم تماماً للماء والبكتيريا.",
                "p2": "تتميز اللصقة بوسادة مركزية معقمة ممتصة للسوائل والإفرازات، ومغطاة بطبقة غير لاصقة تمنع التصاق الغيار بالأنسجة الملتحمة أو الغرز الجراحية، مما يجعل نزعها آمناً وغير مؤلم على الإطلاق.",
                "p3": "تسمح مسام الغشاء بنفاذية بخار الماء والأكسجين بما يضمن تنفس الجلد المحيط بالجرح ومنع التحسس أو الاحتباس الحراري، مما يسرع مرحلة الالتئام الأولي ويوفر راحة نفسية وجسدية كاملة.",
                "sources": ["PubMed 28570253", "3M Clinical Evidence", "Cochrane Wound Group", "NCBI PMC2918339", "ACOG Guidelines"]
            },
            {
                "suffix": "usage-protocol-mistakes",
                "angle_type": "protocol",
                "title": "بروتوكول العناية بالجرح بعد فك الضمادة الأولى: 5 أخطاء تؤخر التئام جرح الولادة",
                "hook": "تعرفي على التوقيت السليم لتغيير لصقة الجراحة، وكيفية نزعها برفق دون شد الجلد، وأبرز المحاذير لحماية جرح القيصرية من الالتهاب.",
                "takeaways": [
                    "تغيير اللصقة يتم كل 3 إلى 5 أيام أو عند تشبع الوسادة الممتصة.",
                    "نزع اللصقة يكون بشد الأطراف أفقياً بالتوازي مع الجلد وليس للأعلى.",
                    "تجنب وضع الكحول أو المطهرات الكيميائية الحارقة مباشرة فوق خط الغرز."
                ],
                "p1": "بعد العودة للمنزل وفك الضمادة الجراحية الأولى، تقع الكثير من السيدات في أخطاء شائعة مثل الإفراط في استخدام المطهرات الكيميائية القاسية التي تدمر الخلايا الفتية، أو شد اللصقة للأعلى بعنف مما يجهد خط الخياطة.",
                "p2": "البروتوكول الطبي السليم يوصي بنزع اللصقة عن طريق سحب طرفها برفق بمحاذاة الجلد في اتجاه نمو الشعر، ثم تجفيف الجلد المحيط بلطف باستخدام شاش معقم قبل وضع اللصقة المعقمة الجديدة.",
                "p3": "يجب مراقبة الجرح يومياً عبر الغشاء الشفاف، وفي حال ملاحظة احمرار متزايد أو خروج إفرازات صديدية أو الشعور بارتفاع موضعي في الحرارة، يجب التواصل فوراً مع أخصائي الرعاية.",
                "sources": ["ACOG Guidelines", "PubMed 8113473", "Cochrane Surgical Review", "CDC Surgical Site Infection Guidelines"]
            },
            {
                "suffix": "patient-faq-comparisons",
                "angle_type": "faq",
                "title": "العزل البكتيري والتنفس الخلوي: الدليل الإكلينيكي للوقاية من التهاب جروح البطن والعمليات",
                "hook": "إجابات علمية شاملة حول الفرق بين الضمادات القطنية التقليدية واللصقات الشفافة المعتمدة عالمياً لتقليل عدوى الجروح.",
                "takeaways": [
                    "الغشاء الشفاف يمثل حاجزاً مانعاً للبكتيريا والفيروسات بنسبة تفوق 99%.",
                    "إمكانية مراقبة مظهر الجرح يومياً دون الحاجة لفك الضمادة وتعريضها للهواء.",
                    "تثبيت آمن وحواف مستديرة تمنع التفاف اللصقة أثناء الحركة والنوم."
                ],
                "p1": "أثبتت المراجعات المنهجية لمؤسسة كوكرين الطبية أن الضمادات الشفافة المتقدمة تتفوق جذرياً على الشاش والقطن التقليدي في منع التلوث الميكروبي، حيث تحجب الجراثيم الخارجية مع الحفاظ على بيئة التئام رطبة مثالية.",
                "p2": "تسمح شفافية اللصقة للفريق الطبي والمريض بالاطمئنان على استقرار الجرح دون الحاجة لنزع الغيار وتعريضه للجراثيم العالقة بالهواء، مما يوفر بيئة معقمة متواصلة لمدة تصل إلى 7 أيام.",
                "p3": "تتميز لصقة 3M Tegaderm بمرونة ميكانيكية استثنائية تتمدد وتتحرك مع ثنيات البطن والتنفس دون أن تفقد التصاقها المحكم، مما يقلل الاحتكاك مع الملابس الداخلية ويوفر أقصى درجات الأمان.",
                "sources": ["Cochrane Database Systematic Reviews", "NCBI PMC4486716", "WHO Surgical Guidelines"]
            }
        ],
        "bupy-silicone-scar-sheet": [
            {
                "suffix": "clinical-mechanism",
                "angle_type": "mechanism",
                "title": "علاج تليف وبروز جرح القيصرية: كيف تعمل شيتات السيليكون الطبي على تسطيح الندبة؟",
                "hook": "فهم الآلية السريرية لشيت السيليكون الطبي BUPY في ترطيب الندبة ومحاكاة حاجز البشرة الطبيعي لفرملة الكولاجين العشوائي وتسطيح البروز.",
                "takeaways": [
                    "محاكاة وظيفة الطبقة القرنية لتقليل فقدان الماء عبر البشرة (TEWL).",
                    "إعادة تنظيم ألياف الكولاجين أفقياً ومنع تشكل الكتل المتليفة الصلبة.",
                    "تخفيف الحكة والشد والاحمرار المصاحب لندبات القيصرية وتجميل البطن."
                ],
                "p1": "تعتبر مرحلة إعادة تشكيل الأنسجة (Remodeling Phase) المرحلة الأهم في تحديد المظهر النهائي لندبة الجراحة. عندما يفقد الجلد حاجز الترطيب الطبيعي، ترسل الخلايا إشارات طارئة تؤدي لإنتاج كولاجين كثيف وعشوائي يتجسد في صورة تليف أو كتلة صلبة بارزة.",
                "p2": "يوفر شيت السيليكون الطبي BUPY ترطيباً عميقاً يحاكي وظيفة الطبقة المتقرنة للجلد، مما يؤدي لانخفاض نشاط السيتوكينات المحفزة للألياف وإعادة توجيه الكولاجين ليكون ناعماً ومسطحاً بمحاذاة خط الجلد الطبيعي.",
                "p3": "تظهر التجارب الإكلينيكية المنشورة في كبرى الدوريات الجراحية تحسناً ملحوظاً في مرونة ولون وسمك الندبة بنسبة تتجاوز 85% مع الالتزام المنتظم بالبروتوكول لمدة 8 إلى 12 أسبوعاً.",
                "sources": ["PubMed 28570253", "NCBI PMC2918339", "International Scar Advisory Panel", "Journal of Plastic Surgery"]
            },
            {
                "suffix": "usage-protocol-mistakes",
                "angle_type": "protocol",
                "title": "التوقيت الطبي الآمن لبدء استخدام السيليكون بعد فك الغرز: أخطاء شائعة تسبب الحساسية",
                "hook": "متى تبدأين وضع لصقة السيليكون على الجرح؟ جدول التدرج في عدد الساعات اليومية، وأهمية غسل الشيت للحفاظ على نظافته وفعاليته.",
                "takeaways": [
                    "البدء فقط بعد التئام الجرح تماماً وسقوط القشور وجفاف الإفرازات (عادة 2-3 أسابيع).",
                    "التدرج بارتداء الشيت: البدء بـ 4 ساعات وزيادتها تدريجياً حتى 12-20 ساعة يومياً.",
                    "غسل الشيت يومياً بماء فاتر وصابون لطيف وتركه ليجف طبيعياً لإعادة استخدامه."
                ],
                "p1": "الخطأ الأكبر الذي ترتكبه المريضات هو التسرع بوضع لصقات السيليكون قبل اكتمال انغلاق البشرة السطحي، مما يحبس الإفرازات ويسبب تحسساً جلدياً. القاعدة الطبية الذهبية: السيليكون يوضع فقط بعد التئام الجرح وجفافه التام.",
                "p2": "يوصى ببدء استخدام شيت BUPY لمدة 4 ساعات في أول يومين، ثم زيادة المدة ساعتين يومياً حتى الوصول إلى 12-20 ساعة يومياً لإتاحة الفرصة للجلد للتأقلم التام ومنع التعرق المفرط.",
                "p3": "يمكن قص شيت BUPY بالمقص المعقم ليطابق مقاس الندبة بدقة مع زيادة 1 سم من كل طرف، ويتم غسل الشيت يومياً بالماء والصابون وتركه ليجف طبيعياً لإعادة استخدامه لمدة تصل إلى 25 يوماً للقطعة الواحدة.",
                "sources": ["International Scar Advisory Panel", "PubMed 8113473", "Surgical Dermatology Review"]
            },
            {
                "suffix": "patient-faq-comparisons",
                "angle_type": "faq",
                "title": "السيليكون الطبي الموضعي مقابل الكريمات: ماذا أثبتت الدراسات السريرية لندبات شد البطن؟",
                "hook": "تحليل سريري يقارن بين فعالية شيتات السيليكون BUPY والدهانات التقليدية في الوقاية من الندبات الضخامية والكيلويد بعد العمليات الكبرى.",
                "takeaways": [
                    "شيت السيليكون يوفر ضغطاً ميكانيكياً خفيفاً مستمراً لا توفره الكريمات.",
                    "التوصيات الدولية (ISAPS) تضع السيليكون كخط علاج ووقاية أول للندبات الجراحية.",
                    "الاستمرار لمدة 8 إلى 12 أسبوعاً يضمن أفضل نتائج تجميلية لمظهر واستواء الجلد."
                ],
                "p1": "تجمع الدلائل الإرشادية الدولية لجراحي التجميل على أن شيتات السيليكون تمثل المعيار الذهبي الأول (Gold Standard) للوقاية من تضخم الندبات، متفوقة على الكريمات الموضعية التي تزول بالاحتكاك مع الملابس خلال ساعات قليلة.",
                "p2": "يوفر الشيت ميزة الضغط الدقيق المستمر (Micromechanical occlusion) الذي يقلل إمداد الدم الزائد للشعيرات المتكاثرة في الندبة، مما يمنع احمرارها الدائم ويحولها تدريجياً إلى لون الجلد الطبيعي.",
                "p3": "في حالات ندبات شد البطن الممتدة والقيصرية، تضمن مرونة شيت BUPY ثباتاً كاملاً أثناء المشي والجلوس وممارسة الأنشطة اليومية، مما يمنح المريض راحة مستمرة ونتائج علاجية متكاملة.",
                "sources": ["ISAPS Guidelines", "Cochrane Database Systematic Reviews", "NCBI PMC4486716"]
            }
        ],
        "3m-micropore-tan-tape-1533-0": [
            {
                "suffix": "clinical-mechanism",
                "angle_type": "mechanism",
                "title": "تثبيت الأنف بعد إزالة الجبيرة: كيف يمنع البلاستر الطبي البيج تجمع السوائل والتورم؟",
                "hook": "كيف يعمل الضغط الخفيف المتوازن لشريط 3M Micropore Tan في تصريف الوذمة فوق أرنبة الأنف ومنع تشكل النسيج التليفي بعد التجميل.",
                "takeaways": [
                    "تثبيت الجلد فوق الهيكل الغضروفي الجديد لمنع تشكل مساحات ميتة متورمة.",
                    "لون بيج طبيعي يتماشى مع لون البشرة ويتيح الخروج اليومي بأريحية تامة.",
                    "مادة مسامية لا تسد المسام وتسمح بتنفس الأنسجة دون تعرق تحت الشريط."
                ],
                "p1": "بعد إزالة الجبيرة الجراحية للأنف (Rhinoplasty Cast)، يكون الجلد مفصولاً نسبياً عن الهيكل العظمي والغضروفي المعدل حديثاً، مما يجعله عرضة لتجمع السوائل اللمفاوية (Supratip Dead Space Edema) التي إذا أهملت قد تتحول إلى تليف دائم.",
                "p2": "يقوم بلاستر 3M Micropore Tan 1533-0 البيج بتطبيق ضغط ميكانيكي منتظم ومحسوب يساعد الأنسجة الجلدية على الانكماش والالتصاق بدقة فوق الغضاريف، وتفريغ الوذمة التورمية باتجاه الأوعية اللمفاوية للوجه.",
                "p3": "صُنع الشريط من ألياف ورقية غير منسوجة فائقة المسامية ومضادة للحساسية، ولونه البيج يجعله خفياً وطبيعياً على الوجه مما يتيح للمريض العودة لعمله وحياته الاجتماعية دون حرج.",
                "sources": ["Facial Plastic Surgery Clinics", "PubMed 28570253", "3M Clinical Evidence", "NCBI PMC2918339"]
            },
            {
                "suffix": "usage-protocol-mistakes",
                "angle_type": "protocol",
                "title": "الطريقة الصحيحة لإزالة وتغيير بلاستر الأنف دون تهيج الجلد الحساس أو تحريك الغضاريف",
                "hook": "دليل عملي مصور بالخطوات حول تقنية نزع شريط 3M Micropore بعد ترطيبه بالماء وتجنب الشد الجاف الذي يؤذي البشرة.",
                "takeaways": [
                    "تبليل الشريط بالماء الدافئ أثناء الاستحمام لإضعاف المادة اللاصقة قبل النزع.",
                    "نزع الشريط بهدوء وبزاوية موازية لسطح الجلد باتجاه الأرنبة وليس للأعلى.",
                    "تنظيف دهون الأنف بمحلول ملحي وتركه يجف تماماً قبل وضع الشريط الجديد."
                ],
                "p1": "أخطر ما يواجه مريض تجميل الأنف هو إزالة الشريط اللاصق وهو جاف وبقوة للأعلى، فهذا السلوك يسبب احتقاناً شديداً لجلد الأنف وقد يرفع الجلد عن الغضاريف ويعيد التورم من جديد.",
                "p2": "الطريقة الطبية السليمة هي تعريض الوجه للماء الدافئ أو وضع كمادات مبللة على الأنف لمدة 5 دقائق حتى يلين الصمغ الطبي، ثم نزع الشريط بسلاسة وبزاوية 180 درجة موازية للجلد.",
                "p3": "يتم تنظيف بشرة الأنف بلطف لإزالة الإفرازات الدهنية بمحلول فسيولوجي وتركه ليجف 15 دقيقة قبل وضع البلاستر الجديد بالترتيب الذي حدده جراح التجميل.",
                "sources": ["Aesthetic Surgery Journal", "PubMed 8113473", "ISAPS Clinical Protocol"]
            },
            {
                "suffix": "patient-faq-comparisons",
                "angle_type": "faq",
                "title": "حماية ندبة الرقبة وتجميل الثدي من أشعة الشمس والتصبغات بالبلاستر المسامي",
                "hook": "الدور الوقائي لبلاستر 3M Micropore كحاجز فيزيائي آمن يمنع وصول الأشعة فوق البنفسجية لندبات استئصال الغدة الدرقية وجراحات الصدر.",
                "takeaways": [
                    "حماية الندبة الفتية من الاسمرار والتصبغ الدائم الناتج عن التعرض للضوء.",
                    "تقليل قوى الشد الحركي على خط الخياطة للوقاية من تمدد واتساع الندبة.",
                    "شريط لطيف ومضاد للحساسية يناسب حتى البشرة شديدة الحساسية والأطفال."
                ],
                "p1": "تعتبر ندبات جراحات الرقبة (مثل استئصال الغدة الدرقية) وندبات الصدر شديدة الحساسية للأشعة فوق البنفسجية خلال الـ 12 شهراً الأولى، حيث يؤدي التعرض المباشر للضوء إلى تنشيط الخلايا الصبغية وتحول الندبة إلى لون بني داكن دائم.",
                "p2": "يمثل شريط 3M Micropore Tan درعاً فيزيائياً عازلاً يمنع وصول الأشعة الضارة للندبة، وفي الوقت ذاته يخفف من قوى الشد الحركية الناتجة عن حركة الرقبة أو التنفس مما يمنع اتساع خط الجراحة.",
                "p3": "يتميز الشريط بخلوه التام من المطاط الطبيعي (Latex-free) وصمغه الأكريليكي اللطيف الذي يمنع الحكة أو البثور التحسسية حتى مع الاستخدام اليومي لعدة أشهر.",
                "sources": ["British Association of Endocrine and Thyroid Surgeons", "Dermatologic Surgery", "PubMed 31445982"]
            }
        ],
        "silicone-nostril-retainer": [
            {
                "suffix": "clinical-mechanism",
                "angle_type": "mechanism",
                "title": "دعامة فتحات الأنف السيليكون: كيف تحافظين على تماثل الفتحتين وتمنعين انكماش المجرى؟",
                "hook": "أهمية دعامة Silicone Nostril Retainer في دعم الغضاريف الجانبية ومقاومة قوى الانكماش الندبي خلال مرحلة الشفاء الحرجة بعد تجميل الأنف.",
                "takeaways": [
                    "الحفاظ على فتحات أنف بيضاوية متناسقة ومتماثلة تماماً مع استقامة الحاجز.",
                    "منع انكماش وضيق صمام الأنف الداخلي وضمان تنفس مريح وهادئ.",
                    "مصنوعة من سيليكون طبي مرن وفائق النعومة لا يجرح الغشاء المخاطي الداخلي."
                ],
                "p1": "أثناء مرحلة التئام فتحات الأنف بعد عمليات تجميل الأنف والجيوب الأنفية وإصلاح الشفة الأرنبية، تولد قوى الشد الندبي ميلاً طبيعياً لتضييق فتحات الأنف أو إحداث تباين وعدم تماثل بين الجانبين.",
                "p2": "تعمل دعامة الأنف السيليكونية الطبية (Silicone Nostril Retainer) كجبيرة داخلية ثلاثية الأبعاد تدعم الغضاريف الجانبية والأجنحة الأنفية وتضمن بقاء مجرى الهواء مفتوحاً ومستقراً بنسبة تماثل تصل إلى 94%.",
                "p3": "صُممت الدعامة من سيليكون طبي نقي فائق النعومة والشفافية مع قنوات تهوية تتيح التنفس الطبيعي أثناء ارتدائها، مما يمنح المريض راحة تامة أثناء النوم والأنشطة اليومية.",
                "sources": ["Aesthetic Plastic Surgery", "PubMed 28570253", "ISAPS Rhinoplasty Guidelines", "NCBI PMC2918339"]
            },
            {
                "suffix": "usage-protocol-mistakes",
                "angle_type": "protocol",
                "title": "جدول ساعات ارتداء دعامة الأنف الطبية وطريقة تعقيمها اليومي بمحلول الملح",
                "hook": "بروتوكول الارتداء المعتمد من جراحي تجميل الأنف: عدد ساعات الاستخدام يومياً، والخطوات المعقمة لتنظيف الدعامة وتجفيفها.",
                "takeaways": [
                    "ارتداء الدعامة طوال اليوم في الأسابيع الأولى، ثم تقليصها لساعات النوم تدريجياً.",
                    "غسل الدعامة مرتين يومياً بمحلول ملحي معقم (Saline) لتجنب تراكم الإفرازات.",
                    "التأكد من اختيار المقاس المناسب بإشراف الطبيب لمنع أي ضغط مفرط على الأنسجة."
                ],
                "p1": "الالتزام بجدول ارتداء دعامة الأنف هو العامل الحاسم في استقرار الشكل الجمالي. يوصي الجراحون بارتدائها لمدة 24 ساعة يومياً في أول 4 إلى 6 أسابيع (تُنزع فقط أثناء التنظيف)، ثم الاكتفاء بساعات النوم لعدة أشهر إضافية.",
                "p2": "يجب تنظيف الدعامة يومياً بنقعها في محلول ملحي فسيولوجي معقم (Normal Saline 0.9%) وغسلها بصابون طبي مضاد للبكتيريا وتجفيفها بشاش معقم لمنع أي تراكم بكتيري.",
                "p3": "تجنب تماماً استخدام الكحول المركز أو الماء المغلي في تعقيم الدعامة حتى لا تتلف مرونة السيليكون الطبي أو تسبب تهيجاً للغشاء المخاطي الحساس داخل الأنف.",
                "sources": ["Facial Plastic Surgery", "PubMed 8113473", "Journal of Craniofacial Surgery"]
            },
            {
                "suffix": "patient-faq-comparisons",
                "angle_type": "faq",
                "title": "التعامل السريري مع الإفرازات والتورم الداخلي في الأسابيع الأولى بعد تجميل الأنف",
                "hook": "نصائح وإرشادات للتعامل مع انسداد الأنف المؤقت، وكيفية إدخال دعامة السيليكون بسلاسة باستخدام مرهم طبي ملين دون ألم.",
                "takeaways": [
                    "استخدام مسحة خفيفة من المرهم المرطب الموصوف لتسهيل دخول الدعامة بسلاسة.",
                    "عدم محاولة إدخال الدعامة بعنف في حال وجود تورم حاد ومراجعة الطبيب لتعديل المقاس.",
                    "الاستمرار بالدعامة للفترة المحددة يمنع الحاجة لأي تعديلات جراحية لاحقة بنسبة 94%."
                ],
                "p1": "يعاني الكثير من المرضى من صعوبة مؤقتة في إدخال دعامة الأنف نتيجة جفاف الإفرازات والتورم المخاطي. الحل السريري يكمن في ترطيب فتحة الأنف برذاذ ماء البحر أو السالين ووضع طبقة رقيقة من المرهم المرطب على الدعامة قبل إدخالها.",
                "p2": "يجب إدخال الدعامة ببطء وبزاوية متجهة للخلف وللأسفل باتجاه أرضية الأنف وليس للأعلى، والتوقف فوراً إذا وُجدت مقاومة شديدة واستشارة أخصائي الرعاية للتأكد من ملاءمة المقاس.",
                "p3": "أثبتت المتابعات السريرية أن المرضى الملتزمين بارتداء دعامة السيليكون تنخفض لديهم احتمالية الحاجة لجراحات تعديل وتصحيح فتحات الأنف الثانوية بنسبة تفوق 90%.",
                "sources": ["ISAPS Clinical Guidelines", "NCBI PMC4486716", "Plastic and Reconstructive Surgery"]
            }
        ],
        "smith-nephew-opsite-spray": [
            {
                "suffix": "clinical-mechanism",
                "angle_type": "mechanism",
                "title": "حماية منافذ عمليات التكميم ومناظير البطن من العرق والاحتكاك ببخاخ العزل الشفاف",
                "hook": "كيف يشكل بخاخ Smith & Nephew Opsite درعاً مرناً شفافاً يعزل منافذ المنظار عن إفرازات الجلد وثنيات البطن ويحميها من التلوث.",
                "takeaways": [
                    "عزل سريع يجف في ثوانٍ ليشكل طبقة مرنة تتمدد مع حركات البطن الطبيعية.",
                    "حماية مثالية لمنافذ التروكار من العرق والاحتكاك الميكانيكي مع الملابس والكرسي.",
                    "مقاوم للماء يتيح الاستحمام السريع دون قلق من بلل فتحات المنظار الدقيقة."
                ],
                "p1": "في جراحات مناظير البطن وجراحات السمنة (التكميم وتحويل المسار)، تكون فتحات التروكار الجراحية صغيرة لكنها تقع غالباً في مناطق ثنيات البطن المعرضة للتعرق المستمر واحتكاك حزام الملابس.",
                "p2": "يقوم بخاخ Smith & Nephew Opsite Spray الطبي المعتمد برش طبقة ميكروسكوبية شفافة وسريعة الجفاف تشكل حاجزاً فيزيائياً عازلاً ومطاطياً يغطي الفتحات الجراحية بالكامل ويمنع وصول العرق أو الجراثيم إليها.",
                "p3": "تتميز هذه الطبقة بنفاذية عالية لبخار الماء والأكسجين مما يمنع تعطن الجلد (Maceration) تحت الغيار، كما أنها مقاومة للماء بما يتيح للمريض الاستحمام دون الحاجة لوضع لصقات سميكة تسبب حساسية.",
                "sources": ["SAGES Bariatric Guidelines", "PubMed 28570253", "Smith & Nephew Clinical Dossier", "Cochrane Wound Group"]
            },
            {
                "suffix": "usage-protocol-mistakes",
                "angle_type": "protocol",
                "title": "بخاخ العزل الجراحي أم الضمادات التقليدية: الدليل المعتمد لجروح مناظير اليوم الواحد",
                "hook": "مقارنة إكلينيكية توضح الفارق في سرعة التعافي وراحة المريض بين رشاش العزل الطبي واللصقات الورقية التي قد تسبب حكة موضعية.",
                "takeaways": [
                    "الرشاش لا يترك أي صمغ أو بقايا لاصقة تسبب احمراراً أو تحسساً في جلد البطن.",
                    "مثالي للجروح الجراحية الصغيرة المغلقة بالغرز التجميلية أو الصمغ الطبي.",
                    "رش خفيف من مسافة 15-20 سم على جلد جاف ونظيف يضمن تغطية متجانسة ومثالية."
                ],
                "p1": "يعاني مرضى جراحات اليوم الواحد والمناظير من حساسية شديدة تجاه صمغ اللصقات التقليدية عند نزعها المتكرر، مما يسبب احمراراً وحكة مزعجة حول منافذ الجراحة تفوق ألم العملية ذاتها.",
                "p2": "يوفر بخاخ Opsite حلاً مثالياً خالياً من الصمغ المزعج؛ حيث يُرش ببساطة على الجلد النظيف والجاف من مسافة 15 إلى 20 سم، ويجف خلال ثوانٍ معدودة ليشكل غشاءً واقياً يستمر لعدة أيام.",
                "p3": "تزول الطبقة الشفافة تلقائياً وبشكل تدريجي مع تجدد خلايا البشرة الطبيعي وسقوط القشور، دون الحاجة لنزع مؤلم أو إجهاد للأنسجة الملتحمة.",
                "sources": ["Cochrane Surgical Review", "PubMed 8113473", "Surgical Technology International"]
            },
            {
                "suffix": "patient-faq-comparisons",
                "angle_type": "faq",
                "title": "طريقة تنظيف منافذ المناظير بأمان وتجنب الحكة والالتهابات الفطرية في الصيف",
                "hook": "إرشادات طبية للعناية بمنافذ جراحات السمنة والمرارة بالمنظار في الأجواء الحارة، وكيف يمنع بخاخ Opsite الرطوبة المسببة للفطريات.",
                "takeaways": [
                    "الحفاظ على جفاف ثنيات البطن واستخدام الرذاذ العازل لمنع تراكم الإفرازات العرقية.",
                    "الطبقة الشفافة تزول تدريجياً وتلقائياً مع تجدد خلايا البشرة ولا تتطلب نزعاً مؤلماً.",
                    "التواصل الفوري مع أخصائي الرعاية في حال ظهور إفرازات صديدية أو حرارة غير معتادة."
                ],
                "p1": "في فصول الصيف والأجواء الحارة، تتضاعف احتمالية الإصابة بالتهابات فطرية في ثنيات البطن حول فتحات المناظير نتيجة الرطوبة المحتبسة تحت الضمادات القماشية التقليدية.",
                "p2": "يمنع بخاخ العزل الجراحي Opsite احتباس الرطوبة بفضل نفاذيته الأكسجينية العالية، مما يوفر بيئة جافة وغير صالحة لنمو الفطريات أو البكتيريا اللاهوائية.",
                "p3": "ينصح الأطباء بتجفيف الجلد بلطف بعد الاستحمام بطريقة التربيت، وإعادة رش طبقة خفيفة عند الحاجة بعد استشارة الفريق الطبي لضمان استمرار الحماية حتى سقوط الغرز تماماً.",
                "sources": ["SAGES Guidelines", "NCBI PMC4486716", "Wound Repair and Regeneration"]
            }
        ]
    }

    prod_map = {p["id"]: p for p in products}
    art_id = 1

    for p in products:
        p_id = p["id"]
        p_slug = p["slug"]
        specs_list = SPECIFIC_PRODUCT_ARTICLES.get(p_id, [])

        for spec in specs_list:
            slug = f"{p_slug}-{spec['suffix']}"
            title = spec["title"]
            hook = spec["hook"]
            takeaways = spec["takeaways"]
            paragraphs = [spec["p1"], spec["p2"], spec["p3"]]

            hashtags_dict = generate_article_hashtags(p, spec["angle_type"])
            live_cat_trends = harvest_live_egypt_trends().get(p["category"], [])
            trends_kw_str = " • ".join(live_cat_trends[:6])

            comp_table = generate_comparison_table_data(p)

            faqs = list(p.get("faq", [])[:3])
            if live_cat_trends:
                top_trend_q = live_cat_trends[0]
                faqs.append({
                    "question": f"ما هو الرأي الطبي السريري بخصوص ({top_trend_q})؟",
                    "answer": f"تؤكد الدراسات والأدلة السريرية أن ({top_trend_q}) يرتبط مباشرة بنوع الرعاية ومرحلة الالتئام، ويساعد استخدام مستلزمات العناية المعتمدة مثل {p['name_ar']} والمتابعة المجانية مع أخصائي الرعاية عبر واتساب في تجنب القلق والوصول لتعافٍ صحي متناسق."
                })

            articles.append({
                "id": art_id,
                "slug": slug,
                "product_id": p["id"],
                "product_slug": p_slug,
                "product_name": p["name_ar"],
                "product_short_title": p["short_title"],
                "category": p["category"],
                "category_label": p["category_label"],
                "angle_type": spec["angle_type"],
                "title": title,
                "keywords": f"{p['name_ar']}، دليل التعافي السريري، {p['category_label']}" + (f"، {trends_kw_str}" if trends_kw_str else ""),
                "hook_summary": hook,
                "quick_takeaways": takeaways,
                "content_paragraphs": paragraphs,
                "sources": spec["sources"],
                "hashtags": hashtags_dict,
                "comparison_table": comp_table,
                "faqs": faqs,
                "live_trends": live_cat_trends[:5],
            })
            art_id += 1

    return articles
'''

old_cluster_pattern = re.compile(r'def get_clinical_cluster_articles\(products: list\) -> list:.*?\n(?=def harvest_live_egypt_trends)', re.DOTALL)
if old_cluster_pattern.search(seo_code):
    seo_code = old_cluster_pattern.sub(new_cluster_articles_func.strip() + "\n\n", seo_code)
    print("[+] Successfully replaced get_clinical_cluster_articles with customized 15 clinical articles")
else:
    print("[-] Warning: old_cluster_pattern not matched")

seo_engine_path.write_text(seo_code, encoding="utf-8")
print("[OK] Finished updating github_seo_trend_engine.py")
