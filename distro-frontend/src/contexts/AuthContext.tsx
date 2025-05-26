'use client'

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie'
import { User, apiClient, LoginRequest } from '@/lib/api'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
  hasPermission: (permission: string) => boolean
  isRole: (role: string) => boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()
  
  const isAuthenticated = !!user
  
  // Initialize auth state on mount
  useEffect(() => {
    initializeAuth()
  }, [])
  
  const initializeAuth = async () => {
    try {
      const token = Cookies.get('access_token')
      const savedUser = localStorage.getItem('user')
      
      if (token && savedUser) {
        // Try to use saved user first for faster loading
        const parsedUser = JSON.parse(savedUser)
        setUser(parsedUser)
        
        // Then refresh from server in background
        try {
          await refreshUser()
        } catch (error) {
          console.warn('Failed to refresh user, using cached data')
        }
      } else if (token) {
        // No saved user but have token, fetch from server
        await refreshUser()
      }
    } catch (error) {
      console.error('Failed to initialize auth:', error)
      // Clear invalid auth data
      clearAuthData()
    } finally {
      setIsLoading(false)
    }
  }
  
  const login = async (credentials: LoginRequest) => {
    try {
      setIsLoading(true)
      const response = await apiClient.login(credentials)
      
      if (response.success) {
        // Store tokens
        Cookies.set('access_token', response.tokens.access, { expires: 7 })
        Cookies.set('refresh_token', response.tokens.refresh, { expires: 30 })
        
        // Store user data
        setUser(response.user)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        // Redirect based on role and tenant type
        redirectAfterLogin(response.user)
      } else {
        throw new Error(response.error || 'Login failed')
      }
    } catch (error: any) {
      console.error('Login error:', error)
      throw new Error(error.response?.data?.error || error.message || 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }
  
  const logout = async () => {
    try {
      await apiClient.logout()
    } catch (error) {
      console.warn('Logout API call failed, but continuing with local cleanup')
    }
    
    clearAuthData()
    
    // Redirect to login
    router.push('/login')
  }
  
  const refreshUser = async () => {
    try {
      const freshUser = await apiClient.getCurrentUser()
      setUser(freshUser)
      localStorage.setItem('user', JSON.stringify(freshUser))
    } catch (error) {
      console.error('Failed to refresh user:', error)
      clearAuthData()
      throw error
    }
  }
  
  const clearAuthData = () => {
    setUser(null)
    Cookies.remove('access_token')
    Cookies.remove('refresh_token')
    localStorage.removeItem('user')
  }
  
  const redirectAfterLogin = (user: User) => {
    const hostname = window.location.hostname
    
    if (hostname === 'localhost') {
      // Public admin - always go to admin dashboard
      router.push('/admin/dashboard')
    } else {
      // Tenant - redirect based on role
      switch (user.role) {
        case 'admin':
        case 'supervisor':
          router.push('/admin/dashboard')
          break
        case 'field_tech':
          router.push('/field/dashboard')
          break
        case 'customer_service':
          router.push('/admin/dashboard') // For now, same as admin
          break
        default:
          router.push('/profile')
      }
    }
  }
  
  const hasPermission = (permission: string): boolean => {
    if (!user) return false
    return user.permissions.includes(permission)
  }
  
  const isRole = (role: string): boolean => {
    if (!user) return false
    return user.role === role
  }
  
  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated,
    login,
    logout,
    refreshUser,
    hasPermission,
    isRole
  }
  
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}