'use client'

import React, { ReactNode, useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { useTenant } from '@/contexts/TenantContext'
import AdminSidebar from '@/components/navigation/AdminSidebar'
import AdminHeader from '@/components/navigation/AdminHeader'
import ProtectedRoute from '@/components/auth/ProtectedRoute'

interface AdminLayoutProps {
  children: ReactNode
  requireAuth?: boolean
}

export default function AdminLayout({
  children,
  requireAuth = true
}: AdminLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  
  if (requireAuth) {
    return (
      <ProtectedRoute requireAuth={requireAuth}>
        <LayoutContent
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
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
    >
      {children}
    </LayoutContent>
  )
}

function LayoutContent({
  children,
  sidebarOpen,
  setSidebarOpen
}: {
  children: ReactNode
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
}) {
  return (
    <div className="h-screen flex overflow-hidden bg-gray-100">
      {/* Sidebar for desktop */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <AdminSidebar />
        </div>
      </div>
      
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 flex z-40 md:hidden">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
            <AdminSidebar mobile onClose={() => setSidebarOpen(false)} />
          </div>
        </div>
      )}
      
      {/* Main content */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <AdminHeader onMenuClick={() => setSidebarOpen(true)} />
        
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