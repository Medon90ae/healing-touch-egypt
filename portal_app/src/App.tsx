import React, { useState, useEffect } from 'react';
import { BookOpen, Video, Layers, Calculator, HelpCircle } from 'lucide-react';
import { CampaignId } from './types/campaign';
import { CAMPAIGNS } from './data/campaignConfig';
import { Header } from './components/Header';
import { HeroSection } from './components/HeroSection';
import { TrustAndSafety } from './components/TrustAndSafety';
import { ClinicalArticle } from './components/ClinicalArticle';
import { ScientificEvidence } from './components/ScientificEvidence';
import { VisualStepGuide } from './components/VisualStepGuide';
import { ClinicalCalculator } from './components/ClinicalCalculator';
import { ProductCatalog } from './components/ProductCatalog';
import { ProtocolTimeline } from './components/ProtocolTimeline';
import { ReviewsAndDoctorEndorsement } from './components/ReviewsAndDoctorEndorsement';
import { ClinicalFaq } from './components/ClinicalFaq';
import { LeadGateModal } from './components/LeadGateModal';
import { StickyMobileBar } from './components/StickyMobileBar';
import { Footer } from './components/Footer';

export type ActiveTab = 'article' | 'video' | 'showcase' | 'calculator' | 'faq';

interface TabDefinition {
  id: ActiveTab;
  label: string;
  shortLabel: string;
  icon: React.ComponentType<{ className?: string }>;
}

const TABS: TabDefinition[] = [
  {
    id: 'article',
    label: 'الدليل والمقال السريري الشامل',
    shortLabel: 'الدليل السريري',
    icon: BookOpen,
  },
  {
    id: 'video',
    label: 'فيديو الشرح العملي السريري',
    shortLabel: 'فيديو الشرح',
    icon: Video,
  },
  {
    id: 'showcase',
    label: 'صور واستعراض المنتجات المعتمدة',
    shortLabel: 'المنتجات المعتمدة',
    icon: Layers,
  },
  {
    id: 'calculator',
    label: 'حاسبة مراحل التعافي السريري',
    shortLabel: 'حاسبة التعافي',
    icon: Calculator,
  },
  {
    id: 'faq',
    label: 'الأسئلة الشائعة والأخطاء الحرجة',
    shortLabel: 'الأسئلة والأخطاء',
    icon: HelpCircle,
  },
];

