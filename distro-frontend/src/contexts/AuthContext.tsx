// distro-frontend/src/contexts/AuthContext.tsx
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import api from '../lib/api';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const token = Cookies.get('access_token');
      if (token) {
        try {
          const response = await api.get('/users/profile/');
          setUser(response.data.data);
        } catch (error) {
          console.error('Failed to load user:', error);
          setUser(null);
          Cookies.remove('access_token');
          Cookies.remove('refresh_token');
        }
      }
      setIsLoading(false);
    };
    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await api.post('/users/auth/login/', { email, password });
      const { tokens, user } = response.data;
      Cookies.set('access_token', tokens.access);
      Cookies.set('refresh_token', tokens.refresh);
      setUser(user);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await api.post('/users/auth/logout/', { refresh_token: Cookies.get('refresh_token') });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      Cookies.remove('access_token');
      Cookies.remove('refresh_token');
      setUser(null);
      setIsLoading(false);
      window.location.href = '/login';
    }
  };

  const refreshUser = async () => {
    try {
      const response = await api.get('/users/profile/');
      setUser(response.data.data);
    } catch (error) {
      console.error('Failed to refresh user:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, refreshUser, isLoading }}>
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