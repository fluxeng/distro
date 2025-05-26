'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  HomeIcon,
  BuildingOfficeIcon,
  CogIcon,
  ChartBarIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'

interface AdminSidebarProps {
  mobile?: boolean
  onClose?: () => void
}

export default function AdminSidebar({ mobile = false, onClose }: AdminSidebarProps) {
  const pathname = usePathname()
  
  const navigation = [
    {
      name: 'Dashboard',
      href: '/admin/dashboard',
      icon: HomeIcon,
      current: pathname === '/admin/dashboard'
    },
    {
      name: 'Utilities',
      href: '/admin/utilities',
      icon: BuildingOfficeIcon,
      current: pathname.includes('/admin/utilities')
    },
    {
      name: 'Analytics',
      href: '/admin/analytics',
      icon: ChartBarIcon,
      current: pathname.includes('/admin/analytics')
    },
    {
      name: 'Settings',
      href: '/admin/settings',
      icon: CogIcon,
      current: pathname.includes('/admin/settings')
    }
  ]
  
  return (
    <div className="flex flex-col flex-grow border-r border-gray-200 pt-5 pb-4 bg-white overflow-y-auto">
      {/* Mobile close button */}
      {mobile && (
        <div className="absolute top-0 right-0 -mr-12 pt-2">
          <button
            type="button"
            className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            onClick={onClose}
          >
            <XMarkIcon className="h-6 w-6 text-white" />
          </button>
        </div>
      )}
      
      {/* Logo */}
      <div className="flex items-center flex-shrink-0 px-4">
        <div className="flex items-center">
          <div className="flex-shrink-0 h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 7.172V5L8 4z" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-900">Distro Admin</p>
            <p className="text-xs text-gray-500">Public Administration</p>
          </div>
        </div>
      </div>
      
      {/* Navigation */}
      <div className="mt-8 flex-grow flex flex-col">
        <nav className="flex-1 px-2 space-y-1">
          {navigation.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className={`
                group flex items-center px-2 py-2 text-sm font-medium rounded-md
                ${item.current
                  ? 'bg-blue-100 text-blue-900'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }
              `}
            >
              <item.icon
                className={`
                  mr-3 flex-shrink-0 h-6 w-6
                  ${item.current
                    ? 'text-blue-500'
                    : 'text-gray-400 group-hover:text-gray-500'
                  }
                `}
              />
              {item.name}
            </Link>
          ))}
        </nav>
      </div>
      
      {/* System info */}
      <div className="flex-shrink-0 px-4 py-4 border-t border-gray-200">
        <div className="text-xs text-gray-500">
          <p>Distro V1 System Admin</p>
          <p className="mt-1">Managing Water Utilities</p>
        </div>
      </div>
    </div>
  )
}