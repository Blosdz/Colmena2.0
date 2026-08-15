import { apiRequest } from './client.js';

export function listProjects({ page = 1, pageSize = 10 } = {}) {
  return apiRequest(`/projects?page=${page}&page_size=${pageSize}`);
}

export function createProject({ ownerUserId, name, projectType, description }) {
  return apiRequest('/projects', {
    method: 'POST',
    body: {
      owner_user_id: ownerUserId,
      name,
      project_type: projectType,
      description: description || null,
    },
  });
}

export function getProject(projectId) {
  return apiRequest(`/projects/${projectId}`);
}

export function updateProject(projectId, payload) {
  return apiRequest(`/projects/${projectId}`, { method: 'PATCH', body: payload });
}
