import React from 'react';
import { MessageSquare, ArrowLeft, ShieldCheck } from 'lucide-react';
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
      aria-label="شريط الاستشارة السريرية السريع"
      className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-[#E2ECE6] px-4 py-3 shadow-[0_-4px_24px_rgba(6,78,59,0.12)]"
    >
      <div className="flex items-center justify-between gap-3">
        {/* Left Side: Clinical Guidance Info (0 Prices) */}
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-1.5 text-[11px] text-[#059669] font-bold">
            <ShieldCheck className="w-3.5 h-3.5 text-[#059669] shrink-0" />
            <span className="truncate">متابعة سريرية متخصصة</span>
          </div>

          <div className="text-xs font-bold text-[#003527] truncate mt-0.5">
            {campaign.surgicalArea}
          </div>

          <div className="text-[11px] text-[#707974] truncate">
            استشارة ومتابعة سريرية مجانية
          </div>
        </div>

        {/* Right Side: Consultation CTA Button */}
        <button
          type="button"
          onClick={() => onOpenLeadModal(currentBundle?.id)}
          className="bg-[#064E3B] active:bg-[#003527] text-white px-4 py-3 rounded-xl font-bold text-xs shadow-md shadow-[#064E3B]/20 transition-all flex items-center gap-1.5 shrink-0 cursor-pointer active:scale-95"
        >
          <MessageSquare className="w-3.5 h-3.5 text-[#82F5C1]" />
          <span>استشيري أخصائية التعافي مجاناً عبر واتساب</span>
          <ArrowLeft className="w-3.5 h-3.5 rtl:rotate-0" />
        </button>
      </div>
    </aside>
  );
};
