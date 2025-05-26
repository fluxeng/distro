'use client'

import React, { useState, useRef, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { useTenant } from '@/contexts/TenantContext'
import Button from '@/components/common/Button'
import {
  Bars3Icon,
  BellIcon,
  UserCircleIcon,
  CogIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/react/24/outline'

interface HeaderProps {
  onMenuClick: () => void
}

export default function Header({ onMenuClick }: HeaderProps) {
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const { user, logout } = useAuth()
  const { tenant } = useTenant()
  const userMenuRef = useRef<HTMLDivElement>(null)
  
  // Close user menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setUserMenuOpen(false)
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])
  
  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
  }
  
  return (
    <div className="relative z-10 flex-shrink-0 flex h-16 bg-white shadow border-b border-gray-200">
      {/* Mobile menu button */}
      <button
        type="button"
        className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 md:hidden"
        onClick={onMenuClick}
      >
        <Bars3Icon className="h-6 w-6" />
      </button>
      
      {/* Header content */}
      <div className="flex-1 px-4 flex justify-between items-center">
        {/* Left side - breadcrumb/title could go here */}
        <div className="flex items-center">
          <h1 className="text-lg font-semibold text-gray-900">
            {/* This could be dynamic based on current page */}
          </h1>
        </div>
        
        {/* Right side */}
        <div className="ml-4 flex items-center md:ml-6 space-x-4">
          {/* Notifications */}
          <button
            type="button"
            className="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <BellIcon className="h-6 w-6" />
          </button>
          
          {/* User menu */}
          <div className="ml-3 relative" ref={userMenuRef}>
            <div>
              <button
                type="button"
                className="max-w-xs bg-white flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                onClick={() => setUserMenuOpen(!userMenuOpen)}
              >
                <span className="sr-only">Open user menu</span>
                {user?.avatar ? (
                  <img
                    className="h-8 w-8 rounded-full"
                    src={user.avatar}
                    alt=""
                  />
                ) : (
                  <div className="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center">
                    <span className="text-sm font-medium text-gray-700">
                      {user?.first_name?.[0] || user?.email?.[0] || '?'}
                    </span>
                  </div>
                )}
              </button>
            </div>
            
            {/* User menu dropdown */}
            {userMenuOpen && (
              <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5">
                <div className="px-4 py-3 border-b border-gray-100">
                  <p className="text-sm font-medium text-gray-900">
                    {user?.first_name ? `${user.first_name} ${user.last_name}` : user?.email}
                  </p>
                  <p className="text-sm text-gray-500">{user?.email}</p>
                  <p className="text-xs text-gray-400 capitalize mt-1">
                    {user?.role?.replace('_', ' ')}
                  </p>
                </div>
                
                
                  href="/profile"
                  className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  <UserCircleIcon className="mr-3 h-5 w-5 text-gray-400" />
                  Your Profile
                </a>
                
                
                  href="/profile/settings"
                  className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  <CogIcon className="mr-3 h-5 w-5 text-gray-400" />
                  Settings
                </a>
                
                <button
                  onClick={handleLogout}
                  className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  <ArrowRightOnRectangleIcon className="mr-3 h-5 w-5 text-gray-400" />
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}