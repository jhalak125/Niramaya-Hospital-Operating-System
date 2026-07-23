import api from './api';

export const dashboardService = {
  async getAdminDashboard() {
    return await api.get('/dashboard/admin');
  },
  async getDoctorDashboard() {
    return await api.get('/dashboard/doctor');
  },
  async getPatientDashboard() {
    return await api.get('/dashboard/patient');
  },
  async getAuthAdminDashboard() {
    return await api.get('/auth/admin-dashboard');
  },
  async getAuthDoctorDashboard() {
    return await api.get('/auth/doctor-dashboard');
  },
  async getAuthAppointmentsManage() {
    return await api.get('/auth/appointments/manage');
  },
};
