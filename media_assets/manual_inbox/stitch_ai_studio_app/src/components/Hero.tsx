import React from 'react';
import { Droplet, Shield, Award, CheckCircle2, ArrowLeft, Truck } from 'lucide-react';

interface HeroProps {
  onStartCalculator: () => void;
  onExploreProtocol: () => void;
  onInstantOrder: () => void;
}

export const Hero: React.FC<HeroProps> = ({
  onStartCalculator,
  onExploreProtocol,
  onInstantOrder
}) => {
  return (
    <section className="relative overflow-hidden pt-8 pb-14 md:py-16 bg-gradient-to-b from-[#f3f7f5] via-[#fbfdfb] to-[#fbfdfb] border-b border-[#e2ece6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-center">
          
          {/* Main Content Column (7 cols) */}
          <div className="lg:col-span-7 space-y-6 text-right">
            
            {/* Clinical Certification Kicker */}
            <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#064e3b] tracking-normal">
              <span className="w-2 h-2 rounded-full bg-[#059669]"></span>
              <span>البروتوكول الطبي المعتمد لجراحة القيصرية في مصر</span>
              <span className="text-[#bfc9c3]" aria-hidden="true">·</span>
              <span className="text-[#059669]">مطابق لمعايير الجراحة المعقمة</span>
            </div>

            {/* Display Hero Headline */}
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-[#064e3b] leading-[1.3] tracking-tight">
              استحمي براحة وأمان تام من اليوم الثالث —{' '}
              <span className="text-[#059669]">
                دون خوف من ملامسة الماء لجرح القيصرية
              </span>
            </h1>

            {/* Body Description */}
            <p className="text-base sm:text-lg text-[#404944] leading-relaxed max-w-2xl font-normal">
              وداعاً للخوف والقلق أثناء الشاور وللصقات الشاش التقليدية المؤلمة. بروتوكول <strong className="font-semibold text-[#064e3b]">هيلينج تاتش</strong> يوفر درعاً هيدروجيلياً عازلاً للماء 100% يمنع التلوث، مع شرائح السيليكون الطبية المتطورة لتسطيح الندبة وتفتيحها بنسبة 92%.
            </p>

            {/* Key Clinical Guarantees */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              <div className="flex items-center gap-2.5 text-sm text-[#121c2a]">
                <CheckCircle2 className="w-5 h-5 text-[#059669] shrink-0" />
                <span>عزل مائي 100% للشاور بدون ألم عند النزع</span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-[#121c2a]">
                <CheckCircle2 className="w-5 h-5 text-[#059669] shrink-0" />
                <span>وقاية سريرية من الجدرة وتضخم الندبات</span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-[#121c2a]">
                <CheckCircle2 className="w-5 h-5 text-[#059669] shrink-0" />
                <span>حجم جراحي ممتد (25×10 سم) يناسب شق القيصرية</span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-[#121c2a]">
                <CheckCircle2 className="w-5 h-5 text-[#059669] shrink-0" />
                <span>الدفع عند الاستلام مع المعاينة أو عبر إنستاباي</span>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5 pt-3">
              <button
                onClick={onStartCalculator}
                className="flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg text-sm sm:text-base font-semibold text-white bg-[#064e3b] hover:bg-[#003527] transition-all shadow-md active:scale-[0.99] cursor-pointer"
              >
                <span>افحصي جاهزية الشاور لمرحلتك الآن</span>
                <ArrowLeft className="w-4 h-4" />
              </button>

              <button
                onClick={onInstantOrder}
                className="flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg text-sm sm:text-base font-semibold text-[#064e3b] bg-white border border-[#064e3b] hover:bg-[#f3f7f5] transition-all cursor-pointer"
              >
                <span>طلب باقة التعافي الثلاثية</span>
                <span className="text-xs px-2 py-0.5 rounded bg-[#82f5c1]/30 text-[#006c4a] font-bold">
                  توفير 400 ج.م
                </span>
              </button>
            </div>

            {/* Delivery & Assurance Subtext */}
            <div className="flex flex-wrap items-center gap-4 text-xs text-[#526058] pt-2">
              <span className="flex items-center gap-1.5">
                <Truck className="w-4 h-4 text-[#059669]" />
                شحن سريع خلال 24-48 ساعة لجميع المحافظات
              </span>
              <span className="text-[#bfc9c3]" aria-hidden="true">·</span>
              <span className="flex items-center gap-1.5">
                <Award className="w-4 h-4 text-[#d97706]" />
                معتمد من أطباء النساء والتوليد وجراحة التجميل
              </span>
            </div>

          </div>

          {/* Visual Showcase Column (5 cols) */}
          <div className="lg:col-span-5">
            <div className="relative rounded-2xl bg-white border border-[#e2ece6] p-6 shadow-sm overflow-hidden">
              
              {/* Header Badge Inside Box */}
              <div className="flex items-center justify-between pb-4 border-b border-[#e2ece6]">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-[#059669]/10 text-[#059669] flex items-center justify-center">
                    <Shield className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-[#064e3b]">الدرع الجراحي المقاوم للماء</h3>
                    <p className="text-[11px] text-[#526058]">مقاس 25×10 سم للشق العرضي القيصري</p>
                  </div>
                </div>
                <span className="text-xs font-semibold text-[#059669] bg-[#82f5c1]/20 px-2.5 py-1 rounded-full">
                  معقم بالكامل EO
                </span>
              </div>

              {/* Graphical Medical Shield Diagram */}
              <div className="my-6 p-4 rounded-xl bg-gradient-to-br from-[#f8f9ff] to-[#eff4ff] border border-[#d9e3f6] flex flex-col items-center justify-center text-center relative">
                
                {/* Visual Water Repel Simulation */}
                <div className="relative w-full max-w-[300px] h-36 rounded-lg bg-white shadow-inner border border-[#bfc9c3] flex items-center justify-center overflow-hidden">
                  
                  {/* Water Droplets simulation */}
                  <div className="absolute top-2 left-4 flex gap-1 items-center text-xs text-sky-600 font-medium bg-sky-50 px-2 py-0.5 rounded border border-sky-100">
                    <Droplet className="w-3.5 h-3.5 fill-sky-400 text-sky-500" />
                    <span>تيار ماء الشاور</span>
                  </div>

                  {/* Barrier Layer */}
                  <div className="w-[85%] h-8 rounded bg-gradient-to-r from-[#82f5c1]/40 via-[#10b981]/30 to-[#82f5c1]/40 border-2 border-[#059669] flex items-center justify-center shadow-sm">
                    <span className="text-xs font-bold text-[#064e3b]">
                      عازل هيدروجيل مائي (100% Waterproof)
                    </span>
                  </div>

                  {/* Wound Protection Zone */}
                  <div className="absolute bottom-2 text-center">
                    <span className="text-[11px] font-semibold text-[#064e3b] bg-[#fbfdfb] px-3 py-0.5 rounded border border-[#e2ece6]">
                      منطقة جرح القيصرية جافة ومعقمة تماماً
                    </span>
                  </div>
                </div>

                <div className="mt-4 flex items-center justify-around w-full text-xs text-[#404944]">
                  <div>
                    <span className="block font-bold text-base text-[#064e3b]">0.02 مم</span>
                    <span className="text-[11px] text-[#526058]">رقة الغشاء الطبي</span>
                  </div>
                  <div className="h-6 w-px bg-[#bfc9c3]"></div>
                  <div>
                    <span className="block font-bold text-base text-[#059669]">100%</span>
                    <span className="text-[11px] text-[#526058]">عزل الماء والصابون</span>
                  </div>
                  <div className="h-6 w-px bg-[#bfc9c3]"></div>
                  <div>
                    <span className="block font-bold text-base text-[#d97706]">0 ألم</span>
                    <span className="text-[11px] text-[#526058]">عند النزع</span>
                  </div>
                </div>
              </div>

              {/* Kit Quick Snapshot */}
              <div className="p-3.5 rounded-xl bg-[#f3f7f5] border border-[#e2ece6] flex items-center justify-between">
                <div>
                  <span className="block text-xs font-bold text-[#064e3b]">
                    باقة البروتوكول الثلاثي الشاملة
                  </span>
                  <span className="text-[11px] text-[#526058]">
                    لصقات شاور + شرائح سيليكون + جل تجديد الندبات
                  </span>
                </div>
                <div className="text-left shrink-0">
                  <span className="block text-base font-bold text-[#059669] tabular-nums">
                    890 ج.م
                  </span>
                  <span className="text-[11px] text-[#707974] line-through tabular-nums">
                    1,290 ج.م
                  </span>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
