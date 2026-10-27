import React, { useState } from 'react';
import { ShieldCheck, MessageSquare, HeartHandshake, Share2, Check, Copy } from 'lucide-react';
import { Campaign, CampaignId } from '../types/campaign';
import { CAMPAIGNS } from '../data/campaignConfig';
import { buildCampaignShareData } from '../utils/share';

interface FooterProps {
  campaign: Campaign;
  onSelectCampaign: (id: CampaignId) => void;
  onOpenLeadModal: () => void;
}

export const Footer: React.FC<FooterProps> = ({
  campaign,
  onSelectCampaign,
  onOpenLeadModal
}) => {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    const baseUrl = typeof window !== 'undefined'
      ? `${window.location.origin}${window.location.pathname}`
      : '';
    const shareData = buildCampaignShareData(campaign, baseUrl);

    if (typeof navigator !== 'undefined' && typeof navigator.share === 'function') {
      try {
        await navigator.share(shareData);
      } catch (err: unknown) {
        if ((err as Error)?.name !== 'AbortError') {
          await copyToClipboard(shareData.url);
        }
      }
    } else {
      await copyToClipboard(shareData.url);
    }
  };

  const copyToClipboard = async (url: string) => {
    try {
      if (typeof navigator !== 'undefined' && navigator.clipboard) {
        await navigator.clipboard.writeText(url);
        setCopied(true);
        setTimeout(() => setCopied(false), 3000);
      }
    } catch (err) {
      console.error('Clipboard copy error:', err);
    }
  };

  return (
    <footer className="bg-[#002117] text-white pt-12 pb-24 md:pb-12 border-t border-[#064E3B]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pb-10 border-b border-white/10">
          {/* Brand Info */}
          <div className="md:col-span-4 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#064E3B] to-[#059669] flex items-center justify-center text-white font-bold text-lg border border-white/20">
                HT
              </div>
              <div>
                <span className="font-bold text-lg text-white">هيلينج تاتش مصر</span>
                <span className="block text-xs text-[#82F5C1]">Healing Touch Egypt • المنظومة السريرية للتعافي</span>
              </div>
            </div>

            <p className="text-xs sm:text-sm text-white/70 leading-relaxed max-w-sm">
              المنظومة الأولى بمصر المتخصصة في بروتوكولات حماية وترميم الجروح الجراحية بعد الولادة القيصرية، تجميل الأنف، جراحات السمنة، واستئصال الغدة الدرقية.
            </p>

            <div className="flex items-center gap-2 text-xs text-[#82F5C1]">
              <ShieldCheck className="w-4 h-4" />
              <span>منتجات معقمة طبياً معتمدة برخص ISO و CE</span>
            </div>
          </div>

          {/* Quick Links to Campaigns */}
          <div className="md:col-span-4 space-y-3">
            <div className="font-bold text-sm text-[#82F5C1]">
              بروتوكولات التعافي المتاحة:
            </div>
            <ul className="space-y-2 text-xs sm:text-sm text-white/80">
              {Object.values(CAMPAIGNS).map((c) => (
                <li key={c.id}>
                  <button
                    type="button"
                    onClick={() => {
                      onSelectCampaign(c.id);
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                    className={`hover:text-[#82F5C1] transition-colors cursor-pointer text-right flex items-center gap-1.5 ${
                      c.id === campaign.id ? 'text-[#82F5C1] font-semibold' : ''
                    }`}
                  >
                    <span>•</span>
                    <span>بروتوكول {c.name}</span>
                    {c.id === campaign.id && (
                      <span className="text-[10px] bg-[#064E3B] text-[#82F5C1] px-1.5 py-0.2 rounded font-medium">
                        الحالي
                      </span>
                    )}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Share & Clinical Consultation */}
          <div className="md:col-span-4 space-y-4">
            {/* Share Feature */}
            <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs sm:text-sm text-[#82F5C1] flex items-center gap-1.5">
                  <Share2 className="w-4 h-4 text-[#82F5C1]" />
                  <span>مشاركة البروتوكول السريري</span>
                </span>
                <span className="text-[10px] text-white/50 bg-white/10 px-2 py-0.5 rounded">
                  {campaign.name}
                </span>
              </div>

              <p className="text-xs text-white/70 leading-relaxed">
                شاركي بروتوكول <strong>{campaign.name}</strong> مع طبيبك المعالج أو أصدقائك للاستشارة والمعاينة.
              </p>

              <button
                type="button"
                onClick={handleShare}
                aria-label={`مشاركة بروتوكول ${campaign.name}`}
                className="w-full flex items-center justify-center gap-2 bg-[#82F5C1]/15 hover:bg-[#82F5C1]/25 text-[#82F5C1] border border-[#82F5C1]/40 px-4 py-2.5 rounded-xl font-bold text-xs transition-all cursor-pointer active:scale-98"
              >
                {copied ? (
                  <>
                    <Check className="w-4 h-4 text-[#82F5C1]" />
                    <span>تم نسخ رابط البروتوكول بنجاح!</span>
                  </>
                ) : (
                  <>
                    <Share2 className="w-4 h-4 text-[#82F5C1]" />
                    <span>مشاركة رابط {campaign.name} الآن</span>
                  </>
                )}
              </button>
            </div>

            {/* Specialist Consultation */}
            <div className="space-y-2">
              <button
                type="button"
                onClick={onOpenLeadModal}
                className="w-full inline-flex items-center justify-center gap-2 bg-[#059669] hover:bg-[#064E3B] text-white px-4 py-2.5 rounded-xl font-bold text-xs transition-colors cursor-pointer"
              >
                <MessageSquare className="w-4 h-4 text-[#82F5C1]" />
                <span>استشيري أخصائية التعافي مجاناً</span>
              </button>
              <p className="text-[11px] text-white/50 text-center">
                استشارة هاتفية وسريرية مجانية لمتابعة حالة الجرح وتحديد المقاسات
              </p>
            </div>
          </div>
        </div>

        {/* Medical Disclaimer & Copyright (Zero Raw Phone Numbers) */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-white/50">
          <p className="text-center sm:text-right leading-relaxed">
            تنويه طبي: الإرشادات والمعلومات الواردة على هذه المنصة تهدف للتثقيف السريري والدعم التمريضي التكميلي ولا تغني عن الاستشارة أو التوجيه الطبي المباشر من جراحك أو طبيبك المعالج.
          </p>
          <div className="shrink-0 text-center sm:text-left flex items-center gap-1">
            <HeartHandshake className="w-3.5 h-3.5 text-[#82F5C1]" />
            <span>جميع الحقوق محفوظة © {new Date().getFullYear()} هيلينج تاتش مصر - Healing Touch Egypt</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
