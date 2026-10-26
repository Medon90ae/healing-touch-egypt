import React from 'react';
import { 
  ShieldCheck, 
  CheckCircle2, 
  Calculator, 
  Sparkles, 
  Award, 
  ArrowLeft,
  Droplets,
  Layers,
  HeartPulse
} from 'lucide-react';
import { Campaign } from '../types/campaign';

interface HeroSectionProps {
  campaign: Campaign;
  onOpenLeadModal: (bundleId?: string) => void;
  onScrollToCalculator: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  campaign,
  onOpenLeadModal,
  onScrollToCalculator
}) => {
  const featuredBundle = campaign.bundles[0];
  const featuredImage = featuredBundle?.imageUrl || campaign.heroImageUrl;

  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-[#F3F7F5] via-[#FBFDFB] to-[#FBFDFB] pt-8 pb-12 sm:pt-12 sm:pb-16 border-b border-[#E2ECE6]">
      {/* Decorative clinical light accents */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-[#82F5C1]/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 left-10 w-72 h-72 bg-[#95D3BA]/15 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          {/* Main Hero Narrative (7 cols on desktop) */}
          <div className="lg:col-span-7 space-y-6 animate-fade-in-up">
            {/* Clinical Endorsement Pill */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] border border-[#D0DBED] text-[#003527] text-xs sm:text-sm font-medium shadow-xs">
              <span className="w-2 h-2 rounded-full bg-[#059669] animate-pulse" />
              <span>{campaign.heroBadge}</span>
            </div>

            {/* Surgical Area Identification */}
            <div className="text-xs font-semibold tracking-wider text-[#059669] uppercase flex items-center gap-1.5">
              <span>نطاق الرعاية السريرية:</span>
              <span className="text-[#003527] font-bold">{campaign.surgicalArea}</span>
            </div>

            {/* Main Headline */}
            <h1 className="text-2xl sm:text-4xl lg:text-5xl font-bold text-[#003527] leading-tight sm:leading-snug">
              {campaign.title}
            </h1>

            {/* Subtitle */}
            <p className="text-base sm:text-lg text-[#404944] leading-relaxed max-w-2xl">
              {campaign.subtitle}
            </p>

            {/* Clinical Highlights Checklist */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              {campaign.heroHighlights.map((highlight, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2.5 p-3 rounded-xl bg-white border border-[#E2ECE6] shadow-xs"
                >
                  <CheckCircle2 className="w-5 h-5 text-[#059669] shrink-0 mt-0.5" />
                  <span className="text-xs sm:text-sm font-medium text-[#121C2A] leading-snug">
                    {highlight}
                  </span>
                </div>
              ))}
            </div>

            {/* CTAs strictly adhering to zero-bypass requirements */}
            <div className="pt-4 flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4">
              <button
                type="button"
                onClick={() => onOpenLeadModal()}
                className="inline-flex items-center justify-center gap-2 bg-[#064E3B] hover:bg-[#003527] text-white px-7 py-4 rounded-xl font-bold text-sm sm:text-base shadow-md shadow-[#064E3B]/20 transition-all duration-200 cursor-pointer active:scale-98 focus:outline-none focus:ring-2 focus:ring-[#059669] focus:ring-offset-2"
                aria-label="تأكيد الطلب وحجز الاستشارة مجاناً"
              >
                <span>تأكيد الطلب وحجز الاستشارة مجاناً</span>
                <ArrowLeft className="w-4 h-4 rtl:rotate-0" />
              </button>

              <button
                type="button"
                onClick={onScrollToCalculator}
                className="inline-flex items-center justify-center gap-2 bg-white hover:bg-[#F3F7F5] text-[#064E3B] border-2 border-[#064E3B] px-6 py-3.5 rounded-xl font-semibold text-sm sm:text-base transition-all duration-200 cursor-pointer active:scale-98"
              >
                <Calculator className="w-4 h-4 text-[#059669]" />
                <span>فحص جاهزية التعافي بالحاسبة السريرية</span>
              </button>
            </div>

            {/* Trust note */}
            <div className="flex flex-wrap items-center gap-3 text-xs text-[#707974] pt-1">
              <span className="inline-flex items-center gap-1 text-[#059669] font-medium">
                <ShieldCheck className="w-4 h-4" />
                منتجات طبية أصلية 100% معقمة ومغلفة
              </span>
              <span>•</span>
              <span>توصيل سريع ومغلف بإحكام حتى باب المنزل</span>
              <span>•</span>
              <span className="text-[#003527] font-semibold">الدفع عند الاستلام</span>
            </div>
          </div>

          {/* Clinical Showcase Card with Product Photography (5 cols on desktop) */}
          <div className="lg:col-span-5 animate-fade-in-up delay-150">
            <div className="relative bg-white rounded-2xl border border-[#E2ECE6] p-4 sm:p-5 shadow-xl shadow-[#064E3B]/5 overflow-hidden">
              {/* Product Packaging Image Showcase */}
              <div className="relative aspect-16/10 rounded-xl overflow-hidden bg-[#F3F7F5] border border-[#E2ECE6] mb-4 group">
                <img
                  src={featuredImage}
                  alt={featuredBundle?.title || campaign.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  loading="eager"
                  onError={(e) => {
                    e.currentTarget.src = 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80';
                  }}
                />
                {/* Floating clinical verification stamps */}
                <div className="absolute top-3 right-3 flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/95 backdrop-blur-xs text-[#003527] text-[11px] font-bold shadow-xs border border-[#D0DBED]">
                  <Droplets className="w-3.5 h-3.5 text-[#059669]" />
                  <span>عازل مائي بنسبة 100%</span>
                </div>

                <div className="absolute bottom-3 right-3 flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#003527]/90 text-white text-[11px] font-semibold shadow-xs">
                  <ShieldCheck className="w-3.5 h-3.5 text-[#82F5C1]" />
                  <span>معتمد سريرياً • Class 1 Medical Device</span>
                </div>
              </div>

              {/* Card Header & Protocol info */}
              <div className="flex items-center justify-between pb-3 border-b border-[#E2ECE6]">
                <div className="flex items-center gap-2">
                  <Award className="w-4 h-4 text-[#D97706]" />
                  <span className="text-xs font-bold text-[#003527] uppercase tracking-wide">
                    {featuredBundle?.title || 'باقة التعافي المتكاملة'}
                  </span>
                </div>
                <span className="text-[11px] font-semibold bg-[#E6EEFF] text-[#064E3B] px-2.5 py-0.5 rounded-full border border-[#D0DBED]">
                  معيار المستشفيات الخاصة
                </span>
              </div>

              {/* Protocol Overview Box */}
              <div className="mt-3 space-y-3">
                <div className="p-3 rounded-xl bg-[#F3F7F5] border border-[#E2ECE6]">
                  <div className="text-xs font-semibold text-[#003527] mb-1">
                    خطة الرعاية السريرية:
                  </div>
                  <p className="text-xs text-[#404944] leading-relaxed line-clamp-3">
                    {campaign.protocolDescription}
                  </p>
                </div>

                {/* Bundle items list */}
                {featuredBundle && (
                  <div className="space-y-1.5">
                    <div className="text-[11px] font-bold text-[#003527]">
                      مكونات البروتوكول داخل الباقة:
                    </div>
                    {featuredBundle.items.slice(0, 3).map((item, idx) => (
                      <div
                        key={idx}
                        className="flex items-center gap-2 text-xs text-[#121C2A] p-1.5 rounded-lg bg-[#FBFDFB] border border-[#E2ECE6]"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5 text-[#059669] shrink-0" />
                        <span className="truncate">{item}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Promo notice */}
                <div className="p-2.5 rounded-xl bg-gradient-to-r from-[#FFDCC3]/40 to-[#FFEFE6] border border-[#FFB77D] flex items-center justify-between">
                  <div className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-[#D97706]" />
                    <span className="text-xs font-bold text-[#4A2400]">
                      كود الخصم الحصري HT10
                    </span>
                  </div>
                  <span className="text-[11px] font-extrabold text-[#D97706] bg-white px-2 py-0.5 rounded-md border border-[#FFB77D]">
                    خصم 10% إضافي
                  </span>
                </div>

                {/* Price and CTA */}
                {featuredBundle && (
                  <div className="pt-2 flex items-center justify-between gap-3">
                    <div>
                      <div className="flex items-baseline gap-1.5">
                        <span className="text-2xl font-extrabold text-[#003527]">
                          {featuredBundle.priceEGP}
                        </span>
                        <span className="text-xs font-bold text-[#059669]">ج.م</span>
                        <span className="text-xs text-[#707974] line-through">
                          {featuredBundle.originalPriceEGP} ج.م
                        </span>
                      </div>
                      <div className="text-[10px] text-[#059669] font-medium">
                        شحن سريع ومغلف
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => onOpenLeadModal(featuredBundle.id)}
                      className="bg-[#064E3B] hover:bg-[#003527] text-white py-2.5 px-4 rounded-xl font-bold text-xs sm:text-sm text-center shadow-xs transition-all duration-200 cursor-pointer active:scale-98"
                    >
                      تأكيد الطلب وحجز الاستشارة مجاناً
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
