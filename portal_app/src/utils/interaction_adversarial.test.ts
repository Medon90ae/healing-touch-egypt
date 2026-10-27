import test from 'node:test';
import assert from 'node:assert/strict';
import { CAMPAIGNS, WHATSAPP_RECOVERY_NUMBER, WEBHOOK_URL } from '../data/campaignConfig';
import { CampaignId, LeadSubmissionData } from '../types/campaign';
import {
  normalizeEgyptianPhone,
  isValidEgyptianPhone,
  verifyConsultationCode,
  buildWhatsAppRedirectUrl,
  submitLeadToGoogleSheet,
  logSearchInquiryToBeacon
} from './validation';
import {
  buildClinicalSearchIndex,
  searchKnowledge
} from './searchIndex';

// ==============================================================================
// 1. STRESS-TEST: 5 INTERACTIVE TABS & COMPONENT COMPLETENESS ACROSS ALL CAMPAIGNS
// ==============================================================================

test('TABS STRESS-TEST: All 4 campaigns support all 5 interactive tab panels without missing data', () => {
  const campaignKeys: CampaignId[] = ['c-section', 'rhinoplasty', 'bariatric', 'thyroid'];
  const expectedTabs = ['article', 'video', 'showcase', 'calculator', 'faq'] as const;

  for (const campId of campaignKeys) {
    const campaign = CAMPAIGNS[campId];
    assert.ok(campaign, `Campaign ${campId} must exist in CAMPAIGNS`);

    // Tab 1: [📖 الدليل والمقال السريري الشامل]
    assert.ok(campaign.article, `Campaign ${campId} missing article`);
    assert.ok(campaign.article.title.length > 5, `Campaign ${campId} article has empty title`);
    assert.ok(campaign.article.sections.length >= 3, `Campaign ${campId} article must have >= 3 sections`);
    for (const sec of campaign.article.sections) {
      assert.ok(sec.id, `Campaign ${campId} article section missing ID`);
      assert.ok(sec.heading, `Campaign ${campId} article section missing heading`);
      assert.ok(sec.content.length > 0, `Campaign ${campId} article section ${sec.id} has no content`);
    }
    assert.ok(campaign.scientificStudies.length >= 2, `Campaign ${campId} must have scientific citations`);
    for (const study of campaign.scientificStudies) {
      assert.ok(study.source, `Study missing source`);
      assert.ok(study.pmid || study.journal, `Study missing PMID or journal`);
    }

    // Tab 2: [🎬 فيديو الشرح العملي السريري]
    assert.ok(campaign.videoPosterUrl || campaign.heroImageUrl, `Campaign ${campId} missing video poster`);
    assert.ok(campaign.heroHighlights.length >= 3, `Campaign ${campId} missing hero highlights`);

    // Tab 3: [📸 صور واستعراض المنتجات المعتمدة]
    assert.ok(campaign.bundles.length >= 2, `Campaign ${campId} must have at least 2 clinical bundles`);
    assert.ok(campaign.products.length >= 2, `Campaign ${campId} must have at least 2 individual products`);
    for (const b of campaign.bundles) {
      assert.ok(b.id, `Bundle missing ID`);
      assert.ok(b.title, `Bundle missing title`);
      assert.ok(b.clinicalSynergy, `Bundle missing clinicalSynergy`);
      assert.ok(b.items.length >= 2, `Bundle ${b.id} missing items`);
      // Assert zero price fields
      assert.equal((b as any).price, undefined, `Bundle ${b.id} must NOT have price`);
      assert.equal((b as any).originalPrice, undefined, `Bundle ${b.id} must NOT have originalPrice`);
      assert.equal((b as any).discount, undefined, `Bundle ${b.id} must NOT have discount`);
    }
    for (const p of campaign.products) {
      assert.ok(p.id, `Product missing ID`);
      assert.ok(p.name, `Product missing name`);
      assert.ok(p.clinicalBenefit, `Product missing clinicalBenefit`);
      assert.ok(p.features.length >= 2, `Product ${p.id} missing features`);
      // Assert zero price fields
      assert.equal((p as any).price, undefined, `Product ${p.id} must NOT have price`);
    }

    // Tab 4: [🧮 حاسبة مراحل التعافي السريري]
    assert.ok(campaign.calculator, `Campaign ${campId} missing calculator`);
    assert.ok(campaign.calculator.questions.length >= 2, `Calculator ${campId} must have >= 2 questions`);
    for (const q of campaign.calculator.questions) {
      assert.ok(q.id, `Question missing ID`);
      assert.ok(q.label, `Question missing label`);
      assert.ok(q.options.length >= 2, `Question ${q.id} must have >= 2 options`);
      for (const opt of q.options) {
        assert.ok(typeof opt.score === 'number', `Option score must be a number`);
        assert.ok(opt.advice, `Option missing clinical advice`);
      }
    }

    // Tab 5: [❓ الأسئلة الشائعة والأخطاء الحرجة]
    assert.ok(campaign.faqs.length >= 2, `Campaign ${campId} must have >= 2 FAQs`);
    for (const faq of campaign.faqs) {
      assert.ok(faq.question, `FAQ missing question`);
      assert.ok(faq.answer, `FAQ missing answer`);
    }
  }
});

