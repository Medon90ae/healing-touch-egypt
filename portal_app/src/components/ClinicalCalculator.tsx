import React from 'react';
import { Campaign } from '../types/campaign';

interface ClinicalCalculatorProps {
  campaign: Campaign;
  onSelectBundleAndOpenModal?: (bundleId: string) => void;
}

/**
 * @deprecated Clinical Calculator is deprecated per patient safety guidelines (R1).
 * Unverified healing stage calculators have been permanently removed.
 */
export const ClinicalCalculator: React.FC<ClinicalCalculatorProps> = () => {
  return null;
};
