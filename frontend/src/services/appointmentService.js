import api from './api';

export const appointmentService = {
  async createAppointment(data) {
    // data: { patient_id, doctor_id, appointment_date, time_slot, reason, notes }
    return await api.post('/appointments/', data);
  },

  async getMyAppointments() {
    return await api.get('/appointments/my');
  },

  async getDoctorAppointments() {
    return await api.get('/appointments/doctor');
  },

  async getAppointmentById(id) {
    return await api.get(`/appointments/${id}`);
  },

  async updateAppointment(id, data) {
    return await api.put(`/appointments/${id}`, data);
  },

  async updateStatus(id, status) {
    // status: "Scheduled" | "Confirmed" | "Completed" | "Cancelled" | "No Show"
    return await api.patch(`/appointments/${id}/status`, { status });
  },

  async getAllAppointments() {
    return await api.get('/appointments/');
  },

  async deleteAppointment(id) {
    return await api.delete(`/appointments/${id}`);
  },
};
