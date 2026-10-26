import React, { useState } from 'react';
import { HelpCircle, ChevronDown } from 'lucide-react';
import { ClinicalFAQ } from '../types/campaign';

interface ClinicalFaqProps {
  faqs: ClinicalFAQ[];
  highlightFaqIndex?: number | null;
}

export const ClinicalFaq: React.FC<ClinicalFaqProps> = ({ faqs, highlightFaqIndex }) => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  // Auto-open FAQ when navigated from search
  React.useEffect(() => {
    if (typeof highlightFaqIndex === 'number' && highlightFaqIndex >= 0) {
      setOpenIndex(highlightFaqIndex);
    }
  }, [highlightFaqIndex]);

  const toggle = (idx: number) => {
    setOpenIndex(openIndex === idx ? null : idx);
  };

  return (
    <section id="clinical-faq" className="scroll-mt-24 py-12 sm:py-16 bg-[#F3F7F5] border-b border-[#E2ECE6]">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Heading */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <HelpCircle className="w-4 h-4 text-[#059669]" />
            <span>الأسئلة الشائعة والاستشارات السريرية</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#003527] mb-2">
            إجابات دقيقة على تساؤلات مرحلة التعافي
          </h2>
          <p className="text-sm text-[#404944]">
            كل ما تحتاجين معرفته حول أمان المنتجات، الاستحمام، وطريقة تطبيق السيليكون.
          </p>
        </div>

        {/* FAQs Accordion */}
        <div className="space-y-3">
          {faqs.map((faq, idx) => {
            const isOpen = openIndex === idx;
            const isHighlighted = highlightFaqIndex === idx;
            return (
              <div
                key={idx}
                id={`faq-${idx}`}
                className={`scroll-mt-36 rounded-xl border overflow-hidden transition-all duration-300 ${
                  isHighlighted
                    ? 'border-[#059669] ring-4 ring-[#82F5C1]/40 shadow-md bg-[#F0FDF4]/40'
                    : 'bg-white border-[#E2ECE6]'
                }`}
              >
                <button
                  type="button"
                  onClick={() => toggle(idx)}
                  className="w-full text-right p-4 sm:p-5 flex items-center justify-between gap-4 cursor-pointer hover:bg-[#FBFDFB]"
                  aria-expanded={isOpen}
                >
                  <span className="font-bold text-sm sm:text-base text-[#003527] leading-snug">
                    {faq.question}
                  </span>
                  <div
                    className={`w-6 h-6 rounded-full bg-[#F3F7F5] flex items-center justify-center shrink-0 transition-transform duration-200 ${
                      isOpen ? 'rotate-180 bg-[#E6EEFF] text-[#064E3B]' : 'text-[#707974]'
                    }`}
                  >
                    <ChevronDown className="w-4 h-4" />
                  </div>
                </button>

                {isOpen && (
                  <div className="px-5 pb-5 pt-1 text-xs sm:text-sm text-[#404944] leading-relaxed border-t border-[#E2ECE6]/50 bg-[#FBFDFB]">
                    {faq.answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
