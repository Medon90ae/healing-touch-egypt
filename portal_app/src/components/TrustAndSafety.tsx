import React from 'react';
import { BadgeCheck, Layers, UserCheck, PackageCheck, Sparkles } from 'lucide-react';
import { useInView } from '../hooks/useInView';

interface TrustPillar {
  id: string;
  icon: React.ElementType;
  title: string;
  badge: string;
  description: string;
  credential: string;
}

const TRUST_PILLARS: TrustPillar[] = [
  {
    id: 'iso-certified',
    icon: BadgeCheck,
    title: 'اعتماد الآيزو العالمي ISO 13485',
    badge: 'ISO 13485 Certified',
    description: 'مطابق للمواصفات القياسية الدولية لنظم إدارة جودة الأجهزة والضمادات الطبية المعقمة.',
    credential: 'شهادة جودة طبية معتمدة'
  },
  {
    id: 'medical-grade',
    icon: Layers,
    title: 'خامات جراحية طبية 100%',
    badge: 'Medical Grade Silicone',
    description: 'سيليكون ومواد بوليميرية خاملة حيوياً (Bio-inert) لا تتفاعل مع الأنسجة وتمنع تضخم الكولاجين.',
    credential: 'نقاء سريري 100%'
  },
  {
    id: 'dermatologist-tested',
    icon: UserCheck,
    title: 'فحص واعتماد أطباء الجلدية',
    badge: 'Dermatologist Tested',
    description: 'تركيبات هيبوالرجينيك خالية تماماً من اللاتكس والمواد الكيميائية القاسية، آمنة للأمهات.',
    credential: 'هيبوالرجينيك للجلد الحساس'
  },
  {
    id: 'secure-shipping',
    icon: PackageCheck,
    title: 'شحن سريع ومغلف بإحكام',
    badge: 'Fast & Discreet Packaging',
    description: 'المنتجات معقمة ومحكمة الغلق مصنعياً، وتصلك داخل طرد مغلف وسري تماماً مع حق المعاينة والفحص قبل الاستلام.',
    credential: 'طرد مغلف وسري 100%'
  }
];

export const TrustAndSafety: React.FC = () => {
  const { ref, isInView } = useInView();
  const delayClasses = ['delay-75', 'delay-150', 'delay-225', 'delay-300'];

  return (
    <section
      ref={ref}
      aria-label="معايير الأمان والموثوقية السريرية"
      className="py-10 sm:py-14 bg-[#FBFDFB] border-b border-[#E2ECE6]"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div
          className={`text-center max-w-2xl mx-auto mb-8 sm:mb-10 transition-all duration-500 ${
            isInView ? 'animate-fade-in-up opacity-100' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E6EEFF] text-[#003527] text-xs font-semibold mb-2.5 border border-[#D0DBED]">
            <Sparkles className="w-3.5 h-3.5 text-[#059669]" />
            <span>معايير الأمان السريري والموثوقية الطبية</span>
          </div>
          <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold text-[#003527]">
            بروتوكولات رعاية مرخصة ومطابقة للمواصفات الدولية
          </h2>
          <p className="text-xs sm:text-sm text-[#404944] mt-2">
            نلتزم بأعلى معايير السلامة والتعقيم الطبي لضمان أفضل نتائج التئام لجرحك دون مضاعفات.
          </p>
        </div>

        {/* 4 Trust & Safety Pillars Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {TRUST_PILLARS.map((pillar, idx) => {
            const Icon = pillar.icon;
            const delayClass = delayClasses[idx % delayClasses.length];

            return (
              <div
                key={pillar.id}
                className={`bg-white rounded-2xl border border-[#E2ECE6] p-5 shadow-xs hover:border-[#059669]/40 hover:shadow-md transition-all duration-300 flex flex-col justify-between group ${
                  isInView ? `animate-fade-in-up ${delayClass} opacity-100` : 'opacity-0 translate-y-6'
                }`}
              >
                <div>
                  {/* Clean Outlined Icon Container */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 rounded-xl border-2 border-[#059669]/30 bg-[#F3F7F5] group-hover:bg-[#E6EEFF] group-hover:border-[#059669] flex items-center justify-center text-[#064E3B] transition-colors">
                      <Icon className="w-6 h-6 stroke-[1.75]" />
                    </div>
                    <span className="text-[10px] font-mono font-semibold text-[#059669] bg-[#E6EEFF] px-2 py-0.5 rounded-full border border-[#D0DBED]">
                      {pillar.badge}
                    </span>
                  </div>

                  {/* Title */}
                  <h3 className="text-sm sm:text-base font-bold text-[#003527] mb-2 leading-snug">
                    {pillar.title}
                  </h3>

                  {/* Description */}
                  <p className="text-xs text-[#404944] leading-relaxed mb-4">
                    {pillar.description}
                  </p>
                </div>

                {/* Footer Credential Tag */}
                <div className="pt-3 border-t border-[#E2ECE6] flex items-center justify-between text-[11px] text-[#059669] font-medium">
                  <span>{pillar.credential}</span>
                  <div className="w-1.5 h-1.5 rounded-full bg-[#059669]" />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
