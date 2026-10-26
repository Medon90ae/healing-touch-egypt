export interface ProductItem {
  id: string;
  phaseNumber: number;
  phaseNameAr: string;
  titleAr: string;
  taglineAr: string;
  descriptionAr: string;
  priceEGP: number;
  originalPriceEGP: number;
  dimensions?: string;
  packCount: string;
  benefits: string[];
  usageInstructions: string[];
  medicalSpecs: string[];
  inKit: boolean;
  featured?: boolean;
}

export interface RecoveryStage {
  stageNumber: number;
  titleAr: string;
  daysRangeAr: string;
  objectiveAr: string;
  careDetailsAr: string;
  showerStatusAr: string;
  recommendedProductId: string;
}

export interface CartItem {
  product: ProductItem;
  quantity: number;
}

export type PaymentMethod = 'cod' | 'instapay';

export interface Governorate {
  id: string;
  nameAr: string;
  shippingFeeEGP: number;
  deliveryDaysAr: string;
}

export interface Order {
  id: string;
  orderNumber: string;
  customerName: string;
  phone: string;
  governorate: string;
  address: string;
  notes?: string;
  paymentMethod: PaymentMethod;
  items: {
    productId: string;
    titleAr: string;
    quantity: number;
    priceEGP: number;
  }[];
  subtotalEGP: number;
  shippingFeeEGP: number;
  discountEGP: number;
  totalEGP: number;
  createdAt: string;
  status: 'confirmed' | 'processing' | 'shipped';
  estimatedDeliveryAr: string;
}

export interface AssessmentInput {
  daysPostOp: number;
  closureType: 'cosmetic_glue' | 'internal_sutures' | 'staples' | 'traditional';
  dressingStatus: 'hospital_dressing' | 'removed_clean' | 'slight_redness' | 'active_leak';
  painOrTension: 'mild' | 'moderate' | 'severe';
}

export interface AssessmentResult {
  currentPhase: number;
  showerSafety: 'safe_with_shield' | 'consult_doctor_first' | 'mature_healing';
  headlineAr: string;
  guidanceAr: string;
  showerProtocolAr: string[];
  warningNoteAr?: string;
  recommendedKitId: string;
}
