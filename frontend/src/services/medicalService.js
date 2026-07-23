import api from './api';

export const medicalService = {
  // Medical Records
  async createMedicalRecord(formData) {
    return await api.post('/medical-records/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  async getPatientRecords(patientId) {
    return await api.get(`/medical-records/patient/${patientId}`);
  },

  async getDoctorRecords() {
    return await api.get('/medical-records/doctor/my');
  },

  async searchMedicalRecords(params = {}) {
    return await api.get('/medical-records/search', { params });
  },

  async getRecordDetails(recordId) {
    return await api.get(`/medical-records/${recordId}`);
  },

  async deleteMedicalRecord(recordId) {
    return await api.delete(`/medical-records/${recordId}`);
  },

  // Prescriptions
  async createPrescription(data) {
    return await api.post('/prescriptions/', data);
  },

  async getPatientPrescriptions(patientId) {
    return await api.get(`/prescriptions/patient/${patientId}`);
  },

  // Billing
  async createBill(data) {
    return await api.post('/billing/', data);
  },

  async getPatientBills(patientId) {
    return await api.get(`/billing/${patientId}`);
  },

  async getAllBills() {
    return await api.get('/billing/');
  },

  // Payments
  async uploadPaymentProof(formData) {
    return await api.post('/payments/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  async verifyPayment(paymentId) {
    return await api.put(`/payments/verify/${paymentId}`);
  },

  async getPaymentDetailsForBill(billId) {
    return await api.get(`/payments/bill/${billId}`);
  },

  // Lab Tests & Reports
  async createLabTest(data) {
    return await api.post('/lab-tests/', data);
  },

  async getPatientLabTests(patientId) {
    return await api.get(`/lab-tests/patient/${patientId}`);
  },

  async searchLabTests(params = {}) {
    return await api.get('/lab-tests/search', { params });
  },

  async createLabReport(formData) {
    return await api.post('/lab-reports/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  async getPatientLabReports(patientId) {
    return await api.get(`/lab-reports/patient/${patientId}`);
  },

  // Audit Logs
  async getAuditLogs() {
    return await api.get('/audit-logs/');
  },

  // Vaidya AI & Symptom Checker
  async analyzeMedicalReport(formData) {
    return await api.post('/vaidya-ai/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  async symptomCheck(symptoms) {
    return await api.post('/ai/symptom-check', { symptoms });
  },
};
