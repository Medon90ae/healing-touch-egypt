import React, { useState, useEffect } from 'react';
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

  // Lead Gate Modal & Selected Bundle state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedBundleId, setSelectedBundleId] = useState<string>(
    activeCampaign.bundles[0]?.id || ''
  );

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

  const handleScrollToCalculator = () => {
    const el = document.getElementById('clinical-calculator');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleScrollToCatalog = () => {
    const el = document.getElementById('product-catalog');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Search navigation highlight state
  const [highlightSectionId, setHighlightSectionId] = useState<string | null>(null);
  const [highlightFaqIndex, setHighlightFaqIndex] = useState<number | null>(null);

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

    // 2. Set highlight targets
    setHighlightSectionId(params.sectionId || null);
    setHighlightFaqIndex(typeof params.faqIndex === 'number' ? params.faqIndex : null);

    // 3. Smooth scroll after DOM updates
    setTimeout(() => {
      const el = document.getElementById(params.targetElementId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else {
        const fallbackId = typeof params.faqIndex === 'number' ? 'clinical-faq' : 'clinical-article';
        const fallbackEl = document.getElementById(fallbackId);
        fallbackEl?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 150);

    // 4. Clear highlight after 4.5 seconds
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
        {/* 1. Hero Section with Clinical Packaging Mockup */}
        <HeroSection
          campaign={activeCampaign}
          onOpenLeadModal={handleOpenLeadModal}
          onScrollToCalculator={handleScrollToCalculator}
        />

        {/* 2. Clinical Trust & Safety Pillars */}
        <TrustAndSafety />

        {/* 3. Comprehensive Clinical Article (Deep Medical Authority) */}
        <ClinicalArticle
          article={activeCampaign.article}
          campaignName={activeCampaign.name}
          highlightSectionId={highlightSectionId}
        />

        {/* 4. Peer-Reviewed Scientific Evidence Table (PubMed & Cochrane) */}
        <ScientificEvidence
          studies={activeCampaign.scientificStudies}
          campaignName={activeCampaign.name}
        />

        {/* 5. Visual Step-by-Step Application Guide */}
        <VisualStepGuide
          campaignId={activeCampaign.id}
          campaignName={activeCampaign.name}
          onScrollToCatalog={handleScrollToCatalog}
        />

        {/* 6. Interactive Clinical Recovery Calculator */}
        <ClinicalCalculator
          campaign={activeCampaign}
          onSelectBundleAndOpenModal={handleOpenLeadModal}
        />

        {/* 7. Product & Protocol Catalog with Rich Photography */}
        <ProductCatalog
          campaign={activeCampaign}
          onOpenLeadModal={handleOpenLeadModal}
        />

        {/* 8. Step-by-Step Clinical Timeline */}
        <ProtocolTimeline campaign={activeCampaign} />

        {/* 9. Verified Egyptian Doctor Endorsements & Patient Reviews */}
        <ReviewsAndDoctorEndorsement campaign={activeCampaign} />

        {/* 10. Clinical FAQs */}
        <ClinicalFaq
          faqs={activeCampaign.faqs}
          highlightFaqIndex={highlightFaqIndex}
        />
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