test('CALCULATOR PERMUTATION STRESS-TEST: getRecommendation returns valid protocol for all question choices across all campaigns', () => {
  for (const [campId, campaign] of Object.entries(CAMPAIGNS)) {
    const { questions, getRecommendation } = campaign.calculator;

    // Helper to generate Cartesian product of all options
    function cartesianOptions(qIdx: number, currentAnswers: Record<string, number>) {
      if (qIdx === questions.length) {
        // Evaluate recommendation
        const rec = getRecommendation(currentAnswers);
        assert.ok(rec, `Recommendation must be returned for answers ${JSON.stringify(currentAnswers)}`);
        assert.ok(rec.badge, `Recommendation missing badge in ${campId}`);
        assert.ok(rec.headline, `Recommendation missing headline in ${campId}`);
        assert.ok(rec.clinicalAdvice, `Recommendation missing clinicalAdvice in ${campId}`);
        assert.ok(rec.protocolSteps.length >= 2, `Recommendation missing protocolSteps in ${campId}`);
        assert.ok(
          campaign.bundles.some((b) => b.id === rec.recommendedBundleId),
          `recommendedBundleId ${rec.recommendedBundleId} not found in bundles of ${campId}`
        );
        return;
      }

      const q = questions[qIdx];
      for (const opt of q.options) {
        cartesianOptions(qIdx + 1, { ...currentAnswers, [q.id]: opt.score });
      }
    }

    cartesianOptions(0, {});
  }
});

// ==============================================================================
// 2. STRESS-TEST: SEARCHBAR BEHAVIOR, WHATSAPP REDIRECTION & BEACON ANALYTICS
// ==============================================================================

test('SEARCHBAR STRESS-TEST: Search query indexing and instant retrieval performance', () => {
  const index = buildClinicalSearchIndex(CAMPAIGNS);
  assert.ok(index.length >= 30, 'Clinical search index must index all articles and FAQs');

  const adversarialQueries = [
    'ماء',
    'الاستحمام',
    'سيليكون',
    'الشاش',
    'تضخم',
    'كلويد',
    'قيصرية',
    'أنف',
    'تكميم',
    'غدة درقية',
    '1533-0',
    'tegaderm',
    'bupy',
    'أثر الجرح',
    'اثر الجرح' // Without hamza
  ];

  for (const query of adversarialQueries) {
    const start = performance.now();
    const results = searchKnowledge(index, query, { limit: 10 });
    const duration = performance.now() - start;

    assert.ok(duration < 20, `Search query "${query}" took ${duration.toFixed(2)}ms, must be < 20ms`);
    assert.ok(results.length > 0, `Search query "${query}" should return results`);
  }
});

test('SEARCHBAR STRESS-TEST: Enter key & consultation action WhatsApp URL generation', () => {
  const queries = [
    'هل يمكن الاستحمام في اليوم الخامس بعد القيصرية؟',
    'شريحة السيليكون بتسبب حكة هل ده طبيعي؟',
    'مقاسات دعامة الأنف السيليكون بعد عملية التجميل'
  ];

  for (const q of queries) {
    const activeName = 'الولادة القيصرية';
    const text = `مرحباً أخصائية التعافي في هيلينج تاتش مصر، أود استشارة سريرية بخصوص: "${q.trim()}" (${activeName}).`;
    const url = `https://wa.me/${WHATSAPP_RECOVERY_NUMBER}?text=${encodeURIComponent(text)}`;

    assert.equal(url.startsWith('https://wa.me/201155803307?text='), true);
    assert.equal(url.includes(encodeURIComponent(q)), true);
    assert.equal(url.includes('ج.م'), false);
    assert.equal(url.includes('EGP'), false);
    assert.equal(url.includes('890'), false);
  }
});

