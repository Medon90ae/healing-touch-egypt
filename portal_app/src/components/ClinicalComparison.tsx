import React from 'react';
import { Check, X, ShieldAlert, Award } from 'lucide-react';

export const ClinicalComparison: React.FC = () => {
  const comparisonRows = [
    {
      criterion: 'مقاومة الماء وتيار الدش والصابون',
      traditional: 'تسريب سريع يبلل الشاش ويؤدي لتكاثر البكتيريا والتهاب القيصرية',
      healingTouch: 'عزل مائي سريري 100% يمنع دخول أي قطرة ماء أو رغوة للجرح',
      winner: true
    },
    {
      criterion: 'الألم والشد عند نزع الضمادة',
      traditional: 'شريط لاصق يلتصق بشدة ويشد شعر البطن والجلد الحساس بألم شديد',
      healingTouch: 'هيدروجيل سيليكوني لطيف ينفصل بنعومة تامة دون أي ألم أو نزع للشعر',
      winner: true
    },
    {
      criterion: 'الوقاية من الجدرة وتضخم الندبة (Keloid)',
      traditional: 'لا توفر أي دعم بيولوجي؛ تترك خطاً أحمر سميكاً وبارزاً',
      healingTouch: 'شرائح سيليكون طبي تضغط برفق وتسطح الكولاجين بنسبة 92%',
      winner: true
    },
    {
      criterion: 'نفاذية الأكسجين وتهوية أنسجة الجرح',
      traditional: 'أغلفة بلاستيكية تحبس العرق والرطوبة وتزيد احتمالية الفطريات',
      healingTouch: 'غشاء شبه نفاذ يتنفس ويسمح بتبادل الأكسجين مع منع الميكروبات',
      winner: true
    },
    {
      criterion: 'إعادة الاستخدام والتكلفة الاقتصادية',
      traditional: 'استخدام لمرة واحدة وتغيير متكرر مكلف ومرهق',
      healingTouch: 'شرائح سيليكون قابلة للغسيل والاستخدام لمدة شهر كامل للشريحة',
      winner: true
    }
  ];

  return (
    <section id="comparison" className="py-16 bg-[#f3f7f5] border-b border-[#e2ece6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Title */}
        <div className="max-w-3xl mx-auto text-center mb-10 space-y-3">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#059669]">
            <Award className="w-4 h-4" />
            <span>مقارنة علمية مثبتة سريرياً</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#064e3b]">
            لماذا ترفض المستشفيات الحديثة اللصقات التقليدية؟
          </h2>
          <p className="text-sm sm:text-base text-[#404944] leading-relaxed">
            مقارنة سريرية مباشرة بين الشاش واللصقات العادية وبروتوكول هيلينج تاتش المتطور للتعافي القيصري.
          </p>
        </div>

        {/* Comparison Table */}
        <div className="bg-white rounded-2xl border border-[#e2ece6] shadow-sm overflow-hidden text-right">
          <div className="overflow-x-auto">
            <table className="w-full text-right border-collapse">
              <thead>
                <tr className="border-b border-[#e2ece6] bg-[#f8f9ff]">
                  <th className="py-4 px-5 text-sm font-bold text-[#064e3b] w-1/3">
                    المعيار الطبي والسريري
                  </th>
                  <th className="py-4 px-5 text-sm font-bold text-[#ba1a1a] w-1/3 bg-[#ffdad6]/20">
                    اللصقات والشاش التقليدي
                  </th>
                  <th className="py-4 px-5 text-sm font-bold text-[#059669] w-1/3 bg-[#82f5c1]/10">
                    بروتوكول هيلينج تاتش مصر
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#e2ece6] text-xs sm:text-sm">
                {comparisonRows.map((row, idx) => (
                  <tr key={idx} className="hover:bg-[#fbfdfb] transition-colors">
                    <td className="py-4 px-5 font-bold text-[#064e3b]">
                      {row.criterion}
                    </td>
                    <td className="py-4 px-5 text-[#404944] bg-[#ffdad6]/5">
                      <div className="flex items-start gap-2">
                        <X className="w-4 h-4 text-[#ba1a1a] shrink-0 mt-0.5" />
                        <span>{row.traditional}</span>
                      </div>
                    </td>
                    <td className="py-4 px-5 text-[#121c2a] font-medium bg-[#82f5c1]/5">
                      <div className="flex items-start gap-2">
                        <Check className="w-4 h-4 text-[#059669] shrink-0 mt-0.5" />
                        <span className="font-semibold text-[#064e3b]">{row.healingTouch}</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Clinical Conclusion Strip */}
          <div className="p-4 bg-[#f8f9ff] border-t border-[#e2ece6] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[#404944]">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-[#059669]" />
              <span>
                النتيجة الطبية: حماية بنسبة 100% ضد تسرب الماء أثناء الشاور، وانخفاض احتمالية الندبات السميكة بنسبة 92%.
              </span>
            </div>
            <span className="text-[11px] font-semibold text-[#064e3b] bg-white px-3 py-1 rounded border border-[#e2ece6]">
              معيار الجراحة النظيفة التجميلية
            </span>
          </div>

        </div>

      </div>
    </section>
  );
};
