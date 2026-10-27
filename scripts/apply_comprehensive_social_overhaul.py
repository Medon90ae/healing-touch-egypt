# -*- coding: utf-8 -*-
"""
Apply comprehensive overhaul to antigravity_social_automation.py:
- Sanitizes all remaining discount / price strings.
- Implements interactive product selection for prompt generation (Option 2).
- Generates dedicated Pomelli, Deep Research, and NotebookLM prompts per product.
- Integrates multi-angle LP building and media routing in auto-daily mode.
"""

import sys
from pathlib import Path

BASE_DIR = Path(r"c:\followUPSHEET\healing_touch").resolve()
SOCIAL_FILE = BASE_DIR / "antigravity_social_automation.py"

content = SOCIAL_FILE.read_text(encoding="utf-8")

# 1. Clean up Reddit text line
content = content.replace(
    '**استشارة مجانية عبر واتساب:** 01155803307 | **كود الخصم:** HT10 (شحن مجاني ومعاينة قبل الدفع)\n\n{tmpl[\'hashtags\']}',
    '**للتوجيه السريري والاستشارة المجانية عبر واتساب:** 01155803307\n\n{tmpl[\'hashtags\']}'
)

# 2. Add product configs and upgrade export_notebooklm_master_source
replacement_export = '''PRODUCT_PROMPT_CONFIGS = {
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


def prompt_user_for_product_selection() -> str:
    """عرض قائمة تفاعلية للمستخدم لاختيار المنتج المطلوب للتركيز عليه في برومبتات اليوم."""
    print("\\n" + "=" * 68)
    print("🌿 هيلينج تاتش مصر | اختر المنتج الطبي ليكون محور البحث والمحتوى اليوم:")
    print("=" * 68)
    print("  [1] ضمادة تيغاديرم الشفافة المقاومة للماء (3M Tegaderm +Pad Film)")
    print("      • المحور: الاستحمام الآمن دون بلل، حماية الجروح والعمليات والقساطر")
    print("  [2] شيت السيليكون المطور للندبات (BUPY Medical Silicone Scar Sheet)")
    print("      • المحور: علاج وتسطيح ندبات القيصرية والجراحة، منع الكيلويد، ترطيب الكولاجين")
    print("  [3] شريط ميكروبور الطبي الملون (3M Micropore Tan Surgical Tape 1533-0)")
    print("      • المحور: تثبيت الأنف بعد التجميل، وقاية ندبات الغدة والرقبة من الشمس")
    print("  [4] دعامات الأنف السيليكونية الطبية (Silicone Nostril Retainer)")
    print("      • المحور: دعم فتحات الأنف، منع انكماش الغضاريف وتماثل الأنف بعد التجميل")
    print("  [5] سبراي أوبسايت العازل للجروح (Smith & Nephew Opsite Post-Op Spray)")
    print("      • المحور: عزل ثقوب مناظير التكميم والسمنة، حاجز ميكروبي فوري شفاف")
    print("  [6] إعداد حزمة شاملة لجميع المنتجات الخمسة معاً")
    print("=" * 68)
    
    choice = ""
    try:
        choice = input("اختر رقم المنتج (1-6) [اضغط Enter لاختيار 1 افتراضياً]: ").strip()
    except Exception:
        choice = "1"
        
    if choice not in ("1", "2", "3", "4", "5", "6"):
        choice = "1"
    return choice


def export_notebooklm_master_source(product_choice: str = None) -> str:
    """تجهيز ملف المعرفة والبرومبت الموحد الشامل الجاهز للرفع المباشر في Google NotebookLM مع برومبتات Pomelli و Deep Research."""
    if product_choice is None:
        # إذا كنا في طرفية تفاعلية، نطلب الاختيار من المستخدم
        if sys.stdin and sys.stdin.isatty():
            product_choice = prompt_user_for_product_selection()
        else:
            product_choice = "1"
            
    is_all = product_choice == "6"
    selected_cfg = PRODUCT_PROMPT_CONFIGS.get(product_choice, PRODUCT_PROMPT_CONFIGS["1"])
    prod_name = "كافة المستلزمات الطبية المعتمدة" if is_all else selected_cfg["name_ar"]

    registry_path = BASE_DIR / "products_registry.json"
    products_data = []
    if registry_path.exists():
        try:
            products_data = json.loads(registry_path.read_text(encoding="utf-8")).get("products", [])
        except Exception:
            pass

    now = datetime.now()
    date_display = now.strftime("%Y-%m-%d %I:%M %p")
    timestamp_filename = now.strftime("%Y-%m-%d_%H-%M-%S")

    # جلب أسئلة الترند الحي من جوجل مصر
    live_trend_queries = []
    try:
        from github_seo_trend_engine import harvest_live_egypt_trends
        live_map = harvest_live_egypt_trends()
        cat_key = selected_cfg["category"]
        live_trend_queries = live_map.get(cat_key, [])
    except Exception:
        pass

    # تجهيز ملف البرومبتات القابل للنسخ المباشر PROMPTS_PACK_TODAY.txt
    prompts_pack_lines = [
        "=====================================================================",
        f"🌿 هيلينج تاتش مصر | حزمة البرومبتات والأوامر السريرية الجاهزة للنسخ",
        f"🎯 المنتج ومحور التركيز: {prod_name}",
        f"📅 تاريخ التوليد: {date_display}",
        "=====================================================================",
        "",
        "---------------------------------------------------------------------",
        "1️⃣ برومبت البحث المعمق في Gemini Deep Research (انسخه وضعه في شات Gemini):",
        "---------------------------------------------------------------------",
        "```text",
        f"بصفتك باحثاً إكلينيكياً واستشارياً في جراحة التعافي وعلاج الندبات في مصر:",
        f"أريد بحثاً سريرياً دقيقاً وموثقاً حول: {selected_cfg['clinical_focus']}.",
        "",
        "الأسئلة السريرية والبحثية المحددة المطلوب الإجابة عليها تفصيلياً:",
    ]
    for q in selected_cfg["gemini_research_queries"]:
        prompts_pack_lines.append(f"• {q}")
    prompts_pack_lines.extend([
        "",
        "مخاوف وتساؤلات المرضى المقلقة المطلوب طمأنتهم علمياً بشأنها:",
    ])
    for anz in selected_cfg["patient_anxieties"]:
        prompts_pack_lines.append(f"• {anz}")
    if live_trend_queries:
        prompts_pack_lines.append("")
        prompts_pack_lines.append("تساؤلات وترندات بحث جوجل مصر الصاعدة هذا الأسبوع للإجابة عليها:")
        for tq in live_trend_queries[:4]:
            prompts_pack_lines.append(f"• {tq}")
    prompts_pack_lines.extend([
        "",
        "الشروط الصارمة للمحتوى الناتج:",
        "1. نبرة طبية توجيهية هادئة تشرح فسيولوجيا التئام الأنسجة وتبدد المخاوف دون تهويل.",
        "2. منع تام لأي عروض تسويقية أو خصومات أو أسعار؛ التركيز 100% على الإرشاد والدعم والتثقيف الصحي.",
        "3. إدراج توجيه واضح للتواصل مع أخصائي التعافي عبر واتساب 01155803307 لأي متابعة للحالة.",
        "```",
        "",
        "---------------------------------------------------------------------",
        "2️⃣ برومبتات توليد الصور الطبية في Google Pomelli (صور واقعية سريرية جاهزة للموقع):",
        "---------------------------------------------------------------------",
        "📌 [أولاً: مقاس البوست المربع 1:1 - مخصص للموقع وفيسبوك وإنستجرام Feed]:",
        "```text",
        selected_cfg["pomelli_prompt_1_1"],
        "```",
        "",
        "📌 [ثانياً: مقاس الستوري والريلز العمودي 9:16 - مخصص لإنستجرام وتيك توك وستوري]:",
        "```text",
        selected_cfg["pomelli_prompt_9_16"],
        "```",
        "",
        "---------------------------------------------------------------------",
        "3️⃣ برومبتات استوديو Google NotebookLM (أدوات Video Overview و Audio Overview):",
        "---------------------------------------------------------------------",
        "📌 [أمر الفيديو التوضيحي Video Overview]:",
        "```text",
        f"أنشئ فيديو شارحاً تفاعلياً (Explainer Video) لحالة التعافي باستخدام {selected_cfg['name_ar']} يركز على بيولوجيا التئام الأنسجة وطريقة العناية السليمة بالخطوات، بنبرة طمأنينة علمية راقية تجيب على قلق المريض من الندبات والالتهاب.",
        "```",
        "",
        "📌 [أمر البودكاست الصوتي Audio Overview (حوار استشاري)]:",
        "```text",
        f"قم بتوليد حوار صوتي بين اثنين من استشاريي التعافي الطبي باللهجة المصرية الراقية يشرحان فيه بأسلوب ودي مريح للمريض أهمية {selected_cfg['name_ar']} في مرحلة التعافي، وكيفية التغلب على الحكة أو القلق بعد العملية وتصحيح المفاهيم الخاطئة الشائعة.",
        "```",
        "",
        "---------------------------------------------------------------------",
        "📥 الخطوة التالية ببساطة:",
        "---------------------------------------------------------------------",
        "1. انسخ البرومبتات أعلاه واستخدمها في المنصات المفتوحة أمامك الآن.",
        "2. احفظ مخرجاتك (الصور، الفيديوهات، النصوص) وضعها في مجلد الاستقبال:",
        f"   👉 {MANUAL_INBOX_DIR}",
        "3. بعد وضع الملفات، شغّل run_project.bat واضغط [1]؛ سيتولى النظام آلياً:",
        "   • قراءة وتصنيف كافة الملفات التي رفعتها.",
        "   • بناء وتحديث صفحات الهبوط المتعددة (Multi-Angle LPs) الخاصة بهذا المنتج.",
        "   • تحديث الموقع الكامل وخريطة السيو sitemap.xml ورفعها لـ GitHub Pages.",
        "   • نشر وتوزيع المنشورات على منصات التواصل مع الروابط الحية!",
        "=====================================================================",
    ])

    prompts_pack_txt = "\\n".join(prompts_pack_lines)
    prompts_pack_file = MANUAL_INBOX_DIR / "PROMPTS_PACK_TODAY.txt"
    prompts_pack_file.write_text(prompts_pack_txt, encoding="utf-8")

    # تجهيز ملف المعرفة المصدر لـ NotebookLM
    md_lines = [
        "# 🌿 الدليل السريري وحزمة المعرفة الموحدة – هيلينج تاتش مصر",
        f"**تاريخ ووقت التوليد:** {date_display}",
        f"**محور التركيز السريري:** {prod_name}",
        "**المهمة الأساسية:** التوجيه السريري والدعم التثقيفي للمرضى بعد العمليات الجراحية وتبديد المخاوف وإرشادهم لبروتوكولات التعافي المعتمدة 2026 دون أي ضغط تجاري أو أسعار.",
        "**رابط الاستشارة المجانية المباشر:** `https://medon90ae.github.io/healing-touch-egypt/wa.html` | واتساب: `01155803307`",
        "\\n" + "=" * 60,
        "## 🎯 توجيهات استوديو Google NotebookLM:",
        "=" * 60,
        "1. اعتمد حصرياً على الحقائق السريرية الموثقة في هذا الملف والمراجع العلمية.",
        "2. أجب على كافة استفسارات وتساؤلات المرضى بنبرة علمية داعمة وهادئة.",
        "3. استخدم أدوات الاستوديو (Video Overview, Audio Overview, Study Guide) لإنتاج محتوى غني.",
        "\\n## 🩺 أولاً: تفاصيل المنتج ومحور الحل السريري:",
        f"### {selected_cfg['name_ar']}",
        f"- **التصنيف:** {selected_cfg['category_badge']}",
        f"- **التركيز السريري:** {selected_cfg['clinical_focus']}",
        "",
        "### التساؤلات والمخاوف السريرية للمرضى:",
    ]
    for anz in selected_cfg["patient_anxieties"]:
        md_lines.append(f"- {anz}")

    md_lines.append("\\n## 📚 ثانياً: المراجع السريرية والأبحاث المعتمدة:")
    md_lines.append("- [1] [The Efficacy of Silicone Gel for the Treatment of Hypertrophic Scars and Keloids (NCBI / PMC2918339)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2918339/)")
    md_lines.append("- [2] [Review of Silicone Gel Sheeting and Silicone Gel for Prevention of Hypertrophic Scars (PubMed 28570253)](https://pubmed.ncbi.nlm.nih.gov/28570253/)")
    md_lines.append("- [3] [3M Tegaderm +Pad Film Dressing Clinical Summary (3M Medical Division)](https://multimedia.3m.com/mws/media/864087O/tegaderm-pad-film-dressing-clinical-summary.pdf)")
    md_lines.append("- [4] [Dressings and topical agents for preventing surgical site infections (Cochrane Systematic Reviews)](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD011048.pub2/full)")
    md_lines.append("- [5] [Effect of Postrhinoplasty Taping on Postoperative Edema (ResearchGate)](https://www.researchgate.net/publication/295878140_Effect_of_Postrhinoplasty_Taping_on_Postoperative_Edema_and_Nasal_Draping_A_Randomized_Clinical_Trial)")

    master_file = NOTEBOOKLM_DIR / "Healing_Touch_NotebookLM_Source.md"
    master_file.write_text("\\n".join(md_lines), encoding="utf-8")
    
    timestamp_file = NOTEBOOKLM_DIR / f"Healing_Touch_Brief_{timestamp_filename}.md"
    timestamp_file.write_text("\\n".join(md_lines), encoding="utf-8")

    print(f"[+] 🎯 تم توليد وتجهيز حزمة البرومبتات للمنتج ({prod_name}) بنجاح!")
    print(f"    👉 ملف البرومبتات المباشر: {prompts_pack_file}")
    print(f"    👉 ملف المعرفة لـ NotebookLM: {master_file}")
    
    return str(master_file)
'''

