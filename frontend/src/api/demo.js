import { apiRequest } from './client.js';

export function createDemoCampaign(projectId, payload) {
  return apiRequest(`/projects/${projectId}/demo-campaign`, { method: 'POST', body: payload });
}

export function getDemoCampaign(projectId) {
  return apiRequest(`/projects/${projectId}/demo-campaign`);
}