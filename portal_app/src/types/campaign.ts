export type CampaignId = 'c-section' | 'rhinoplasty' | 'bariatric' | 'thyroid';

export interface Product {
  id: string;
  name: string;
  brand: string;
  badge: string;
  specification: string;
  description: string;
  clinicalBenefit: string;
  features: string[];
  imageUrl: string;
  galleryImages: string[];
}

export interface Bundle {
  id: string;
  title: string;
  subtitle: string;
  tag: string;
  isPopular?: boolean;
  clinicalSynergy: string;
  items: string[];
  badge: string;
  imageUrl: string;
  galleryImages: string[];
}

export interface CalculatorQuestionOption {
  label: string;
  score: number;
  advice: string;
}

export interface CalculatorQuestion {
  id: string;
  label: string;
  description: string;
  options: CalculatorQuestionOption[];
}

export interface CalculatorRecommendation {
  status: 'ready' | 'caution' | 'early';
  badge: string;
  headline: string;
  clinicalAdvice: string;
  recommendedBundleId: string;
  protocolSteps: string[];
}

export interface ClinicalFAQ {
  question: string;
  answer: string;
}

export interface ClinicalEndorsement {
  doctorName: string;
  title: string;
  hospital: string;
  statement: string;
  seal: string;
}

export interface Review {
  author: string;
  location: string;
  procedure: string;
  stars: number;
  comment: string;
  timeAgo: string;
  verified: boolean;
}

export interface ClinicalArticleCallout {
  type: 'caution' | 'tip' | 'quote';
  title: string;
  text: string;
}

export interface ClinicalArticleSection {
  id: string;
  heading: string;
  content: string[];
  callout?: ClinicalArticleCallout;
}

export interface ClinicalArticleData {
  title: string;
  readTimeMinutes: number;
  reviewerDoctor: string;
  lastReviewedDate: string;
  introduction: string;
  sections: ClinicalArticleSection[];
  keyTakeaways: string[];
}

export interface EvidenceStudy {
  id: string;
  source: string;
  journal: string;
  procedure: string;
  sampleSize: string;
  finding: string;
  statHighlight: string;
  pmid: string;
  evidenceGrade: string;
}

export interface GalleryProductImage {
  id?: string;
  url: string;
  title: string;
  subtitle: string;
  clinicalFunction?: string;
  tag?: string;
}

export interface Campaign {
  id: CampaignId;
  name: string;
  slug: string;
  title: string;
  subtitle: string;
  surgicalArea: string;
  heroBadge: string;
  heroHighlights: string[];
  heroImageUrl: string;
  videoUrl?: string;
  videoPosterUrl?: string;
  videoTitle?: string;
  videoDuration?: string;
  galleryImages?: GalleryProductImage[];
  primaryRecommendation: string;
  protocolDescription: string;
  products: Product[];
  bundles: Bundle[];
  article: ClinicalArticleData;
  scientificStudies: EvidenceStudy[];
  calculator: {
    title: string;
    subtitle: string;
    metricName: string;
    questions: CalculatorQuestion[];
    getRecommendation: (answers: Record<string, number>) => CalculatorRecommendation;
  };
  timeline: {
    phase: string;
    weekRange: string;
    title: string;
    action: string;
    tip: string;
  }[];
  faqs: ClinicalFAQ[];
  doctorEndorsement: ClinicalEndorsement;
  reviews: Review[];
}

export interface LeadSubmissionData {
  fullName: string;            // Min 2 characters
  phone: string;               // 11 Egyptian digits (01...)
  surgeryType: string;         // C-section, rhinoplasty, bariatric, thyroidectomy
  daysPostOp: string;          // Days elapsed since surgery / recovery stage
  governorate: string;         // Egyptian governorate
  inquiryNotes: string;        // Specific question or symptom
  timestamp: string;           // ISO 8601
  source: 'lead_modal' | 'search_bar' | 'consultation_button';
  campaignId?: CampaignId;
  campaignName?: string;
  bundleId?: string;
  bundleTitle?: string;
  address?: string;
  notes?: string;
  promoCode?: string;
  sourceUrl?: string;
}
