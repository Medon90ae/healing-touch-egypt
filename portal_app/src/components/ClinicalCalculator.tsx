import React, { useState } from 'react';
import { Calculator, CheckCircle2, AlertCircle, Sparkles, RefreshCw, ArrowLeft } from 'lucide-react';
import { Campaign } from '../types/campaign';

interface ClinicalCalculatorProps {
  campaign: Campaign;
  onSelectBundleAndOpenModal: (bundleId: string) => void;
}

export const ClinicalCalculator: React.FC<ClinicalCalculatorProps> = ({
  campaign,
  onSelectBundleAndOpenModal
}) => {
  const { calculator } = campaign;
  // Initialize with the first option of each question
  const [answers, setAnswers] = useState<Record<string, number>>(() => {
    const initial: Record<string, number> = {};
    calculator.questions.forEach((q) => {
      initial[q.id] = q.options[0]?.score ?? 0;
    });
    return initial;
  });

  const [selectedIndices, setSelectedIndices] = useState<Record<string, number>>(() => {
    const initial: Record<string, number> = {};
    calculator.questions.forEach((q) => {
      initial[q.id] = 0;
    });
    return initial;
  });

  const handleSelectOption = (questionId: string, optionIndex: number, score: number) => {
    setSelectedIndices((prev) => ({ ...prev, [questionId]: optionIndex }));
    setAnswers((prev) => ({ ...prev, [questionId]: score }));
  };

  const recommendation = calculator.getRecommendation(answers);

  return (
    <section id="clinical-calculator" className="py-12 sm:py-16 bg-[#F3F7F5] border-b border-[#E2ECE6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Heading */}
        <div className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <Calculator className="w-4 h-4 text-[#059669]" />
            <span>الحاسبة السريرية التفاعلية</span>
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#003527] mb-3">
            {calculator.title}
          </h2>
          <p className="text-sm sm:text-base text-[#404944]">
            {calculator.subtitle}
          </p>
        </div>

        {/* Calculator Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Questions Container (7 cols) */}
          <div className="lg:col-span-7 space-y-6">
            {calculator.questions.map((question, qIdx) => {
              const currentChoiceIndex = selectedIndices[question.id] ?? 0;
              return (
                <div
                  key={question.id}
                  className="bg-white rounded-2xl border border-[#E2ECE6] p-5 sm:p-6 shadow-xs"
                >
                  <div className="flex items-center gap-2.5 mb-2">
                    <span className="w-6 h-6 rounded-full bg-[#064E3B] text-white text-xs font-bold flex items-center justify-center shrink-0">
                      {qIdx + 1}
                    </span>
                    <h3 className="text-sm sm:text-base font-bold text-[#003527]">
                      {question.label}
                    </h3>
                  </div>
                  <p className="text-xs text-[#707974] mb-4 pr-8">
                    {question.description}
                  </p>

                  {/* Options */}
                  <div className="space-y-2.5 pr-2">
                    {question.options.map((option, optIdx) => {
                      const isSelected = currentChoiceIndex === optIdx;
                      return (
                        <button
                          key={optIdx}
                          type="button"
                          onClick={() => handleSelectOption(question.id, optIdx, option.score)}
                          className={`w-full text-right p-3.5 rounded-xl border text-xs sm:text-sm transition-all duration-150 cursor-pointer flex items-start gap-3 ${
                            isSelected
                              ? 'bg-[#F3F7F5] border-[#059669] ring-1 ring-[#059669] shadow-xs'
                              : 'bg-white border-[#E2ECE6] hover:bg-[#FBFDFB] hover:border-[#BFC9C3]'
                          }`}
                        >
                          <div
                            className={`w-4 h-4 rounded-full border-2 shrink-0 mt-0.5 flex items-center justify-center transition-colors ${
                              isSelected
                                ? 'border-[#059669] bg-[#059669]'
                                : 'border-[#BFC9C3] bg-white'
                            }`}
                          >
                            {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-white" />}
                          </div>
                          <div className="flex-1">
                            <div className="font-semibold text-[#121C2A]">
                              {option.label}
                            </div>
                            <div className="text-[11px] text-[#404944] mt-0.5 leading-normal">
                              {option.advice}
                            </div>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Real-Time Clinical Result & Recommendation (5 cols) */}
          <div className="lg:col-span-5 sticky top-28">
            <div className="bg-white rounded-2xl border-2 border-[#059669]/30 p-6 shadow-xl shadow-[#064E3B]/5 overflow-hidden relative">
              {/* Header Badge */}
              <div className="flex items-center justify-between pb-4 border-b border-[#E2ECE6]">
                <div className="flex items-center gap-2">
                  {recommendation.status === 'ready' ? (
                    <CheckCircle2 className="w-5 h-5 text-[#059669]" />
                  ) : (
                    <AlertCircle className="w-5 h-5 text-[#D97706]" />
                  )}
                  <span className="text-xs font-bold text-[#003527] uppercase">
                    نتيجة التقييم السريري
                  </span>
                </div>

                <button
                  type="button"
                  onClick={() => {
                    const resetIndices: Record<string, number> = {};
                    const resetAnswers: Record<string, number> = {};
                    calculator.questions.forEach((q) => {
                      resetIndices[q.id] = 0;
                      resetAnswers[q.id] = q.options[0]?.score ?? 0;
                    });
                    setSelectedIndices(resetIndices);
                    setAnswers(resetAnswers);
                  }}
                  className="text-xs text-[#707974] hover:text-[#064E3B] flex items-center gap-1 cursor-pointer"
                  title="إعادة ضبط الحاسبة"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>إعادة الفحص</span>
                </button>
              </div>

              {/* Result Pill */}
              <div className="mt-4">
                <span
                  className={`inline-block text-xs font-bold px-3 py-1 rounded-full ${
                    recommendation.status === 'ready'
                      ? 'bg-[#82F5C1]/30 text-[#003527] border border-[#059669]'
                      : 'bg-[#FFDCC3]/50 text-[#6A3700] border border-[#FFB77D]'
                  }`}
                >
                  {recommendation.badge}
                </span>

                <h3 className="text-base sm:text-lg font-bold text-[#003527] mt-2 mb-2 leading-snug">
                  {recommendation.headline}
                </h3>

                <p className="text-xs sm:text-sm text-[#404944] leading-relaxed mb-4 p-3 bg-[#F3F7F5] rounded-xl border border-[#E2ECE6]">
                  {recommendation.clinicalAdvice}
                </p>
              </div>

              {/* Protocol Action Steps */}
              <div className="space-y-2 mb-6">
                <div className="text-xs font-bold text-[#003527] flex items-center gap-1">
                  <Sparkles className="w-3.5 h-3.5 text-[#059669]" />
                  <span>خطوات البروتوكول الموصى بها لحالتك:</span>
                </div>
                {recommendation.protocolSteps.map((step, sIdx) => (
                  <div key={sIdx} className="flex items-start gap-2 text-xs text-[#121C2A]">
                    <span className="w-4 h-4 rounded-full bg-[#E6EEFF] text-[#064E3B] text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                      {sIdx + 1}
                    </span>
                    <span className="leading-snug">{step}</span>
                  </div>
                ))}
              </div>

              {/* Primary Action Button: strictly labeled and zero-bypass */}
              <div className="space-y-2 pt-2 border-t border-[#E2ECE6]">
                <button
                  type="button"
                  onClick={() => onSelectBundleAndOpenModal(recommendation.recommendedBundleId)}
                  className="w-full bg-[#064E3B] hover:bg-[#003527] text-white py-3.5 px-4 rounded-xl font-bold text-sm text-center shadow-md shadow-[#064E3B]/15 transition-all duration-200 cursor-pointer active:scale-98 flex items-center justify-center gap-2"
                >
                  <span>تأكيد الطلب وحجز الاستشارة مجاناً</span>
                  <ArrowLeft className="w-4 h-4" />
                </button>
                <p className="text-[11px] text-center text-[#707974]">
                  استشارة هاتفية وطبية مجانية من أخصائية التعافي لتوضيح طريقة الاستخدام
                </p>
                <div className="flex items-center justify-center gap-2 text-[11px] text-[#059669] font-medium">
                  <span>شحن سريع ومغلف لكافة المحافظات</span>
                  <span>•</span>
                  <span>معاينة وفحص قبل الاستلام</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
