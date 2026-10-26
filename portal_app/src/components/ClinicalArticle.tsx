import React, { useState } from 'react';
import { 
  BookOpen, 
  Clock, 
  UserCheck, 
  AlertTriangle, 
  Lightbulb, 
  Quote, 
  ChevronDown, 
  ChevronUp, 
  Bookmark, 
  CheckCircle2,
  FileText
} from 'lucide-react';
import { ClinicalArticleData } from '../types/campaign';
import { useInView } from '../hooks/useInView';

interface ClinicalArticleProps {
  article: ClinicalArticleData;
  campaignName: string;
  highlightSectionId?: string | null;
}

export const ClinicalArticle: React.FC<ClinicalArticleProps> = ({
  article,
  campaignName,
  highlightSectionId,
}) => {
  const { ref, isInView } = useInView();
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>(() => {
    // Default open all sections for maximum reading authority, but allow collapse
    return article.sections.reduce((acc, sec) => ({ ...acc, [sec.id]: true }), {});
  });

  // Ensure targeted section from search is expanded
  React.useEffect(() => {
    if (highlightSectionId) {
      setExpandedSections((prev) => ({ ...prev, [highlightSectionId]: true }));
    }
  }, [highlightSectionId]);

  const toggleSection = (id: string) => {
    setExpandedSections((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const renderCallout = (callout: NonNullable<ClinicalArticleData['sections'][0]['callout']>) => {
    switch (callout.type) {
      case 'caution':
        return (
          <div className="my-5 p-4 sm:p-5 rounded-2xl bg-[#FFF8F6] border-r-4 border-r-[#BA1A1A] border border-[#FFDAD6] text-[#121C2A] shadow-xs">
            <div className="flex items-center gap-2 mb-2 text-[#BA1A1A] font-bold text-sm sm:text-base">
              <AlertTriangle className="w-5 h-5 shrink-0" />
              <span>{callout.title}</span>
            </div>
            <p className="text-xs sm:text-sm text-[#404944] leading-relaxed">
              {callout.text}
            </p>
          </div>
        );
      case 'tip':
        return (
          <div className="my-5 p-4 sm:p-5 rounded-2xl bg-[#F0FDF4] border-r-4 border-r-[#059669] border border-[#DCFCE7] text-[#121C2A] shadow-xs">
            <div className="flex items-center gap-2 mb-2 text-[#059669] font-bold text-sm sm:text-base">
              <Lightbulb className="w-5 h-5 shrink-0 text-[#059669]" />
              <span>{callout.title}</span>
            </div>
            <p className="text-xs sm:text-sm text-[#404944] leading-relaxed">
              {callout.text}
            </p>
          </div>
        );
      case 'quote':
      default:
        return (
          <div className="my-5 p-4 sm:p-5 rounded-2xl bg-[#EFF4FF] border-r-4 border-r-[#003527] border border-[#DEE9FC] text-[#121C2A] shadow-xs">
            <div className="flex items-center gap-2 mb-2 text-[#003527] font-bold text-sm sm:text-base">
              <Quote className="w-5 h-5 shrink-0 text-[#059669]" />
              <span>{callout.title}</span>
            </div>
            <p className="text-xs sm:text-sm text-[#404944] leading-relaxed italic">
              "{callout.text}"
            </p>
          </div>
        );
    }
  };

  return (
    <article
      id="clinical-article"
      ref={ref}
      className="py-12 sm:py-16 bg-white border-b border-[#E2ECE6]"
    >
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Article Meta Header */}
        <header
          className={`transition-all duration-500 mb-8 sm:mb-12 ${
            isInView ? 'animate-fade-in-up opacity-100' : 'opacity-0 translate-y-4'
          }`}
        >
          {/* Section pill */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs sm:text-sm font-semibold mb-3 border border-[#D0DBED]">
            <BookOpen className="w-4 h-4 text-[#059669]" />
            <span>الدليل الإكلينيكي المعتمد • {campaignName}</span>
          </div>

          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#003527] leading-tight sm:leading-snug mb-4">
            {article.title}
          </h2>

          {/* Editorial Credentials bar */}
          <div className="flex flex-wrap items-center gap-y-2 gap-x-4 text-xs sm:text-sm text-[#404944] pb-6 border-b border-[#E2ECE6]">
            <div className="flex items-center gap-1.5 font-semibold text-[#003527]">
              <UserCheck className="w-4 h-4 text-[#059669]" />
              <span>مراجعة وتدقيق طبي: {article.reviewerDoctor}</span>
            </div>
            <span className="hidden sm:inline text-[#BFC9C3]">•</span>
            <div className="flex items-center gap-1 text-[#707974]">
              <Clock className="w-4 h-4" />
              <span>وقت القراءة: {article.readTimeMinutes} دقائق</span>
            </div>
            <span className="hidden sm:inline text-[#BFC9C3]">•</span>
            <div className="flex items-center gap-1 text-[#707974]">
              <FileText className="w-4 h-4" />
              <span>آخر تحديث سريري: {article.lastReviewedDate}</span>
            </div>
          </div>
        </header>

        {/* Executive Summary / Key Takeaways Box */}
        <div
          className={`mb-10 p-5 sm:p-7 rounded-2xl bg-gradient-to-br from-[#F3F7F5] via-[#FBFDFB] to-[#F3F7F5] border-2 border-[#82F5C1] shadow-sm transition-all duration-500 delay-100 ${
            isInView ? 'animate-fade-in-up opacity-100' : 'opacity-0 translate-y-4'
          }`}
        >
          <div className="flex items-center gap-2 mb-3">
            <Bookmark className="w-5 h-5 text-[#059669]" />
            <h3 className="text-base sm:text-lg font-bold text-[#003527]">
              أبرز الخلاصات السريرية والتوصيات المباشرة للتعافي
            </h3>
          </div>
          <p className="text-xs sm:text-sm text-[#404944] mb-4 leading-relaxed">
            وفقاً لتوصيات الجمعية العالمية لعلاج الندبات (International Advisory Panel on Scar Management):
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {article.keyTakeaways.map((takeaway, idx) => (
              <div
                key={idx}
                className="flex items-start gap-2.5 p-3 rounded-xl bg-white border border-[#E2ECE6]"
              >
                <CheckCircle2 className="w-4 h-4 text-[#059669] shrink-0 mt-0.5" />
                <span className="text-xs sm:text-sm text-[#121C2A] font-medium leading-relaxed">
                  {takeaway}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Introduction Narrative */}
        <div className="prose prose-sm sm:prose-base max-w-none mb-10 text-[#121C2A] leading-relaxed">
          <p className="text-sm sm:text-base lg:text-lg text-[#121C2A] leading-loose font-normal bg-[#F8F9FF] p-5 sm:p-6 rounded-2xl border border-[#D9E3F6]">
            {article.introduction}
          </p>
        </div>

        {/* Quick Table of Contents Jump Links */}
        <div className="mb-10 p-4 sm:p-5 rounded-2xl bg-white border border-[#E2ECE6] shadow-2xs">
          <div className="text-xs font-bold text-[#003527] uppercase tracking-wider mb-3">
            فهرس محاور الدليل السريري:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs sm:text-sm">
            {article.sections.map((section, idx) => (
              <a
                key={section.id}
                href={`#${section.id}`}
                className="flex items-center gap-2 p-2 rounded-lg hover:bg-[#F3F7F5] text-[#003527] font-medium transition-colors group"
              >
                <span className="w-5 h-5 rounded-full bg-[#E6EEFF] text-[#003527] text-xs flex items-center justify-center font-bold group-hover:bg-[#059669] group-hover:text-white transition-colors">
                  {idx + 1}
                </span>
                <span className="truncate">{section.heading.replace(/^\d+\.\s*/, '')}</span>
              </a>
            ))}
          </div>
        </div>

        {/* Deep Dive Article Sections */}
        <div className="space-y-8 sm:space-y-12">
          {article.sections.map((section) => {
            const isExpanded = expandedSections[section.id] ?? true;
            const isHighlighted = highlightSectionId === section.id;
            return (
              <section
                key={section.id}
                id={section.id}
                className={`scroll-mt-36 p-6 sm:p-8 rounded-2xl bg-[#FBFDFB] border transition-all duration-300 ${
                  isHighlighted
                    ? 'border-[#059669] ring-4 ring-[#82F5C1]/40 shadow-lg bg-[#F0FDF4]/50'
                    : 'border-[#E2ECE6] shadow-xs hover:border-[#95D3BA]'
                }`}
              >
                <div
                  className="flex items-center justify-between cursor-pointer select-none"
                  onClick={() => toggleSection(section.id)}
                >
                  <h3 className="text-base sm:text-xl font-bold text-[#003527] leading-snug">
                    {section.heading}
                  </h3>
                  <button
                    type="button"
                    className="p-1 rounded-lg text-[#707974] hover:bg-[#E2ECE6]/50 transition-colors"
                    aria-label={isExpanded ? 'طي المحتوى' : 'عرض المحتوى'}
                  >
                    {isExpanded ? (
                      <ChevronUp className="w-5 h-5 text-[#059669]" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-[#059669]" />
                    )}
                  </button>
                </div>

                {isExpanded && (
                  <div className="mt-5 space-y-4 pt-4 border-t border-[#E2ECE6] text-[#404944] text-sm sm:text-base leading-loose animate-fade-in-up">
                    {section.content.map((paragraph, pIdx) => (
                      <p key={pIdx} className="leading-relaxed sm:leading-loose">
                        {paragraph}
                      </p>
                    ))}

                    {/* Integrated Callout Box */}
                    {section.callout && renderCallout(section.callout)}
                  </div>
                )}
              </section>
            );
          })}
        </div>

        {/* Doctor Syndicate Seal */}
        <div className="mt-12 p-4 sm:p-5 rounded-2xl bg-[#F3F7F5] border border-[#D0DBED] flex flex-col sm:flex-row items-center justify-between gap-4 text-xs sm:text-sm text-[#404944]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-[#003527] text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-xs">
              RX
            </div>
            <div>
              <div className="font-bold text-[#003527]">
                هذا المحتوى الطبي خاضع للمعايير التوجيهية العالمية لطب الجراحة والترميم
              </div>
              <div className="text-xs text-[#707974]">
                معد ومراجع سريرياً بواسطة استشاريين مصريين معتمدين بنقابة الأطباء لرفع التوعية الوقائية
              </div>
            </div>
          </div>
          <span className="text-[11px] font-bold text-[#059669] bg-white px-3 py-1 rounded-full border border-[#82F5C1] shrink-0">
            Clinical Peer-Reviewed
          </span>
        </div>
      </div>
    </article>
  );
};
