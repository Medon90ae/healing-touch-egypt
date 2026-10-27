# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

p = Path(r'c:\followUPSHEET\healing_touch\campaign_landing_engine.py')
code = p.read_text(encoding='utf-8')

multi_angle_expansion = '''
# =============================================================================
# 3️⃣ محرك بناء صفحات الهبوط المتعددة للمنتج نفسه (Multi-Angle Product LPs)
# =============================================================================
MULTI_ANGLE_LANDING_PAGES_SPEC = {
    "bupy-silicone-scar-sheet": [
        {
            "slug": "bupy-silicone-scar-flattening",
            "title": "علاج تليف وبروز جرح القيصرية وتسطيح الندبة بشيت السيليكون الطبي BUPY",
            "category": "c-section",
            "lead": "كيف تعمل شيتات السيليكون الطبي المتطورة على فرملة إنتاج الكولاجين العشوائي وتنعيم الكتل الصلبة الناتجة عن ندبات القيصرية وجراحات شد البطن.",
            "narrative": """تعتبر مرحلة إعادة تشكيل الأنسجة (Remodeling Phase) المرحلة الأكثر حساسية بعد جراحات البطن والقيصرية. عندما تجف أنسجة الجرح وتفقد رطوبتها الطبيعية، تتكاثر خلايا الفايبروبلاست وتنتج ألياف كولاجين كثيفة غير منتظمة تظهر في صورة بروز جراحي أو كتلة قاسية تحت الجلد.
            
أثبتت المراجعات السريرية أن شيتات السيليكون الطبي BUPY توفر بيئة إغلاق ميكروسكوبية تحاكي الطبقة القرنية للبشرة، مما يخفف التوتر الشعيري ويقلل فقدان السوائل عبر البشرة (TEWL). هذا الترطيب العميق يرسل إشارات بيولوجية للخلايا الليفية لتنظيم ألياف الكولاجين بصورة أفقية مسطحة، مما يؤدي لاستواء الندبة وتراجع بروزها بنسبة تتجاوز 85% خلال 8 إلى 12 أسبوعاً.""",
            "faqs": [
                ("متى ألاحظ بداية استواء الندبة وتراجع الكتلة المتليفة؟", "تبدأ الملاحظات السريرية الأولية في تحسن ملمس ومرونة الندبة وتلاشي الحكة خلال أول أسبوعين إلى 3 أسابيع، بينما يكتمل التسطيح واستعادة لون الجلد الطبيعي تدريجياً بين الشهر الثاني والثالث من الالتزام اليومي."),
                ("هل يصلح شيت السيليكون لندبات القيصرية القديمة؟", "نعم، أثبتت الدراسات فعالية السيليكون الطبي الموضعي في تحسين الندبات المتليفة حتى عمر سنتين، مع التوصية بالاستمرار لمدة لا تقل عن 12 أسبوعاً للحصول على أفضل استواء سريري.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        },
        {
            "slug": "bupy-silicone-timeline-keloid-prevention",
            "title": "التوقيت الطبي الصحيح لبدء استخدام السيليكون بعد فك الغرز والوقاية من الكيلويد",
            "category": "c-section",
            "lead": "الدليل الإكلينيكي لتحديد الموعد الآمن لبدء وضع لصقات السيليكون بعد اكتمال انغلاق البشرة، والجدول التدريجي لساعات الارتداء اليومي.",
            "narrative": """أحد أكثر الأخطاء شيوعاً التي تسبب انتكاسة في التئام الجروح هو التسرع بوضع لصقات السيليكون قبل اكتمال انغلاق طبقة البشرة السطحية. القاعدة الطبية المعتمدة من الجمعية الدولية لجراحي التجميل (ISAPS) تؤكد: لا توضع لصقات السيليكون أبداً فوق جرح مفتوح أو رطب أو يحتوي على إفرازات.
            
الموعد الطبي السليم يبدأ عادة بعد أسبوعين إلى 3 أسابيع من الجراحة، وفور سقوط القشور الجافة والتأكد من التئام الحواف تماماً. يبدأ المريض بجدول تدريجي: 4 ساعات يومياً في أول يومين، ثم زيادة ساعتين يومياً حتى الوصول إلى 12 - 20 ساعة يومياً، مما يمنع حدوث أي تعرق مفرط أو حساسية ويمنع تشكل الكيلويد مبكراً.""",
            "faqs": [
                ("ماذا أفعل إذا شعرت بحكة أو احمرار خفيف في بداية الاستخدام؟", "هذا مؤشر على الحاجة للتدرج اللطيف؛ قومي بنزع الشيت وغسل المنطقة بماء فاتر وتجفيفها، ثم تقليل ساعات الارتداء اليومي إلى 4-6 ساعات لعدة أيام حتى تتأقلم البشرة، مع التأكد من نظافة الشيت وغسله يومياً."),
                ("هل يقي شيت السيليكون من تحول الجرح إلى ندبة سميكة داكنة؟", "نعم، العزل والضغط الميكانيكي المستمر يمنعان اتساع خط الجراحة ويقللان التروية الدموية المفرطة للشعيرات السطحية، مما يحافظ على خط خياطة رفيع فاتح اللون.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        },
        {
            "slug": "bupy-silicone-daily-care-washing-guide",
            "title": "روتين الغسيل اليومي وإعادة استخدام شيت السيليكون BUPY وتجنب الحساسية",
            "category": "c-section",
            "lead": "كيف تغسلين وتحافظين على شيت السيليكون الطبي ليدوم معك حتى 25 يوماً للقطعة الواحدة بكفاءة التصاق وترطيب كاملة.",
            "narrative": """يتميز رول شيت السيليكون BUPY بقابلية الغسيل وإعادة الاستخدام المتكرر، مما يجعله الخيار الاقتصادي والسريري الأوفر والأنسب لعلاج الندبات الطويلة كجروح القيصرية وشد البطن.
            
للحفاظ على كفاءة الالتصاق والطبقة العلاجية: يتم غسل الشيت يومياً بماء فاتر وصابون لطيف خالٍ من الزيوت أو العطور، ثم يُشطف جيداً بالماء ويُترك على سطح نظيف ليجف تلقائياً في الهواء دون استخدام مناديل ورقية قد تترك وبراً على السيليكون. بعد الجفاف، يستعيد الشيت قدرته الطبيعية على الالتصاق ويوضع مجدداً فوق الجلد النظيف والجاف.""",
            "faqs": [
                ("كم يوماً تدوم قطعة الشيت الواحدة بعد قصها؟", "تدوم القطعة الواحدة من 20 إلى 25 يوماً مع الغسيل اليومي السليم، ويمكن قص الرول كاملاً إلى قطع متتالية تكفي كورس العلاج لعدة أشهر."),
                ("هل يمكن وضع كريمات مرطبة تحت شيت السيليكون؟", "لا، يجب أن يوضع شيت السيليكون مباشرة فوق جلد نظيف وجاف تماماً؛ وضع أي زيوت أو كريمات يقلل التصاق الشيت ويسبب انسداد المسام وظهور حبوب دهنية.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        }
    ],
    "3m-tegaderm-plus-pad": [
        {
            "slug": "tegaderm-showering-waterproof-protection",
            "title": "فوبيا الاستحمام بعد الولادة القيصرية وعزل الجرح بلصقة 3M Tegaderm + Pad",
            "category": "c-section",
            "lead": "كيف تضمنين الاستحمام اليومي بأمان تام دون تسرب قطرة ماء واحدة لخط الخياطة، مع وسادة معقمة ممتصة للإفرازات.",
            "narrative": """تشعر الأمهات بعد الجراحة بالقلق الشديد من ملامسة ماء الاستحمام للجرح خوفاً من انتقال الميكروبات أو تفكك الغرز. تم تصميم لصقة 3M Tegaderm + Pad الطبية بغشاء بولي يوريثان شفاف فائق الرقة ومقاوم بنسبة 100% لنفاذ الماء والبكتيريا والفيروسات.
            
تتيح اللصقة للأم الاستحمام الطبيعي بماء دافئ وصابون بحرية تامة دون الحاجة لتغطية الجرح بأكياس بلاستيكية مزعجة. وتحتوي في مركزها على وسادة معقمة عالية الامتصاص مغطاة بطبقة خاصة تمنع التصاقها بخط الجراحة، مما يجعل نزعها بعد الاستحمام أو بعد عدة أيام أمراً سهلاً وخالياً تماماً من الألم.""",
            "faqs": [
                ("هل يمكن الاستحمام فور وضع اللصقة في المستشفى أو المنزل؟", "نعم، فور تثبيت اللصقة والتأكد من التصاق حوافها الشفافة بالجلد الجاف بشكل محكم، توفر عزلاً مائياً فورياً بنسبة 100% يسمح بالاستحمام الآمن."),
                ("كم يوماً يمكن ترك لصقة 3M Tegaderm على الجرح؟", "يمكن ترك اللصقة على الجرح من 4 إلى 7 أيام طالما ظلت الحواف ملتصقة والوسادة المركزية نظيفة، ويتم تغييرها عند تشبع الوسادة أو تراخي الحواف.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        },
        {
            "slug": "tegaderm-sterile-dressing-change-guide",
            "title": "بروتوكول تغيير اللصقة المعقمة بعد فك الضمادة الأولى دون شد الجلد",
            "category": "c-section",
            "lead": "الخطوات السريرية السليمة لنزع واستبدال ضمادة الجراحة المعقمة دون إجهاد خط الخياطة أو التسبب في تهيج الجلد.",
            "narrative": """تغيير الغيار الجراحي الأول في المنزل يتطلب عناية دقيقة لتجنب فتح الغرز أو نقل العدوى. الخطأ الأبرز هو نزع اللصقة بشكل عمودي للأعلى، وهو ما يسبب شداً مفاجئاً على حواف الجرح.
            
البروتوكول الطبي المعتمد: اغسلي يديك جيداً بالماء والصابون، ثم ابدئي بنزع أطراف اللصقة الشفافة بهدوء وموازاة مع سطح الجلد باتجاه نمو الشعر. جففي الجلد المحيط بشاش معقم، ثم ثبتي لصقة 3M Tegaderm + Pad الجديدة من المنتصف باتجاه الأطراف مع الضغط الخفيف على الحواف لضمان إحكام العزل.""",
            "faqs": [
                ("هل أحتاج لوضع مطهر بيتادين أو كحول قبل وضع اللصقة الجديدة؟", "لا ينصح بوضع الكحول أو البيتادين المركز مباشرة وتركه رطباً؛ بل يُنصح بتنظيف الجلد المحيط بمحلول ملحي وتركه ليجف تماماً قبل تثبيت اللصقة المعقمة."),
                ("ما هي علامات التحذير التي تستوجب مراجعة الطبيب؟", "إذا لاحظتِ احمراراً متزايداً يتجاوز 2 سم حول الجرح، أو سخونة موضعية شديدة، أو خروج إفرازات ذات رائحة غير معتادة، يجب استشارة الفريق الطبي فوراً.")
            ],
            "video_fallback": "campaign_c-section_video.mp4"
        }
    ],
    "3m-micropore-tan-tape-1533-0": [
        {
            "slug": "3m-micropore-rhinoplasty-taping-protocol",
            "title": "تثبيت الأنف بعد إزالة الجبيرة ومنع التورم ببلاستر 3M Micropore Tan البيج",
            "category": "rhinoplasty",
            "lead": "كيف يفرغ الضغط المتوازن للبلاستر الطبي البيج 1533-0 الوذمة التورمية ويحافظ على التصاق الجلد بالهيكل الغضروفي الجديد.",
            "narrative": """بعد رفع الجبيرة البلاستيكية أو الجبسية عن الأنف بعد عملية التجميل، يميل الجلد والأنسجة الرخوة للتورم السريع وتجمع السوائل اللمفاوية (Supratip Edema). يمثل بلاستر 3M Micropore Tan 1533-0 الأداة السريرية الأساسية لضبط التعافي في هذه المرحلة.
            
يتميز البلاستر البيج الأصلي بأنه شريط ورقي مسامي خفيف يسمح بتنفس مسام البشرة ويفرغ الضغط بالتساوي فوق جسر الأنف وأرنبته، مما يجبر الجلد على الانكماش والتطابق مع الهيكل العظمي والغضروفي الجديد، ويمنع تشكل الأنسجة الميتة المتليفة مع لون بيج طبيعي وغير لافت.""",
            "faqs": [
                ("كم ساعة يجب وضع البلاستر يومياً بعد إزالة الجبيرة؟", "يوصي معظم جراحي التجميل بوضع البلاستر طوال اليوم (24 ساعة) خلال أول أسبوعين إلى 3 أسابيع، ثم الاكتفاء بوضعه أثناء النوم لمدة شهرين إلى 3 أشهر إضافية."),
                ("كيف أزيل البلاستر دون إيذاء جلد الأنف؟", "بللي البلاستر بالماء الدافئ أثناء الاستحمام حتى يرتخي الصمغ، ثم اسحبيه برفق شديد بمحاذاة الجلد في اتجاه الأرنبة دون شد للأعلى.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        },
        {
            "slug": "3m-micropore-thyroid-neck-sun-protection",
            "title": "حماية ندبة الرقبة وتجميل الصدر من أشعة الشمس والتصبغ بالبلاستر المسامي",
            "category": "thyroid",
            "lead": "الدور الوقائي لبلاستر 3M Micropore كحاجز فيزيائي آمن يمنع وصول الأشعة الضارة لندبات استئصال الغدة الدرقية وجراحات الرقبة.",
            "narrative": """تتعرض ندبات جراحات الرقبة وأعلى الصدر لأشعة الشمس اليومية أثناء الخروج والقيادة، مما يحفز الخلايا الصبغية (Melanocytes) لإنتاج تصبغات بنية داكنة يصعب علاجها لاحقاً.
            
يعمل شريط 3M Micropore Tan كدرع فيزيائي آمن يعكس الأشعة فوق البنفسجية ويمنع وصولها للندبة الحديثة، وفي الوقت نفسه يخفف قوى الشد الحركي الناتجة عن التفاف الرقبة، مما يضمن التئام الجرح في صورة خط أبيض رفيع للغاية وغير ملحوظ.""",
            "faqs": [
                ("هل يسبب بلاستر 3M Micropore حساسية لجلد الرقبة الحساس؟", "صُنع الشريط من ألياف ورقية غير منسوجة مع صمغ أكريليكي خالٍ تماماً من مادة اللاتكس، مما يجعله مضاداً للحساسية ومناسباً للبشرة الحساسة لشهور طويلة."),
                ("متى يمكن البدء بوضع الشريط على ندبة الرقبة؟", "يبدأ استخدامه بعد سقوط خيوط الجراحة والتئام خط الخياطة التام، ويُغير كل 2-3 أيام بعد الاستحمام.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        }
    ],
    "silicone-nostril-retainer": [
        {
            "slug": "silicone-nostril-retainer-symmetry-care",
            "title": "دعامة فتحات الأنف السيليكونية الطبية والحفاظ على تماثل الفتحتين بعد التجميل",
            "category": "rhinoplasty",
            "lead": "كيف تمنع الدعامة السيليكونية انكماش مجرى الهواء الداخلي وتحافظ على فتحات أنف متناسقة ومتماثلة بعد جراحات التجميل وإصلاح الحاجز.",
            "narrative": """تعتبر قوى الانكماش الندبي الداخلي (Cicatricial Contraction) من أكبر التحديات بعد جراحات تجميل الأنف وإصلاح الشفة الأرنبية، حيث تميل الأنسجة الداخلية للتضييق غير المتماثل مما قد يشوه مظهر الفتحات أو يسبب صعوبة في التنفس.
            
تعمل دعامة الأنف السيليكونية (Silicone Nostril Retainer) كدعامة تشريحية مرنة تحافظ على الشكل البيضاوي المتناسق للفتحتين وتمنع التصاق الأنسجة أو انكماش صمام الأنف الداخلي، مع خامة سيليكون طبي فائق النعومة لا يضغط على الغضاريف أو يسبب تقرحات.""",
            "faqs": [
                ("هل تعيق دعامة الأنف التنفس الطبيعي أثناء ارتدائها؟", "لا، الدعامة مزودة بقنوات هوائية واسعة تتيح مرور تيار الهواء بسلاسة والتنفس الطبيعي حتى أثناء النوم."),
                ("كيف يتم اختيار المقاس الصحيح للدعامة؟", "يتم اختيار المقاس بدقة من المقاسات المعتمدة (0 إلى 6) بما يطابق حجم فتحة الأنف دون تمديد زائد للأنسجة، وتحت إشراف أخصائي الرعاية أو الجراح المعالج.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        }
    ],
    "smith-nephew-opsite-spray": [
        {
            "slug": "opsite-spray-bariatric-trocar-protection",
            "title": "حماية منافذ عمليات التكميم ومناظير البطن من العرق والاحتكاك ببخاخ Smith & Nephew Opsite",
            "category": "bariatric",
            "lead": "كيف يشكل بخاخ العزل الجراحي الشفاف طبقة مرنة تحمي فتحات التروكار من العرق وثنيات البطن واحتكاك الملابس اليومي.",
            "narrative": """في جراحات السمنة كالتكميم وتحويل المسار وجراحات المرارة بالمنظار، تتوزع منافذ المنظار الدقيقة على جدار البطن وتتعرض باستمرار للاحتكاك مع حزام البنطال أو العرق المتجمع في ثنيات الجلد.
            
يشكل بخاخ Smith & Nephew Opsite Spray غشاءً مطاطياً شفافاً وفائق الرقة يجف خلال ثوانٍ معدودة بعد الرش، ليوفر حاجزاً فيزيائياً عازلاً يمنع تسرب العرق أو البكتيريا للجروح، مع نفاذية ممتازة للأكسجين تسمح للجلد بالتنفس الطبيعي وتمنع التحسس الناتج عن اللصقات التقليدية.""",
            "faqs": [
                ("هل يتيح بخاخ Opsite الاستحمام اليومي دون قلق؟", "نعم، الطبقة الشفافة مقاومة للماء وتتيح الاستحمام بماء دافئ بلطف، مع تجفيف الجلد بطريقة التربيت الخفيف دون فرك."),
                ("كيف تتم إزالة طبقة البخاخ العازل عن الجلد؟", "لا تحتاج الطبقة لأي نزع أو شد؛ فهي تتلاشى تلقائياً وبشكل تدريجي مع تجدد خلايا البشرة الطبيعي وسقوط القشور.")
            ],
            "video_fallback": "campaign_bariatric_video.mp4"
        }
    ]
}


def generate_all_multi_angle_product_lps() -> list:
    """
    توليد مصفوفة صفحات الهبوط المتعددة والشاملة لكافة المنتجات الطبية (R2-R6).
    """
    created_pages = []
    products = load_products_data()

    for prod_id, specs in MULTI_ANGLE_LANDING_PAGES_SPEC.items():
        matched_prod = next((p for p in products if p.get("id") == prod_id), None)
        prod_title = matched_prod.get("name_ar", "مستلزم طبي معتمد") if matched_prod else "مستلزم طبي معتمد"

        for spec in specs:
            slug = spec["slug"]
            lp_file = LP_DIR / f"{slug}.html"
            page_public_url = f"{SITE_BASE_URL}/lp/{slug}.html"

            # استدعاء الفيديو المخصص إن وجد في docs/assets
            video_rel_path = ""
            video_name = spec.get("video_fallback", "")
            if video_name and (DOCS_DIR / "assets" / video_name).exists():
                video_rel_path = f"../assets/{video_name}"

            # إنشاء بطاقات المنتجات الموصى بها سريرياً
            recommended_prods = [p for p in products if p.get("id") == prod_id]
            if not recommended_prods:
                recommended_prods = products[:2]

            prods_cards_html = []
            for p in recommended_prods:
                prods_cards_html.append(f"""
                <div class="product-lp-card">
                  <div class="prod-badge">{p.get('badge', 'مستلزم طبي معتمد')}</div>
                  <h3>{p.get('name_ar')}</h3>
                  <p class="prod-desc">{p.get('short_summary', p.get('clinical_summary', ''))[:160]}...</p>
                  <div class="prod-clinical-role" style="margin-bottom: 16px; padding: 10px 0; border-top: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9;">
                    <span class="clinical-badge" style="font-size: 0.88rem; font-weight: 800; color: var(--teal-deep);">🛡️ وظيفته: دعم التعافي السريري الآمن</span>
                  </div>
                  <a href="{SITE_BASE_URL}/wa.html?case={spec['category']}&code=HT10&topic={urllib.parse.quote(p.get('name_ar'))}" target="_blank" rel="noopener" class="btn-hero-primary" style="display:block; text-align:center; text-decoration:none; padding:12px 18px; border-radius:10px; font-weight:800;">
                    💬 استشارة سريرية مجانية حول المنتج
                  </a>
                </div>
                """)

            faq_html = "\\n".join([f"""
            <details class="faq-accordion-item">
              <summary class="faq-question">❓ {q}</summary>
              <div class="faq-answer">{a}</div>
            </details>
            """ for q, a in spec["faqs"]])

            video_block = ""
            if video_rel_path:
                video_block = f"""
                <div class="video-container-card">
                  <div class="video-header-tag">🎬 فيديو الشرح السريري التطبيقي المعتمد</div>
                  <video controls autoplay muted loop playsinline class="lp-video-player">
                    <source src="{video_rel_path}" type="video/mp4">
                    متصفحك لا يدعم تشغيل الفيديو المباشر.
                  </video>
                  <p class="video-caption">شرح إكلينيكي مفصل لخطوات التطبيق الصحيح وتجنب الأخطاء الشائعة أثناء مرحلة التعافي.</p>
                </div>
                """

            wa_direct_link = f"https://wa.me/{OFFICIAL_WA_PHONE}?text={urllib.parse.quote(f'أهلاً بكِ، قرأت الدليل السريري حول ({spec[\"title\"]}) في موقع هيلينج تاتش، وأود استشارة سريرية مجانية حول حالتي للتعافي (كود المتابعة: {OFFICIAL_PROMO_CODE}).')}"

            html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{spec['title']} | هيلينج تاتش مصر</title>
  <meta name="description" content="{spec['lead']}">
  <link rel="canonical" href="{page_public_url}">
  
  <meta property="og:type" content="article">
  <meta property="og:title" content="{spec['title']} | هيلينج تاتش مصر">
  <meta property="og:description" content="{spec['lead']}">
  <meta property="og:image" content="../assets/og-image.jpg">
  <meta property="og:url" content="{page_public_url}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    :root {{
      --teal-deep: #064E3B;
      --teal-dark: #065F46;
      --emerald: #059669;
      --mint: #10B981;
      --mint-light: #ECFDF5;
      --amber: #D97706;
      --amber-light: #FEF3C7;
      --surface: #FFFFFF;
      --bg-soft: #F8FAFC;
      --border: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #475569;
      --radius: 16px;
      --shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.08), 0 8px 10px -6px rgba(6, 78, 59, 0.04);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }}
    body {{ background: var(--bg-soft); color: var(--text-main); line-height: 1.75; direction: rtl; padding-bottom: 90px; }}
    
    .top-banner {{ background: var(--teal-deep); color: #fff; text-align: center; font-size: 0.88rem; font-weight: 700; padding: 10px 16px; display: flex; justify-content: center; align-items: center; gap: 8px; flex-wrap: wrap; }}
    .top-banner .code-pill {{ background: var(--amber); color: #fff; padding: 3px 10px; border-radius: 20px; font-weight: 800; letter-spacing: 0.5px; }}
    
    .nav-bar {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto; }}
    .nav-logo {{ font-size: 1.35rem; font-weight: 900; color: var(--teal-deep); text-decoration: none; display: flex; align-items: center; gap: 8px; }}
    .btn-nav-wa {{ background: var(--teal-dark); color: #fff; padding: 9px 18px; border-radius: 10px; font-weight: 700; font-size: 0.9rem; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: 0.2s; cursor: pointer; border: none; }}
    .btn-nav-wa:hover {{ background: var(--emerald); }}

    .container {{ max-width: 980px; margin: 32px auto; padding: 0 20px; }}

    .hero-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 36px; box-shadow: var(--shadow); margin-bottom: 32px; }}
    .category-tag {{ display: inline-block; background: var(--mint-light); color: var(--teal-deep); font-weight: 800; font-size: 0.88rem; padding: 6px 14px; border-radius: 20px; margin-bottom: 16px; border: 1px solid #A7F3D0; }}
    .hero-title {{ font-size: 1.95rem; font-weight: 900; color: var(--teal-deep); line-height: 1.35; margin-bottom: 16px; }}
    .hero-lead {{ font-size: 1.12rem; color: var(--text-muted); margin-bottom: 24px; }}
    
    .trust-badges-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 28px; }}
    .trust-badge-item {{ background: #F1F5F9; border-radius: 10px; padding: 12px 14px; font-weight: 700; font-size: 0.88rem; color: #1E293B; display: flex; align-items: center; gap: 8px; }}
    
    .hero-cta-row {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .btn-hero-primary {{ flex: 1; min-width: 260px; background: #059669; color: #fff; padding: 14px 24px; border-radius: 12px; font-size: 1.05rem; font-weight: 800; text-align: center; border: none; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25); text-decoration: none; display: inline-block; }}
    .btn-hero-primary:hover {{ background: #047857; transform: translateY(-2px); }}
    .btn-hero-secondary {{ flex: 1; min-width: 220px; background: #F8FAFC; color: var(--teal-deep); border: 2px solid var(--border); padding: 14px 20px; border-radius: 12px; font-size: 1rem; font-weight: 800; text-align: center; text-decoration: none; display: flex; justify-content: center; align-items: center; }}
    .btn-hero-secondary:hover {{ background: #F1F5F9; }}

    .video-container-card {{ background: #0F172A; border-radius: var(--radius); padding: 20px; margin-bottom: 32px; color: #fff; }}
    .video-header-tag {{ color: #6EE7B7; font-weight: 800; font-size: 0.95rem; margin-bottom: 12px; }}
    .lp-video-player {{ width: 100%; max-height: 480px; border-radius: 12px; background: #000; outline: none; }}
    .video-caption {{ font-size: 0.88rem; color: #94A3B8; margin-top: 10px; }}

    .clinical-narrative-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; margin-bottom: 32px; box-shadow: var(--shadow); }}
    .clinical-narrative-card h2 {{ font-size: 1.45rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 16px; }}
    .narrative-body {{ font-size: 1.05rem; line-height: 1.85; color: #334155; white-space: pre-line; margin-bottom: 24px; }}

    .products-section-title {{ font-size: 1.5rem; font-weight: 900; color: var(--teal-deep); margin-bottom: 20px; }}
    .products-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-bottom: 36px; }}
    .product-lp-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); display: flex; flex-direction: column; justify-content: space-between; }}
    .product-lp-card h3 {{ font-size: 1.25rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 8px; }}
    .prod-desc {{ font-size: 0.92rem; color: var(--text-muted); margin-bottom: 16px; line-height: 1.6; }}

    .faq-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; box-shadow: var(--shadow); margin-bottom: 36px; }}
    .faq-title {{ font-size: 1.45rem; font-weight: 800; color: var(--teal-deep); margin-bottom: 20px; }}
    .faq-accordion-item {{ border-bottom: 1px solid var(--border); padding: 16px 0; }}
    .faq-accordion-item:last-child {{ border-bottom: none; }}
    .faq-question {{ font-weight: 700; font-size: 1.05rem; color: var(--teal-dark); cursor: pointer; outline: none; }}
    .faq-answer {{ margin-top: 10px; font-size: 0.95rem; color: var(--text-muted); line-height: 1.7; padding-right: 20px; }}

    .footer-bar {{ background: var(--teal-deep); color: #E2E8F0; text-align: center; padding: 28px 20px; font-size: 0.88rem; }}
    .footer-bar a {{ color: #A7F3D0; text-decoration: none; margin: 0 8px; font-weight: 700; }}

    .sticky-mobile-cta {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--surface); border-top: 1px solid var(--border); padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 -4px 16px rgba(0,0,0,0.06); z-index: 999; }}
    .btn-sticky-wa {{ background: #25D366; color: #fff; padding: 10px 20px; border-radius: 10px; font-weight: 800; text-decoration: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; }}

    @media (max-width: 640px) {{
      .hero-card {{ padding: 24px; }}
      .hero-title {{ font-size: 1.55rem; }}
    }}
  </style>
</head>
<body>

  <div class="top-banner">
    <span>🛡️ دليل إرشادي سريري مستقل موثق بالدراسات — كود الاستشارة والمتابعة المجانية:</span>
    <span class="code-pill">{OFFICIAL_PROMO_CODE}</span>
  </div>

  <header class="nav-bar">
    <a href="{SITE_BASE_URL}/" class="nav-logo">
      <span>🛡️ هيلينج تاتش مصر | Healing Touch</span>
    </a>
    <a href="{wa_direct_link}" target="_blank" rel="noopener" class="btn-nav-wa">
      💬 تواصل واتساب مجاناً
    </a>
  </header>

  <main class="container">
    <section class="hero-card">
      <div class="category-tag">دليل التعافي السريري والحلول الطبية</div>
      <h1 class="hero-title">{spec['title']}</h1>
      <p class="hero-lead">{spec['lead']}</p>
      
      <div class="trust-badges-grid">
        <div class="trust-badge-item">✅ موثق بدراسات PubMed & Cochrane</div>
        <div class="trust-badge-item">🛡️ مستلزمات طبية أصلية ومعتمدة 100%</div>
        <div class="trust-badge-item">💬 استشارة سريرية وتوجيه مجاني على واتساب</div>
      </div>

      <div class="hero-cta-row">
        <a href="{wa_direct_link}" target="_blank" rel="noopener" class="btn-hero-primary">
          💬 استشارة سريرية مجانية عبر واتساب
        </a>
        <a href="{SITE_BASE_URL}/portal/" class="btn-hero-secondary">
          🩺 دليلك التفاعلي وحاسبة التعافي
        </a>
      </div>
    </section>

    {video_block}

    <section class="clinical-narrative-card">
      <h2>📖 الشرح السريري والآلية العلمية للتعافي</h2>
      <div class="narrative-body">{spec['narrative']}</div>
      <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:12px; padding:16px 20px;">
        <span style="font-weight:800; color:#065F46;">💡 نصيحة سريرية:</span>
        <span style="color:#166534; font-size:0.95rem;"> احرصي على استشارة أخصائي الرعاية السريرية قبل البدء لتحديد المقاس والبروتوكول الملائم تماماً لتاريخ عمليتك.</span>
      </div>
    </section>

    <section>
      <h2 class="products-section-title">🛡️ المستلزم الطبي الموصى به لهذه المرحلة</h2>
      <div class="products-grid">
        {"".join(prods_cards_html)}
      </div>
    </section>

    <section class="faq-card">
      <h2 class="faq-title">❓ الأسئلة الشائعة والأخطاء الحرجة</h2>
      {faq_html}
    </section>
  </main>

  <footer class="footer-bar">
    <p>جميع الحقوق محفوظة © 2026 هيلينج تاتش مصر | محتوى إرشادي توجيهي غير تجاري</p>
    <p style="margin-top:8px;">
      <a href="{SITE_BASE_URL}/">الصفحة الرئيسية</a> |
      <a href="{SITE_BASE_URL}/portal/">البوابة التفاعلية</a> |
      <a href="{wa_direct_link}" target="_blank" rel="noopener">استشارة واتساب مجانية</a>
    </p>
  </footer>

  <div class="sticky-mobile-cta">
    <div>
      <span style="font-size:0.85rem; font-weight:800; color:var(--teal-deep); display:block;">استشارة ومتابعة سريرية</span>
      <span style="font-size:0.75rem; color:var(--text-muted);">كود الدعم: {OFFICIAL_PROMO_CODE}</span>
    </div>
    <a href="{wa_direct_link}" target="_blank" rel="noopener" class="btn-sticky-wa">
      💬 استشارة واتساب مجانية
    </a>
  </div>

</body>
</html>
"""
            lp_file.write_text(html_content, encoding="utf-8")
            created_pages.append({
                "slug": slug,
                "local_file": str(lp_file),
                "public_url": page_public_url,
                "title": spec["title"],
                "category": spec["category"]
            })

    print(f"[+] تم بناء وتحديث {len(created_pages)} صفحة هبوط مستقلة ومتخصصة لكل منتج طبي في docs/lp/!")
    return created_pages
'''

if "def generate_all_multi_angle_product_lps" not in code:
    code = code + "\n" + multi_angle_expansion
    p.write_text(code, encoding='utf-8')
    print("[+] Successfully added generate_all_multi_angle_product_lps to campaign_landing_engine.py")
else:
    print("[=] generate_all_multi_angle_product_lps already present")