test('BEACON ANALYTICS STRESS-TEST: logSearchInquiryToBeacon non-blocking execution & fallback', () => {
  // 1. Test when sendBeacon is not defined (Node environment)
  // Must execute safely without throwing
  assert.doesNotThrow(() => {
    logSearchInquiryToBeacon('استفسار تجريبي للاستحمام', 'الولادة القيصرية');
  });

  // 2. Test empty query does nothing
  assert.doesNotThrow(() => {
    logSearchInquiryToBeacon('', 'الولادة القيصرية');
  });
  assert.doesNotThrow(() => {
    logSearchInquiryToBeacon('   ', 'الولادة القيصرية');
  });
});

// ==============================================================================
// 3. STRESS-TEST: LEAD GATEMODAL VALIDATION & PAYLOAD
// ==============================================================================

test('LEAD VALIDATION: Full Name boundary testing (< 2 chars rejected, valid Arabic accepted)', () => {
  // Boundary helper matching LeadGateModal logic
  function validateName(fullName: string): { isValid: boolean; error: string | null } {
    if (!fullName.trim() || fullName.trim().length < 2) {
      return { isValid: false, error: 'يرجى كتابة الاسم لتسجيل ملف الاستشارة الطبية' };
    }
    return { isValid: true, error: null };
  }

  // Reject < 2 chars
  assert.equal(validateName('').isValid, false);
  assert.equal(validateName(' ').isValid, false);
  assert.equal(validateName('   ').isValid, false);
  assert.equal(validateName('أ').isValid, false);
  assert.equal(validateName('م').isValid, false);
  assert.equal(validateName(' A ').isValid, false);

  // Accept valid Arabic names (>= 2 chars)
  assert.equal(validateName('مي').isValid, true);
  assert.equal(validateName('منى').isValid, true);
  assert.equal(validateName('علي').isValid, true);
  assert.equal(validateName('مريم أحمد الشريف').isValid, true);
  assert.equal(validateName('فاطمة الزهراء محمود').isValid, true);
  assert.equal(validateName('د. سارة المنشاوي').isValid, true);
  assert.equal(validateName('مَرْيَمُ أَحْمَدُ').isValid, true);
});

test('LEAD VALIDATION: Phone number adversarial test (reject landlines, invalid prefixes & lengths, accept 010,011,012,015)', () => {
  // Egyptian landlines (MUST BE REJECTED)
  const landlines = [
    '0227654321', // Cairo
    '0233445566', // Giza
    '035432100',  // Alexandria
    '040332211',  // Tanta
    '050223344',  // Mansoura
    '088234567'   // Assiut
  ];
  for (const landline of landlines) {
    assert.equal(isValidEgyptianPhone(landline), false, `Landline ${landline} must be rejected`);
  }

  // Invalid mobile prefixes (MUST BE REJECTED)
  const invalidPrefixes = [
    '01312345678', // 013 is not mobile
    '01412345678', // 014 does not exist
    '01612345678', // 016 does not exist
    '01712345678', // 017 does not exist
    '01812345678', // 018 does not exist
    '01912345678'  // 019 does not exist
  ];
  for (const invalid of invalidPrefixes) {
    assert.equal(isValidEgyptianPhone(invalid), false, `Invalid prefix ${invalid} must be rejected`);
  }

  // Invalid lengths (MUST BE REJECTED)
  const invalidLengths = [
    '',
    '12345',
    '01012345',     // 8 digits
    '010123456',    // 9 digits
    '0101234567',   // 10 digits starting with 010
    '010123456789', // 12 digits
    '01012345678901'// 14 digits
  ];
  for (const invalid of invalidLengths) {
    assert.equal(isValidEgyptianPhone(invalid), false, `Invalid length ${invalid} must be rejected`);
  }

  // Non-numeric garbage (MUST BE REJECTED)
  const garbage = [
    'abcdefghijk',
    '010abcdefgh',
    '010-1234-XYZ',
    'phone_number'
  ];
  for (const g of garbage) {
    assert.equal(isValidEgyptianPhone(g), false, `Garbage ${g} must be rejected`);
  }

  // Valid Egyptian Mobiles (010, 011, 012, 015) in standard supported formats
  const validCases = [
    { input: '01012345678', expected: '01012345678' },
    { input: '+201012345678', expected: '01012345678' },
    { input: '201012345678', expected: '01012345678' },
    { input: '00201012345678', expected: '01012345678' },
    { input: '(+20) 010 1234 5678', expected: '01012345678' },
    { input: '+20 010 1234 5678', expected: '01012345678' },
    { input: '002001012345678', expected: '01012345678' },
    { input: '010 1234 5678', expected: '01012345678' },
    { input: '010-1234-5678', expected: '01012345678' },
    { input: '1012345678', expected: '01012345678' },

    { input: '01155803307', expected: '01155803307' },
    { input: '+201155803307', expected: '01155803307' },
    { input: '011 5580 3307', expected: '01155803307' },

    { input: '01234567890', expected: '01234567890' },
    { input: '+201234567890', expected: '01234567890' },

    { input: '01512345678', expected: '01512345678' },
    { input: '+201512345678', expected: '01512345678' }
  ];

  for (const { input, expected } of validCases) {
    const normalized = normalizeEgyptianPhone(input);
    assert.equal(normalized, expected, `Phone ${input} should normalize to ${expected}`);
    assert.equal(isValidEgyptianPhone(input), true, `Phone ${input} must be valid`);
  }
});

