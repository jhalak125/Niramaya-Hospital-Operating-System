import axios from 'axios';

// Use Vite proxy '/api' when in dev server, or direct backend origin
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 120s timeout for AI OCR and inference
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach bearer token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('niramaya_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle backend standard json wrapping and errors
api.interceptors.response.use(
  (response) => {
    if (response.data && typeof response.data === 'object' && 'success' in response.data) {
      return response.data.data !== undefined ? response.data.data : response.data;
    }
    return response.data;
  },
  (error) => {
    // If proxied /api returned network error, try fallback directly to http://127.0.0.1:8000
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'Network error connecting to Niramaya Hospital API';
    return Promise.reject(new Error(message));
  }
);

export default api;
