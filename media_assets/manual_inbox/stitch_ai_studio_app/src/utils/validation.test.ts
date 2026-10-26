import test from 'node:test';
import assert from 'node:assert/strict';
import {
  normalizeEgyptianPhone,
  isValidEgyptianPhone,
  calculateOrderPrice,
  buildWhatsAppRedirectUrl
} from './validation';
import { LeadSubmissionData } from '../types/campaign';

test('normalizeEgyptianPhone handles various Egyptian prefixes and spaces', () => {
  assert.equal(normalizeEgyptianPhone('01012345678'), '01012345678');
  assert.equal(normalizeEgyptianPhone('+201012345678'), '01012345678');
  assert.equal(normalizeEgyptianPhone('201155803307'), '01155803307');
  assert.equal(normalizeEgyptianPhone('012 3456 7890'), '01234567890');
  assert.equal(normalizeEgyptianPhone('015-1234-5678'), '01512345678');
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

test('calculateOrderPrice applies HT10 promo code correctly', () => {
  const result = calculateOrderPrice(1000, 'HT10');
  assert.equal(result.isPromoValid, true);
  assert.equal(result.discountApplied, 100);
  assert.equal(result.finalPriceEGP, 900);
  assert.equal(result.promoCode, 'HT10');

  // Case insensitive
  const resultLower = calculateOrderPrice(890, 'ht10');
  assert.equal(resultLower.isPromoValid, true);
  assert.equal(resultLower.discountApplied, 89);
  assert.equal(resultLower.finalPriceEGP, 801);

  // Invalid code
  const resultInvalid = calculateOrderPrice(890, 'INVALID');
  assert.equal(resultInvalid.isPromoValid, false);
  assert.equal(resultInvalid.discountApplied, 0);
  assert.equal(resultInvalid.finalPriceEGP, 890);
});

test('buildWhatsAppRedirectUrl constructs valid WhatsApp URL containing lead details', () => {
  const mockLead: LeadSubmissionData = {
    fullName: 'أحمد محمود',
    phone: '01012345678',
    governorate: 'القاهرة',
    address: 'مدينة نصر - الحي السابع',
    notes: 'أرجو التوصيل بعد الساعة 4 عصراً',
    campaignId: 'c-section',
    campaignName: 'الولادة القيصرية',
    bundleId: 'csection-complete-protocol',
    bundleTitle: 'بروتوكول التعافي القيصري الشامل (الذهبي)',
    priceEGP: 890,
    finalPriceEGP: 801,
    discountApplied: 89,
    promoCode: 'HT10',
    sourceUrl: 'https://example.com/?campaign=c-section',
    timestamp: '2026-10-26T12:00:00Z'
  };

  const url = buildWhatsAppRedirectUrl(mockLead);
  assert.equal(url.startsWith('https://wa.me/201155803307?text='), true);
  assert.equal(url.includes(encodeURIComponent('أحمد محمود')), true);
  assert.equal(url.includes(encodeURIComponent('01012345678')), true);
  assert.equal(url.includes(encodeURIComponent('القاهرة')), true);
  assert.equal(url.includes(encodeURIComponent('HT10')), true);
  assert.equal(url.includes(encodeURIComponent('801 ج.م')), true);
});
