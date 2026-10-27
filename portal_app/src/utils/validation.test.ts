import test from 'node:test';
import assert from 'node:assert/strict';
import {
  normalizeEgyptianPhone,
  isValidEgyptianPhone,
  verifyConsultationCode,
  buildWhatsAppRedirectUrl
} from './validation';
import { LeadSubmissionData } from '../types/campaign';

test('normalizeEgyptianPhone handles various Egyptian prefixes and spaces', () => {
  assert.equal(normalizeEgyptianPhone('01012345678'), '01012345678');
  assert.equal(normalizeEgyptianPhone('+201012345678'), '01012345678');
  assert.equal(normalizeEgyptianPhone('201155803307'), '01155803307');
  assert.equal(normalizeEgyptianPhone('012 3456 7890'), '01234567890');
  assert.equal(normalizeEgyptianPhone('015-1234-5678'), '01512345678');
  assert.equal(normalizeEgyptianPhone('(+20) 010 1234 5678'), '01012345678');
  assert.equal(normalizeEgyptianPhone('+20 010 1234 5678'), '01012345678');
  assert.equal(normalizeEgyptianPhone('002001012345678'), '01012345678');
});

test('isValidEgyptianPhone validates valid and invalid Egyptian phone numbers', () => {
  assert.equal(isValidEgyptianPhone('01012345678'), true);
  assert.equal(isValidEgyptianPhone('01155803307'), true);
  assert.equal(isValidEgyptianPhone('01298765432'), true);
  assert.equal(isValidEgyptianPhone('01511223344'), true);
  assert.equal(isValidEgyptianPhone('+201012345678'), true);

  // Invalid numbers
  assert.equal(isValidEgyptianPhone('01312345678'), false); // 013 is not mobile
  assert.equal(isValidEgyptianPhone('0101234567'), false); // only 10 digits
  assert.equal(isValidEgyptianPhone('010123456789'), false); // 12 digits
  assert.equal(isValidEgyptianPhone('abcdefghijk'), false);
  assert.equal(isValidEgyptianPhone(''), false);
});

test('verifyConsultationCode validates HT10 clinical consultation benefit without prices', () => {
  const result = verifyConsultationCode('HT10');
  assert.equal(result.isPromoValid, true);
  assert.equal(result.promoCode, 'HT10');
  assert.equal(result.benefitDescription.includes('استشارة سريرية مجانية'), true);

  // Case insensitive
  const resultLower = verifyConsultationCode('ht10');
  assert.equal(resultLower.isPromoValid, true);
  assert.equal(resultLower.promoCode, 'HT10');

  // Invalid code
  const resultInvalid = verifyConsultationCode('INVALID');
  assert.equal(resultInvalid.isPromoValid, false);
  assert.equal(resultInvalid.benefitDescription, '');
});

test('buildWhatsAppRedirectUrl constructs valid clinical triage WhatsApp URL without prices', () => {
  const mockLead: LeadSubmissionData = {
    fullName: 'مريم أحمد الشريف',
    phone: '01012345678',
    surgeryType: 'الولادة القيصرية',
    daysPostOp: 'الأسبوع الثاني (14 يوماً)',
    governorate: 'القاهرة',
    inquiryNotes: 'عندي حكة خفيفة وعايزة أعرف طريقة وضع السيليكون بالظبط',
    source: 'lead_modal',
    timestamp: '2026-10-27T12:00:00Z'
  };

  const url = buildWhatsAppRedirectUrl(mockLead);
  assert.equal(url.startsWith('https://wa.me/201155803307?text='), true);
  assert.equal(url.includes(encodeURIComponent('مريم أحمد الشريف')), true);
  assert.equal(url.includes(encodeURIComponent('01012345678')), true);
  assert.equal(url.includes(encodeURIComponent('الولادة القيصرية')), true);
  assert.equal(url.includes(encodeURIComponent('الأسبوع الثاني (14 يوماً)')), true);
  assert.equal(url.includes(encodeURIComponent('القاهرة')), true);
  assert.equal(url.includes(encodeURIComponent('عندي حكة خفيفة')), true);
  assert.equal(url.includes(encodeURIComponent('هيلينج تاتش مصر')), true);

  // Assert ZERO commercial pricing or currency symbols
  assert.equal(url.includes('ج.م'), false);
  assert.equal(url.includes('EGP'), false);
  assert.equal(url.includes('890'), false);
  assert.equal(url.includes('801'), false);
  assert.equal(url.includes('خصم'), false);
});
