import React, { useState } from 'react';
import { AssessmentInput } from '../types/protocol';
import { calculateRecoveryReadiness } from '../utils/calculator';
import { PROTOCOL_PRODUCTS } from '../data/protocolData';
import {
  Calendar,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  ShoppingBag,
  Info
} from 'lucide-react';

interface StageCalculatorProps {
  onSelectProduct: (productId: string) => void;
  onAddToCart: (productId: string) => void;
}

export const StageCalculator: React.FC<StageCalculatorProps> = ({
  onSelectProduct,
  onAddToCart
}) => {
  const [daysPostOp, setDaysPostOp] = useState<number>(5);
  const [closureType, setClosureType] = useState<AssessmentInput['closureType']>('internal_sutures');
  const [dressingStatus, setDressingStatus] = useState<AssessmentInput['dressingStatus']>('removed_clean');
  const [painOrTension, setPainOrTension] = useState<AssessmentInput['painOrTension']>('mild');

  const assessment = calculateRecoveryReadiness({
    daysPostOp,
    closureType,
    dressingStatus,
    painOrTension
  });

  const recommendedProduct = PROTOCOL_PRODUCTS.find(
    (p) => p.id === assessment.recommendedKitId
  ) || PROTOCOL_PRODUCTS[0];

  return (
    <section id="calculator" className="py-14 bg-[#f3f7f5] border-b border-[#e2ece6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center mb-10 space-y-3">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#059669]">
            <Sparkles className="w-4 h-4" />
            <span>حاسبة سريرية معتمدة من استشاريي التوليد والجراحة</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#064e3b]">
            حاسبة مرحلة التعافي القيصري وفحص جاهزية الشاور الآمن
          </h2>
          <p className="text-sm sm:text-base text-[#404944] leading-relaxed">
            حددي عدد الأيام وحالة الجرح للحصول على التوجيه الطبي الفوري الخاص بك، وبروتوكول الاستحمام الآمن دون مجازفة بحدوث التهاب أو تسرب للماء.
          </p>
        </div>

        {/* 2-Column Assessment Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Form Controls Column (6 cols) */}
          <div className="lg:col-span-6 bg-white p-6 sm:p-7 rounded-2xl border border-[#e2ece6] shadow-sm space-y-6">
            
            {/* Input 1: Days Post-Op */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-bold text-[#064e3b] flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-[#059669]" />
                  <span>كم يوماً مضى على ولادتك القيصرية؟</span>
                </label>
                <span className="text-sm font-bold text-[#059669] bg-[#82f5c1]/20 px-3 py-0.5 rounded-full tabular-nums">
                  اليوم {daysPostOp}
                </span>
              </div>

              {/* Slider */}
              <input
                type="range"
                min="1"
                max="90"
                value={daysPostOp}
                onChange={(e) => setDaysPostOp(Number(e.target.value))}
                className="w-full accent-[#059669] h-2 bg-[#e2ece6] rounded-lg cursor-pointer"
              />

              {/* Quick Select Milestones */}
              <div className="flex flex-wrap gap-2 mt-2.5">
                {[
                  { label: 'اليوم 3 (أول شاور)', days: 3 },
                  { label: 'اليوم 7 (الأسبوع الأول)', days: 7 },
                  { label: 'اليوم 14 (سقوط القشور)', days: 14 },
                  { label: 'اليوم 28 (بدء السيليكون)', days: 28 },
                  { label: 'اليوم 60 (التسطيح)', days: 60 }
                ].map((item) => (
                  <button
                    key={item.days}
                    type="button"
                    onClick={() => setDaysPostOp(item.days)}
                    className={`text-xs px-2.5 py-1 rounded-md transition-all cursor-pointer ${
                      daysPostOp === item.days
                        ? 'bg-[#064e3b] text-white font-semibold'
                        : 'bg-[#f3f7f5] text-[#404944] hover:bg-[#e2ece6]'
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Input 2: Incision Closure Type */}
            <div>
              <label className="block text-sm font-bold text-[#064e3b] mb-2">
                نوع إغلاق جرح القيصرية (المستخدم في المستشفى):
              </label>
              <div className="grid grid-cols-2 gap-2.5">
                {[
                  { id: 'internal_sutures', title: 'خياطة تجميلية داخلية', note: 'غرز مدفونة تذوب تلقائياً' },
                  { id: 'cosmetic_glue', title: 'لصق طبي تجميلي', note: 'شريط لاصق طبي دون خيوط' },
                  { id: 'staples', title: 'كبس جراحي (دبابيس)', note: 'تُفك بعد 7-10 أيام' },
                  { id: 'traditional', title: 'غرز تقليدية', note: 'خيوط جراحية خارجية تُفك' }
                ].map((type) => (
                  <button
                    key={type.id}
                    type="button"
                    onClick={() => setClosureType(type.id as any)}
                    className={`p-3 rounded-xl border text-right transition-all cursor-pointer ${
                      closureType === type.id
                        ? 'border-[#059669] bg-[#f3f7f5] shadow-xs ring-1 ring-[#059669]/20'
                        : 'border-[#e2ece6] hover:border-[#bfc9c3] bg-white'
                    }`}
                  >
                    <span className="block text-xs font-bold text-[#121c2a]">{type.title}</span>
                    <span className="block text-[11px] text-[#526058] mt-0.5">{type.note}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Input 3: Dressing / Incision Status */}
            <div>
              <label className="block text-sm font-bold text-[#064e3b] mb-2">
                الحالة الحالية للجرح والضمادة:
              </label>
              <div className="space-y-2">
                {[
                  {
                    id: 'removed_clean',
                    title: 'تمت إزالة ضمادة المستشفى والجرح نظيف وجاف',
                    desc: 'الجلد هادئ ولا يوجد نزيف أو بلل.'
                  },
                  {
                    id: 'hospital_dressing',
                    title: 'ما زالت ضمادة المستشفى موضوعة',
                    desc: 'تريدين الاستحمام دون أن تتبلل الضمادة أو الجرح.'
                  },
                  {
                    id: 'slight_redness',
                    title: 'احمرار طفيف أو حكة سطحية طبيعية',
                    desc: 'احتكاك بحزام البطن أو الملابس دون ألم حاد.'
                  },
                  {
                    id: 'active_leak',
                    title: 'تنبيه: يوجد تسريب سوائل أو إفرازات نشطة',
                    desc: 'بلل مستمر أو ألم نابض يتطلب تقييماً دقيقاً.'
                  }
                ].map((status) => (
                  <button
                    key={status.id}
                    type="button"
                    onClick={() => setDressingStatus(status.id as any)}
                    className={`w-full p-3 rounded-xl border text-right transition-all cursor-pointer flex items-start gap-2.5 ${
                      dressingStatus === status.id
                        ? status.id === 'active_leak'
                          ? 'border-[#ba1a1a] bg-[#ffdad6]/20'
                          : 'border-[#059669] bg-[#f3f7f5] ring-1 ring-[#059669]/20'
                        : 'border-[#e2ece6] hover:border-[#bfc9c3] bg-white'
                    }`}
                  >
                    <div className="mt-0.5">
                      {status.id === 'active_leak' ? (
                        <ShieldAlert className="w-4 h-4 text-[#ba1a1a]" />
                      ) : (
                        <CheckCircle2
                          className={`w-4 h-4 ${
                            dressingStatus === status.id ? 'text-[#059669]' : 'text-[#bfc9c3]'
                          }`}
                        />
                      )}
                    </div>
                    <div>
                      <span
                        className={`block text-xs font-bold ${
                          status.id === 'active_leak' ? 'text-[#ba1a1a]' : 'text-[#121c2a]'
                        }`}
                      >
                        {status.title}
                      </span>
                      <span className="block text-[11px] text-[#526058] mt-0.5">{status.desc}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

          </div>

          {/* Clinical Results & Action Column (6 cols) */}
          <div className="lg:col-span-6 space-y-5">
            
            {/* Main Verdict Card */}
            <div className="bg-white p-6 sm:p-7 rounded-2xl border border-[#e2ece6] shadow-sm">
              
              {/* Verdict Header Status */}
              <div className="flex items-center gap-2 mb-3">
                {assessment.showerSafety === 'safe_with_shield' && (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-[#82f5c1]/30 text-[#006c4a]">
                    <CheckCircle2 className="w-4 h-4 text-[#059669]" />
                    جاهزية الاستحمام: ضوء أخضر مع درع هيلينج تاتش
                  </span>
                )}
                {assessment.showerSafety === 'mature_healing' && (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-[#eff4ff] text-[#064e3b]">
                    <CheckCircle2 className="w-4 h-4 text-[#059669]" />
                    جاهزية الاستحمام: مرحلة الشاور الطبيعي والعناية بالندبة
                  </span>
                )}
                {assessment.showerSafety === 'consult_doctor_first' && (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-[#ffdad6] text-[#ba1a1a]">
                    <AlertTriangle className="w-4 h-4 text-[#ba1a1a]" />
                    تنبيه أمان: استشارة الطبيب مطلوبة قبل الشاور
                  </span>
                )}
              </div>

              {/* Headline */}
              <h3 className="text-lg sm:text-xl font-bold text-[#064e3b] mb-2 leading-snug">
                {assessment.headlineAr}
              </h3>

              {/* Guidance Text */}
              <p className="text-sm text-[#404944] leading-relaxed mb-5">
                {assessment.guidanceAr}
              </p>

              {/* Step-by-Step Shower Instructions for Today */}
              <div className="rounded-xl bg-[#f8f9ff] border border-[#dee9fc] p-4 mb-5">
                <h4 className="text-xs font-bold text-[#064e3b] mb-2 flex items-center gap-1.5">
                  <Info className="w-4 h-4 text-[#059669]" />
                  <span>خطوات الاستحمام الآمنة الموصى بها لمرحلتك الحالية:</span>
                </h4>
                <ul className="space-y-2 text-xs text-[#121c2a]">
                  {assessment.showerProtocolAr.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="w-5 h-5 rounded-full bg-[#064e3b] text-white text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                        {idx + 1}
                      </span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Warning note if any */}
              {assessment.warningNoteAr && (
                <div className="p-3 rounded-lg bg-[#ffdad6]/40 border border-[#ba1a1a]/20 text-xs text-[#93000a] mb-4">
                  {assessment.warningNoteAr}
                </div>
              )}

              {/* Recommended Product Box */}
              <div className="p-4 rounded-xl border border-[#059669]/30 bg-gradient-to-br from-[#f3f7f5] to-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <span className="text-[11px] font-semibold text-[#059669] block">
                    المنتج الموصى به طبياً لمرحلتك:
                  </span>
                  <h4 className="text-sm font-bold text-[#064e3b]">
                    {recommendedProduct.titleAr}
                  </h4>
                  <span className="text-xs text-[#526058]">
                    {recommendedProduct.taglineAr}
                  </span>
                </div>

                <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
                  <div className="text-left">
                    <span className="block text-base font-bold text-[#059669] tabular-nums">
                      {recommendedProduct.priceEGP} ج.م
                    </span>
                    <span className="text-[11px] text-[#707974] line-through tabular-nums">
                      {recommendedProduct.originalPriceEGP} ج.م
                    </span>
                  </div>

                  <button
                    onClick={() => onAddToCart(recommendedProduct.id)}
                    className="flex items-center gap-1.5 px-4 py-2.5 rounded-lg text-xs font-bold text-white bg-[#064e3b] hover:bg-[#003527] transition-all shadow-xs cursor-pointer whitespace-nowrap"
                  >
                    <ShoppingBag className="w-3.5 h-3.5" />
                    <span>إضافة للسلة</span>
                  </button>
                </div>
              </div>

            </div>

            {/* OB-GYN Clinical Tip Card */}
            <div className="p-4 rounded-xl bg-white border border-[#e2ece6] flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-[#d97706]/10 text-[#d97706] flex items-center justify-center shrink-0">
                <CheckCircle2 className="w-5 h-5 text-[#d97706]" />
              </div>
              <div className="text-xs text-[#404944] leading-relaxed">
                <strong className="font-bold text-[#064e3b] block mb-0.5">نصيحة الفريق الطبي لأمهات مصر:</strong>
                تذكري دائماً أن تجفيف منطقة القيصرية يكون بأسلوب "الطبطبة" الرقيقة بقطعة قطنية نظيفة، دون أي مسح عنيف، والابتعاد عن الكحول أو المطهرات اللاذعة بعد التئام السطح الخارجي.
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>
  );
};
