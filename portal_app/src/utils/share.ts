import { Campaign } from '../types/campaign';

export interface ShareDataPayload {
  title: string;
  text: string;
  url: string;
}

/**
 * Builds the canonical share payload for a given campaign.
 */
export function buildCampaignShareData(
  campaign: Campaign,
  baseUrl: string = ''
): ShareDataPayload {
  const cleanBase = baseUrl.split('?')[0].split('#')[0];
  const url = cleanBase ? `${cleanBase}?campaign=${campaign.id}` : `?campaign=${campaign.id}`;

  return {
    title: `Clinical Sanctuary | بروتوكول ${campaign.name}`,
    text: `${campaign.title} - المنظومة السريرية المعتمدة لحماية وترميم الجروح الجراحية`,
    url
  };
}
