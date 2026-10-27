import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  Search,
  X,
  BookOpen,
  HelpCircle,
  ArrowLeft,
  Sparkles,
  Command,
  Filter,
  Check,
  MessageSquare
} from 'lucide-react';
import { CampaignId } from '../types/campaign';
import { CAMPAIGNS, WHATSAPP_RECOVERY_NUMBER } from '../data/campaignConfig';
import {
  buildClinicalSearchIndex,
  searchKnowledge,
  SearchableItem,
  SearchResult,
  POPULAR_CLINICAL_SEARCHES
} from '../utils/searchIndex';

interface SearchBarProps {
  activeCampaignId: CampaignId;
  onNavigateToResult: (params: {
    campaignId: CampaignId;
    targetElementId: string;
    sectionId?: string;
    faqIndex?: number;
  }) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  activeCampaignId,
  onNavigateToResult,
}) => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [filterType, setFilterType] = useState<'all' | 'article' | 'faq'>('all');
  const [currentCampaignOnly, setCurrentCampaignOnly] = useState(false);
  
  const searchContainerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Pre-build searchable index across all campaigns
  const searchIndex = useMemo(() => buildClinicalSearchIndex(CAMPAIGNS), []);

  // Compute search results
  const results: SearchResult[] = useMemo(() => {
    if (!query.trim()) return [];
    return searchKnowledge(searchIndex, query, {
      filterType,
      currentCampaignOnly,
      activeCampaignId,
      limit: 12,
    });
  }, [searchIndex, query, filterType, currentCampaignOnly, activeCampaignId]);

  // Counts for filters
  const counts = useMemo(() => {
    if (!query.trim()) return { all: 0, article: 0, faq: 0 };
    const allResults = searchKnowledge(searchIndex, query, {
      filterType: 'all',
      currentCampaignOnly,
      activeCampaignId,
      limit: 100,
    });
    return {
      all: allResults.length,
      article: allResults.filter((r) => r.item.type === 'article').length,
      faq: allResults.filter((r) => r.item.type === 'faq').length,
    };
  }, [searchIndex, query, currentCampaignOnly, activeCampaignId]);

  // Keyboard shortcut listener (Ctrl+K or ⌘K, or / when not typing)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsOpen(true);
        setTimeout(() => inputRef.current?.focus(), 50);
      } else if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
        inputRef.current?.blur();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  // Click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        searchContainerRef.current &&
        !searchContainerRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  const handleSelectResult = (item: SearchableItem) => {
    onNavigateToResult({
      campaignId: item.campaignId,
      targetElementId: item.targetElementId,
      sectionId: item.sectionId,
      faqIndex: item.faqIndex,
    });
    setIsOpen(false);
  };

  const handleQuickSearch = (keyword: string) => {
    setQuery(keyword);
    setIsOpen(true);
    inputRef.current?.focus();
  };

  const handleDirectWhatsAppConsultation = (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    const activeName = CAMPAIGNS[activeCampaignId]?.name || 'موسوعة التعافي';
    const text = `مرحباً، أود استشارة أخصائية التعافي في هيلينج تاتش بخصوص: "${searchQuery.trim()}" (${activeName}).`;
    const url = `https://wa.me/${WHATSAPP_RECOVERY_NUMBER}?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank');
    setIsOpen(false);
  };

  const activeCampaignName = CAMPAIGNS[activeCampaignId]?.name || 'الجراحة الحالية';

  return (
    <div ref={searchContainerRef} className="relative w-full">
      {/* Search Bar Input Container */}
      <div
        className={`relative flex items-center bg-white rounded-xl border transition-all duration-200 shadow-2xs ${
          isOpen
            ? 'border-[#059669] ring-2 ring-[#059669]/20 shadow-md'
            : 'border-[#E2ECE6] hover:border-[#80BEA6]'
        }`}
      >
        <div className="flex items-center pl-3 pr-3 text-[#059669] pointer-events-none">
          <Search className="w-4 h-4 sm:w-5 sm:h-5 text-[#059669]" />
        </div>

        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            if (!isOpen) setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              if (query.trim()) {
                handleDirectWhatsAppConsultation(query.trim());
              }
            }
          }}
          placeholder="ابحث في المقالات الإكلينيكية، الاستحمام، السيليكون، والأسئلة الشائعة..."
          className="w-full py-2.5 sm:py-3 text-xs sm:text-sm text-[#121C2A] placeholder-[#707974] bg-transparent outline-none pr-1 pl-2"
          aria-label="بحث محلي في المقالات والأسئلة الشائعة"
        />

        {/* Clear, Consultation or Shortcut badges */}
        <div className="flex items-center gap-1.5 pl-3 pr-1">
          {query.trim() && (
            <button
              type="button"
              onClick={() => handleDirectWhatsAppConsultation(query.trim())}
              className="flex items-center gap-1 bg-[#059669] hover:bg-[#047857] text-white text-[11px] sm:text-xs font-bold px-2.5 sm:px-3 py-1.5 rounded-lg shadow-2xs transition-all cursor-pointer active:scale-95 shrink-0"
              title="تأكيد البحث والتحويل لاستشارة واتساب فوراً"
            >
              <MessageSquare className="w-3.5 h-3.5 text-[#82F5C1]" />
              <span className="hidden sm:inline">اسألي واتساب</span>
              <span className="sm:hidden">واتساب</span>
            </button>
          )}

          {query ? (
            <button
              type="button"
              onClick={() => {
                setQuery('');
                inputRef.current?.focus();
              }}
              className="p-1 rounded-md text-[#707974] hover:text-[#121C2A] hover:bg-[#F3F7F5] transition-colors"
              aria-label="مسح نص البحث"
            >
              <X className="w-4 h-4" />
            </button>
          ) : (
            <div className="hidden sm:flex items-center gap-1 px-2 py-1 rounded-md bg-[#F3F7F5] border border-[#E2ECE6] text-[10px] font-mono text-[#707974]">
              <Command className="w-3 h-3" />
              <span>K</span>
            </div>
          )}
        </div>
      </div>

      {/* Dropdown Flyout Panel */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl border border-[#E2ECE6] shadow-xl z-50 overflow-hidden max-h-[80vh] flex flex-col animate-fade-in-up">
          
          {/* Prominent Direct WhatsApp Consultation Banner (Visible when typing) */}
          {query.trim() && (
            <div
              onClick={() => handleDirectWhatsAppConsultation(query.trim())}
              className="p-3 sm:p-4 bg-gradient-to-r from-[#E6F4F1] via-[#DCFCE7] to-[#E6EEFF] border-b border-[#82F5C1] flex items-center justify-between gap-3 cursor-pointer hover:bg-[#D1FAE5] transition-all group"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[#059669] text-white flex items-center justify-center shrink-0 shadow-md group-hover:scale-105 transition-transform">
                  <MessageSquare className="w-5 h-5 text-[#82F5C1]" />
                </div>
                <div>
                  <div className="text-xs sm:text-sm font-bold text-[#003527] flex items-center gap-2">
                    <span>استشارة فورية بخصوص: "{query.trim()}"</span>
                    <span className="text-[10px] bg-[#059669] text-white px-2 py-0.5 rounded-full font-bold animate-pulse">
                      واتساب متاح الآن
                    </span>
                  </div>
                  <div className="text-[11px] sm:text-xs text-[#065F46] mt-0.5">
                    اضغطي هنا لنقل سؤالك مباشرة إلى أخصائية التعافي والإجابة المعتمدة فوراً
                  </div>
                </div>
              </div>
              <div className="inline-flex items-center gap-1.5 text-xs font-bold text-white bg-[#064E3B] group-hover:bg-[#003527] px-3.5 py-2 rounded-xl shadow-xs transition-all shrink-0">
                <span>تأكيد وسؤال واتساب</span>
                <ArrowLeft className="w-3.5 h-3.5 rtl:rotate-0" />
              </div>
            </div>
          )}
          {/* Filter Bar & Scope Switcher */}
          <div className="p-3 sm:p-4 bg-[#F8F9FF] border-b border-[#E2ECE6] flex flex-wrap items-center justify-between gap-2 text-xs">
            {/* Type Filter Chips */}
            <div className="flex items-center gap-1.5">
              <span className="text-[#404944] font-semibold hidden md:inline ml-1 flex items-center gap-1">
                <Filter className="w-3.5 h-3.5 text-[#059669]" />
                التصنيف:
              </span>
              <button
                type="button"
                onClick={() => setFilterType('all')}
                className={`px-3 py-1 rounded-full font-medium transition-colors ${
                  filterType === 'all'
                    ? 'bg-[#003527] text-white shadow-xs'
                    : 'bg-white text-[#404944] hover:bg-[#E2ECE6] border border-[#E2ECE6]'
                }`}
              >
                الكل {counts.all > 0 ? `(${counts.all})` : ''}
              </button>
              <button
                type="button"
                onClick={() => setFilterType('article')}
                className={`px-3 py-1 rounded-full font-medium transition-colors flex items-center gap-1 ${
                  filterType === 'article'
                    ? 'bg-[#003527] text-white shadow-xs'
                    : 'bg-white text-[#404944] hover:bg-[#E2ECE6] border border-[#E2ECE6]'
                }`}
              >
                <BookOpen className="w-3 h-3 text-[#059669]" />
                المقالات السريرية {counts.article > 0 ? `(${counts.article})` : ''}
              </button>
              <button
                type="button"
                onClick={() => setFilterType('faq')}
                className={`px-3 py-1 rounded-full font-medium transition-colors flex items-center gap-1 ${
                  filterType === 'faq'
                    ? 'bg-[#003527] text-white shadow-xs'
                    : 'bg-white text-[#404944] hover:bg-[#E2ECE6] border border-[#E2ECE6]'
                }`}
              >
                <HelpCircle className="w-3 h-3 text-[#059669]" />
                الأسئلة الشائعة {counts.faq > 0 ? `(${counts.faq})` : ''}
              </button>
            </div>

            {/* Surgery Scope Switcher */}
            <button
              type="button"
              onClick={() => setCurrentCampaignOnly(!currentCampaignOnly)}
              className={`text-xs px-2.5 py-1 rounded-lg border transition-all flex items-center gap-1.5 cursor-pointer ${
                currentCampaignOnly
                  ? 'bg-[#E6EEFF] text-[#003527] border-[#059669] font-semibold'
                  : 'bg-white text-[#707974] border-[#E2ECE6] hover:bg-[#F3F7F5]'
              }`}
            >
              <span className={`w-3.5 h-3.5 rounded flex items-center justify-center border ${currentCampaignOnly ? 'bg-[#059669] border-[#059669] text-white' : 'border-[#707974]'}`}>
                {currentCampaignOnly && <Check className="w-2.5 h-2.5" />}
              </span>
              <span>بحث في ({activeCampaignName}) فقط</span>
            </button>
          </div>

          {/* Results List or Suggestions */}
          <div className="overflow-y-auto max-h-[60vh] p-2 sm:p-3 divide-y divide-[#E2ECE6]/60">
            {/* If Query is empty: Show popular suggestions */}
            {!query.trim() && (
              <div className="p-4 sm:p-5">
                <div className="flex items-center gap-2 mb-3 text-xs font-bold text-[#003527]">
                  <Sparkles className="w-4 h-4 text-[#FF9939]" />
                  <span>الموضوعات والاستفسارات الأكثر بحثاً من المرضى:</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {POPULAR_CLINICAL_SEARCHES.map((keyword, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => handleQuickSearch(keyword)}
                      className="px-3 py-1.5 rounded-lg bg-[#F3F7F5] hover:bg-[#E6EEFF] text-[#003527] text-xs font-medium border border-[#E2ECE6] hover:border-[#82F5C1] transition-all flex items-center gap-1.5 cursor-pointer"
                    >
                      <Search className="w-3 h-3 text-[#059669]" />
                      <span>{keyword}</span>
                    </button>
                  ))}
                </div>
                <p className="mt-4 text-xs text-[#707974] leading-relaxed">
                  اكتب أي كلمة طبية مثل "تجميل"، "الاستحمام"، "السيليكون"، "تضخم الندبة"، أو "الشاش" للوصول الفوري للمعلومة المعتمدة.
                </p>
              </div>
            )}

            {/* If Query entered but no results */}
            {query.trim() && results.length === 0 && (
              <div className="p-8 text-center text-[#707974]">
                <HelpCircle className="w-10 h-10 text-[#707974]/60 mx-auto mb-3" />
                <h4 className="text-sm font-bold text-[#121C2A] mb-1">
                  لم يتم العثور على نتائج تطابق "{query}"
                </h4>
                <p className="text-xs text-[#404944] max-w-sm mx-auto mb-4">
                  جرّب البحث بكلمات أخرى مثل "استحمام"، "سيليكون"، "شاش"، أو اختر من المقترحات الشائعة:
                </p>
                <div className="flex flex-wrap justify-center gap-2">
                  {POPULAR_CLINICAL_SEARCHES.slice(0, 4).map((keyword, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => handleQuickSearch(keyword)}
                      className="px-2.5 py-1 rounded-md bg-[#F3F7F5] text-[#003527] text-xs hover:bg-[#E6EEFF] transition-colors"
                    >
                      {keyword}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Search Results Display */}
            {results.map(({ item, highlightedTitle, highlightedSnippet }) => {
              const isDifferentCampaign = item.campaignId !== activeCampaignId;
              const isArticle = item.type === 'article';

              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => handleSelectResult(item)}
                  className="w-full text-right p-3 sm:p-4 rounded-xl hover:bg-[#F3F7F5] transition-all cursor-pointer group flex flex-col gap-1.5 focus:outline-none focus:bg-[#F3F7F5]"
                >
                  {/* Item Badges */}
                  <div className="flex items-center justify-between gap-2 text-[11px]">
                    <div className="flex items-center gap-2">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-semibold ${
                          isArticle
                            ? 'bg-[#E6EEFF] text-[#003527] border border-[#D0DBED]'
                            : 'bg-[#DCFCE7] text-[#006C4A] border border-[#82F5C1]'
                        }`}
                      >
                        {isArticle ? (
                          <BookOpen className="w-3 h-3 text-[#059669]" />
                        ) : (
                          <HelpCircle className="w-3 h-3 text-[#059669]" />
                        )}
                        <span>{item.categoryLabel}</span>
                      </span>

                      {/* Surgical Campaign Tag */}
                      <span className="text-[#404944] font-medium flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-[#059669]" />
                        {item.campaignName}
                        {isDifferentCampaign && (
                          <span className="text-[10px] text-[#D97706] font-semibold bg-[#FFDCC3]/40 px-1.5 py-0.2 rounded">
                            تبديل الجراحة
                          </span>
                        )}
                      </span>
                    </div>

                    <span className="text-xs text-[#059669] font-medium hidden sm:inline-flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <span>انتقال سريع</span>
                      <ArrowLeft className="w-3.5 h-3.5" />
                    </span>
                  </div>

                  {/* Title with Highlights */}
                  <h4
                    className="font-bold text-sm sm:text-base text-[#003527] group-hover:text-[#059669] transition-colors leading-snug"
                    dangerouslySetInnerHTML={{ __html: highlightedTitle }}
                  />

                  {/* Context Snippet with Highlights */}
                  <p
                    className="text-xs sm:text-sm text-[#404944] line-clamp-2 leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: highlightedSnippet }}
                  />
                </button>
              );
            })}
          </div>

          {/* Bottom Footer Info */}
          <div className="p-2.5 sm:p-3 bg-[#F8F9FF] border-t border-[#E2ECE6] flex items-center justify-between text-xs text-[#707974]">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#82F5C1]" />
              <span>بحث محلي فوري وآمن يغطي كافة البروتوكولات والأسئلة الشائعة</span>
            </div>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="text-[#059669] hover:underline font-medium cursor-pointer"
            >
              إغلاق [Esc]
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
