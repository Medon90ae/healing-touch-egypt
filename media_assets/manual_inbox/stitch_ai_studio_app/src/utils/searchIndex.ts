import { Campaign, CampaignId } from '../types/campaign';

export interface SearchableItem {
  id: string;
  campaignId: CampaignId;
  campaignName: string;
  type: 'article' | 'faq';
  categoryLabel: string;
  title: string;
  snippet: string;
  fullContent: string;
  normalizedTitle: string;
  normalizedContent: string;
  targetElementId: string;
  sectionId?: string;
  faqIndex?: number;
}

export interface SearchResult {
  item: SearchableItem;
  score: number;
  highlightedTitle: string;
  highlightedSnippet: string;
}

/**
 * Normalizes Arabic text by removing diacritics, tatweel, and normalizing letter variants (alef, taa marbuta, yaa).
 */
export function normalizeArabic(text: string): string {
  if (!text) return '';
  return text
    // Remove Arabic diacritics (tashkeel)
    .replace(/[\u064B-\u065F\u0670]/g, '')
    // Remove tatweel (kashida)
    .replace(/\u0640/g, '')
    // Normalize Alef variants (أ, إ, آ, ٱ) -> ا
    .replace(/[أإآٱ]/g, 'ا')
    // Normalize Taa Marbuta (ة) -> ه
    .replace(/ة/g, 'ه')
    // Normalize Alef Maksura (ى) -> ي
    .replace(/ى/g, 'ي')
    // Trim and lower case (for Latin terms like 3M, Tegaderm, BUPY)
    .toLowerCase()
    .trim();
}

/**
 * Builds a search index of all clinical articles and FAQs across all surgical campaigns.
 */
export function buildClinicalSearchIndex(campaigns: Record<CampaignId, Campaign>): SearchableItem[] {
  const items: SearchableItem[] = [];

  Object.values(campaigns).forEach((camp) => {
    // 1. Index Clinical Article Overview & Key Takeaways
    if (camp.article) {
      const takeawaysText = camp.article.keyTakeaways.join(' ');
      const introText = `${camp.article.introduction} ${takeawaysText}`;
      
      items.push({
        id: `article-overview-${camp.id}`,
        campaignId: camp.id,
        campaignName: camp.name,
        type: 'article',
        categoryLabel: 'مقال إكلينيكي • المقدمة والتوصيات',
        title: camp.article.title,
        snippet: camp.article.introduction.slice(0, 150) + '...',
        fullContent: `${camp.article.title} ${introText}`,
        normalizedTitle: normalizeArabic(camp.article.title),
        normalizedContent: normalizeArabic(`${camp.article.title} ${introText}`),
        targetElementId: 'clinical-article',
      });

      // Index Each Section of the Clinical Article
      camp.article.sections.forEach((sec) => {
        const paragraphsText = sec.content.join(' ');
        const calloutText = sec.callout ? `${sec.callout.title} ${sec.callout.text}` : '';
        const sectionFull = `${sec.heading} ${paragraphsText} ${calloutText}`;

        items.push({
          id: `article-sec-${camp.id}-${sec.id}`,
          campaignId: camp.id,
          campaignName: camp.name,
          type: 'article',
          categoryLabel: 'مقال إكلينيكي • محور سريري',
          title: sec.heading.replace(/^\d+\.\s*/, ''),
          snippet: (sec.content[0] || '').slice(0, 160) + '...',
          fullContent: sectionFull,
          normalizedTitle: normalizeArabic(sec.heading),
          normalizedContent: normalizeArabic(sectionFull),
          targetElementId: sec.id,
          sectionId: sec.id,
        });
      });
    }

    // 2. Index FAQs
    if (camp.faqs && camp.faqs.length > 0) {
      camp.faqs.forEach((faq, idx) => {
        items.push({
          id: `faq-${camp.id}-${idx}`,
          campaignId: camp.id,
          campaignName: camp.name,
          type: 'faq',
          categoryLabel: 'سؤال وجواب سريري',
          title: faq.question,
          snippet: faq.answer.slice(0, 160) + '...',
          fullContent: `${faq.question} ${faq.answer}`,
          normalizedTitle: normalizeArabic(faq.question),
          normalizedContent: normalizeArabic(`${faq.question} ${faq.answer}`),
          targetElementId: `faq-${idx}`,
          faqIndex: idx,
        });
      });
    }
  });

  return items;
}

export interface SearchOptions {
  filterType?: 'all' | 'article' | 'faq';
  currentCampaignOnly?: boolean;
  activeCampaignId?: CampaignId;
  limit?: number;
}

/**
 * Searches the clinical knowledge base using normalized token matching and relevance scoring.
 */
