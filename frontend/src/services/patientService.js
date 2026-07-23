import api from './api';

export const patientService = {
  async getAllPatients() {
    return await api.get('/patients/');
  },

  async getPatientById(id) {
    return await api.get(`/patients/${id}`);
  },

  async createPatient(patientData) {
    return await api.post('/patients/', patientData);
  },

  async updatePatient(id, patientData) {
    return await api.put(`/patients/${id}`, patientData);
  },

  async deletePatient(id) {
    return await api.delete(`/patients/${id}`);
  },
};
