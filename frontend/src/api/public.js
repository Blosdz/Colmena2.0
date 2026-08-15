import { apiRequest } from './client.js';

export function getPublicStudy(publicId) {
  return apiRequest(`/public/studies/${publicId}`, { skipAuth: true });
}

export function createPublicResponseSession(publicId) {
  return apiRequest(`/public/studies/${publicId}/response-sessions`, {
    method: 'POST',
    skipAuth: true,
  });
}
