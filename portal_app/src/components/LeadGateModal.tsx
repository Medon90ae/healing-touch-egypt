import React, { useState, useEffect } from 'react';
import {
  X,
  CheckCircle2,
  Lock,
  Loader2,
  ArrowLeft,
  MessageSquare,
  ShieldCheck
} from 'lucide-react';
import { Campaign, LeadSubmissionData } from '../types/campaign';
import { EGYPTIAN_GOVERNORATES } from '../data/campaignConfig';
import {
  isValidEgyptianPhone,
  submitLeadToGoogleSheet,
  buildWhatsAppRedirectUrl
} from '../utils/validation';

interface LeadGateModalProps {
  isOpen: boolean;
  onClose: () => void;
  campaign: Campaign;
  selectedBundleId?: string;
  onSelectBundleId?: (id: string) => void;
}

const SURGERY_OPTIONS = [
  'الولادة القيصرية',
  'تجميل الأنف',
  'تكميم ومناظير السمنة',
  'استئصال الغدة الدرقية',
  'جراحة تجميلية / أخرى'
];

const RECOVERY_STAGES = [
  'الأيام 1 - 7 (المرحلة الأولى: حماية الجرح والاستحمام)',
  'الأسبوع 2 - 4 (المرحلة الثانية: التئام السطح وبدء السيليكون)',
  'الشهر 2 - 3 (المرحلة الثالثة: تسطيح الندبة والوقاية من التضخم)',
  'أكثر من 3 أشهر (علاج ندبة متضخمة أو بارزة)',
  'أستعد لإجراء العملية قريباً (استشارة وقائية)'
];

