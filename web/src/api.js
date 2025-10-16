import axios from 'axios';
import { API_BASE_URL } from './config';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const workerAPI = {
  getAll: () => api.get('/worker/all'),
  getById: (id) => api.get(`/worker/${id}`),
  add: (data) => api.post('/worker/add', data),
  update: (id, data) => api.put(`/worker/${id}`, data),
  delete: (id) => api.delete(`/worker/${id}`),
};

export const roleAPI = {
  getAll: () => api.get('/role/all'),
  getById: (id) => api.get(`/role/${id}`),
  add: (data) => api.post('/role/add', data),
  update: (id, data) => api.put(`/role/${id}`, data),
  delete: (id) => api.delete(`/role/${id}`),
};

export const predictionAPI = {
  predictFit: (roleId, topN = 5) => api.post('/predict-fit', { role_id: roleId, top_n: topN }),
  trainModel: () => api.post('/train-model'),
};

export const assignmentAPI = {
  create: (data) => api.post('/assignment/create', data),
  addFeedback: (id, data) => api.put(`/assignment/${id}/feedback`, data),
  getAll: () => api.get('/assignment/all'),
};

export const analyticsAPI = {
  getOverview: () => api.get('/analytics/overview'),
};

export default api;
