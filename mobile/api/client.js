import axios from 'axios';
import config from '../config';

const api = axios.create({
  baseURL: config.API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Worker APIs
export const workerAPI = {
  getAll: () => api.get('/worker/all'),
  getById: (id) => api.get(`/worker/${id}`),
  add: (data) => api.post('/worker/add', data),
  update: (id, data) => api.put(`/worker/${id}`, data),
  delete: (id) => api.delete(`/worker/${id}`),
};

// Role APIs
export const roleAPI = {
  getAll: () => api.get('/role/all'),
  getById: (id) => api.get(`/role/${id}`),
  add: (data) => api.post('/role/add', data),
  update: (id, data) => api.put(`/role/${id}`, data),
  delete: (id) => api.delete(`/role/${id}`),
};

// Prediction APIs
export const predictionAPI = {
  predictFit: (roleId, topN = 3) => api.post('/predict-fit', { role_id: roleId, top_n: topN }),
  trainModel: () => api.post('/train-model'),
};

// Assignment APIs
export const assignmentAPI = {
  create: (data) => api.post('/assignment/create', data),
  addFeedback: (id, data) => api.put(`/assignment/${id}/feedback`, data),
  getAll: () => api.get('/assignment/all'),
};

// Analytics APIs
export const analyticsAPI = {
  getOverview: () => api.get('/analytics/overview'),
};

export default api;
