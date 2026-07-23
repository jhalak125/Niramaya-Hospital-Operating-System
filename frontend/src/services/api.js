import axios from 'axios';

// Automatically target local backend on localhost, or live Render origin in production
const isLocalhost = typeof window !== 'undefined' &&
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

const API_BASE_URL = import.meta.env.VITE_API_URL ||
  (isLocalhost ? 'http://localhost:8000' : 'https://niramaya-hospital-operating-system.onrender.com');

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
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('niramaya_token');
    }
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'Network error connecting to Niramaya Hospital API';
    return Promise.reject(new Error(message));
  }
);

export default api;
