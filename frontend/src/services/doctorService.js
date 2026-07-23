import api from './api';

export const doctorService = {
  async getAllDoctors() {
    return await api.get('/doctors/');
  },

  async searchDoctors(params = {}) {
    // params: { department, specialization, status, min_experience, page, limit }
    return await api.get('/doctors/search', { params });
  },

  async getDoctorById(id) {
    return await api.get(`/doctors/${id}`);
  },

  async createDoctor(doctorData) {
    return await api.post('/doctors/', doctorData);
  },

  async updateDoctor(id, doctorData) {
    return await api.put(`/doctors/${id}`, doctorData);
  },

  async deleteDoctor(id) {
    return await api.delete(`/doctors/${id}`);
  },
};
