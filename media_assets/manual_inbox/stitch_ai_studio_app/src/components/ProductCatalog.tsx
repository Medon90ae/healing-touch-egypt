import React, { useState } from 'react';
import { PackageCheck, ShieldCheck, Check, Sparkles, ArrowLeft, Tag, Eye } from 'lucide-react';
import { Campaign } from '../types/campaign';
import { useInView } from '../hooks/useInView';

interface ProductCatalogProps {
  campaign: Campaign;
  onOpenLeadModal: (bundleId?: string) => void;
}

export const ProductCatalog: React.FC<ProductCatalogProps> = ({
  campaign,
  onOpenLeadModal
}) => {
  const [activeTab, setActiveTab] = useState<'bundles' | 'individual'>('bundles');
  const { ref, isInView } = useInView();

  const delayClasses = ['delay-75', 'delay-150', 'delay-225'];

  return (
    <section id="product-catalog" ref={ref} className="py-12 sm:py-16 bg-[#FBFDFB]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div
          className={`text-center max-w-3xl mx-auto mb-10 transition-all duration-500 ${
            isInView ? 'animate-fade-in-up opacity-100' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <PackageCheck className="w-4 h-4 text-[#059669]" />
            <span>باقات التعافي المعتمدة والأسعار</span>
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#003527] mb-3">
            اختاري باقة التعافي المناسبة لمرحلة جرحك
          </h2>
          <p className="text-sm sm:text-base text-[#404944]">
            جميع المنتجات الطبية معقمة ومحكمة الغلق مصنعياً، خالية من اللاتكس ومسجلة طبياً. الشحن سريع ومغلف لكافة محافظات مصر والدفع عند الاستلام بعد المعاينة.
          </p>

          {/* Toggle between Bundles and Individual Products */}
          <div className="mt-6 inline-flex p-1 rounded-xl bg-[#F3F7F5] border border-[#E2ECE6]">
            <button
              type="button"
              onClick={() => setActiveTab('bundles')}
              className={`px-5 py-2 rounded-lg text-xs sm:text-sm font-bold transition-all cursor-pointer ${
                activeTab === 'bundles'
                  ? 'bg-[#064E3B] text-white shadow-xs'
                  : 'text-[#404944] hover:text-[#003527]'
              }`}
            >
              باقات البروتوكول المتكاملة (الأكثر توفيراً)
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('individual')}
              className={`px-5 py-2 rounded-lg text-xs sm:text-sm font-bold transition-all cursor-pointer ${
                activeTab === 'individual'
                  ? 'bg-[#064E3B] text-white shadow-xs'
                  : 'text-[#404944] hover:text-[#003527]'
              }`}
            >
              المنتجات والملحقات الفردية
            </button>
          </div>
        </div>

        {/* Tab 1: Bundles */}
        {activeTab === 'bundles' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 items-stretch">
            {campaign.bundles.map((bundle, bIdx) => {
              const discountAmount = bundle.originalPriceEGP - bundle.priceEGP;
              const delayClass = delayClasses[bIdx % delayClasses.length];
              return (
                <div
                  key={bundle.id}
                  className={`relative bg-white rounded-2xl border transition-all duration-300 flex flex-col justify-between overflow-hidden group ${
                    isInView ? `animate-fade-in-up ${delayClass} opacity-100` : 'opacity-0 translate-y-6'
                  } ${
                    bundle.isPopular
                      ? 'border-2 border-[#059669] shadow-xl shadow-[#064E3B]/10 ring-1 ring-[#059669]'
                      : 'border-[#E2ECE6] shadow-sm hover:shadow-md'
                  }`}
                >
                  {/* Top Popular Ribbon */}
                  {bundle.isPopular && (
                    <div className="bg-[#059669] text-white text-[11px] font-bold text-center py-1.5 uppercase tracking-wider flex items-center justify-center gap-1">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>{bundle.tag}</span>
                    </div>
                  )}

                  {/* High Resolution Product Bundle Image with Sterile Badge */}
                  <div className="relative aspect-16/10 overflow-hidden bg-[#F3F7F5] border-b border-[#E2ECE6]">
                    <img
                      src={bundle.imageUrl}
                      alt={bundle.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                      onError={(e) => {
                        e.currentTarget.src = 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80';
                      }}
                    />
                    <div className="absolute top-2.5 right-2.5 px-2.5 py-1 rounded-full bg-white/95 backdrop-blur-xs text-[#003527] text-[11px] font-bold shadow-xs border border-[#D0DBED] flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-[#059669]" />
                      <span>غلاف مصنعي محكم</span>
                    </div>

                    <div className="absolute bottom-2.5 right-2.5">
                      <span className="text-[11px] font-bold text-[#D97706] bg-white/95 backdrop-blur-xs px-2.5 py-0.5 rounded-full border border-[#FFB77D] shadow-xs">
                        {bundle.badge}
                      </span>
                    </div>
                  </div>

                  <div className="p-6">
                    {/* Badge and Title */}
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="text-xs font-semibold text-[#059669]">
                        {bundle.savingsText}
                      </span>
                      {!bundle.isPopular && (
                        <span className="text-[11px] text-[#707974] bg-[#F3F7F5] px-2 py-0.5 rounded">
                          {bundle.tag}
                        </span>
                      )}
                    </div>

                    <h3 className="text-lg font-bold text-[#003527] mb-1">
                      {bundle.title}
                    </h3>
                    <p className="text-xs text-[#404944] mb-4 leading-relaxed">
                      {bundle.subtitle}
                    </p>

                    {/* Pricing */}
                    <div className="p-4 rounded-xl bg-[#F3F7F5] border border-[#E2ECE6] mb-5">
                      <div className="flex items-baseline gap-2 mb-1">
                        <span className="text-3xl font-extrabold text-[#003527]">
                          {bundle.priceEGP}
                        </span>
                        <span className="text-sm font-bold text-[#059669]">ج.م</span>
                        <span className="text-sm text-[#707974] line-through mr-2">
                          {bundle.originalPriceEGP} ج.م
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-xs text-[#059669] font-semibold">
                        <span>وفرتِ {discountAmount} ج.م</span>
                        <span className="text-[11px] text-[#D97706] bg-white px-2 py-0.5 rounded border border-[#FFB77D]">
                          كود HT10 يخصم 10% إضافية!
                        </span>
                      </div>
                    </div>

                    {/* Items included */}
                    <div className="space-y-2.5 mb-6">
                      <div className="text-xs font-bold text-[#003527]">محتويات الباقة:</div>
                      {bundle.items.map((item, i) => (
                        <div key={i} className="flex items-start gap-2 text-xs text-[#121C2A]">
                          <Check className="w-4 h-4 text-[#059669] shrink-0 mt-0.5" />
                          <span className="leading-snug">{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Card Bottom CTA */}
                  <div className="p-6 pt-0 mt-auto border-t border-[#E2ECE6]/50">
                    <button
                      type="button"
                      onClick={() => onOpenLeadModal(bundle.id)}
                      className={`w-full py-3.5 px-4 rounded-xl font-bold text-xs sm:text-sm text-center transition-all duration-200 cursor-pointer active:scale-98 flex items-center justify-center gap-2 ${
                        bundle.isPopular
                          ? 'bg-[#064E3B] hover:bg-[#003527] text-white shadow-md shadow-[#064E3B]/20'
                          : 'bg-[#F3F7F5] hover:bg-[#E2ECE6] text-[#003527] border border-[#E2ECE6]'
                      }`}
                    >
                      <span>تأكيد الطلب وحجز الاستشارة مجاناً</span>
                      <ArrowLeft className="w-4 h-4 rtl:rotate-0" />
                    </button>
                    <p className="text-[11px] text-center text-[#707974] mt-2">
                      شحن سريع ومغلف • فحص الشحنة قبل الدفع
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Tab 2: Individual Products */}
        {activeTab === 'individual' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            {campaign.products.map((prod, pIdx) => (
              <div
                key={prod.id}
                className={`bg-white rounded-2xl border border-[#E2ECE6] overflow-hidden shadow-xs flex flex-col justify-between group animate-fade-in-up ${
                  delayClasses[pIdx % delayClasses.length]
                }`}
              >
                {/* Product Photo */}
                <div className="relative aspect-16/10 bg-[#F3F7F5] border-b border-[#E2ECE6] overflow-hidden">
                  <img
                    src={prod.imageUrl}
                    alt={prod.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    loading="lazy"
                    onError={(e) => {
                      e.currentTarget.src = 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80';
                    }}
                  />
                  <div className="absolute top-2.5 right-2.5 px-2.5 py-0.5 rounded-full bg-white/90 backdrop-blur-xs text-[11px] font-bold text-[#059669] shadow-xs border border-[#E2ECE6]">
                    {prod.brand}
                  </div>
                  <div className="absolute bottom-2.5 right-2.5 px-2 py-0.5 rounded bg-[#003527]/85 text-white text-[10px] font-semibold">
                    {prod.badge}
                  </div>
                </div>

                <div className="p-6 flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="text-base font-bold text-[#003527] mb-1">
                      {prod.name}
                    </h3>
                    <div className="text-xs text-[#707974] mb-3">
                      {prod.specification}
                    </div>
                    <p className="text-xs text-[#404944] mb-4 leading-relaxed">
                      {prod.description}
                    </p>

                    <div className="p-3 bg-[#F3F7F5] rounded-xl border border-[#E2ECE6] mb-4 text-xs text-[#064E3B] font-medium">
                      <span className="font-bold">الفائدة السريرية: </span>
                      {prod.clinicalBenefit}
                    </div>

                    {/* Features */}
                    <div className="space-y-1.5 mb-5">
                      {prod.features.map((feat, fIdx) => (
                        <div key={fIdx} className="flex items-center gap-2 text-xs text-[#121C2A]">
                          <div className="w-1.5 h-1.5 rounded-full bg-[#059669]" />
                          <span>{feat}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-[#E2ECE6]">
                    <div className="flex items-baseline justify-between mb-3">
                      <div className="flex items-baseline gap-1.5">
                        <span className="text-2xl font-bold text-[#003527]">
                          {prod.priceEGP}
                        </span>
                        <span className="text-xs font-semibold text-[#059669]">ج.م</span>
                        <span className="text-xs text-[#707974] line-through mr-1">
                          {prod.originalPriceEGP} ج.م
                        </span>
                      </div>
                      <span className="text-[11px] text-[#059669] font-bold bg-[#E6EEFF] px-2 py-0.5 rounded">
                        وفرتِ {prod.originalPriceEGP - prod.priceEGP} ج.م
                      </span>
                    </div>

                    <button
                      type="button"
                      onClick={() => onOpenLeadModal(campaign.bundles[0]?.id)}
                      className="w-full bg-[#064E3B] hover:bg-[#003527] text-white py-3 px-4 rounded-xl font-bold text-xs sm:text-sm text-center transition-all cursor-pointer active:scale-98"
                    >
                      تأكيد الطلب وحجز الاستشارة مجاناً
                    </button>
                    <p className="text-[10px] text-center text-[#707974] mt-1.5">
                      شحن سريع ومغلف بإحكام لكافة المحافظات
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};
