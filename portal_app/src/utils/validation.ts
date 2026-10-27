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

  // Strip international prefix (0020 or 20)
  if (cleaned.startsWith('0020')) {
    cleaned = cleaned.slice(4);
  } else if (cleaned.startsWith('20')) {
    cleaned = cleaned.slice(2);
  }

  // Ensure standard domestic leading zero (010, 011, 012, 015)
  if (cleaned.startsWith('0')) {
    // Already has leading zero, preserve it
  } else if (cleaned.startsWith('1')) {
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
 * Verifies promo / consultation code validity without commercial pricing.
 */
export function verifyConsultationCode(enteredCode: string): {
  isPromoValid: boolean;
  promoCode: string;
  benefitDescription: string;
} {
  const cleanCode = (enteredCode || '').trim().toUpperCase();
  if (cleanCode === PROMO_CODE_CONFIG.code) {
    return {
      isPromoValid: true,
      promoCode: PROMO_CODE_CONFIG.code,
      benefitDescription: 'كود HT10 مفعل: استشارة سريرية مجانية + حق فتح ومعاينة الشحنة قبل الاستلام'
    };
  }

  return {
    isPromoValid: false,
    promoCode: cleanCode,
    benefitDescription: ''
  };
}

/**
 * Submits triage lead data to the Google Sheets Webhook via POST with mode: 'no-cors'.
 * Zero commercial pricing or calculations.
 */
export async function submitLeadToGoogleSheet(data: LeadSubmissionData): Promise<{ success: boolean; error?: string }> {
  try {
    const normPhone = normalizeEgyptianPhone(data.phone);
    const contextTopic = `${data.surgeryType || data.campaignName || 'استشارة سريرية'} - ${data.daysPostOp || 'مرحلة التعافي'} - ${data.governorate} - ${data.inquiryNotes || data.notes || ''}`;
    const pageUrl = data.sourceUrl || (typeof window !== 'undefined' ? window.location.href : '');

    const payload = {
      // Keys expected by Google Apps Script Webhook
      patient_name: data.fullName,
      patient_phone: normPhone,
      context_topic: contextTopic,
      channel: data.source || 'whatsapp',
      promo_code: data.promoCode || 'HT10',
      page_url: pageUrl,

      // Standard aliases for compatibility
      name: data.fullName,
      fullName: data.fullName,
      client_name: data.fullName,
      phone: normPhone,
      client_phone: normPhone,
      topic: contextTopic,

      // Clinical Triage Fields
      surgery_type: data.surgeryType || data.campaignName || '',
      days_post_op: data.daysPostOp || '',
      governorate: data.governorate,
      inquiry_notes: data.inquiryNotes || data.notes || '',
      address: data.address || '',
      source: data.source || 'lead_modal',
      timestamp: data.timestamp || new Date().toISOString()
    };

    // 1. Try navigator.sendBeacon for instant non-blocking delivery that survives redirects
    if (typeof navigator !== 'undefined' && navigator.sendBeacon) {
      try {
        const blob = new Blob([JSON.stringify(payload)], { type: 'text/plain' });
        navigator.sendBeacon(WEBHOOK_URL, blob);
      } catch (beaconErr) {
        console.warn('sendBeacon delivery fallback:', beaconErr);
      }
    }

    // 2. Also dispatch fetch with no-cors mode
    fetch(WEBHOOK_URL, {
      method: 'POST',
      mode: 'no-cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    }).catch((fetchErr) => {
      console.warn('Background lead fetch error:', fetchErr);
    });

    return { success: true };
  } catch (err: unknown) {
    console.error('Lead webhook submission error:', err);
    return { success: true };
  }
}

/**
 * Asynchronously logs search queries to the Google Sheet webhook via beacon/fetch
 * without blocking navigation or modal flow.
 */
export function logSearchInquiryToBeacon(searchQuery: string, campaignName?: string): void {
  if (!searchQuery.trim()) return;
  const pageUrl = typeof window !== 'undefined' ? window.location.href : '';
  const payload = {
    patient_name: 'استفسار بحث سريري فوري',
    patient_phone: '',
    context_topic: `بحث فوري: "${searchQuery.trim()}" (${campaignName || 'المنظومة السريرية'})`,
    channel: 'search_bar',
    promo_code: 'HT10',
    page_url: pageUrl,
    topic: `بحث فوري: "${searchQuery.trim()}"`,
    inquiry_notes: searchQuery.trim(),
    source: 'search_bar',
    timestamp: new Date().toISOString()
  };

  if (typeof navigator !== 'undefined' && navigator.sendBeacon) {
    try {
      const blob = new Blob([JSON.stringify(payload)], { type: 'text/plain' });
      navigator.sendBeacon(WEBHOOK_URL, blob);
      return;
    } catch {
      // fallback to fetch
    }
  }

  try {
    fetch(WEBHOOK_URL, {
      method: 'POST',
      mode: 'no-cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    }).catch(() => {});
  } catch {}
}

/**
 * Builds the WhatsApp clinical triage handoff link.
 * Strictly adheres to the zero-commerce clinical triage template.
 */
export function buildWhatsAppRedirectUrl(data: LeadSubmissionData): string {
  const normPhone = normalizeEgyptianPhone(data.phone);
  const arabicText = [
    `مرحباً أخصائية التعافي الطبي في هيلينج تاتش مصر،`,
    `أود استشارة سريرية بخصوص حالتي:`,
    `▪️ الاسم: ${data.fullName}`,
    `▪️ رقم الهاتف: ${normPhone}`,
    `▪️ نوع العملية: ${data.surgeryType || data.campaignName || 'استشارة عامة'}`,
    `▪️ مرحلة الجرح / الأيام بعد العملية: ${data.daysPostOp || 'غير محدد'}`,
    `▪️ المحافظة: ${data.governorate}`,
    data.inquiryNotes ? `▪️ تفاصيل الاستفسار: ${data.inquiryNotes}` : (data.notes ? `▪️ تفاصيل الاستفسار: ${data.notes}` : '▪️ تفاصيل الاستفسار: طلب إرشادات العناية بالتعافي وتحديد المقاسات المناسبة'),
    `\nأرجو التواصل لتحديد بروتوكول العناية والمتابعة السريرية.`
  ]
    .filter(Boolean)
    .join('\n');

  return `https://wa.me/${WHATSAPP_RECOVERY_NUMBER}?text=${encodeURIComponent(arabicText)}`;
}
