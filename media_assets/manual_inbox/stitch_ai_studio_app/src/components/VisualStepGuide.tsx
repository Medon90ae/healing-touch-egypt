import React from 'react';
import { 
  Sparkles, 
  Droplets, 
  ShieldCheck, 
  Layers, 
  CheckCircle2, 
  AlertCircle,
  Clock,
  ArrowDown
} from 'lucide-react';
import { CampaignId } from '../types/campaign';
import { useInView } from '../hooks/useInView';

interface VisualStepGuideProps {
  campaignId: CampaignId;
  campaignName: string;
  onScrollToCatalog: () => void;
}

interface StepItem {
  stepNumber: number;
  title: string;
  subtitle: string;
  timing: string;
  description: string;
  proTip: string;
  imageUrl: string;
  badges: string[];
}

export const VisualStepGuide: React.FC<VisualStepGuideProps> = ({
  campaignId,
  campaignName,
  onScrollToCatalog
}) => {
  const { ref, isInView } = useInView();

  const getStepsForCampaign = (): StepItem[] => {
    switch (campaignId) {
      case 'rhinoplasty':
        return [
          {
            stepNumber: 1,
            title: 'تنظيف وتطهير جلد الأنف',
            subtitle: 'إزالة الإفرازات الدهنية برفق',
            timing: 'دقيقة واحدة صباحاً ومساءً',
            description: 'امسحي جلد الأنف بمحلول ملحي معقم (Saline) أو كحول طبي 70% وجففيه تماماً بقطنة طبية خالية من الوبر. جفاف الجلد التام هو سر ثبات اللاصق الطبي.',
            proTip: 'تجنبي استخدام المرطبات أو الزيوت قبل اللصق لأنها تمنع التصاق الميكروبور بالبشرة.',
            imageUrl: 'https://images.unsplash.com/photo-1512290900672-1f5539d91fbd?auto=format&fit=crop&w=600&q=80',
            badges: ['تطهير معقم', 'خالي من الزيوت']
          },
          {
            stepNumber: 2,
            title: 'تثبيت دعامة فتحات الأنف السيليكونية',
            subtitle: 'الحفاظ على التناظر الهيكلي لمجرى التنفس',
            timing: 'يومياً خلال ساعات النوم',
            description: 'مرري دعامة الأنف الطبية المصنوعة من السيليكون النقي برفق داخل فتحات الأنف مع تليينها بنقطة سيروم طبي لمنع تضيق فتحات التنفس أثناء التئام الغضاريف.',
            proTip: 'نظفي الدعامة يومياً بالماء الفاتر والصابون الطبي غير المعطر قبل إعادة ارتدائها.',
            imageUrl: 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80',
            badges: ['سيليكون نقي 100%', 'مجرى هواء آمن']
          },
          {
            stepNumber: 3,
            title: 'تطبيق بلاستر 3M Micropore بضغط متزن',
            subtitle: 'تقنية التثبيت المتدرج لتصريف تورم الأرنبة',
            timing: 'من 6 إلى 8 أسابيع متواصلة',
            description: 'قصي 3 إلى 4 شرائح من شريط 3M البيج وثبتيها بنمط متقاطع على جسر الأرنبة مع ضغط متوازن من الأسفل للأعلى لطرد السوائل اللمفاوية المحتبسة.',
            proTip: 'انزعي البلاستر دائماً بتبليله بالماء الدافئ دون شده بقوة لحماية الغضاريف الملتحمة حديثاً.',
            imageUrl: 'https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80',
            badges: ['3M أصلي بلون البشرة', 'تصريف السوائل']
          }
        ];
      case 'bariatric':
        return [
          {
            stepNumber: 1,
            title: 'تنظيف فتحات التروكار وتجفيفها التام',
            subtitle: 'التحضير السريري لمواضع المناظير الجراحية',
            timing: 'اليوم 7 إلى 10 بعد العملية',
            description: 'اغسلي مواضع الثقوب الجراحية بلطف بماء فاتر ورغوة طبية مضادة للبكتيريا، ثم جففي بمنديل معقم بلمسات خفيفة جداً بدون أي فرك.',
            proTip: 'تأكدي من سقوط القشور السطحية الجافة تلقائياً قبل تغطية الجرح بأي مادة حاجزة.',
            imageUrl: 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80',
            badges: ['تعقيم جراحي', 'بدون احتكاك']
          },
          {
            stepNumber: 2,
            title: 'رش سبراي Opsite الشفاف العازل',
            subtitle: 'طبقة فيلم بولي يوريثان مرنة ومقاومة للماء',
            timing: 'قبل الاستحمام مباشرة',
            description: 'رجي عبوة سبراي Opsite ورشي طبقة رقيقة على مسافة 15 سم فوق فتحات المناظير. تجف خلال 40 ثانية مشكلة درعاً عازلاً غير مرئي يمنع تسرب المياه نهائياً.',
            proTip: 'السبراي يسمح للجلد بالتنفس الطبيعي ويتساقط تدريجياً مع تجدد خلايا الجلد دون أي ألم.',
            imageUrl: 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?auto=format&fit=crop&w=600&q=80',
            badges: ['درع سائل فوري', 'مقاوم للماء 100%']
          },
          {
            stepNumber: 3,
            title: 'تطبيق شرائح السيليكون على مواضع الثقوب',
            subtitle: 'تسطيح فوري ومنع تصبغ نقاط المنظار',
            timing: '12 ساعة يومياً لمدة 8 أسابيع',
            description: 'قصي مربعات صغيرة من شرائح BUPY السيليكونية لتغطي كل فتحة بزيادة 1 سم عن الحواف. توفر الشريحة ضغطاً يمنع تضخم الندبة وتوحد لون الجلد.',
            proTip: 'اغسلي الشريحة يومياً وجففيها لإعادة استخدامها لأكثر من 20 يوماً بكفاءة كاملة.',
            imageUrl: 'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?auto=format&fit=crop&w=600&q=80',
            badges: ['سيليكون BUPY الأصلي', 'تسطيح ومنع التصبغ']
          }
        ];
      case 'thyroid':
        return [
          {
            stepNumber: 1,
            title: 'تطهير خط الرقبة العرضي بلطف',
            subtitle: 'حماية منطقة الغدة الدرقية الحساسة',
            timing: 'اليوم 10 إلى 14 بعد فك الغرز',
            description: 'نظفي ثنية الرقبة بلطف بماء معقم وجففي المحيط تماماً. نظراً لأن جلد الرقبة رقيق جداً، يجب تجنب الشد العنيف أو العطور نهائياً.',
            proTip: 'احرصي على عدم تعريض الجرح لحرارة المجفف أو البخار الكثيف في هذه المرحلة المبكرة.',
            imageUrl: 'https://images.unsplash.com/photo-1512290900672-1f5539d91fbd?auto=format&fit=crop&w=600&q=80',
            badges: ['أمان تام للرقبة', 'خالي من العطور']
          },
          {
            stepNumber: 2,
            title: 'تطبيق شريحة BUPY السيليكونية فائقة الرقة',
            subtitle: 'مرونة مطاطية تتماشى مع حركة الرقبة والبلع',
            timing: 'ارتداء مستمر ليل نهار',
            description: 'ثبتي شريحة السيليكون بطول خط الجرح. تمتاز شريحة BUPY بسماكة 0.5 مم فائقة النعومة وتتحرك بانسيابية مع حركات البلع والالتفات دون انفصال.',
            proTip: 'الترطيب الدائم للسيليكون يمنع إحساس الخنق أو الشد المزعج المصاحب لندبات الغدة.',
            imageUrl: 'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?auto=format&fit=crop&w=600&q=80',
            badges: ['سماكة 0.5 مم مرنة', 'تثبيت مع حركة البلع']
          },
          {
            stepNumber: 3,
            title: 'حماية الجرح العرضي بشريط 3M الواقي من الشمس',
            subtitle: 'حجب الأشعة فوق البنفسجية ومنع اسمرار الأثر',
            timing: 'عند الخروج والتعرض للضوء النهاري',
            description: 'ثبتي شريط 3M Micropore بلون البشرة فوق شريحة السيليكون أو بعد نزعها لحجب أشعة الشمس المباشرة وحماية الندبة من فرط التصبغ (Hyperpigmentation).',
            proTip: 'أشعة الشمس هي العدو الأول لندبة الرقبة؛ حجب الضوء يضمن تلاشي الخط ليماثل لون الرقبة الطبيعي.',
            imageUrl: 'https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80',
            badges: ['حماية UV', 'تطابق تام مع لون الجلد']
          }
        ];
      case 'c-section':
      default:
        return [
          {
            stepNumber: 1,
            title: 'تجهيز وتجفيف محيط الجرح القيصري',
            subtitle: 'التنظيف الطبي بلمسات لطيفة بدون احتكاك',
            timing: 'الخطوة الأولى قبل الاستحمام أو تثبيت السيليكون',
            description: 'اغسلي محيط أسفل البطن بماء فاتر ورغوة صابون طبي غير معطر. جففي حواف الجرح القيصري بالتربيت الخفيف جداً بواسطة شاش معقم قطني. تجنبي تماماً فرك الجرح بالليفة أو استخدام الكحول المركز.',
            proTip: 'تأكدي أن الجلد جاف تماماً وخالٍ من أي زيوت أو كريمات لضمان أقصى التصاق للضمادات.',
            imageUrl: 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80',
            badges: ['تعقيم معتمد', 'تربيت بدون فرك']
          },
          {
            stepNumber: 2,
            title: 'تثبيت درع الاستحمام العازل 3M Tegaderm',
            subtitle: 'عزل مائي ميكانيكي بنسبة 100% أثناء الاستحمام',
            timing: 'أول 10 إلى 14 يوماً مع كل استحمام',
            description: 'انزعي الغلاف الواقي لضمادة 3M Tegaderm وضعي الغشاء الشفاف مباشرة فوق جرح القيصرية مع الضغط على الأطراف بلطف لإحكام الغلق. استمتعي بحمامك المنعش دون أي خوف من تسرب المياه أو الشامبو.',
            proTip: 'بعد الانتهاء من الاستحمام، انزعي الضمادة برفق من زاوية مائلة ببطء لمنع شد الجلد.',
            imageUrl: 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?auto=format&fit=crop&w=600&q=80',
            badges: ['عزل مائي 100%', 'منفذ للبخار والغازات']
          },
          {
            stepNumber: 3,
            title: 'تطبيق شرائح السيليكون BUPY بالضغط المتوازن',
            subtitle: 'المرحلة العلاجية المستمرة لتسطيح الندبة وتوحيد اللون',
            timing: 'من اليوم 10 حتى 12 أسبوعاً',
            description: 'قصي شريحة BUPY السيليكونية لتتجاوز طرفي الجرح القيصري بمقدار 1 إلى 2 سم. ضعي الجانب اللاصق مباشرة على أثر الجرح مع ضغط ناعم. ابدئي بـ 4 ساعات يومياً ثم زيديها تدريجياً حتى 12 إلى 24 ساعة.',
            proTip: 'اغسلي الشريحة يومياً بماء دافئ وصابون طبي ودعيها تجف ذاتياً؛ يمكن إعادة استخدام نفس الشريحة لـ 20-30 يوماً.',
            imageUrl: 'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?auto=format&fit=crop&w=600&q=80',
            badges: ['سيليكون BUPY المعتمد', 'قابلة للغسيل وإعادة الاستخدام']
          }
        ];
    }
  };

  const steps = getStepsForCampaign();

  return (
    <section
      id="visual-step-guide"
      ref={ref}
      className="py-12 sm:py-16 bg-white border-b border-[#E2ECE6]"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div
          className={`text-center max-w-3xl mx-auto mb-12 transition-all duration-500 ${
            isInView ? 'animate-fade-in-up opacity-100' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <Layers className="w-4 h-4 text-[#059669]" />
            <span>دليل التطبيق السريري العملي (Visual Application Guide)</span>
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#003527] mb-3">
            3 خطوات بسيطة لبروتوكول تعافي آمن ومثالي
          </h2>
          <p className="text-sm sm:text-base text-[#404944]">
            اتباع الخطوات بالترتيب التشريحي الصحيح يضمن أفضل نتائج تجميلية ويمنع المضاعفات الميكروبية بنسبة 100%.
          </p>
        </div>

        {/* 3 Steps Visual Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {steps.map((step, idx) => (
            <div
              key={step.stepNumber}
              className={`flex flex-col bg-[#FBFDFB] rounded-2xl border border-[#E2ECE6] overflow-hidden shadow-sm hover:shadow-md transition-all duration-300 ${
                isInView ? `animate-fade-in-up delay-${idx * 100} opacity-100` : 'opacity-0 translate-y-6'
              }`}
            >
              {/* Image Container with Badges */}
              <div className="relative aspect-4/3 overflow-hidden bg-[#F3F7F5] border-b border-[#E2ECE6] group">
                <img
                  src={step.imageUrl}
                  alt={step.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  loading="lazy"
                  onError={(e) => {
                    // Fallback to placeholder if external image fails
                    e.currentTarget.src = 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80';
                  }}
                />
                {/* Step Number Badge */}
                <div className="absolute top-3 right-3 w-10 h-10 rounded-xl bg-[#003527] text-white flex items-center justify-center font-bold text-lg shadow-md border border-[#82F5C1]">
                  {step.stepNumber}
                </div>

                {/* Badges on bottom */}
                <div className="absolute bottom-3 right-3 flex flex-wrap gap-1.5">
                  {step.badges.map((b, bIdx) => (
                    <span
                      key={bIdx}
                      className="px-2 py-0.5 rounded-full bg-white/90 backdrop-blur-xs text-[#003527] text-[11px] font-bold shadow-2xs border border-[#E2ECE6]"
                    >
                      {b}
                    </span>
                  ))}
                </div>
              </div>

              {/* Content Body */}
              <div className="p-6 flex-1 flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-center gap-1.5 text-xs text-[#059669] font-bold mb-1">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{step.timing}</span>
                  </div>
                  <h3 className="text-lg font-bold text-[#003527] mb-1">
                    {step.title}
                  </h3>
                  <div className="text-xs text-[#707974] font-medium mb-3">
                    {step.subtitle}
                  </div>
                  <p className="text-xs sm:text-sm text-[#404944] leading-relaxed">
                    {step.description}
                  </p>
                </div>

                {/* Pro-Tip Box */}
                <div className="p-3 rounded-xl bg-[#EFF4FF] border border-[#DEE9FC] text-xs text-[#003527] flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#059669] shrink-0 mt-0.5" />
                  <div className="leading-relaxed">
                    <span className="font-bold">نصيحة أخصائية التعافي: </span>
                    {step.proTip}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Action Callout */}
        <div className="mt-10 p-5 rounded-2xl bg-gradient-to-r from-[#F3F7F5] via-white to-[#F3F7F5] border border-[#D0DBED] flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-right">
          <div>
            <div className="text-sm font-bold text-[#003527]">
              تريدين الحصول على كافة أدوات البروتوكول في حقيبة واحدة معتمدة؟
            </div>
            <div className="text-xs text-[#707974]">
              تصفحي باقات البروتوكول المجهزة طبياً بأفضل سعر شامل الاستشارة المجانية والتوصيل السريع
            </div>
          </div>
          <button
            type="button"
            onClick={onScrollToCatalog}
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-[#064E3B] hover:bg-[#003527] text-white text-xs sm:text-sm font-bold transition-all shadow-xs cursor-pointer active:scale-98 shrink-0"
          >
            <span>عرض باقات البروتوكول</span>
            <ArrowDown className="w-4 h-4" />
          </button>
        </div>
      </div>
    </section>
  );
};
