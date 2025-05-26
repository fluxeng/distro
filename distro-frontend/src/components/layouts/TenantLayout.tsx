'use client'

import React, { ReactNode, useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { useTenant } from '@/contexts/TenantContext'
import Sidebar from '@/components/navigation/Sidebar'
import Header from '@/components/navigation/Header'
import ProtectedRoute from '@/components/auth/ProtectedRoute'

interface TenantLayoutProps {
  children: ReactNode
  requireAuth?: boolean
  requiredPermissions?: string[]
  requiredRole?: string
}

export default function TenantLayout({
  children,
  requireAuth = true,
  requiredPermissions = [],
  requiredRole
}: TenantLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user } = useAuth()
  const { tenant } = useTenant()
  
  if (requireAuth) {
    return (
      <ProtectedRoute
        requireAuth={requireAuth}
        requiredPermissions={requiredPermissions}
        requiredRole={requiredRole}
      >
        <LayoutContent
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          user={user}
          tenant={tenant}
        >
          {children}
        </LayoutContent>
      </ProtectedRoute>
    )
  }
  
  return (
    <LayoutContent
      sidebarOpen={sidebarOpen}
      setSidebarOpen={setSidebarOpen}
      user={user}
      tenant={tenant}
    >
      {children}
    </LayoutContent>
  )
}

function LayoutContent({
  children,
  sidebarOpen,
  setSidebarOpen,
  user,
  tenant
}: {
  children: ReactNode
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
  user: any
  tenant: any
}) {
  return (
    <div className="h-screen flex overflow-hidden bg-gray-100">
      {/* Sidebar for desktop */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <Sidebar />
        </div>
      </div>
      
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 flex z-40 md:hidden">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
            <Sidebar mobile onClose={() => setSidebarOpen(false)} />
          </div>
        </div>
      )}
      
      {/* Main content */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}