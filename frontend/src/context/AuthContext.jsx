import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('niramaya_token') || null);
  const [loading, setLoading] = useState(true);

  // Fetch current user if token exists on mount; also restore guest session if present
  useEffect(() => {
    const initAuth = async () => {
      // Check for a persisted guest session first
      const guestData = localStorage.getItem('niramaya_guest_user');
      if (guestData) {
        try {
          setUser(JSON.parse(guestData));
        } catch (_) {
          localStorage.removeItem('niramaya_guest_user');
        }
        setLoading(false);
        return;
      }

      if (token) {
        try {
          const userData = await authService.getMe();
          setUser(userData);
        } catch (error) {
          console.error('Failed to fetch current user profile:', error);
          logout();
        }
      }
      setLoading(false);
    };
    initAuth();
  }, [token]);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await authService.login(email, password);
      const accessToken = response.access_token;
      if (accessToken) {
        localStorage.setItem('niramaya_token', accessToken);
        setToken(accessToken);
        const userData = await authService.getMe();
        setUser(userData);
        return userData;
      }
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    return await authService.register(userData);
  };

  const googleLogin = async (idToken) => {
    setLoading(true);
    try {
      const response = await authService.googleLogin(idToken);
      if (response && response.access_token) {
        localStorage.setItem('niramaya_token', response.access_token);
        setToken(response.access_token);
        setUser(response.user);
        return response.user;
      }
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('niramaya_token');
    localStorage.removeItem('niramaya_guest_user');
    setToken(null);
    setUser(null);
  };

  // Guest login: creates a mock user object without calling the backend
  const guestLogin = (role) => {
    const GUEST_PROFILES = {
      doctor: { sub: 'guest_doctor', _id: 'guest_doctor', full_name: 'Dr. Guest Doctor', email: 'guest.doctor@niramaya.demo', role: 'doctor', is_guest: true },
      admin:  { sub: 'guest_admin',  _id: 'guest_admin',  full_name: 'Guest Admin',      email: 'guest.admin@niramaya.demo',  role: 'admin',  is_guest: true },
      patient:{ sub: 'guest_patient',_id: 'guest_patient',full_name: 'Guest Patient',    email: 'guest.patient@niramaya.demo',role: 'patient',is_guest: true },
    };
    const mockUser = GUEST_PROFILES[role];
    if (!mockUser) return;
    localStorage.setItem('niramaya_guest_user', JSON.stringify(mockUser));
    setUser(mockUser);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        role: user?.role || null,
        login,
        register,
        googleLogin,
        guestLogin,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
