import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('niramaya_token') || null);
  const [loading, setLoading] = useState(true);

  // Fetch current user if token exists on mount
  useEffect(() => {
    const initAuth = async () => {
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
    setToken(null);
    setUser(null);
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
