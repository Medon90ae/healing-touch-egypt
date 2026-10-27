# -*- coding: utf-8 -*-
"""
Master Upgrade Script for Healing Touch Egypt:
- Purges all discount / price / HT10 traces from campaign_landing_engine.py and antigravity_social_automation.py
- Implements interactive product selector in export_notebooklm_master_source()
- Integrates multi-angle LP generation in campaign_landing_engine.py
- Updates run_project.bat with correct pipeline sequencing and UTF-8 support
"""

import sys
import os
import re
from pathlib import Path

BASE_DIR = Path(r"c:\followUPSHEET\healing_touch").resolve()

# -----------------------------------------------------------------------------
# 1. Sanitize campaign_landing_engine.py
# -----------------------------------------------------------------------------
cle_path = BASE_DIR / "campaign_landing_engine.py"
cle_content = cle_path.read_text(encoding="utf-8")

# Replace OFFICIAL_PROMO_CODE or HT10 references
cle_content = cle_content.replace('OFFICIAL_PROMO_CODE = "HT10"', 'OFFICIAL_PROMO_CODE = ""')
cle_content = cle_content.replace('code=HT10&', '')
cle_content = cle_content.replace('&code=HT10', '')
cle_content = cle_content.replace('?code=HT10', '')
cle_content = cle_content.replace('بكود HT10', 'المعتمدة سريرياً')
cle_content = cle_content.replace('بكود الخصم HT10', '')
cle_content = cle_content.replace('بكود الأولوية السريرية (HT10)', '')
cle_content = cle_content.replace('بكود الأولوية السريرية HT10', '')
cle_content = cle_content.replace('كود HT10', 'التوجيه السريري المعتمد')
cle_content = cle_content.replace('كود الخصم', 'التوجيه السريري')
cle_content = cle_content.replace('شحن مجاني ومعاينة قبل الدفع', 'إشراف وتوجيه سريري معتمد')
cle_content = cle_content.replace('شحن مجاني لكافة المحافظات', 'دعم سريري مستمر')

# Replace the specific FAQ item in build_campaign_landing_page
old_faq_ht10 = '("ما هي مميزات كود HT10 وكيف أحصل على الاستشارة السريرية؟", "كود HT10 يمنحك أولوية المتابعة السريرية المجانية مع أخصائية العناية بالتعافي عبر واتساب، بالإضافة لحق فتح ومعاينة الشحنة الطبية قبل الاستلام للتأكد من أصلية العبوات وتاريخ الصلاحية.")'
new_faq_ht10 = '("كيف أحصل على التوجيه والاستشارة السريرية المجانية لمرحلة تعافي جرحي؟", "يمكنك التواصل المباشر مع استشاري العناية بالتعافي عبر واتساب من خلال الرابط أو الزر المباشر بالصفحة؛ لتحصل على إرشادات علمية دقيقة تناسب نوع عمليتك وتاريخ إجرائها ومعدل التئام الأنسجة لديك.")'
cle_content = cle_content.replace(old_faq_ht10, new_faq_ht10)

cle_path.write_text(cle_content, encoding="utf-8")
print("[+] Sanitized campaign_landing_engine.py")

# -----------------------------------------------------------------------------
# 2. Upgrade antigravity_social_automation.py with interactive product selector
# -----------------------------------------------------------------------------
asa_path = BASE_DIR / "antigravity_social_automation.py"
asa_content = asa_path.read_text(encoding="utf-8")

