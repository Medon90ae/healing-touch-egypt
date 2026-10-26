import React from 'react';
import { Star, ArrowLeft } from 'lucide-react';
import { Campaign } from '../types/campaign';

interface StickyMobileBarProps {
  campaign: Campaign;
  selectedBundleId?: string;
  onOpenLeadModal: (bundleId?: string) => void;
}

export const StickyMobileBar: React.FC<StickyMobileBarProps> = ({
  campaign,
  selectedBundleId,
  onOpenLeadModal
}) => {
  const currentBundle =
    campaign.bundles.find((b) => b.id === selectedBundleId) || campaign.bundles[0];

  return (
    <aside
      aria-label="شريط الطلب السريع"
      className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-[#E2ECE6] px-4 py-3 shadow-[0_-4px_24px_rgba(6,78,59,0.08)]"
    >
      <div className="flex items-center justify-between gap-3">
        {/* Left Side: Kit & Price Info */}
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-1 text-[11px] text-[#D97706] font-bold">
            <div className="flex items-center">
              <Star className="w-3 h-3 fill-[#D97706]" />
              <Star className="w-3 h-3 fill-[#D97706]" />
              <Star className="w-3 h-3 fill-[#D97706]" />
              <Star className="w-3 h-3 fill-[#D97706]" />
              <Star className="w-3 h-3 fill-[#D97706]" />
            </div>
            <span>(4.9/5) معتمد</span>
          </div>

          <div className="text-xs font-bold text-[#003527] truncate">
            {currentBundle.title}
          </div>

          <div className="flex items-baseline gap-1 mt-0.5">
            <span className="text-base font-extrabold text-[#064E3B]">
              {currentBundle.priceEGP}
            </span>
            <span className="text-[11px] font-bold text-[#059669]">ج.م</span>
            <span className="text-[10px] text-[#707974] line-through mr-1">
              {currentBundle.originalPriceEGP} ج.م
            </span>
          </div>
        </div>

        {/* Right Side: CTA Button (Strictly labeled as required) */}
        <button
          type="button"
          onClick={() => onOpenLeadModal(currentBundle.id)}
          className="bg-[#064E3B] active:bg-[#003527] text-white px-4 py-3 rounded-xl font-bold text-xs shadow-md shadow-[#064E3B]/20 transition-all flex items-center gap-1.5 shrink-0 cursor-pointer"
        >
          <span>تأكيد الطلب وحجز الاستشارة</span>
          <ArrowLeft className="w-3.5 h-3.5" />
        </button>
      </div>
    </aside>
  );
};