export function searchKnowledge(
  index: SearchableItem[],
  rawQuery: string,
  options: SearchOptions = {}
): SearchResult[] {
  const {
    filterType = 'all',
    currentCampaignOnly = false,
    activeCampaignId,
    limit = 10,
  } = options;

  const trimmed = rawQuery.trim();
  if (!trimmed) return [];

  const normalizedQuery = normalizeArabic(trimmed);
  // Split into individual search tokens (filtering out very short words of 1 char)
  const tokens = normalizedQuery.split(/\s+/).filter((t) => t.length > 1);
  if (tokens.length === 0) return [];

  const results: SearchResult[] = [];

  for (const item of index) {
    // Type filter
    if (filterType !== 'all' && item.type !== filterType) {
      continue;
    }

    // Current campaign filter if requested
    if (currentCampaignOnly && activeCampaignId && item.campaignId !== activeCampaignId) {
      continue;
    }

    let score = 0;
    const title = item.normalizedTitle;
    const content = item.normalizedContent;

    // Check exact phrase match in title (highest value)
    if (title.includes(normalizedQuery)) {
      score += 100;
    } else if (content.includes(normalizedQuery)) {
      score += 50;
    }

    // Check token matches
    let matchedTokensCount = 0;
    for (const token of tokens) {
      if (title.includes(token)) {
        score += 25;
        matchedTokensCount++;
      } else if (content.includes(token)) {
        score += 10;
        matchedTokensCount++;
      }
    }

    // If none of the tokens matched, skip this item
    if (matchedTokensCount === 0 && score === 0) {
      continue;
    }

    // Boost score if item matches the user's currently viewed surgical campaign
    if (activeCampaignId && item.campaignId === activeCampaignId) {
      score += 15;
    }

    // Generate relevant snippet and highlights
    const { highlightedSnippet, highlightedTitle } = createHighlights(
      item.title,
      item.fullContent,
      rawQuery,
      tokens
    );

    results.push({
      item,
      score,
      highlightedTitle,
      highlightedSnippet,
    });
  }

  // Sort descending by score
  results.sort((a, b) => b.score - a.score);

  return results.slice(0, limit);
}

/**
 * Helper to safely escape regex characters.
 */
function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Extracts a window around matching terms and applies highlight marks.
 */
function createHighlights(
  originalTitle: string,
  originalContent: string,
  _rawQuery: string,
  tokens: string[]
): { highlightedTitle: string; highlightedSnippet: string } {
  // Title highlighting
  let highlightedTitle = originalTitle;
  tokens.forEach((token) => {
    const pattern = buildArabicFuzzyRegex(token);
    if (pattern) {
      highlightedTitle = highlightedTitle.replace(pattern, (match) => `<mark class="bg-[#82F5C1]/50 text-[#003527] font-semibold px-0.5 rounded">${match}</mark>`);
    }
  });

  // Snippet extraction around the first match
  let snippet = '';
  const firstToken = tokens[0];
  const regex = buildArabicFuzzyRegex(firstToken);
  
  if (regex) {
    const match = regex.exec(originalContent);
    if (match) {
      const matchIndex = match.index;
      const start = Math.max(0, matchIndex - 60);
      const end = Math.min(originalContent.length, matchIndex + 140);
      snippet = (start > 0 ? '...' : '') + originalContent.slice(start, end).trim() + (end < originalContent.length ? '...' : '');
    }
  }

  if (!snippet) {
    snippet = originalContent.slice(0, 160) + '...';
  }

  // Apply highlights to snippet
  let highlightedSnippet = snippet;
  tokens.forEach((token) => {
    const pattern = buildArabicFuzzyRegex(token);
    if (pattern) {
      highlightedSnippet = highlightedSnippet.replace(pattern, (match) => `<mark class="bg-[#82F5C1]/50 text-[#003527] font-semibold px-0.5 rounded">${match}</mark>`);
    }
  });

  return {
    highlightedTitle,
    highlightedSnippet,
  };
}

/**
 * Builds a regex that matches normalized Arabic letters (e.g. matching 'ا', 'أ', 'إ', 'آ').
 */
function buildArabicFuzzyRegex(token: string): RegExp | null {
  if (!token || token.length < 2) return null;

  try {
    const parts = token.split('').map((ch) => {
      if (ch === 'ا' || ch === 'أ' || ch === 'إ' || ch === 'آ') {
        return '[اأإآٱ]';
      }
      if (ch === 'ه' || ch === 'ة') {
        return '[هة]';
      }
      if (ch === 'ي' || ch === 'ى') {
        return '[يى]';
      }
      return escapeRegex(ch);
    });

    return new RegExp(`(${parts.join('')})`, 'gi');
  } catch {
    return null;
  }
}

/**
 * Suggested quick search queries for patients.
 */
export const POPULAR_CLINICAL_SEARCHES = [
  'الاستحمام والمياه',
  'شرائح السيليكون',
  'الكلويد وتضخم الجرح',
  'حكة واحمرار الجرح',
  'إزالة الشاش والضمادة',
  'أشعة الشمس وحماية الندبة',
  'لاصق تجميل الأنف',
  'فتحات المنظار والتكميم',
];
