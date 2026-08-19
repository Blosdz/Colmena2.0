import { apiRequest } from './client.js';

export function registerUser({ email, username, password, firstName, lastName, organizationName, legalName, taxId, organizationType }) {
  return apiRequest('/auth/register', {
    method: 'POST',
    skipAuth: true,
    body: {
      email,
      username,
      password,
      first_name: firstName || null,
      last_name: lastName || null,
      organization: organizationName
        ? {
            name: organizationName,
            legal_name: legalName || null,
            tax_id: taxId || null,
            organization_type: organizationType || null,
          }
        : null,
    },
  });
}

export function loginUser({ email, password }) {
  return apiRequest('/auth/login', {
    method: 'POST',
    skipAuth: true,
    body: { email, password },
  });
}

export function fetchCurrentUser() {
  return apiRequest('/auth/me');
}