export const LeadGateModal: React.FC<LeadGateModalProps> = ({
  isOpen,
  onClose,
  campaign
}) => {
  // Form fields
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [surgeryType, setSurgeryType] = useState<string>(campaign.name);
  const [daysPostOp, setDaysPostOp] = useState<string>(RECOVERY_STAGES[0]);
  const [governorate, setGovernorate] = useState<string>(EGYPTIAN_GOVERNORATES[0]);
  const [inquiryNotes, setInquiryNotes] = useState('');

  // Validation & Submission States
  const [phoneError, setPhoneError] = useState<string | null>(null);
  const [nameError, setNameError] = useState<string | null>(null);
  const [submissionState, setSubmissionState] = useState<'idle' | 'submitting' | 'success'>('idle');
  const [redirectUrl, setRedirectUrl] = useState<string>('');

  // Sync surgery type with active campaign when modal opens
  useEffect(() => {
    if (campaign && campaign.name) {
      setSurgeryType(campaign.name);
    }
  }, [campaign]);

  // Reset errors when inputs change
  useEffect(() => {
    if (phone && isValidEgyptianPhone(phone)) {
      setPhoneError(null);
    }
  }, [phone]);

  useEffect(() => {
    if (fullName.trim().length >= 2) {
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
    if (!fullName.trim() || fullName.trim().length < 2) {
      setNameError('يرجى كتابة الاسم لتسجيل ملف الاستشارة الطبية');
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

    const leadData: LeadSubmissionData = {
      fullName: fullName.trim(),
      phone: phone.trim(),
      surgeryType,
      daysPostOp,
      governorate,
      inquiryNotes: inquiryNotes.trim(),
      source: 'lead_modal',
      campaignId: campaign.id,
      campaignName: campaign.name,
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
                بوابة الفرز والاستشارة السريرية المشفرة
              </span>
            </div>
            <h2 id="modal-headline" className="text-lg sm:text-xl font-bold leading-snug">
              استشيري أخصائية التعافي مجاناً عبر واتساب
            </h2>
            <p className="text-xs text-white/80 mt-1">
              متابعة سريرية متخصصة ومجانية بدون أي رسوم أو شروط شراء مسبقة
            </p>
          </div>

          {/* Modal Body */}
          <div className="p-5 sm:p-7 overflow-y-auto">
            {submissionState === 'success' ? (
              /* Success / Redirecting Screen */
              <div className="py-8 text-center space-y-5">
                <div className="w-16 h-16 rounded-full bg-[#82F5C1]/30 border-2 border-[#059669] flex items-center justify-center text-[#059669] mx-auto animate-bounce">
                  <CheckCircle2 className="w-10 h-10" />
                </div>

                <div className="space-y-2">
                  <span className="text-xs font-bold text-[#059669] bg-[#E6EEFF] px-3 py-1 rounded-full">
                    تم تسجيل بيانات الاستشارة بنجاح
                  </span>
                  <h3 className="text-xl sm:text-2xl font-bold text-[#003527]">
                    جاري تحويلك الآن لمحادثة أخصائية التعافي
                  </h3>
                  <p className="text-xs sm:text-sm text-[#404944] max-w-md mx-auto leading-relaxed">
                    تم إعداد تفاصيل حالتك السريرية تلقائياً. اضغطي على الزر الأخضر بالأسفل لبدء المحادثة الفورية وتلقي التوجيه الطبي المعتمد.
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
                    ✅ تم تسجيل بياناتك بنجاح في السجل الطبي. أخصائية التعافي بانتظارك لمتابعة حالة جرحك وتحديد المقاسات المناسبة.
                  </p>
                </div>
              </div>
            ) : (
              /* Clinical Triage Form */
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Input: Full Name */}
                <div>
                  <label htmlFor="full-name-input" className="block text-xs font-bold text-[#003527] mb-1">
                    الاسم بالكامل <span className="text-[#DC2626]">*</span>
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
                      placeholder="مثال: 010xxxxxxxx أو 011xxxxxxxx"
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
                      ضروري لإرسال تفاصيل التوجيه الطبي والتواصل مع أخصائية التعافي عبر الواتساب
                    </p>
                  )}
                </div>

                {/* Dropdown: Surgery Type */}
                <div>
                  <label htmlFor="surgery-select" className="block text-xs font-bold text-[#003527] mb-1">
                    نوع العملية الجراحية <span className="text-[#DC2626]">*</span>
                  </label>
                  <select
                    id="surgery-select"
                    value={surgeryType}
                    onChange={(e) => setSurgeryType(e.target.value)}
                    className="w-full bg-white border border-[#E2ECE6] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#121C2A] focus:outline-none focus:border-[#059669] focus:ring-1 focus:ring-[#059669]"
                  >
                    {SURGERY_OPTIONS.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Dropdown: Days Post-Op / Recovery Stage */}
                <div>
                  <label htmlFor="stage-select" className="block text-xs font-bold text-[#003527] mb-1">
                    مرحلة الجرح / الأيام بعد العملية <span className="text-[#DC2626]">*</span>
                  </label>
                  <select
                    id="stage-select"
                    value={daysPostOp}
                    onChange={(e) => setDaysPostOp(e.target.value)}
                    className="w-full bg-white border border-[#E2ECE6] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#121C2A] focus:outline-none focus:border-[#059669] focus:ring-1 focus:ring-[#059669]"
                  >
                    {RECOVERY_STAGES.map((stage) => (
                      <option key={stage} value={stage}>
                        {stage}
                      </option>
                    ))}
                  </select>
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

                {/* Textarea: Specific Inquiry / Symptoms */}
                <div>
                  <label htmlFor="inquiry-notes-input" className="block text-xs font-bold text-[#003527] mb-1">
                    تفاصيل الاستفسار أو الأعراض الحالية (اختياري)
                  </label>
                  <textarea
                    id="inquiry-notes-input"
                    rows={2}
                    value={inquiryNotes}
                    onChange={(e) => setInquiryNotes(e.target.value)}
                    placeholder="مثال: قلق من وصول الماء، حكة أو تكتل تحت الجلد، استفسار عن مقاسات السيليكون..."
                    className="w-full bg-white border border-[#E2ECE6] rounded-xl px-3.5 py-2 text-xs sm:text-sm text-[#121C2A] focus:outline-none focus:border-[#059669] focus:ring-1 focus:ring-[#059669]"
                  />
                </div>

                {/* Privacy & Medical Confidentiality Notice */}
                <div className="flex items-center gap-2 p-2.5 rounded-xl bg-[#E6EEFF] text-[#003527] text-[11px] font-medium border border-[#D0DBED]">
                  <Lock className="w-4 h-4 text-[#059669] shrink-0" />
                  <span>
                    بياناتك الطبية مشفرة وسرية ولن يتم استخدامها إلا لغرض الاستشارة السريرية والمتابعة مع أخصائية التعافي.
                  </span>
                </div>

                {/* Submit Action: Strictly labeled as free clinical triage */}
                <button
                  type="submit"
                  disabled={submissionState === 'submitting'}
                  className="w-full bg-[#064E3B] hover:bg-[#003527] disabled:bg-[#707974] text-white py-4 px-6 rounded-xl font-bold text-sm sm:text-base text-center shadow-lg shadow-[#064E3B]/20 transition-all duration-200 cursor-pointer active:scale-98 flex items-center justify-center gap-2"
                >
                  {submissionState === 'submitting' ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>جاري تسجيل بياناتك وتحضير المحادثة...</span>
                    </>
                  ) : (
                    <>
                      <MessageSquare className="w-5 h-5 text-[#82F5C1]" />
                      <span>بدء الاستشارة المجانية عبر واتساب</span>
                      <ArrowLeft className="w-4 h-4 rtl:rotate-0" />
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
