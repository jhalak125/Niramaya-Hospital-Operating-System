import api from './api';

export const notificationService = {
  async getMyNotifications() {
    return await api.get('/notifications/my');
  },

  async markAsRead(id) {
    return await api.put(`/notifications/${id}/read`);
  },

  async deleteNotification(id) {
    return await api.delete(`/notifications/${id}`);
  },

  async createNotification(data) {
    // data: { user_id, title, message, type }
    return await api.post('/notifications/', data);
  },
};
