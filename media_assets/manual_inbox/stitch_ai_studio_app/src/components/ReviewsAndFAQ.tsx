import React, { useState } from 'react';
import { CLINICAL_FAQS } from '../data/protocolData';
import { Star, ChevronDown, ChevronUp, MessageCircleHeart, HelpCircle, CheckCircle2 } from 'lucide-react';

export const ReviewsAndFAQ: React.FC = () => {
  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(0);

  const reviews = [
    {
      name: 'د. ياسمين الشناوي',
      city: 'القاهرة (التجمع الخامس)',
      role: 'طبيبة صيدلانية وأم للمرة الثانية',
      date: 'منذ أسبوعين',
      rating: 5,
      comment:
        'في قيصريتي الأولى كنت مرعوبة من الشاور والشاش التقليدي كان بيتبلل ومسبب لي التهاب شديد. في ولادتي الثانية استخدمت لصقات هيلينج تاتش من اليوم الرابع؛ عزل مائي 100% ونزع لطيف جداً بدون أي ألم. وشرائح السيليكون خلت الخط ناعم ومسطح تماماً.',
      verified: 'شراء موثق - باقة البروتوكول الثلاثي'
    },
    {
      name: 'مروة عبد الرحمن',
      city: 'الإسكندرية (سموحة)',
      role: 'مهندسة برمجيات',
      date: 'منذ 3 أسابيع',
      rating: 5,
      comment:
        'الشاور الدافئ بعد القيصرية كان طوق النجاة لظهري ورقبتي من تعب الرضاعة. اللصقة مقاسها 25 سم كبير ومغطي الجرح بالكامل وما سربتش نقطة مية واحدة مع الشامبو. والتوصيل وصلني في إسكندرية تاني يوم والدفع عند الاستلام بعد ما عاينت العبوة.',
      verified: 'شراء موثق - درع الشاور العازل'
    },
    {
      name: 'نوران حسام',
      city: 'الدقهلية (المنصورة)',
      role: 'معلمة لغة إنجليزية',
      date: 'منذ شهر',
      rating: 5,
      comment:
        'شرائح السيليكون الطبية اختراع حقيقي! كانت ملابسي والبنطلون بيحتكوا بالجرح ويسببوا حرقان. الشريحة ناعمة جداً وبتتغسل وتستخدم تاني، وخلال شهر ونصف خط الجرح فتح لونه جداً ومفيش أي أثر للبروز.',
      verified: 'شراء موثق - باقة البروتوكول الثلاثي'
    }
  ];

  return (
    <section id="faq" className="py-16 bg-[#f3f7f5] border-b border-[#e2ece6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Testimonials Block */}
        <div className="mb-16">
          <div className="max-w-3xl mx-auto text-center mb-10 space-y-3">
            <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#059669]">
              <MessageCircleHeart className="w-4 h-4" />
              <span>تجارب حقيقية موثقة من أمهات مصر</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-[#064e3b]">
              تجارب أمهات تعافين بثقة وأمان كامل
            </h2>
            <p className="text-sm sm:text-base text-[#404944]">
              أكثر من 12,000 أم في كافة المحافظات استعدن راحة الشاور والتعافي الأملس لجرح القيصرية.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-right">
            {reviews.map((rev, idx) => (
              <div
                key={idx}
                className="bg-white rounded-2xl border border-[#e2ece6] p-6 shadow-xs flex flex-col justify-between"
              >
                <div>
                  {/* Rating Stars */}
                  <div className="flex items-center gap-1 mb-3 text-[#d97706]">
                    {[...Array(rev.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-[#d97706]" />
                    ))}
                  </div>

                  <p className="text-xs sm:text-sm text-[#404944] leading-relaxed mb-4">
                    "{rev.comment}"
                  </p>
                </div>

                <div className="pt-4 border-t border-[#e2ece6]">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-xs sm:text-sm font-bold text-[#064e3b]">
                        {rev.name}
                      </h4>
                      <p className="text-[11px] text-[#526058]">{rev.city} · {rev.role}</p>
                    </div>
                    <span className="text-[11px] text-[#707974]">{rev.date}</span>
                  </div>

                  <div className="mt-2 flex items-center gap-1.5 text-[11px] font-medium text-[#059669]">
                    <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                    <span>{rev.verified}</span>
                  </div>
                </div>

              </div>
            ))}
          </div>
        </div>

        {/* Clinical FAQ Block */}
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-8 space-y-2">
            <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#064e3b]">
              <HelpCircle className="w-4 h-4 text-[#059669]" />
              <span>إجابات استشارية طبية</span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-[#064e3b]">
              الأسئلة الشائعة حول بروتوكول التعافي القيصري والشاور
            </h3>
          </div>

          <div className="space-y-3 text-right">
            {CLINICAL_FAQS.map((faq, index) => {
              const isOpen = openFaqIndex === index;
              return (
                <div
                  key={index}
                  className="bg-white rounded-xl border border-[#e2ece6] overflow-hidden transition-all shadow-xs"
                >
                  <button
                    onClick={() => setOpenFaqIndex(isOpen ? null : index)}
                    className="w-full py-4 px-5 flex items-center justify-between gap-4 text-right cursor-pointer hover:bg-[#fbfdfb]"
                  >
                    <span className="text-sm font-bold text-[#064e3b] leading-snug">
                      {faq.q}
                    </span>
                    <span className="shrink-0 text-[#059669]">
                      {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                    </span>
                  </button>

                  {isOpen && (
                    <div className="px-5 pb-5 text-xs sm:text-sm text-[#404944] leading-relaxed border-t border-[#f3f7f5] pt-3">
                      {faq.a}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

        </div>

      </div>
    </section>
  );
};
