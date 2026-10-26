import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeArabic, buildClinicalSearchIndex, searchKnowledge } from './searchIndex';
import { CAMPAIGNS } from '../data/campaignConfig';

test('normalizeArabic properly normalizes Arabic diacritics, alefs, taa marbuta, and yaa', () => {
  // Alef variations
  assert.equal(normalizeArabic('أحمد إبراهيم آمنة ٱستماع'), 'احمد ابراهيم امنه استماع');
  // Taa Marbuta & Haa
  assert.equal(normalizeArabic('جراحة قيصرية دقيقة'), 'جراحه قيصريه دقيقه');
  // Yaa & Alef Maksura
  assert.equal(normalizeArabic('مستشفى مصطفى شافي'), 'مستشفي مصطفي شافي');
  // Diacritics (tashkeel) & kashida
  assert.equal(normalizeArabic('الشَّاشُ الطِّبِّيُّ الْمُعَقَّمُ'), 'الشاش الطبي المعقم');
  assert.equal(normalizeArabic('جـراحـة'), 'جراحه');
});

test('buildClinicalSearchIndex indexes articles and FAQs across campaigns', () => {
  const index = buildClinicalSearchIndex(CAMPAIGNS);
  assert.ok(index.length > 20, 'Index should have comprehensive entries');

  const articleItems = index.filter((item) => item.type === 'article');
  const faqItems = index.filter((item) => item.type === 'faq');

  assert.ok(articleItems.length > 10, 'Should have multiple article sections');
  assert.ok(faqItems.length > 10, 'Should have multiple FAQs');
});

test('searchKnowledge finds relevant results for "استحمام" (showering)', () => {
  const index = buildClinicalSearchIndex(CAMPAIGNS);
  const results = searchKnowledge(index, 'الاستحمام');

  assert.ok(results.length > 0, 'Should return results for الاستحمام');
  const hasWaterOrShower = results.some(
    (r) => r.item.title.includes('استحمام') || r.item.fullContent.includes('استحمام')
  );
  assert.equal(hasWaterOrShower, true);
});

test('searchKnowledge normalizes query: searching with or without hamza yields results', () => {
  const index = buildClinicalSearchIndex(CAMPAIGNS);
  const resultsWithHamza = searchKnowledge(index, 'إزالة الشاش');
  const resultsWithoutHamza = searchKnowledge(index, 'ازالة الشاش');

  assert.ok(resultsWithHamza.length > 0);
  assert.ok(resultsWithoutHamza.length > 0);
  assert.equal(resultsWithHamza[0].item.id, resultsWithoutHamza[0].item.id);
});

test('searchKnowledge respects filterType for faq and article', () => {
  const index = buildClinicalSearchIndex(CAMPAIGNS);
  const faqOnly = searchKnowledge(index, 'سيليكون', { filterType: 'faq' });
  const articleOnly = searchKnowledge(index, 'سيليكون', { filterType: 'article' });

  assert.ok(faqOnly.length > 0);
  assert.ok(articleOnly.length > 0);
  assert.ok(faqOnly.every((r) => r.item.type === 'faq'));
  assert.ok(articleOnly.every((r) => r.item.type === 'article'));
});