# Replace export_notebooklm_master_source in the content
lines = content.splitlines(keepends=True)
start_line = None
end_line = None
for i, l in enumerate(lines):
    if l.strip().startswith("def export_notebooklm_master_source"):
        start_line = i
    if start_line is not None and i > start_line and l.strip().startswith("def copy_to_windows_clipboard"):
        end_line = i
        break

if start_line is not None and end_line is not None:
    new_lines = lines[:start_line] + [replacement_export + "\n\n"] + lines[end_line:]
    content = "".join(new_lines)
    print(f"[+] Replaced export_notebooklm_master_source between lines {start_line+1} and {end_line+1}")
else:
    print("[!] Could not find bounds for export_notebooklm_master_source replacement")

# 3. In run_unified_studio_and_publish, ensure cle.generate_all_multi_angle_product_lps() is invoked!
if "cle.generate_all_multi_angle_product_lps()" not in content:
    target_call = 'lp_res = cle.build_campaign_landing_page('
    replacement_call = '''# توليد وتحديث كافة صفحات الهبوط متعددة الزوايا للمنتجات الطبية
    try:
        multi_lps = cle.generate_all_multi_angle_product_lps()
        print(f"[+] 🌐 تم بناء وتحديث {len(multi_lps)} صفحة هبوط مستقلة ومتخصصة لكل منتج في docs/lp/!")
    except Exception as e:
        print(f"[!] تنبيه تحديث صفحات الهبوط: {e}")

    lp_res = cle.build_campaign_landing_page('''
    content = content.replace(target_call, replacement_call)
    print("[+] Added generate_all_multi_angle_product_lps call inside run_unified_studio_and_publish")

# 4. In main(), add --product argument
if '--product' not in content:
    target_parser = 'parser.add_argument("--index", type=int, default=None, help="رقم القالب السريري اختيارياً")'
    replacement_parser = '''parser.add_argument("--product", type=str, default=None, choices=["1", "2", "3", "4", "5", "6", "tegaderm", "bupy", "micropore", "nostril-retainer", "opsite", "all"], help="رقم المنتج المراد تحضير البرومبتات والمصادر له")
    parser.add_argument("--index", type=int, default=None, help="رقم القالب السريري اختيارياً")'''
    content = content.replace(target_parser, replacement_parser)

    # In args.mode == "notebooklm": pass args.product
    content = content.replace(
        'if args.mode == "notebooklm":\n        src_path = export_notebooklm_master_source()',
        'if args.mode == "notebooklm":\n        src_path = export_notebooklm_master_source(product_choice=args.product)'
    )
    print("[+] Added --product CLI argument and hooked it to export_notebooklm_master_source")

SOCIAL_FILE.write_text(content, encoding="utf-8")
print("[+] Successfully wrote updated antigravity_social_automation.py")
