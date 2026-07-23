import api from './api';

export const authService = {
  async login(email, password) {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    // Send as x-www-form-urlencoded for OAuth2PasswordRequestForm
    const response = await api.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response; // { access_token, token_type }
  },

  async register(userData) {
    // userData: { full_name, email, password, phone, role }
    const response = await api.post('/auth/register', userData);
    return response;
  },

  async getMe() {
    const response = await api.get('/auth/me');
    return response;
  },

  async googleLogin(idToken) {
    const response = await api.post('/auth/google-login', { token: idToken });
    return response;
  },
};
