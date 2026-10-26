import React from 'react';
import { Calendar, Lightbulb } from 'lucide-react';
import { Campaign } from '../types/campaign';
import { useInView } from '../hooks/useInView';

interface ProtocolTimelineProps {
  campaign: Campaign;
}

export const ProtocolTimeline: React.FC<ProtocolTimelineProps> = ({ campaign }) => {
  const { ref, isInView } = useInView();
  const delayClasses = ['delay-75', 'delay-150', 'delay-225'];

  return (
    <section ref={ref} className="py-12 sm:py-16 bg-[#F3F7F5] border-b border-[#E2ECE6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div
          className={`text-center max-w-3xl mx-auto mb-10 transition-all duration-500 ${
            isInView ? 'animate-fade-in-up opacity-100' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <Calendar className="w-4 h-4 text-[#059669]" />
            <span>الجدول الزمني للتعافي السريري</span>
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#003527] mb-3">
            مراحل الشفاء والتئام الجرح أسبوعاً بأسبوع
          </h2>
          <p className="text-sm sm:text-base text-[#404944]">
            خريطة طريق سريرية مدروسة ترشدك خطوة بخطوة للوصول إلى جرح غير مرئي وبشرة ناعمة وصحية.
          </p>
        </div>

        {/* Timeline Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          {campaign.timeline.map((step, idx) => {
            const delayClass = delayClasses[idx % delayClasses.length];
            return (
              <div
                key={idx}
                className={`bg-white rounded-2xl border border-[#E2ECE6] p-6 shadow-xs relative flex flex-col justify-between transition-all duration-300 ${
                  isInView ? `animate-fade-in-up ${delayClass} opacity-100` : 'opacity-0 translate-y-6'
                }`}
              >
                {/* Step indicator */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xs font-bold text-white bg-[#064E3B] px-3 py-1 rounded-full">
                      {step.phase}
                    </span>
                    <span className="text-xs font-semibold text-[#059669] bg-[#E6EEFF] px-2.5 py-1 rounded-full">
                      {step.weekRange}
                    </span>
                  </div>

                  <h3 className="text-base sm:text-lg font-bold text-[#003527] mb-2">
                    {step.title}
                  </h3>

                  <p className="text-xs sm:text-sm text-[#121C2A] leading-relaxed mb-4">
                    {step.action}
                  </p>
                </div>

                {/* Tip Box */}
                <div className="p-3.5 rounded-xl bg-[#FBFDFB] border border-[#E2ECE6] text-xs text-[#404944] flex items-start gap-2.5">
                  <Lightbulb className="w-4 h-4 text-[#D97706] shrink-0 mt-0.5" />
                  <div className="leading-snug">
                    <strong className="text-[#003527] block mb-0.5">نصيحة الطبيب:</strong>
                    {step.tip}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
