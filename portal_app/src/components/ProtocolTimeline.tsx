import React from 'react';
import { Campaign } from '../types/campaign';

interface ProtocolTimelineProps {
  campaign?: Campaign;
}

/**
 * @deprecated Fixed clinical timeline is deprecated per patient safety guidelines (R1).
 * Generalized non-individualized healing schedules have been permanently removed.
 */
export const ProtocolTimeline: React.FC<ProtocolTimelineProps> = () => {
  return null;
};
