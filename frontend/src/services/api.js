import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============================================================
// AUTH APIs
// ============================================================
export const authAPI = {
  register: (email, fullName, password) =>
    api.post('/auth/register', { email, full_name: fullName, password }),
  
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  getCurrentUser: () =>
    api.get('/auth/me'),
};

// ============================================================
// SUBJECT APIs
// ============================================================
export const subjectAPI = {
  create: (name, description, examDate) =>
    api.post('/subjects', { name, description, exam_date: examDate }),
  
  getAll: () =>
    api.get('/subjects'),
  
  getOne: (id) =>
    api.get(`/subjects/${id}`),
  
  update: (id, data) =>
    api.put(`/subjects/${id}`, data),
  
  delete: (id) =>
    api.delete(`/subjects/${id}`),
};

// ============================================================
// TASK APIs
// ============================================================
export const taskAPI = {
  create: (subjectId, title, description, difficulty, estimatedHours, deadline) =>
    api.post('/tasks', {
      subject_id: subjectId,
      title,
      description,
      difficulty,
      estimated_hours: estimatedHours,
      deadline,
    }),
  
  getAll: (subjectId = null) => {
    const url = subjectId ? `/tasks?subject_id=${subjectId}` : '/tasks';
    return api.get(url);
  },
  
  getOne: (id) =>
    api.get(`/tasks/${id}`),
  
  update: (id, data) =>
    api.put(`/tasks/${id}`, data),
  
  delete: (id) =>
    api.delete(`/tasks/${id}`),
  
  markComplete: (id) =>
    api.patch(`/tasks/${id}/complete`),
};

// ============================================================
// SCHEDULE APIs
// ============================================================
export const scheduleAPI = {
  getAll: () =>
    api.get('/schedule'),
  
  getWeek: () =>
    api.get('/schedule/week'),
  
  generate: () =>
    api.post('/schedule/generate'),
  
  clear: () =>
    api.delete('/schedule/clear'),
};

export default api;