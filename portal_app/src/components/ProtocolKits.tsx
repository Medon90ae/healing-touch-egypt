import React, { useState } from 'react';
import { PROTOCOL_PRODUCTS } from '../data/protocolData';
import { ProductItem } from '../types/protocol';
import {
  ShieldCheck,
  Droplet,
  Sparkles,
  ShoppingBag,
  CheckCircle,
  Truck,
  HeartHandshake,
  Layers
} from 'lucide-react';

interface ProtocolKitsProps {
  onAddToCart: (productId: string) => void;
  onInstantBuy: (productId: string) => void;
}

export const ProtocolKits: React.FC<ProtocolKitsProps> = ({
  onAddToCart,
  onInstantBuy
}) => {
  const [activeTab, setActiveTab] = useState<'all' | 'bundle' | 'phases'>('all');

  const bundleProduct = PROTOCOL_PRODUCTS.find((p) => p.id === 'complete-protocol-bundle')!;
  const individualPhases = PROTOCOL_PRODUCTS.filter((p) => p.id !== 'complete-protocol-bundle');

  return (
    <section id="products" className="py-16 bg-[#fbfdfb] border-b border-[#e2ece6]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Title */}
        <div className="max-w-3xl mx-auto text-center mb-10 space-y-3">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#064e3b]">
            <Layers className="w-4 h-4 text-[#059669]" />
            <span>المواصفات الطبية المعتمدة للتعافي القيصري</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-[#064e3b]">
            باقات بروتوكول التعافي القيصري وعلاج الندبات
          </h2>
          <p className="text-sm sm:text-base text-[#404944] leading-relaxed">
            اختاري الباقة الشاملة الموصى بها لرعاية عام كامل من الالتئام والتسطيح، أو اختاري مستلزمات مرحلتك الحالية بدقة.
          </p>

          {/* Interactive Filter Control */}
          <div className="inline-flex items-center gap-1 p-1 bg-[#f3f7f5] rounded-xl border border-[#e2ece6] mt-3">
            <button
              onClick={() => setActiveTab('all')}
              className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
                activeTab === 'all'
                  ? 'bg-white text-[#064e3b] shadow-xs'
                  : 'text-[#404944] hover:text-[#064e3b]'
              }`}
            >
              جميع المنتجات والباقات
            </button>
            <button
              onClick={() => setActiveTab('bundle')}
              className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
                activeTab === 'bundle'
                  ? 'bg-white text-[#064e3b] shadow-xs'
                  : 'text-[#404944] hover:text-[#064e3b]'
              }`}
            >
              الباقة الثلاثية الشاملة (الأكثر طلباً)
            </button>
            <button
              onClick={() => setActiveTab('phases')}
              className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
                activeTab === 'phases'
                  ? 'bg-white text-[#064e3b] shadow-xs'
                  : 'text-[#404944] hover:text-[#064e3b]'
              }`}
            >
              المراحل الفردية (شاور / سيليكون / جل)
            </button>
          </div>
        </div>

        {/* Featured 3-Phase Bundle Hero Card */}
        {(activeTab === 'all' || activeTab === 'bundle') && (
          <div className="mb-12 rounded-3xl bg-gradient-to-br from-[#064e3b] to-[#003527] text-white p-7 sm:p-10 shadow-lg relative overflow-hidden">
            
            {/* Subtle background decoration */}
            <div className="absolute top-0 left-0 w-96 h-96 bg-[#059669]/10 rounded-full blur-3xl pointer-events-none" />

            <div className="relative grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              
              {/* Bundle Info (7 cols) */}
              <div className="lg:col-span-7 space-y-4 text-right">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-[#82f5c1]/20 text-[#82f5c1]">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>توفير 400 ج.م + شحن مجاني لكافة محافظات مصر</span>
                </div>

                <h3 className="text-2xl sm:text-3xl font-bold leading-tight">
                  {bundleProduct.titleAr}
                </h3>

                <p className="text-sm sm:text-base text-[#d9e3f6] leading-relaxed">
                  {bundleProduct.descriptionAr}
                </p>

                {/* Key components breakdown */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
                  <div className="p-3 rounded-xl bg-white/10 backdrop-blur-xs border border-white/10">
                    <span className="block text-xs font-bold text-[#82f5c1] mb-1">المرحلة 1: درع الشاور</span>
                    <span className="block text-[11px] text-[#f3f7f5]">10 لصقات عازلة للماء 100% للشاور المريح</span>
                  </div>
                  <div className="p-3 rounded-xl bg-white/10 backdrop-blur-xs border border-white/10">
                    <span className="block text-xs font-bold text-[#82f5c1] mb-1">المرحلة 2: السيليكون الطبي</span>
                    <span className="block text-[11px] text-[#f3f7f5]">3 شرائح قابلة للغسيل لتسطيح الندبة 3 أشهر</span>
                  </div>
                  <div className="p-3 rounded-xl bg-white/10 backdrop-blur-xs border border-white/10">
                    <span className="block text-xs font-bold text-[#82f5c1] mb-1">المرحلة 3: جل التجديد</span>
                    <span className="block text-[11px] text-[#f3f7f5]">جل سيراميد 50 مل لتفتيح التصبغات وتوحيد اللون</span>
                  </div>
                </div>

                {/* Benefits List */}
                <div className="space-y-2 pt-2">
                  {bundleProduct.benefits.slice(0, 3).map((benefit, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-xs sm:text-sm text-[#eff4ff]">
                      <CheckCircle className="w-4 h-4 text-[#82f5c1] shrink-0" />
                      <span>{benefit}</span>
                    </div>
                  ))}
                </div>

              </div>

              {/* Price & Purchase Actions Box (5 cols) */}
              <div className="lg:col-span-5 bg-white text-[#121c2a] rounded-2xl p-6 sm:p-7 shadow-md border border-[#e2ece6] text-right space-y-5">
                
                <div className="flex items-baseline justify-between border-b border-[#e2ece6] pb-4">
                  <div>
                    <span className="block text-xs font-bold text-[#526058]">سعر الباقة الشاملة:</span>
                    <div className="flex items-baseline gap-2 mt-1">
                      <span className="text-3xl font-extrabold text-[#064e3b] tabular-nums">
                        {bundleProduct.priceEGP} ج.م
                      </span>
                      <span className="text-sm text-[#707974] line-through tabular-nums">
                        {bundleProduct.originalPriceEGP} ج.م
                      </span>
                    </div>
                  </div>
                  <span className="text-xs font-bold px-2.5 py-1 rounded-md bg-[#ffdad6] text-[#ba1a1a]">
                    خصم 31%
                  </span>
                </div>

                <div className="space-y-2 text-xs text-[#404944]">
                  <div className="flex items-center gap-2">
                    <Truck className="w-4 h-4 text-[#059669]" />
                    <span className="font-semibold text-[#064e3b]">شحن مجاني متاح اليوم</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-[#059669]" />
                    <span>الدفع عند الاستلام مع المعاينة أو عبر إنستاباي</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <HeartHandshake className="w-4 h-4 text-[#059669]" />
                    <span>متابعة سريرية واستشارات استخدام عبر واتساب</span>
                  </div>
                </div>

                <div className="space-y-2.5 pt-2">
                  <button
                    onClick={() => onInstantBuy(bundleProduct.id)}
                    className="w-full py-3.5 px-6 rounded-xl text-sm sm:text-base font-bold text-white bg-[#064e3b] hover:bg-[#003527] transition-all shadow-md active:scale-[0.99] cursor-pointer flex items-center justify-center gap-2"
                  >
                    <ShoppingBag className="w-4 h-4" />
                    <span>طلب فوري للباقة المتكاملة</span>
                  </button>

                  <button
                    onClick={() => onAddToCart(bundleProduct.id)}
                    className="w-full py-2.5 px-6 rounded-xl text-xs sm:text-sm font-semibold text-[#064e3b] bg-[#f3f7f5] hover:bg-[#e2ece6] transition-all border border-[#e2ece6] cursor-pointer"
                  >
                    إضافة إلى سلة المشتريات
                  </button>
                </div>

              </div>

            </div>

          </div>
        )}

        {/* Individual Phases Grid */}
        {(activeTab === 'all' || activeTab === 'phases') && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
            {individualPhases.map((phase) => (
              <div
                key={phase.id}
                className="bg-white rounded-2xl border border-[#e2ece6] p-6 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow text-right"
              >
                <div>
                  {/* Phase Kicker */}
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-[#059669]">
                      {phase.phaseNameAr}
                    </span>
                    <span className="text-[11px] text-[#526058] bg-[#f3f7f5] px-2 py-0.5 rounded">
                      {phase.packCount}
                    </span>
                  </div>

                  {/* Title & Tagline */}
                  <h4 className="text-base font-bold text-[#064e3b] mb-1 leading-snug">
                    {phase.titleAr}
                  </h4>
                  <p className="text-xs text-[#059669] font-medium mb-3">
                    {phase.taglineAr}
                  </p>

                  <p className="text-xs text-[#404944] leading-relaxed mb-4">
                    {phase.descriptionAr}
                  </p>

                  {/* Dimension or Spec if present */}
                  {phase.dimensions && (
                    <div className="mb-4 p-2.5 rounded-lg bg-[#f8f9ff] border border-[#d9e3f6] text-[11px] text-[#064e3b] flex items-center justify-between">
                      <span className="font-semibold">الأبعاد الجراحية:</span>
                      <span className="font-bold tabular-nums">{phase.dimensions}</span>
                    </div>
                  )}

                  {/* Benefits */}
                  <div className="space-y-1.5 mb-5 border-t border-[#e2ece6] pt-3">
                    {phase.benefits.slice(0, 3).map((benefit, i) => (
                      <div key={i} className="flex items-start gap-1.5 text-xs text-[#121c2a]">
                        <CheckCircle className="w-3.5 h-3.5 text-[#059669] shrink-0 mt-0.5" />
                        <span>{benefit}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Card Bottom Pricing & Actions */}
                <div className="border-t border-[#e2ece6] pt-4 mt-2">
                  <div className="flex items-baseline justify-between mb-3">
                    <span className="text-xs text-[#526058]">السعر للعبوة:</span>
                    <div className="flex items-baseline gap-1.5">
                      <span className="text-xl font-bold text-[#064e3b] tabular-nums">
                        {phase.priceEGP} ج.م
                      </span>
                      <span className="text-xs text-[#707974] line-through tabular-nums">
                        {phase.originalPriceEGP} ج.م
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => onAddToCart(phase.id)}
                      className="py-2.5 px-3 rounded-lg text-xs font-semibold text-[#064e3b] bg-[#f3f7f5] hover:bg-[#e2ece6] border border-[#e2ece6] transition-colors cursor-pointer"
                    >
                      إضافة للسلة
                    </button>
                    <button
                      onClick={() => onInstantBuy(phase.id)}
                      className="py-2.5 px-3 rounded-lg text-xs font-bold text-white bg-[#064e3b] hover:bg-[#003527] transition-colors cursor-pointer"
                    >
                      شراء فوري
                    </button>
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
