import React from 'react';
import { ShieldCheck, Truck, Clock, Sparkles, MessageSquare } from 'lucide-react';
import { CampaignId } from '../types/campaign';
import { CAMPAIGNS } from '../data/campaignConfig';
import { SearchBar } from './SearchBar';

interface HeaderProps {
  activeCampaignId: CampaignId;
  onSelectCampaign: (id: CampaignId) => void;
  onOpenLeadModal: (bundleId?: string) => void;
  onNavigateToSearchResult: (params: {
    campaignId: CampaignId;
    targetElementId: string;
    sectionId?: string;
    faqIndex?: number;
  }) => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeCampaignId,
  onSelectCampaign,
  onOpenLeadModal,
  onNavigateToSearchResult,
}) => {
  const campaignsList = Object.values(CAMPAIGNS);

  return (
    <header className="sticky top-0 z-40 bg-[#FBFDFB]/95 backdrop-blur-md border-b border-[#E2ECE6]">
      {/* Top clinical announcement bar */}
      <div className="bg-[#003527] text-white text-xs sm:text-sm py-2 px-4">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-3 mx-auto sm:mx-0">
            <span className="inline-flex items-center gap-1 text-[#82F5C1] font-medium">
              <Truck className="w-3.5 h-3.5" />
              شحن سريع لجميع محافظات مصر (24-48 ساعة)
            </span>
            <span className="hidden md:inline text-white/40">•</span>
            <span className="hidden md:inline-flex items-center gap-1 text-white/90">
              <ShieldCheck className="w-3.5 h-3.5 text-[#82F5C1]" />
              الدفع عند الاستلام مع فحص الشحنة
            </span>
            <span className="hidden lg:inline text-white/40">•</span>
            <span className="hidden lg:inline-flex items-center gap-1 text-[#82F5C1]">
              <Sparkles className="w-3.5 h-3.5 text-[#82F5C1]" />
              استشارة سريرية مجانية ومتابعة مستمرة للتعافي
            </span>
          </div>

          <div className="hidden sm:flex items-center gap-2 text-xs text-[#95D3BA]">
            <Clock className="w-3.5 h-3.5" />
            <span>متابعة سريرية متخصصة للأمهات والمرضى</span>
          </div>
        </div>
      </div>

      {/* Main navigation & brand identity */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 sm:gap-4">
          <div className="flex items-center justify-between gap-3">
            {/* Brand Logo & Medical Seal */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-br from-[#064E3B] to-[#006C4A] flex items-center justify-center text-white shadow-md shadow-[#064E3B]/15 shrink-0">
                <span className="font-bold text-lg sm:text-xl tracking-tighter">HT</span>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-lg sm:text-xl text-[#003527] tracking-tight">
                    هيلينج تاتش مصر
                  </span>
                  <span className="hidden md:inline-block text-[11px] font-semibold bg-[#E6EEFF] text-[#003527] px-2 py-0.5 rounded-full border border-[#D0DBED]">
                    Healing Touch Egypt
                  </span>
                </div>
                <p className="text-xs text-[#404944] hidden sm:block">
                  المنظومة السريرية المعتمدة لحماية وترميم الجروح الجراحية بمصر
                </p>
              </div>
            </div>

            {/* Compact Consultation trigger for mobile */}
            <div className="lg:hidden shrink-0">
              <button
                onClick={() => onOpenLeadModal()}
                type="button"
                className="inline-flex items-center gap-1.5 bg-[#064E3B] hover:bg-[#003527] text-white px-3 py-2 rounded-lg font-semibold text-xs shadow-xs transition-all duration-200 cursor-pointer active:scale-98"
                aria-label="استشيري أخصائية التعافي مجاناً"
              >
                <MessageSquare className="w-3.5 h-3.5 text-[#82F5C1]" />
                <span>استشارة مجاناً</span>
              </button>
            </div>
          </div>

          {/* Prominent Local Clinical Search Bar */}
          <div className="w-full lg:max-w-lg xl:max-w-xl mx-auto lg:mx-0">
            <SearchBar
              activeCampaignId={activeCampaignId}
              onNavigateToResult={onNavigateToSearchResult}
            />
          </div>

          {/* Action Button: Strictly labeled as required (desktop) */}
          <div className="hidden lg:flex items-center gap-2 sm:gap-3 shrink-0">
            <button
              onClick={() => onOpenLeadModal()}
              type="button"
              className="inline-flex items-center gap-2 bg-[#064E3B] hover:bg-[#003527] text-white px-4 sm:px-5 py-2.5 rounded-lg font-semibold text-xs sm:text-sm shadow-sm transition-all duration-200 cursor-pointer active:scale-98 focus:outline-none focus:ring-2 focus:ring-[#059669] focus:ring-offset-2"
              aria-label="استشيري أخصائية التعافي مجاناً"
            >
              <MessageSquare className="w-4 h-4 text-[#82F5C1]" />
              <span>استشيري أخصائية التعافي مجاناً</span>
            </button>
          </div>
        </div>

        {/* Campaign Switcher Navigation Tabs */}
        <div className="mt-3 pt-3 border-t border-[#E2ECE6] overflow-x-auto no-scrollbar">
          <div className="flex items-center gap-2 min-w-max pb-1">
            <span className="text-xs font-semibold text-[#404944] ml-2 flex items-center gap-1">
              اختر نوع الجراحة:
            </span>
            {campaignsList.map((c) => {
              const isActive = c.id === activeCampaignId;
              return (
                <button
                  key={c.id}
                  onClick={() => onSelectCampaign(c.id)}
                  type="button"
                  className={`px-3.5 py-1.5 rounded-full text-xs sm:text-sm font-medium transition-all duration-200 cursor-pointer flex items-center gap-1.5 ${
                    isActive
                      ? 'bg-[#064E3B] text-white shadow-sm ring-1 ring-[#064E3B]'
                      : 'bg-[#F3F7F5] text-[#404944] hover:bg-[#E2ECE6] hover:text-[#003527]'
                  }`}
                  aria-pressed={isActive}
                >
                  <span
                    className={`w-2 h-2 rounded-full ${
                      isActive ? 'bg-[#82F5C1]' : 'bg-[#707974]'
                    }`}
                  />
                  <span>{c.name}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </header>
  );
};
