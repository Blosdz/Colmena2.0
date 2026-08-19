import { apiRequest } from './client.js';

export function getCompanyProfile() {
  return apiRequest('/company/profile');
}

export function saveCompanyProfile(payload) {
  return apiRequest('/company/profile', { method: 'PUT', body: payload });
}