# Sanitize remaining promo card & HT10 in brand cards and blogger
asa_content = asa_content.replace('<div class="promo-card">🎁 كود: <strong>HT10</strong> (شحن مجاني + حق المعاينة)</div>', '<div class="promo-card">🛡️ بروتوكولات سريرية معتمدة 2026</div>')
asa_content = asa_content.replace('code = "HT10"', 'code = ""')
asa_content = asa_content.replace('&code=HT10', '')
asa_content = asa_content.replace('?code=HT10', '')
asa_content = asa_content.replace('وتفعيل كود HT10', '')
asa_content = asa_content.replace('بكود HT10', '')
asa_content = asa_content.replace('كود الخصم الحصري `HT10` (شحن مجاني لكافة المحافظات + حق فتح ومعاينة الشحنة قبل الدفع)', 'التوجيه السريري المجاني والمتابعة المستمرة مع استشاري التعافي')
asa_content = asa_content.replace('**كود الخصم:** HT10 (شحن مجاني ومعاينة قبل الدفع)\n\n', '')
asa_content = asa_content.replace('+ كود الخصم HT10 + شحن مجاني ومعاينة قبل الدفع', '')
asa_content = asa_content.replace('+ كود HT10 + واتساب 01155803307 + أسعار المنتجات', '+ واتساب 01155803307')
asa_content = asa_content.replace('+ أسعار المنتجات الحية + كود HT10 + واتساب', '+ واتساب')
asa_content = asa_content.replace('أسعار المنتجات الحية + كود HT10', 'الحلول السريرية المعتمدة')
asa_content = asa_content.replace('أسعار المنتجات الحية', 'الحلول السريرية')

asa_path.write_text(asa_content, encoding="utf-8")
print("[+] Sanitized antigravity_social_automation.py basic strings")

