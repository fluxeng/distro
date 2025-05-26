'use client'

import React from 'react'
import {
  Bars3Icon,
  BellIcon
} from '@heroicons/react/24/outline'

interface AdminHeaderProps {
  onMenuClick: () => void
}

export default function AdminHeader({ onMenuClick }: AdminHeaderProps) {
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
        {/* Left side */}
        <div className="flex items-center">
          <h1 className="text-lg font-semibold text-gray-900">
            System Administration
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
          
          {/* System status indicator */}
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-400 rounded-full"></div>
            <span className="text-sm text-gray-500">System Online</span>
          </div>
        </div>
      </div>
    </div>
  )
}