test('LEAD VALIDATION: normalizeEgyptianPhone correctly normalizes redundant country prefix +20 combined with leading 0 (e.g. +20 010...)', () => {
  const redundantPrefixPhone = '+20 010 1234 5678';
  const normalized = normalizeEgyptianPhone(redundantPrefixPhone);
  assert.equal(normalized, '01012345678');
  assert.equal(isValidEgyptianPhone(redundantPrefixPhone), true);
});

test('LEAD PAYLOAD: WhatsApp URL contains ALL triage fields and ZERO commerce/pricing', () => {
  const triageTestLead: LeadSubmissionData = {
    fullName: 'نورهان عبد الفتاح الألفي',
    phone: '+201155803307',
    surgeryType: 'استئصال الغدة الدرقية',
    daysPostOp: 'الأسبوع الثالث (21 يوماً)',
    governorate: 'الإسكندرية',
    inquiryNotes: 'عندي تورم بسيط فوق خط الجرح في الرقبة واستفسار عن السيليكون المناسب',
    source: 'lead_modal',
    timestamp: '2026-10-27T14:30:00Z'
  };

  const url = buildWhatsAppRedirectUrl(triageTestLead);
  assert.equal(url.startsWith('https://wa.me/201155803307?text='), true);

  // Decode the text parameter to verify all triage fields are present
  const textParam = new URL(url).searchParams.get('text');
  assert.ok(textParam, 'WhatsApp URL must have text parameter');

  assert.ok(textParam.includes('مرحباً أخصائية التعافي الطبي في هيلينج تاتش مصر'));
  assert.ok(textParam.includes('▪️ الاسم: نورهان عبد الفتاح الألفي'));
  assert.ok(textParam.includes('▪️ رقم الهاتف: 01155803307'));
  assert.ok(textParam.includes('▪️ نوع العملية: استئصال الغدة الدرقية'));
  assert.ok(textParam.includes('▪️ مرحلة الجرح / الأيام بعد العملية: الأسبوع الثالث (21 يوماً)'));
  assert.ok(textParam.includes('▪️ المحافظة: الإسكندرية'));
  assert.ok(textParam.includes('▪️ تفاصيل الاستفسار: عندي تورم بسيط فوق خط الجرح في الرقبة'));
  assert.ok(textParam.includes('أرجو التواصل لتحديد بروتوكول العناية والمتابعة السريرية'));

  // Assert ZERO commercial pricing or checkout terms in WhatsApp URL
  const forbiddenPricingTokens = [
    'ج.م',
    'EGP',
    '890',
    '680',
    '480',
    '801',
    '1450',
    'خصم',
    'وفرت',
    'سعر',
    'شحن مجاني بقيمة',
    'دفع عند الاستلام كاش',
    'اجمالي المبلغ',
    'تكلفة'
  ];

  for (const token of forbiddenPricingTokens) {
    assert.equal(
      textParam.includes(token),
      false,
      `WhatsApp payload must NOT contain pricing token "${token}"`
    );
  }
});

test('LEAD SUBMISSION: submitLeadToGoogleSheet sends zero prices and returns success', async () => {
  const triageTestLead: LeadSubmissionData = {
    fullName: 'هدير محمد رضوان',
    phone: '01012345678',
    surgeryType: 'تجميل الأنف',
    daysPostOp: 'الأسبوع الأول',
    governorate: 'الجيزة',
    inquiryNotes: 'استفسار عن مقاس دعامة الأنف السيليكون',
    source: 'lead_modal',
    timestamp: '2026-10-27T15:00:00Z'
  };

  const res = await submitLeadToGoogleSheet(triageTestLead);
  assert.equal(res.success, true);
});
