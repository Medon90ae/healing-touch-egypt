export type CampaignId = 'c-section' | 'rhinoplasty' | 'bariatric' | 'thyroid';

export interface Product {
  id: string;
  name: string;
  brand: string;
  badge: string;
  specification: string;
  description: string;
  clinicalBenefit: string;
  priceEGP: number;
  originalPriceEGP: number;
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
  priceEGP: number;
  originalPriceEGP: number;
  items: string[];
  badge: string;
  savingsText: string;
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
  fullName: string;
  phone: string;
  governorate: string;
  address?: string;
  notes?: string;
  campaignId: CampaignId;
  campaignName: string;
  bundleId: string;
  bundleTitle: string;
  priceEGP: number;
  finalPriceEGP: number;
  discountApplied: number;
  promoCode: string;
  sourceUrl: string;
  timestamp: string;
}
