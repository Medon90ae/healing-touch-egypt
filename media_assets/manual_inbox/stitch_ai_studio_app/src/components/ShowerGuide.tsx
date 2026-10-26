import React from 'react';
import { Sparkles, ShowerHead, CheckCircle2, Heart } from 'lucide-react';

export const ShowerGuide: React.FC = () => {
  const steps = [
    {
      num: '01',
      title: 'تنظيف وتجفيف محيط الجرح',
      desc: 'تأكدي من جفاف الجلد المحيط بالشق الجراحي بنعومة تامة باستخدام قطنة نظيفة وبطريقة الطبطبة الرقيقة دون حك.',
      highlight: 'الجلد الجاف يضمن التصاقاً محكماً للدرع'
    },
    {
      num: '02',
      title: 'تثبيت درع الشاور العازل 25×10 سم',
      desc: 'انزعي الورقة الواقية الخلفية وضعي اللصقة بحيث يكون شق القيصرية في المنتصف، مع تمرير أصابعك بلطف على الحواف لتفريغ الهواء.',
      highlight: 'حواف هيدروجيل عازلة للماء 100%'
    },
    {
      num: '03',
      title: 'الاستحمام بحرية واسترخاء تام',
      desc: 'استمتعي بشاور دافئ يريح عضلات ظهرك وبطنك المشدودة بعد الولادة. يمكنك غسل شعرك واستخدام الصابون والشامبو بأمان كامل.',
      highlight: 'صفر قطرة ماء تصل لجرحك'
    },
    {
      num: '04',
      title: 'نزع اللصقة برفق وسلاسة',
      desc: 'بعد الانتهاء من الشاور وتجفيف جسمك، انزعي طرف اللصقة بلطف من زاوية علوية إلى أسفل؛ تنفصل كطبقة جل ناعمة دون أدنى ألم أو شد.',
      highlight: 'خالية تماماً من الشد المؤلم'
    }
  ];

  return (
    <section id="guide" className="py-16 bg-[#fbfdfb] border-b border-[#e2ece6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Title */}
        <div className="max-w-3xl mx-auto text-center mb-12 space-y-3">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#059669]">
            <ShowerHead className="w-4 h-4" />
            <span>بروتوكول الشاور الطبي خطوة بخطوة</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#064e3b]">
            كيف تستحمين بأمان بعد القيصرية دون خوف؟
          </h2>
          <p className="text-sm sm:text-base text-[#404944] leading-relaxed">
            دليل عملي مبسط مصمم لأمهات مصر لضمان أقصى درجات النظافة الشخصية والراحة النفسية والوقاية من التلوث الجراحي.
          </p>
        </div>

        {/* 4 Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 text-right">
          {steps.map((step) => (
            <div
              key={step.num}
              className="bg-white rounded-2xl border border-[#e2ece6] p-6 shadow-xs relative flex flex-col justify-between hover:-translate-y-1 transition-transform"
            >
              <div>
                {/* Step Number Badge */}
                <div className="flex items-center justify-between mb-4">
                  <span className="text-3xl font-extrabold text-[#059669]/20 font-mono">
                    {step.num}
                  </span>
                  <span className="w-8 h-8 rounded-full bg-[#f3f7f5] text-[#064e3b] flex items-center justify-center text-xs font-bold border border-[#e2ece6]">
                    خطوة
                  </span>
                </div>

                <h3 className="text-base font-bold text-[#064e3b] mb-2 leading-snug">
                  {step.title}
                </h3>

                <p className="text-xs sm:text-sm text-[#404944] leading-relaxed mb-4">
                  {step.desc}
                </p>
              </div>

              {/* Step Highlight Footer */}
              <div className="pt-3 border-t border-[#e2ece6] flex items-center gap-1.5 text-xs font-semibold text-[#059669]">
                <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                <span>{step.highlight}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Postpartum Empathy Card */}
        <div className="mt-10 p-6 rounded-2xl bg-gradient-to-r from-[#f3f7f5] via-[#f8f9ff] to-[#f3f7f5] border border-[#dee9fc] flex flex-col sm:flex-row items-center gap-5 text-right">
          <div className="w-12 h-12 rounded-2xl bg-[#064e3b] text-white flex items-center justify-center shrink-0 shadow-sm">
            <Heart className="w-6 h-6 text-[#82f5c1]" />
          </div>
          <div className="space-y-1">
            <h4 className="text-sm font-bold text-[#064e3b]">
              رسالة دعم من فريق هيلينج تاتش الطبي لكل أم جديدة:
            </h4>
            <p className="text-xs sm:text-sm text-[#404944] leading-relaxed">
              الاستحمام بالماء الدافئ بعد الولادة القيصرية ليس مجرد نظافة، بل هو علاج نفسي وجسدي يعيد لك الحيوية ويخفف آلام الرقبة والظهر الناتجة عن الرضاعة. لا تدعي القلق يحرمك من هذه اللحظة اليومية بفضل الدرع العازل المعقم.
            </p>
          </div>
        </div>

      </div>
    </section>
  );
};
