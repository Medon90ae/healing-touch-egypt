import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCampaignShareData } from './share';
import { CAMPAIGNS } from '../data/campaignConfig';

test('buildCampaignShareData builds correct title, text, and URL for C-Section', () => {
  const cSection = CAMPAIGNS['c-section'];
  const shareData = buildCampaignShareData(cSection, 'https://example.com/app');

  assert.equal(shareData.title.includes('الولادة القيصرية'), true);
  assert.equal(shareData.text.includes(cSection.title), true);
  assert.equal(shareData.url, 'https://example.com/app?campaign=c-section');
});

test('buildCampaignShareData builds correct URL for Rhinoplasty and cleans existing query params', () => {
  const rhino = CAMPAIGNS['rhinoplasty'];
  const shareData = buildCampaignShareData(rhino, 'https://example.com/app?old=123#test');

  assert.equal(shareData.title.includes('تجميل الأنف'), true);
  assert.equal(shareData.url, 'https://example.com/app?campaign=rhinoplasty');
});
