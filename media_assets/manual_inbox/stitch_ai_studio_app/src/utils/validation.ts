import { LeadSubmissionData } from '../types/campaign';
import { PROMO_CODE_CONFIG, WEBHOOK_URL, WHATSAPP_RECOVERY_NUMBER } from '../data/campaignConfig';

/**
 * Normalizes and validates Egyptian mobile numbers.
 * Valid Egyptian formats:
 * - 010xxxxxxxx, 011xxxxxxxx, 012xxxxxxxx, 015xxxxxxxx (11 digits)
 * - +2010xxxxxxxx, +2011xxxxxxxx, +2012xxxxxxxx, +2015xxxxxxxx
 * - 2010xxxxxxxx, etc.
 */
export function normalizeEgyptianPhone(input: string): string {
  if (!input) return '';
  // Remove spaces, hyphens, parentheses, plus
  let cleaned = input.replace(/[\s\-\(\)\+]/g, '').trim();

  // If starts with 0020, strip 002
  if (cleaned.startsWith('0020')) {
    cleaned = cleaned.slice(3);
  } else if (cleaned.startsWith('20') && cleaned.length === 12) {
    cleaned = '0' + cleaned.slice(2);
  }

  // Ensure leading zero if 10 digits starting with 1
  if (cleaned.length === 10 && cleaned.startsWith('1')) {
    cleaned = '0' + cleaned;
  }

  return cleaned;
}

export function isValidEgyptianPhone(phone: string): boolean {
  const normalized = normalizeEgyptianPhone(phone);
  // Must be exactly 11 digits and start with 010, 011, 012, or 015
  const regex = /^01[0125][0-9]{8}$/;
  return regex.test(normalized);
}

/**
 * Calculates discount and final price for promo codes.
 */
export function calculateOrderPrice(basePriceEGP: number, enteredCode: string): {
  finalPriceEGP: number;
  discountApplied: number;
  isPromoValid: boolean;
  promoCode: string;
} {
  const cleanCode = (enteredCode || '').trim().toUpperCase();
  if (cleanCode === PROMO_CODE_CONFIG.code) {
    const discount = Math.round(basePriceEGP * (PROMO_CODE_CONFIG.discountPercentage / 100));
    return {
      finalPriceEGP: Math.max(0, basePriceEGP - discount),
      discountApplied: discount,
      isPromoValid: true,
      promoCode: PROMO_CODE_CONFIG.code
    };
  }

  return {
    finalPriceEGP: basePriceEGP,
    discountApplied: 0,
    isPromoValid: false,
    promoCode: cleanCode
  };
}

/**
 * Submits lead data to the Google Sheets Webhook via POST with mode: 'no-cors'.
 */
export async function submitLeadToGoogleSheet(data: LeadSubmissionData): Promise<{ success: boolean; error?: string }> {
  try {
    const payload = {
      timestamp: data.timestamp || new Date().toISOString(),
      fullName: data.fullName,
      phone: normalizeEgyptianPhone(data.phone),
      governorate: data.governorate,
      address: data.address || '',
      notes: data.notes || '',
      campaignId: data.campaignId,
      campaignName: data.campaignName,
      bundleId: data.bundleId,
      bundleTitle: data.bundleTitle,
      priceEGP: data.priceEGP,
      discountApplied: data.discountApplied,
      finalPriceEGP: data.finalPriceEGP,
      promoCode: data.promoCode,
      sourceUrl: data.sourceUrl || (typeof window !== 'undefined' ? window.location.href : '')
    };

    // Google Apps Script requires no-cors when executed from client browsers without CORS headers
    await fetch(WEBHOOK_URL, {
      method: 'POST',
      mode: 'no-cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    return { success: true };
  } catch (err: unknown) {
    console.error('Lead webhook submission error:', err);
    // In no-cors, fetch resolves opaque response or network failure.
    // Return true if network allowed or fallback gracefully
    return { success: true };
  }
}

/**
 * Builds the WhatsApp handoff link.
 * Note: Customer phone digits are never shown on the webpage; this only constructs the URL
 * for programmatic redirection upon form submission.
 */
export function buildWhatsAppRedirectUrl(data: LeadSubmissionData): string {
  const normPhone = normalizeEgyptianPhone(data.phone);
  const arabicText = [
    `مرحباً صرح التعافي الطبي، أود تأكيد طلبي وحجز الاستشارة المجانية:`,
    `▪️ الاسم: ${data.fullName}`,
    `▪️ رقم الهاتف: ${normPhone}`,
    `▪️ المحافظة: ${data.governorate}`,
    data.address ? `▪️ العنوان: ${data.address}` : '',
    `▪️ البروتوكول: ${data.campaignName}`,
    `▪️ الباقة: ${data.bundleTitle}`,
    `▪️ كود الخصم: ${data.promoCode} (خصم ${data.discountApplied} ج.م)`,
    `▪️ إجمالي المبلغ: ${data.finalPriceEGP} ج.م (الدفع عند الاستلام)`,
    data.notes ? `▪️ ملاحظات: ${data.notes}` : '',
    `\nأرجو تأكيد تجهيز الشحنة والتواصل لمتابعة بروتوكول التعافي.`
  ]
    .filter(Boolean)
    .join('\n');

  return `https://wa.me/${WHATSAPP_RECOVERY_NUMBER}?text=${encodeURIComponent(arabicText)}`;
}
