import React, { useState, useEffect } from 'react';
import {
  X,
  ShieldCheck,
  CheckCircle2,
  Lock,
  Loader2,
  Sparkles,
  ArrowLeft,
  Truck,
  MessageSquare
} from 'lucide-react';
import { Campaign, LeadSubmissionData } from '../types/campaign';
import { EGYPTIAN_GOVERNORATES, PROMO_CODE_CONFIG } from '../data/campaignConfig';
import {
  isValidEgyptianPhone,
  calculateOrderPrice,
  submitLeadToGoogleSheet,
  buildWhatsAppRedirectUrl
} from '../utils/validation';

interface LeadGateModalProps {
  isOpen: boolean;
  onClose: () => void;
  campaign: Campaign;
  selectedBundleId?: string;
  onSelectBundleId: (id: string) => void;
}

export const LeadGateModal: React.FC<LeadGateModalProps> = ({
  isOpen,
  onClose,
  campaign,
  selectedBundleId,
  onSelectBundleId
}) => {
  // Form fields
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [governorate, setGovernorate] = useState<string>(EGYPTIAN_GOVERNORATES[0]);
  const [address, setAddress] = useState('');
  const [notes, setNotes] = useState('');
  const [promoCodeInput, setPromoCodeInput] = useState(PROMO_CODE_CONFIG.code);

  // Validation & Submission States
  const [phoneError, setPhoneError] = useState<string | null>(null);
  const [nameError, setNameError] = useState<string | null>(null);
  const [submissionState, setSubmissionState] = useState<'idle' | 'submitting' | 'success'>('idle');
  const [redirectUrl, setRedirectUrl] = useState<string>('');
  const [orderReference, setOrderReference] = useState<string>('');

  // Active bundle selection
  const currentBundle =
    campaign.bundles.find((b) => b.id === selectedBundleId) || campaign.bundles[0];

  const { finalPriceEGP, discountApplied, isPromoValid } = calculateOrderPrice(
    currentBundle.priceEGP,
    promoCodeInput
  );

  // Reset errors when inputs change
  useEffect(() => {
    if (phone && isValidEgyptianPhone(phone)) {
      setPhoneError(null);
    }
  }, [phone]);

  useEffect(() => {
    if (fullName.trim().length >= 3) {
      setNameError(null);
    }
  }, [fullName]);

  // Handle closing modal
  const handleModalClose = () => {
    if (submissionState === 'submitting') return;
    setSubmissionState('idle');
    onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // 1. Strict Validation
    let hasError = false;
    if (!fullName.trim() || fullName.trim().length < 3) {
      setNameError('يرجى كتابة الاسم ثلاثي لتسجيل الفحص الطبي والشحنة');
      hasError = true;
    } else {
      setNameError(null);
    }

    if (!isValidEgyptianPhone(phone)) {
      setPhoneError('يرجى إدخال رقم هاتف محمول مصري صحيح مكون من 11 رقماً (مثال: 010, 011, 012, 015)');
      hasError = true;
    } else {
      setPhoneError(null);
    }

    if (hasError) return;

    // 2. Prepare Lead Data
    setSubmissionState('submitting');
    const orderId = `CS-${Math.floor(100000 + Math.random() * 900000)}`;
    setOrderReference(orderId);

    const leadData: LeadSubmissionData = {
      fullName: fullName.trim(),
      phone: phone.trim(),
      governorate,
      address: address.trim(),
      notes: notes.trim(),
      campaignId: campaign.id,
      campaignName: campaign.name,
      bundleId: currentBundle.id,
      bundleTitle: currentBundle.title,
      priceEGP: currentBundle.priceEGP,
      finalPriceEGP,
      discountApplied,
      promoCode: isPromoValid ? PROMO_CODE_CONFIG.code : promoCodeInput.trim(),
      sourceUrl: typeof window !== 'undefined' ? window.location.href : '',
      timestamp: new Date().toISOString()
    };

    // 3. Build programmatic WhatsApp redirection URL upfront
    const targetWhatsAppUrl = buildWhatsAppRedirectUrl(leadData);
    setRedirectUrl(targetWhatsAppUrl);
    setSubmissionState('success');

    // 4. Background non-blocking lead submission to Google Sheet (using beacon & fetch)
    submitLeadToGoogleSheet(leadData).catch((sheetErr) => {
      console.warn('Background lead submission warning:', sheetErr);
    });

    // 5. Immediate user-initiated redirect to WhatsApp while click event is active
    try {
      const waWin = window.open(targetWhatsAppUrl, '_blank');
      if (!waWin || waWin.closed || typeof waWin.closed === 'undefined') {
        window.location.assign(targetWhatsAppUrl);
      }
    } catch {
      window.location.href = targetWhatsAppUrl;
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-[#003527]/60 backdrop-blur-sm transition-opacity"
        onClick={handleModalClose}
        aria-hidden="true"
      />

      <div className="min-h-full flex items-center justify-center p-3 sm:p-4 text-center">
        <div
          className="relative bg-white rounded-3xl text-right overflow-hidden shadow-2xl transform transition-all w-full max-w-xl border border-[#E2ECE6] my-auto max-h-[92vh] flex flex-col"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-headline"
        >
          {/* Header Banner */}
          <div className="bg-[#064E3B] text-white p-5 sm:p-6 relative shrink-0">
            <button
              type="button"
              onClick={handleModalClose}
              disabled={submissionState === 'submitting'}
              className="absolute left-4 top-4 text-white/80 hover:text-white p-1 rounded-full hover:bg-white/10 transition-colors cursor-pointer"
              aria-label="إغلاق النافذة"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-[#82F5C1] animate-pulse" />
              <span className="text-xs font-semibold text-[#82F5C1]">
                بوابة الحجز والخصوصية الطبية المشفرة
              </span>
            </div>
            <h2 id="modal-headline" className="text-lg sm:text-xl font-bold leading-snug">
              تأكيد الطلب وحجز الاستشارة الطبية مجاناً
            </h2>
            <p className="text-xs text-white/80 mt-1">
              بروتوكول: <strong>{campaign.name}</strong> • الدفع نقدياً عند الاستلام بعد المعاينة
            </p>
          </div>

          {/* Modal Body */}
          <div className="p-5 sm:p-7 overflow-y-auto">
            {submissionState === 'success' ? (
              /* Success / Redirecting Screen (Zero Raw Phone Numbers Visible) */
              <div className="py-8 text-center space-y-5">
                <div className="w-16 h-16 rounded-full bg-[#82F5C1]/30 border-2 border-[#059669] flex items-center justify-center text-[#059669] mx-auto animate-bounce">
                  <CheckCircle2 className="w-10 h-10" />
                </div>

                <div className="space-y-2">
                  <span className="text-xs font-bold text-[#059669] bg-[#E6EEFF] px-3 py-1 rounded-full">
                    رقم الطلب المرجعي: {orderReference}
                  </span>
                  <h3 className="text-xl sm:text-2xl font-bold text-[#003527]">
                    تم تسجيل طلبك وحجز استشارتك بنجاح!
                  </h3>
                  <p className="text-xs sm:text-sm text-[#404944] max-w-md mx-auto leading-relaxed">
                    تم إرسال بياناتك المشفرة لفريق التجهيز السريري. جاري تحويلك الآن تلقائياً لمتابعة التفاصيل وجدول الاستخدام مع أخصائية التعافي...
                  </p>
                </div>

                {/* Prominent Direct WhatsApp Open Button */}
                <div className="pt-2 space-y-3">
                  <a
                    href={redirectUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full inline-flex items-center justify-center gap-2.5 bg-[#059669] hover:bg-[#047857] text-white py-4 px-6 rounded-2xl font-extrabold text-base sm:text-lg shadow-lg shadow-[#059669]/30 transition-all active:scale-98 animate-pulse"
                    aria-label="اضغطي هنا لفتح محادثة واتساب الآن مباشرة"
                  >
                    <MessageSquare className="w-6 h-6 text-[#82F5C1]" />
                    <span>اضغطي هنا لفتح محادثة واتساب الآن مباشرة</span>
                  </a>
                  <p className="text-xs text-[#065F46] font-semibold bg-[#DCFCE7] p-2.5 rounded-xl border border-[#82F5C1]">
                    ✅ تم تسجيل بياناتك بنجاح في السجل الطبي. اضغطي على الزر الأخضر أعلاه لبدء المحادثة الفورية وتأكيد الاستشارة مع أخصائية التعافي.
                  </p>
                </div>
              </div>
            ) : (
              /* Order Form (Strict Zero-Bypass Lead Gate) */
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Bundle Selector */}
                <div>
                  <label htmlFor="bundle-select" className="block text-xs font-bold text-[#003527] mb-1.5">
                    الباقة المختارة:
                  </label>
                  <select
                    id="bundle-select"
                    value={currentBundle.id}
                    onChange={(e) => onSelectBundleId(e.target.value)}
                    className="w-full bg-[#F3F7F5] border border-[#E2ECE6] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm font-semibold text-[#121C2A] focus:outline-none focus:border-[#059669] focus:ring-1 focus:ring-[#059669]"
                  >
                    {campaign.bundles.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.title} — {b.priceEGP} ج.م ({b.tag})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Input: Full Name */}
                <div>
                  <label htmlFor="full-name-input" className="block text-xs font-bold text-[#003527] mb-1">
                    الاسم بالكامل (ثلاثي) <span className="text-[#DC2626]">*</span>
                  </label>
                  <input
                    id="full-name-input"
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="مثال: مريم أحمد الشريف"
                    className={`w-full bg-white border rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#121C2A] focus:outline-none transition-colors ${
                      nameError
                        ? 'border-[#DC2626] ring-1 ring-[#DC2626]'
                        : 'border-[#E2ECE6] focus:border-[#059669] focus:ring-1 focus:ring-[#059669]'
                    }`}
                  />
                  {nameError && (
                    <p className="text-[11px] text-[#DC2626] mt-1 font-medium">{nameError}</p>
                  )}
                </div>

                {/* Input: Egyptian Phone Number */}
                <div>
                  <label htmlFor="phone-input" className="block text-xs font-bold text-[#003527] mb-1">
                    رقم الهاتف المحمول / الواتساب <span className="text-[#DC2626]">*</span>
                  </label>
                  <div className="relative">
                    <input
                      id="phone-input"
                      type="tel"
                      required
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="مثال: 010xxxxxxxx أو 012xxxxxxxx"
                      dir="ltr"
                      className={`w-full bg-white border rounded-xl px-3.5 py-2.5 text-left text-xs sm:text-sm text-[#121C2A] font-mono focus:outline-none transition-colors ${
                        phoneError
                          ? 'border-[#DC2626] ring-1 ring-[#DC2626]'
                          : 'border-[#E2ECE6] focus:border-[#059669] focus:ring-1 focus:ring-[#059669]'
                      }`}
                    />
                    <span className="absolute right-3 top-2.5 text-[11px] text-[#707974] font-semibold pointer-events-none">
                      EG (+20)
                    </span>
                  </div>
                  {phoneError ? (
                    <p className="text-[11px] text-[#DC2626] mt-1 font-medium">{phoneError}</p>
                  ) : (
                    <p className="text-[10px] text-[#707974] mt-1">
                      ضروري لإرسال تفاصيل شحنتك والتواصل مع أخصائية التعافي عبر الواتساب
                    </p>
                  )}
                </div>

                {/* Dropdown: Egyptian Governorate */}
                <div>
                  <label htmlFor="gov-select" className="block text-xs font-bold text-[#003527] mb-1">
                    المحافظة <span className="text-[#DC2626]">*</span>
                  </label>
                  <select
                    id="gov-select"
                    value={governorate}
                    onChange={(e) => setGovernorate(e.target.value)}
                    className="w-full bg-white border border-[#E2ECE6] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#121C2A] focus:outline-none focus:border-[#059669] focus:ring-1 focus:ring-[#059669]"
                  >
                    {EGYPTIAN_GOVERNORATES.map((gov) => (
                      <option key={gov} value={gov}>
                        {gov}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Input: Detailed Address */}
                <div>
                  <label htmlFor="address-input" className="block text-xs font-bold text-[#003527] mb-1">
                    العنوان التفصيلي وملاحظات الاستلام (اختياري)
                  </label>
                  <input
                    id="address-input"
                    type="text"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    placeholder="مثال: الحي، اسم الشارع، رقم العمارة أو علامة مميزة"
                    className="w-full bg-white border border-[#E2ECE6] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#121C2A] focus:outline-none focus:border-[#059669] focus:ring-1 focus:ring-[#059669]"
                  />
                </div>

                {/* Promo Code & Order Summary */}
                <div className="p-4 rounded-2xl bg-[#F3F7F5] border border-[#E2ECE6] space-y-2.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#404944]">سعر الباقة الأساسي:</span>
                    <span className="font-bold text-[#121C2A]">{currentBundle.priceEGP} ج.م</span>
                  </div>

                  {/* Promo Code Field */}
                  <div className="flex items-center gap-2 pt-1">
                    <input
                      type="text"
                      value={promoCodeInput}
                      onChange={(e) => setPromoCodeInput(e.target.value)}
                      placeholder="كود الخصم"
                      className="bg-white border border-[#E2ECE6] rounded-lg px-2.5 py-1 text-xs font-mono uppercase text-center w-28 focus:outline-none focus:border-[#059669]"
                    />
                    <div className="flex-1 text-xs">
                      {isPromoValid ? (
                        <span className="text-[#059669] font-bold flex items-center gap-1">
                          <Sparkles className="w-3.5 h-3.5" />
                          تم تطبيق كود HT10 (وفرتِ {discountApplied} ج.م)
                        </span>
                      ) : (
                        <span className="text-[#707974]">أدخلي HT10 للحصول على خصم 10%</span>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#404944] flex items-center gap-1">
                      <Truck className="w-3.5 h-3.5 text-[#059669]" />
                      الشحن السريع والمغلف:
                    </span>
                    <span className="font-bold text-[#059669]">مجاني مع الباقة الشاملة</span>
                  </div>

                  <div className="pt-2 border-t border-[#E2ECE6] flex items-baseline justify-between">
                    <div>
                      <div className="text-xs font-bold text-[#003527]">
                        إجمالي المبلغ المطلوب عند الاستلام:
                      </div>
                      <div className="text-[11px] text-[#707974]">
                        شامل الاستشارة الطبية ومتابعة التعافي
                      </div>
                    </div>
                    <div className="text-xl font-extrabold text-[#064E3B]">
                      {finalPriceEGP} <span className="text-xs font-bold text-[#059669]">ج.م</span>
                    </div>
                  </div>
                </div>

                {/* Privacy & Medical Encryption Guarantee */}
                <div className="flex items-center gap-2 p-2.5 rounded-xl bg-[#E6EEFF] text-[#003527] text-[11px] font-medium border border-[#D0DBED]">
                  <Lock className="w-4 h-4 text-[#059669] shrink-0" />
                  <span>
                    بياناتك الطبية مشفرة ومحمية بخصوصية سريرية تامة ولن يتم استخدامها إلا لغرض التوصيل والمتابعة.
                  </span>
                </div>

                {/* Submit Action: Strictly labeled as required */}
                <button
                  type="submit"
                  disabled={submissionState === 'submitting'}
                  className="w-full bg-[#064E3B] hover:bg-[#003527] disabled:bg-[#707974] text-white py-4 px-6 rounded-xl font-bold text-sm sm:text-base text-center shadow-lg shadow-[#064E3B]/20 transition-all duration-200 cursor-pointer active:scale-98 flex items-center justify-center gap-2"
                >
                  {submissionState === 'submitting' ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>جاري تسجيل بياناتك السريرية وتأكيد حجز الاستشارة...</span>
                    </>
                  ) : (
                    <>
                      <span>تأكيد الطلب وحجز الاستشارة مجاناً</span>
                      <ArrowLeft className="w-4 h-4" />
                    </>
                  )}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
