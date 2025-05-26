'use client'

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { headers } from 'next/headers'

interface TenantInfo {
  type: 'public' | 'tenant'
  id: string
  domain: string
  name?: string
}

interface TenantContextType {
  tenant: TenantInfo
  isPublicAdmin: boolean
  isTenant: boolean
  getTenantApiUrl: () => string
}

const TenantContext = createContext<TenantContextType | undefined>(undefined)

interface TenantProviderProps {
  children: ReactNode
}

export function TenantProvider({ children }: TenantProviderProps) {
  const [tenant, setTenant] = useState<TenantInfo>({
    type: 'public',
    id: 'public',
    domain: 'localhost',
    name: 'Distro Admin'
  })
  
  useEffect(() => {
    // Detect tenant info from browser
    if (typeof window !== 'undefined') {
      const hostname = window.location.hostname
      
      if (hostname === 'localhost' || hostname === '127.0.0.1') {
        setTenant({
          type: 'public',
          id: 'public',
          domain: hostname,
          name: 'Distro Admin'
        })
      } else if (hostname.includes('localhost')) {
        const subdomain = hostname.split('.')[0]
        setTenant({
          type: 'tenant',
          id: subdomain,
          domain: hostname,
          name: `${subdomain.charAt(0).toUpperCase() + subdomain.slice(1)} Water Utility`
        })
      }
    }
  }, [])
  
  const isPublicAdmin = tenant.type === 'public'
  const isTenant = tenant.type === 'tenant'
  
  const getTenantApiUrl = (): string => {
    if (tenant.type === 'public') {
      return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    } else {
      return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    }
  }
  
  const value: TenantContextType = {
    tenant,
    isPublicAdmin,
    isTenant,
    getTenantApiUrl
  }
  
  return (
    <TenantContext.Provider value={value}>
      {children}
    </TenantContext.Provider>
  )
}

export const useTenant = () => {
  const context = useContext(TenantContext)
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider')
  }
  return context
}