'use client'

import React, { useEffect, useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { getAssets, getUsers, getZones } from '@/lib/api'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import {
  MapIcon,
  UsersIcon,
  WrenchScrewdriverIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'

interface TenantDashboardStats {
  totalAssets: number
  totalUsers: number
  totalZones: number
  recentAssets: any[]
}

export default function TenantDashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<TenantDashboardStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  
  useEffect(() => {
    loadDashboardData()
  }, [])
  
  const loadDashboardData = async () => {
    try {
      setIsLoading(true)
      
      // Load data in parallel
      const [assets, users, zones] = await Promise.all([
        getAssets().catch(() => []),
        getUsers().catch(() => []),
        getZones().catch(() => [])
      ])
      
      const dashboardStats: TenantDashboardStats = {
        totalAssets: assets.length,
        totalUsers: users.length,
        totalZones: zones.length,
        recentAssets: assets.slice(0, 5)
      }
      
      setStats(dashboardStats)
    } catch (error: any) {
      console.error('Failed to load dashboard data:', error)
      setError(error.message || 'Failed to load dashboard data')
    } finally {
      setIsLoading(false)
    }
  }
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="lg" />
      </div>
    )
  }
  
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="text-sm text-red-700">{error}</div>
      </div>
    )
  }
  
  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return 'Good morning'
    if (hour < 18) return 'Good afternoon'
    return 'Good evening'
  }
  
  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-gray-900">
            {getGreeting()}, {user?.first_name || 'User'}!
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Here's what's happening with your water utility today.
          </p>
        </div>
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <MapIcon className="h-6 w-6 text-blue-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Assets
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats?.totalAssets || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UsersIcon className="h-6 w-6 text-green-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Team Members
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats?.totalUsers || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <WrenchScrewdriverIcon className="h-6 w-6 text-yellow-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Service Zones
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats?.totalZones || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-6 w-6 text-purple-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Active Issues
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    0
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            
              href="/infrastructure/map"
              className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300"
            >
              <div>
                <span className="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 group-hover:bg-blue-100">
                  <MapIcon className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium">
                  <span className="absolute inset-0" aria-hidden="true" />
                  View Infrastructure Map
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  Interactive map of all water assets
                </p>
              </div>
            </a>
            
            {user?.role !== 'field_tech' && (
              
                href="/admin/users"
                className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-green-500 rounded-lg border border-gray-200 hover:border-gray-300"
              >
                <div>
                  <span className="rounded-lg inline-flex p-3 bg-green-50 text-green-700 group-hover:bg-green-100">
                    <UsersIcon className="h-6 w-6" />
                  </span>
                </div>
                <div className="mt-4">
                  <h3 className="text-lg font-medium">
                    <span className="absolute inset-0" aria-hidden="true" />
                    Manage Users
                  </h3>
                  <p className="mt-2 text-sm text-gray-500">
                    Add and manage team members
                  </p>
                </div>
              </a>
            )}
            
            {user?.role === 'field_tech' && (
              
                href="/field/scan"
                className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-yellow-500 rounded-lg border border-gray-200 hover:border-gray-300"
              >
                <div>
                  <span className="rounded-lg inline-flex p-3 bg-yellow-50 text-yellow-700 group-hover:bg-yellow-100">
                    <WrenchScrewdriverIcon className="h-6 w-6" />
                  </span>
                </div>
                <div className="mt-4">
                  <h3 className="text-lg font-medium">
                    <span className="absolute inset-0" aria-hidden="true" />
                    Field Tools
                  </span>
                  <p className="mt-2 text-sm text-gray-500">
                    QR scanner and field operations
                  </p>
                </div>
              </a>
            )}
          </div>
        </div>
      </div>
      
      {/* Recent Assets */}
      {stats?.recentAssets && stats.recentAssets.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Recent Assets
            </h3>
            <div className="overflow-hidden">
              <ul className="divide-y divide-gray-200">
                {stats.recentAssets.map((asset) => (
                  <li key={asset.id} className="py-3">
                    <div className="flex items-center space-x-4">
                      <div className="flex-shrink-0">
                        <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                          <span className="text-sm font-medium text-blue-600">
                            {asset.asset_type_name?.[0] || 'A'}
                          </span>
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {asset.name || asset.asset_id}
                        </p>
                        <p className="text-sm text-gray-500">
                          {asset.asset_type_name} • {asset.status}
                        </p>
                      </div>
                      <div className="flex-shrink-0">
                        
                          href={`/infrastructure/assets/${asset.id}`}
                          className="text-blue-600 hover:text-blue-500 text-sm font-medium"
                        >
                          View
                        </a>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}