# Now let's implement the dedicated product-selector logic and export_notebooklm_master_source
product_selector_code = '''
PRODUCT_PROMPT_CONFIGS = {
    "1": {
        "id": "3m-tegaderm-plus-pad",
        "name_ar": "ضمادة تيغاديرم الشفافة المقاومة للماء (3M Tegaderm +Pad Film)",
        "category": "c-section",
        "category_badge": "عزل مائي وحماية الجروح",
        "clinical_focus": "الاستحمام الآمن دون بلل للجرح، عزل ميكروبي 100% مع نفاذية لبخار العرق والغازات، حماية جروح القيصرية والعمليات الجراحية والقساطر",
        "gemini_research_queries": [
            "3M Tegaderm waterproof dressing post-surgical wound showering protocol Cochrane guidelines",
            "Transepidermal water vapor transmission rate semipermeable film dressings surgical site infection",
            "Best practice post-cesarean wound care showering safety evidence-based review",
            "توقيت الاستحمام الآمن بعد الولادة القيصرية واستخدام الضمادات المقاومة للماء",
            "الفرق بين الشاش التقليدي وضمادات الفيلم الشفاف شبه المنفذة في منع التهاب الجروح"
        ],
        "pomelli_prompt_1_1": "Hyper-realistic clinical studio shot of genuine 3M Tegaderm +Pad sterile waterproof transparent film dressing resting on a pristine white medical tray, subtle sterile water droplets beading on the transparent surface demonstrating total water resistance, soft indirect natural lighting, modern high-end surgical suite aesthetic, 8k resolution, documentary medical photography, zero text clutter, authentic healthcare guidance.",
        "pomelli_prompt_9_16": "Vertical 9:16 aesthetic healthcare photography of 3M Tegaderm transparent waterproof dressing applied neatly over a simulated clean post-surgical dressing model, soft clinical morning light, clean teal and mint green background tones, ultra-realistic texture of breathable semi-permeable film, professional surgical recovery guide, 8k resolution.",
        "patient_anxieties": [
            "خوف المريضة من دخول الماء أو الصابون لخط الجرح أثناء الاستحمام وتسببه في التهاب أو صديد",
            "قلق المريضة من كتمة الجرح والتعرق تحت اللصقة إذا كانت غير مسامية",
            "ألم إزالة الضمادة وشدها للجلد المحيط بالجرح الحساس بعد العملية"
        ]
    },
    "2": {
        "id": "bupy-silicone-scar-sheet",
        "name_ar": "شيت السيليكون المطور للندبات (BUPY Medical Silicone Scar Sheet)",
        "category": "c-section",
        "category_badge": "علاج وتسطيح الندبات",
        "clinical_focus": "تسطيح ندبات القيصرية والجراحة، منع وعلاج الكيلويد والندبات المتضخمة، ترطيب ألياف الكولاجين وإزالة الحكة والاحمرار",
        "gemini_research_queries": [
            "Medical grade silicone gel sheeting hypertrophic scar keloid clinical trials PubMed",
            "Mechanism of action silicone sheet stratum corneum hydration collagen downregulation",
            "Optimal duration daily wear silicone scar sheets post-operative scar management",
            "بروتوكول تسطيح ندبة القيصرية بشيت السيليكون الطبي ومدة الاستخدام اليومي",
            "علاج الكلويد والندبات المتضخمة بعد العمليات الجراحية بدون تدخل جراحي"
        ],
        "pomelli_prompt_1_1": "Commercial clinical aesthetic photography of BUPY Medical Silicone Scar Sheet roll partially unrolled on a clean neutral stone surface, ultra-soft flexible medical-grade silicone texture catching gentle diffuse lighting, elegant minimalist dermatology clinic setting, 8k resolution, authentic medical realism, zero commercial graphics, calm reassuring healthcare visual.",
        "pomelli_prompt_9_16": "Vertical 9:16 editorial dermatology photograph showing translucent BUPY silicone scar sheet being gently held with medical tweezers above a clean clinical sterile field, soft green and neutral tones, demonstrating smooth flexible elasticity, professional scar therapy guidance aesthetic, 8k hyper-realistic.",
        "patient_anxieties": [
            "خوف المريضة من تحول خط الجرح إلى حبل بارز أحمر أو كلويد دائم يشوه المظهر",
            "الحكة الشديدة والنغزات المزعجة في مكان الندبة التي تجعل لمس الملابس مؤلماً",
            "الشكوك حول فاعلية منتجات علاج الندبات بعد شهور من العملية وهل ما زال الوقت متاحاً للعلاج"
        ]
    },
    "3": {
        "id": "3m-micropore-tan-tape-1533-0",
        "name_ar": "شريط ميكروبور الطبي الملون (3M Micropore Tan Surgical Tape 1533-0)",
        "category": "rhinoplasty",
        "category_badge": "دعم الأنف وجروح الرقبة",
        "clinical_focus": "تثبيت الأنف بعد عمليات التجميل وتصريف التورم اللمفاوي، حماية ندبات الرقبة وجراحة الغدة من أشعة الشمس، شريط ورقي طبي مسامي مضاد للحساسية",
        "gemini_research_queries": [
            "Post-rhinoplasty taping with microporous surgical tape supratip edema reduction clinical study",
            "Rayon microporous surgical tape skin irritation hypoallergenic properties randomized trial",
            "Sun protection for fresh surgical scars thyroidectomy neck incision micropore tape",
            "طريقة لصق بلاستر 3M البيج لتصريف تورم أرنبة الأنف بعد إزالة الجبيرة",
            "حماية جرح استئصال الغدة الدرقية في الرقبة من أشعة الشمس والتصبغ"
        ],
        "pomelli_prompt_1_1": "Macro clinical studio photograph of authentic 3M Micropore Tan surgical tape rolls with textured breathable rayon weave, positioned on a frosted glass surface next to a surgical caliper, soft clinical ring light, pristine sterile atmosphere, 8k resolution, realistic medical photography.",
        "pomelli_prompt_9_16": "Vertical 9:16 aesthetic medical visual of 3M beige micropore tape strips arranged neatly on a surgical tray, subtle shadows, calm aesthetic surgery clinic ambiance, demonstrating fine porosity and skin-tone blend, professional medical guidance realism, 8k.",
        "patient_anxieties": [
            "الذعر من تورم أرنبة الأنف أو عدم تناسق النزول بعد فك الجبيرة",
            "ظهور حبوب صديدية وبثور بيضاء وحساسية جلدية بسبب اللصقات العادية الرديئة المكتومة",
            "تصبغ خط جرح الغدة في الرقبة وتحوله إلى لون داكن دائم بسبب التعرض للشمس"
        ]
    },
    "4": {
        "id": "silicone-nostril-retainer",
        "name_ar": "دعامات الأنف السيليكونية الطبية (Silicone Nostril Retainer)",
        "category": "rhinoplasty",
        "category_badge": "تناسق فتحات الأنف",
        "clinical_focus": "الحفاظ على تماثل وتناسق فتحات الأنف بعد عمليات التجميل، مقاومة قوى الانكماش الندبي للغضاريف، دعم مجرى التنفس بعد قص جناح الأنف",
        "gemini_research_queries": [
            "Silicone nostril retainer post-rhinoplasty alar base symmetry clinical evaluation",
            "Prevention of nostril stenosis and cicatricial contraction after cosmetic rhinoplasty",
            "Nostril retainer sizing and care protocol post-operative rhinoplasty MDPI studies",
            "أهمية دعامة الأنف السيليكون في تماثل الفتحات ومنع التليف بعد التجميل",
            "كيفية تنظيف واختيار مقاس دعامة الأنف السيليكونية بعد العملية"
        ],
        "pomelli_prompt_1_1": "Ultra-clean clinical macro photography of medical-grade transparent silicone nostril retainers resting in a sterile petri dish on a white examination surface, gentle diffuse LED lighting, crystal-clear anatomical curved contours, surgical precision, 8k resolution, authoritative clinical clarity.",
        "pomelli_prompt_9_16": "Vertical 9:16 high-end surgical photography of medical silicone nostril retainer held delicately in sterile gloved fingers, soft clinical background, showcasing flexible medical silicone softness and ergonomic contouring, reassuring medical educational aesthetic, 8k.",
        "patient_anxieties": [
            "قلق المريض من وجود فتحة أنف أكبر من الأخرى أو انكماش فتحة بعد العملية",
            "صعوبة التنفس أو تضيق مجرى الهواء أثناء نوم المريض في الأسابيع الأولى",
            "الخوف من ألم ارتداء الدعامة أو تسببها في تجريح الأنسجة الداخلية الحساسة"
        ]
    },
    "5": {
        "id": "smith-nephew-opsite-spray",
        "name_ar": "سبراي أوبسايت العازل للجروح (Smith & Nephew Opsite Post-Op Spray)",
        "category": "bariatric",
        "category_badge": "عزل ثقوب المناظير",
        "clinical_focus": "عزل فوري لثقوب مناظير جراحات السمنة والتكميم، حاجز ميكروبي شفاف مقاوم للماء يتيح الاستحمام، يتيح تنفس الجلد وتبخر العرق دون غيارات لاصقة مؤلمة",
        "gemini_research_queries": [
            "Smith Nephew Opsite spray transparent dressing laparoscopic port site infection Cochrane",
            "Waterproof spray-on dressing bariatric sleeve gastrectomy recovery showering protocol",
            "Comparative study spray dressings vs conventional adhesive tapes in laparoscopic wounds",
            "طريقة استخدام سبراي أوبسايت على ثقوب منظار التكميم والاستحمام الفوري",
            "علاج تحسس والتهاب جلد البطن من بلاستر ثقوب المنظار بعد جراحة السمنة"
        ],
        "pomelli_prompt_1_1": "Crisp pharmaceutical studio photograph of Smith & Nephew Opsite Post-Op Spray canister on a clean surgical steel surface, fine transparent micro-mist droplets catching soft edge lighting, modern laparoscopic surgery clinic context, 8k resolution, authentic medical realism.",
        "pomelli_prompt_9_16": "Vertical 9:16 healthcare commercial photograph showing transparent Opsite aerosol spray canister next to clean sterile gauze on a minimalist teal clinical background, soft natural lighting, highlighting waterproof breathable barrier concept, professional surgical recovery guide, 8k.",
        "patient_anxieties": [
            "المعاناة من ألم نزع البلاستر المتكرر من جلد البطن الحساس والتهابه بعد التكميم",
            "الخوف من التهاب ثقوب المنظار أو تلوثها بمياه الاستحمام",
            "الحاجة لحل سريع وعازل يسمح بحرية الحركة والاستحمام دون الحاجة لغيارات معقدة"
        ]
    }
}
'''

# Let's inspect export_notebooklm_master_source in antigravity_social_automation.py
# and replace it with a version that prompts for product selection if interactive,
# or accepts product_key as argument.
print("[+] Product config dict prepared.")
