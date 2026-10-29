import React, { useState, useMemo } from 'react';
import { 
  ShieldCheck, 
  CheckCircle2, 
  Layers, 
  Sparkles, 
  Play, 
  ArrowLeft,
  BookOpen,
  Image as ImageIcon,
  Video,
  MessageSquare,
  Clock
} from 'lucide-react';
import { Campaign, GalleryProductImage } from '../types/campaign';

interface HeroSectionProps {
  campaign: Campaign;
  onOpenLeadModal: (bundleId?: string) => void;
  onScrollToCatalog?: () => void;
  onSelectTab?: (tab: 'article' | 'video' | 'showcase' | 'faq') => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  campaign,
  onOpenLeadModal,
  onScrollToCatalog,
  onSelectTab
}) => {
  const [activeMediaTab, setActiveMediaTab] = useState<'video' | 'gallery'>('video');
  const [selectedGalleryIdx, setSelectedGalleryIdx] = useState(0);

  const allGallery: GalleryProductImage[] = useMemo(() => {
    return campaign.galleryImages || [
      {
        url: campaign.heroImageUrl,
        title: 'مستلزمات التعافي السريري المعتمدة',
        subtitle: 'منتجات طبية أصلية 100% معقمة ومغلفة لحماية موضع الجراحة',
        clinicalFunction: 'عزل ميكانيكي وترطيب عميق لموضع الجراحة'
      }
    ];
  }, [campaign.galleryImages, campaign.heroImageUrl]);

  const activePhotoIndex = selectedGalleryIdx < allGallery.length ? selectedGalleryIdx : 0;
  const currentPhoto = allGallery[activePhotoIndex] || allGallery[0];

  const handleScrollToArticle = () => {
    if (onSelectTab) {
      onSelectTab('article');
    }
    const el = document.getElementById('clinical-article');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-[#F3F7F5] via-[#FBFDFB] to-[#FBFDFB] pt-6 pb-10 sm:pt-8 sm:pb-14 border-b border-[#E2ECE6]">
      {/* Decorative clinical light accents */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-[#82F5C1]/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 left-10 w-72 h-72 bg-[#95D3BA]/15 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 items-start">
          
          {/* Main Hero Narrative & Trending Question (7 cols on desktop) */}
          <div className="lg:col-span-7 space-y-5 animate-fade-in-up">
            
            {/* Clinical Endorsement Pill */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] border border-[#D0DBED] text-[#003527] text-xs sm:text-sm font-semibold shadow-2xs">
              <span className="w-2.5 h-2.5 rounded-full bg-[#059669] animate-pulse" />
              <span>{campaign.heroBadge}</span>
            </div>

            {/* Surgical Area Identification */}
            <div className="text-xs font-bold tracking-wider text-[#059669] uppercase flex items-center gap-1.5">
              <span>نطاق الرعاية السريرية:</span>
              <span className="text-[#003527] font-extrabold">{campaign.surgicalArea}</span>
            </div>

            {/* Main Headline: The Catchy Trending Google Question */}
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-[#003527] leading-tight sm:leading-snug">
              {campaign.title}
            </h1>

            {/* Subtitle / Comprehensive Answer Preview */}
            <p className="text-sm sm:text-base text-[#404944] leading-relaxed max-w-2xl">
              {campaign.subtitle}
            </p>

            {/* Quick 3-4 Clinical Highlights Checklist */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
              {campaign.heroHighlights.map((highlight, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2 p-2.5 rounded-xl bg-white border border-[#E2ECE6] shadow-2xs"
                >
                  <CheckCircle2 className="w-4 h-4 text-[#059669] shrink-0 mt-0.5" />
                  <span className="text-xs sm:text-sm font-medium text-[#121C2A] leading-snug">
                    {highlight}
                  </span>
                </div>
              ))}
            </div>

            {/* CTAs: Content & Clinical Guidance First */}
            <div className="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5 sm:gap-3">
              <button
                type="button"
                onClick={() => onOpenLeadModal()}
                className="inline-flex items-center justify-center gap-2 bg-[#064E3B] hover:bg-[#003527] text-white px-6 py-3.5 rounded-xl font-bold text-sm sm:text-base shadow-md shadow-[#064E3B]/20 transition-all duration-200 cursor-pointer active:scale-98"
                aria-label="استشيري أخصائية التعافي مجاناً"
              >
                <MessageSquare className="w-4 h-4 text-[#82F5C1]" />
                <span>استشيري أخصائية التعافي مجاناً</span>
                <ArrowLeft className="w-4 h-4 rtl:rotate-0" />
              </button>

              <button
                type="button"
                onClick={handleScrollToArticle}
                className="inline-flex items-center justify-center gap-2 bg-white hover:bg-[#F3F7F5] text-[#064E3B] border-2 border-[#064E3B] px-5 py-3 rounded-xl font-semibold text-xs sm:text-sm transition-all duration-200 cursor-pointer active:scale-98"
              >
                <BookOpen className="w-4 h-4 text-[#059669]" />
                <span>الدليل والشرح التشريحي الكامل</span>
              </button>

              <button
                type="button"
                onClick={() => {
                  if (onSelectTab) onSelectTab('showcase');
                  if (onScrollToCatalog) {
                    onScrollToCatalog();
                  } else {
                    const el = document.getElementById('product-catalog');
                    el?.scrollIntoView({ behavior: 'smooth' });
                  }
                }}
                className="inline-flex items-center justify-center gap-1.5 bg-[#F3F7F5] hover:bg-[#E6EEFF] text-[#003527] border border-[#D0DBED] px-4 py-3 rounded-xl font-semibold text-xs sm:text-sm transition-all duration-200 cursor-pointer active:scale-98"
              >
                <Layers className="w-4 h-4 text-[#059669]" />
                <span>المنتجات المعتمدة</span>
              </button>
            </div>

            {/* Trust note */}
            <div className="flex flex-wrap items-center gap-2.5 text-xs text-[#707974] pt-1">
              <span className="inline-flex items-center gap-1 text-[#059669] font-semibold">
                <ShieldCheck className="w-4 h-4" />
                مستلزمات طبية أصلية 100% معقمة ومحكمة الغلق
              </span>
              <span>•</span>
              <span>متابعة سريرية متخصصة للأمهات والمرضى بمصر</span>
              <span>•</span>
              <span className="text-[#003527] font-bold">حق المعاينة والفحص عند الاستلام</span>
            </div>
          </div>

          {/* Right Column: Embedded Clinical Video Player & Medical Supplies Showcase (5 cols on desktop) */}
          <div className="lg:col-span-5 animate-fade-in-up delay-100">
            <div className="relative bg-white rounded-2xl border border-[#E2ECE6] shadow-xl shadow-[#064E3B]/5 overflow-hidden">
              
              {/* Media Switcher Tabs */}
              <div className="flex border-b border-[#E2ECE6] bg-[#F8F9FF]">
                <button
                  type="button"
                  onClick={() => setActiveMediaTab('video')}
                  className={`flex-1 py-3 px-3 text-xs sm:text-sm font-bold flex items-center justify-center gap-2 transition-all cursor-pointer border-b-2 ${
                    activeMediaTab === 'video'
                      ? 'border-[#059669] text-[#003527] bg-white'
                      : 'border-transparent text-[#707974] hover:text-[#121C2A] hover:bg-[#F3F7F5]'
                  }`}
                >
                  <Video className="w-4 h-4 text-[#059669]" />
                  <span>فيديو الشرح السريري</span>
                  {campaign.videoDuration && (
                    <span className="text-[10px] bg-[#E6EEFF] text-[#064E3B] px-1.5 py-0.2 rounded-full font-semibold">
                      {campaign.videoDuration}
                    </span>
                  )}
                </button>

                <button
                  type="button"
                  onClick={() => setActiveMediaTab('gallery')}
                  className={`flex-1 py-3 px-3 text-xs sm:text-sm font-bold flex items-center justify-center gap-2 transition-all cursor-pointer border-b-2 ${
                    activeMediaTab === 'gallery'
                      ? 'border-[#059669] text-[#003527] bg-white'
                      : 'border-transparent text-[#707974] hover:text-[#121C2A] hover:bg-[#F3F7F5]'
                  }`}
                >
                  <ImageIcon className="w-4 h-4 text-[#059669]" />
                  <span>استعراض المستلزمات الطبية</span>
                  <span className="text-[10px] bg-[#DCFCE7] text-[#006C4A] px-1.5 py-0.2 rounded-full font-semibold">
                    {allGallery.length} صور
                  </span>
                </button>
              </div>

              {/* Tab 1: Video Player Container */}
              {activeMediaTab === 'video' && (
                <div className="p-3.5 space-y-3">
                  <div className="relative aspect-16/10 rounded-xl overflow-hidden bg-black border border-[#E2ECE6] group shadow-inner">
                    {campaign.videoUrl ? (
                      <video
                        poster={campaign.videoPosterUrl || campaign.heroImageUrl}
                        controls
                        playsInline
                        preload="metadata"
                        className="w-full h-full object-cover"
                      >
                        <source src={campaign.videoUrl} type="video/mp4" />
                        <source src={`../assets/${campaign.id === 'c-section' ? 'campaign_c-section_video.mp4' : 'campaign_bariatric_video.mp4'}`} type="video/mp4" />
                        <source src={`/healing-touch-egypt/assets/${campaign.id === 'c-section' ? 'campaign_c-section_video.mp4' : 'campaign_bariatric_video.mp4'}`} type="video/mp4" />
                        متصفحك لا يدعم مشغل الفيديو المباشر.
                      </video>
                    ) : (
                      <div className="w-full h-full relative">
                        <img
                          src={campaign.videoPosterUrl || campaign.heroImageUrl}
                          alt={campaign.videoTitle || campaign.title}
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 bg-[#003527]/50 flex flex-col items-center justify-center text-white p-4 text-center">
                          <button
                            type="button"
                            onClick={() => onOpenLeadModal()}
                            className="w-14 h-14 rounded-full bg-[#059669] hover:bg-[#047857] text-white flex items-center justify-center shadow-lg transition-transform hover:scale-110 active:scale-95 cursor-pointer mb-2"
                            aria-label="مشاهدة شرح الفيديو التفاعلي"
                          >
                            <Play className="w-6 h-6 fill-current translate-x-0.5" />
                          </button>
                          <span className="text-xs font-bold">انقري لطلب فيديو الشرح المباشر لحالتك</span>
                        </div>
                      </div>
                    )}
                    
                    {/* Badge Overlay */}
                    <div className="absolute top-2.5 right-2.5 flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#003527]/90 text-white text-[11px] font-semibold backdrop-blur-xs pointer-events-none">
                      <Clock className="w-3 h-3 text-[#82F5C1]" />
                      <span>{campaign.videoDuration || 'شرح عملي'}</span>
                    </div>
                  </div>

                  {/* Video Title and Caption */}
                  <div className="p-2.5 rounded-xl bg-[#F3F7F5] border border-[#E2ECE6]">
                    <div className="text-xs font-bold text-[#003527] mb-0.5">
                      {campaign.videoTitle || 'شرح سريري معتمد للتعامل مع موضع الجراحة'}
                    </div>
                    <p className="text-[11px] text-[#404944] leading-relaxed">
                      يوضح الفيديو التوضيحي طريقة العزل المائي للضمادات الطبية وكيفية حماية موضع الخياطة من التلوث أثناء الحركة والاستحمام.
                    </p>
                  </div>
                </div>
              )}

              {/* Tab 2: Clean Product Images Showcase */}
              {activeMediaTab === 'gallery' && (
                <div className="p-3.5 space-y-3">
                  
                  {/* Clean Image Frame */}
                  <div className="w-full flex justify-center bg-[#F8FAF9] rounded-2xl p-2 border border-[#E2ECE6]">
                    <div className="relative overflow-hidden rounded-xl bg-white border border-[#E2ECE6] shadow-sm transition-all duration-300 w-full max-h-[380px] aspect-4/3 mx-auto">
                      <img
                        src={currentPhoto?.url}
                        alt={currentPhoto?.title}
                        className="w-full h-full object-cover transition-all duration-300"
                        loading="eager"
                      />

                      {/* Top Badge: Clinical Status */}
                      <div className="absolute top-2.5 right-2.5 flex items-center gap-1.5">
                        <span className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-[#003527]/90 backdrop-blur-md text-white text-[10px] sm:text-[11px] font-bold border border-white/20 shadow-xs">
                          <ShieldCheck className="w-3.5 h-3.5 text-[#82F5C1]" />
                          <span>{currentPhoto?.tag || 'منتج طبي أصلي'}</span>
                        </span>
                      </div>

                      {/* Bottom Description Overlay */}
                      <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/90 via-black/60 to-transparent p-3 sm:p-4 text-white">
                        <div className="text-xs sm:text-sm font-bold leading-snug">
                          {currentPhoto?.title}
                        </div>
                        <div className="text-[11px] text-white/90 line-clamp-2 mt-0.5">
                          {currentPhoto?.subtitle}
                        </div>
                        {currentPhoto?.clinicalFunction && (
                          <div className="text-[10px] text-[#82F5C1] font-semibold mt-1 flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#82F5C1]" />
                            <span>الوظيفة السريرية: {currentPhoto.clinicalFunction}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Thumbnails Row */}
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between text-[11px] text-[#707974]">
                      <span>انقري على أي صورة لمعاينة المستلزمات الطبية:</span>
                      <span className="font-semibold text-[#003527]">
                        {activePhotoIndex + 1} من {allGallery.length}
                      </span>
                    </div>

                    <div className="grid grid-cols-4 sm:grid-cols-5 gap-2 max-h-24 overflow-y-auto p-1">
                      {allGallery.map((item, idx) => {
                        const isSelected = activePhotoIndex === idx;
                        return (
                          <button
                            key={item.id || idx}
                            type="button"
                            onClick={() => setSelectedGalleryIdx(idx)}
                            className={`relative aspect-square rounded-xl overflow-hidden border-2 transition-all cursor-pointer group ${
                              isSelected
                                ? 'border-[#059669] ring-2 ring-[#059669]/40 scale-102 shadow-xs'
                                : 'border-[#E2ECE6] opacity-70 hover:opacity-100'
                            }`}
                          >
                            <img
                              src={item.url}
                              alt={item.title}
                              className="w-full h-full object-cover"
                              loading="lazy"
                            />
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Clinical Utility Note */}
                  <div className="p-2.5 rounded-xl bg-[#F0FDF4] border border-[#DCFCE7] text-xs text-[#065F46] flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 shrink-0 text-[#059669] mt-0.5" />
                    <div>
                      <strong>المعايير السريرية المعتمدة: </strong>
                      <span>مستلزمات طبية أصلية 100% معقمة ومحكمة الغلق لحماية موضع الجراحة من التلوث وتسهيل التعافي الآمن.</span>
                    </div>
                  </div>

                </div>
              )}

              {/* Bottom Quick Action Box inside Media Card */}
              <div className="p-3 bg-[#F8F9FF] border-t border-[#E2ECE6] flex items-center justify-between gap-2">
                <div className="flex items-center gap-1.5 text-xs text-[#003527] font-bold">
                  <Sparkles className="w-3.5 h-3.5 text-[#059669]" />
                  <span>استشارة سريرية مجانية متاحة الآن</span>
                </div>
                <button
                  type="button"
                  onClick={() => onOpenLeadModal()}
                  className="bg-[#064E3B] hover:bg-[#003527] text-white py-2 px-3.5 rounded-xl font-bold text-xs shadow-xs transition-all cursor-pointer active:scale-98"
                >
                  استشيري أخصائية التعافي
                </button>
              </div>

            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
