import api from './api';

export const analyticsService = {
  async getDashboardAnalytics() {
    return await api.get('/analytics/dashboard');
  },

  async getRevenueAnalytics() {
    return await api.get('/analytics/revenue');
  },

  async getTopDoctorsAnalytics() {
    return await api.get('/analytics/top-doctors');
  },

  async getAppointmentsAnalytics() {
    return await api.get('/analytics/appointments');
  },

  async getLabTestsAnalytics() {
    return await api.get('/analytics/lab-tests');
  },

  async getPaymentsAnalytics() {
    return await api.get('/analytics/payments');
  },
};