export default function App() {
  // Campaign selector state, synced with URL query parameter ?campaign=...
  const [activeCampaignId, setActiveCampaignId] = useState<CampaignId>(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const queryCampaign = params.get('campaign') as CampaignId;
      if (queryCampaign && CAMPAIGNS[queryCampaign]) {
        return queryCampaign;
      }
    }
    return 'c-section';
  });

  const activeCampaign = CAMPAIGNS[activeCampaignId] || CAMPAIGNS['c-section'];

  // Tab state: default to clinical comprehensive guide
  const [activeTab, setActiveTab] = useState<ActiveTab>('article');

  // Lead Gate Modal & Selected Bundle state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedBundleId, setSelectedBundleId] = useState<string>(
    activeCampaign.bundles[0]?.id || ''
  );

  // Search navigation highlight state
  const [highlightSectionId, setHighlightSectionId] = useState<string | null>(null);
  const [highlightFaqIndex, setHighlightFaqIndex] = useState<number | null>(null);

  // Update URL parameter when campaign changes
  const handleSelectCampaign = (id: CampaignId) => {
    setActiveCampaignId(id);
    setSelectedBundleId(CAMPAIGNS[id]?.bundles[0]?.id || '');
    if (typeof window !== 'undefined') {
      const url = new URL(window.location.href);
      url.searchParams.set('campaign', id);
      window.history.pushState({}, '', url.toString());
    }
  };

  // Sync with browser back/forward buttons
  useEffect(() => {
    const handlePopState = () => {
      const params = new URLSearchParams(window.location.search);
      const queryCampaign = params.get('campaign') as CampaignId;
      if (queryCampaign && CAMPAIGNS[queryCampaign]) {
        setActiveCampaignId(queryCampaign);
        setSelectedBundleId(CAMPAIGNS[queryCampaign]?.bundles[0]?.id || '');
      }
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Update default selected bundle when campaign changes
  useEffect(() => {
    if (!activeCampaign.bundles.find((b) => b.id === selectedBundleId)) {
      setSelectedBundleId(activeCampaign.bundles[0]?.id || '');
    }
  }, [activeCampaignId, activeCampaign.bundles, selectedBundleId]);

  const handleOpenLeadModal = (bundleId?: string) => {
    if (bundleId) {
      setSelectedBundleId(bundleId);
    }
    setIsModalOpen(true);
  };

  const handleSwitchTab = (tabId: ActiveTab) => {
    setActiveTab(tabId);
    setTimeout(() => {
      const navElement = document.getElementById('portal-tab-navigation');
      if (navElement) {
        navElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 50);
  };

  const handleScrollToCalculator = () => {
    setActiveTab('calculator');
    setTimeout(() => {
      const el = document.getElementById('clinical-calculator') || document.getElementById('main-tab-content');
      el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  };

  const handleScrollToCatalog = () => {
    setActiveTab('showcase');
    setTimeout(() => {
      const el = document.getElementById('product-catalog') || document.getElementById('main-tab-content');
      el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  };

  const handleNavigateToSearchResult = (params: {
    campaignId: CampaignId;
    targetElementId: string;
    sectionId?: string;
    faqIndex?: number;
  }) => {
    // 1. Switch campaign if needed
    if (params.campaignId !== activeCampaignId) {
      handleSelectCampaign(params.campaignId);
    }

    // 2. Select corresponding tab based on target element
    if (typeof params.faqIndex === 'number' || params.targetElementId.startsWith('faq-')) {
      setActiveTab('faq');
    } else if (params.targetElementId === 'clinical-calculator') {
      setActiveTab('calculator');
    } else if (params.targetElementId === 'product-catalog') {
      setActiveTab('showcase');
    } else if (params.targetElementId === 'visual-step-guide') {
      setActiveTab('video');
    } else {
      setActiveTab('article');
    }

    // 3. Set highlight targets
    setHighlightSectionId(params.sectionId || null);
    setHighlightFaqIndex(typeof params.faqIndex === 'number' ? params.faqIndex : null);

    // 4. Smooth scroll after DOM updates and tab render
    setTimeout(() => {
      const el = document.getElementById(params.targetElementId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else {
        const fallbackEl = document.getElementById('main-tab-content');
        fallbackEl?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 150);

    // 5. Clear highlight after 4.5 seconds
    setTimeout(() => {
      setHighlightSectionId(null);
      setHighlightFaqIndex(null);
    }, 4500);
  };

  return (
    <div className="min-h-screen bg-[#FBFDFB] text-[#121C2A] flex flex-col font-sans selection:bg-[#82F5C1] selection:text-[#003527]">
      {/* App Header with Campaign Switcher & Local Search Bar */}
      <Header
        activeCampaignId={activeCampaignId}
        onSelectCampaign={handleSelectCampaign}
        onOpenLeadModal={handleOpenLeadModal}
        onNavigateToSearchResult={handleNavigateToSearchResult}
      />

      {/* Main Content-First Educational & Clinical Portal */}
      <main className="flex-1">
        {/* Hero Section with Clinical Packaging Mockup & Interactive Showcase */}
        <HeroSection
          campaign={activeCampaign}
          onOpenLeadModal={handleOpenLeadModal}
          onScrollToCalculator={handleScrollToCalculator}
          onSelectTab={handleSwitchTab}
        />

        {/* 5-Tab Segmented UI Navigation Bar */}
        <nav
          id="portal-tab-navigation"
          aria-label="أقسام المنظومة السريرية"
          className="sticky top-[69px] sm:top-[77px] z-30 bg-white/95 backdrop-blur-md border-y border-[#E2ECE6] shadow-xs"
        >
          <div className="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
            <div
              role="tablist"
              className="flex items-center gap-1.5 sm:gap-2 py-2.5 overflow-x-auto no-scrollbar scroll-smooth"
            >
              {TABS.map((tab) => {
                const IconComponent = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    role="tab"
                    id={`tab-${tab.id}`}
                    aria-selected={isActive}
                    aria-controls={`panel-${tab.id}`}
                    type="button"
                    onClick={() => handleSwitchTab(tab.id)}
                    className={`flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-200 shrink-0 cursor-pointer select-none active:scale-95 ${
                      isActive
                        ? 'bg-[#064E3B] text-white shadow-sm shadow-[#064E3B]/25 ring-2 ring-[#064E3B]'
                        : 'bg-[#F3F7F5] text-[#404944] hover:bg-[#E2ECE6] hover:text-[#003527]'
                    }`}
                  >
                    <IconComponent
                      className={`w-4 h-4 shrink-0 ${
                        isActive ? 'text-[#82F5C1]' : 'text-[#059669]'
                      }`}
                    />
                    <span className="hidden sm:inline">{tab.label}</span>
                    <span className="inline sm:hidden">{tab.shortLabel}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </nav>

        {/* Tab Content Panels */}
        <div id="main-tab-content" className="relative min-h-[600px]">
          {/* Tab 1: [📖 الدليل والمقال السريري الشامل] */}
          {activeTab === 'article' && (
            <div
              id="panel-article"
              role="tabpanel"
              aria-labelledby="tab-article"
              className="animate-fade-in"
            >
              <ClinicalArticle
                article={activeCampaign.article}
                campaignName={activeCampaign.name}
                highlightSectionId={highlightSectionId}
              />
              <ScientificEvidence
                studies={activeCampaign.scientificStudies}
                campaignName={activeCampaign.name}
              />
              <TrustAndSafety />
            </div>
          )}

          {/* Tab 2: [🎬 فيديو الشرح العملي السريري] */}
          {activeTab === 'video' && (
            <div
              id="panel-video"
              role="tabpanel"
              aria-labelledby="tab-video"
              className="animate-fade-in"
            >
              {/* Clinical Video Showcase Header Card */}
              <section className="py-10 sm:py-14 bg-gradient-to-b from-[#F3F7F5] to-white border-b border-[#E2ECE6]">
                <div className="max-w-5xl mx-auto px-4 sm:px-6">
                  <div className="bg-white rounded-3xl border border-[#D0DBED] shadow-lg overflow-hidden p-6 sm:p-8">
                    <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-6 mb-6">
                      <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-[#064E3B] text-white flex items-center justify-center shrink-0 shadow-md">
                        <Video className="w-6 h-6 sm:w-7 sm:h-7 text-[#82F5C1]" />
                      </div>
                      <div>
                        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#E6EEFF] text-[#003527] text-xs font-semibold mb-2">
                          <span>فيديو الشرح العملي السريري</span>
                          {activeCampaign.videoDuration && (
                            <span className="text-[#059669]">• {activeCampaign.videoDuration}</span>
                          )}
                        </div>
                        <h2 className="text-xl sm:text-2xl font-bold text-[#003527]">
                          {activeCampaign.videoTitle || `الشرح العملي السريري لبروتوكول ${activeCampaign.name}`}
                        </h2>
                        <p className="text-xs sm:text-sm text-[#404944] mt-1">
                          تطبيق سريري خطوة بخطوة من أخصائيي العناية بالجروح لحماية موضع الجراحة ومنع التلوث الميكروبي
                        </p>
                      </div>
                    </div>

                    {/* Video Player */}
                    <div className="relative aspect-video rounded-2xl overflow-hidden bg-black/90 shadow-inner border border-black/10">
                      <video
                        poster={activeCampaign.videoPosterUrl || activeCampaign.heroImageUrl}
                        controls
                        playsInline
                        className="w-full h-full object-contain"
                      >
                        {activeCampaign.videoUrl && (
                          <source src={activeCampaign.videoUrl} type="video/mp4" />
                        )}
                        <source
                          src={`./assets/${activeCampaign.id === 'c-section' ? 'campaign_c-section_video.mp4' : 'campaign_bariatric_video.mp4'}`}
                          type="video/mp4"
                        />
                        <source
                          src={`/healing-touch-egypt/assets/${activeCampaign.id === 'c-section' ? 'campaign_c-section_video.mp4' : 'campaign_bariatric_video.mp4'}`}
                          type="video/mp4"
                        />
                        متصفحك لا يدعم تشغيل الفيديو المباشر.
                      </video>
                    </div>
                  </div>
                </div>
              </section>

              {/* Visual Step Guide */}
              <VisualStepGuide
                campaignId={activeCampaign.id}
                campaignName={activeCampaign.name}
                onScrollToCatalog={handleScrollToCatalog}
              />
            </div>
          )}

          {/* Tab 3: [📸 صور واستعراض المنتجات المعتمدة] */}
          {activeTab === 'showcase' && (
            <div
              id="panel-showcase"
              role="tabpanel"
              aria-labelledby="tab-showcase"
              className="animate-fade-in"
            >
              <ProductCatalog
                campaign={activeCampaign}
                onOpenLeadModal={handleOpenLeadModal}
              />
            </div>
          )}

          {/* Tab 4: [🧮 حاسبة مراحل التعافي السريري] */}
          {activeTab === 'calculator' && (
            <div
              id="panel-calculator"
              role="tabpanel"
              aria-labelledby="tab-calculator"
              className="animate-fade-in"
            >
              <ClinicalCalculator
                campaign={activeCampaign}
                onSelectBundleAndOpenModal={handleOpenLeadModal}
              />
              <ProtocolTimeline campaign={activeCampaign} />
            </div>
          )}

          {/* Tab 5: [❓ الأسئلة الشائعة والأخطاء الحرجة] */}
          {activeTab === 'faq' && (
            <div
              id="panel-faq"
              role="tabpanel"
              aria-labelledby="tab-faq"
              className="animate-fade-in"
            >
              <ClinicalFaq
                faqs={activeCampaign.faqs}
                highlightFaqIndex={highlightFaqIndex}
              />
              <ReviewsAndDoctorEndorsement campaign={activeCampaign} />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <Footer
        campaign={activeCampaign}
        onSelectCampaign={handleSelectCampaign}
        onOpenLeadModal={() => handleOpenLeadModal()}
      />

      {/* Sticky Mobile Conversion Bar */}
      <StickyMobileBar
        campaign={activeCampaign}
        selectedBundleId={selectedBundleId}
        onOpenLeadModal={handleOpenLeadModal}
      />

      {/* The ZERO-BYPASS Lead Gate Modal */}
      <LeadGateModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        campaign={activeCampaign}
        selectedBundleId={selectedBundleId}
        onSelectBundleId={setSelectedBundleId}
      />
    </div>
  );
}
