'use client'

import React, { useEffect, useState } from 'react'
import { getTenants } from '@/lib/api'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import {
  BuildingOfficeIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface DashboardStats {
  totalUtilities: number
  activeUtilities: number
  inactiveUtilities: number
  recentActivity: any[]
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  
  useEffect(() => {
    loadDashboardData()
  }, [])
  
  const loadDashboardData = async () => {
    try {
      setIsLoading(true)
      const tenants = await getTenants()
      
      const dashboardStats: DashboardStats = {
        totalUtilities: tenants.length,
        activeUtilities: tenants.filter(t => t.is_active && !t.is_deleted).length,
        inactiveUtilities: tenants.filter(t => !t.is_active || t.is_deleted).length,
        recentActivity: tenants.slice(0, 5).map(t => ({
          id: t.id,
          name: t.name,
          action: 'Created',
          time: t.created_on,
          status: t.is_active ? 'active' : 'inactive'
        }))
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
  
  if (!stats) {
    return <div>No data available</div>
  }
  
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">System Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of all water utilities in the Distro platform
        </p>
      </div>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BuildingOfficeIcon className="h-6 w-6 text-gray-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Utilities
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats.totalUtilities}
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
                <CheckCircleIcon className="h-6 w-6 text-green-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Active Utilities
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats.activeUtilities}
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
                <XCircleIcon className="h-6 w-6 text-red-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Inactive Utilities
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats.inactiveUtilities}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Recent Activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Recent Activity
          </h3>
          
          {stats.recentActivity.length === 0 ? (
            <p className="text-sm text-gray-500">No recent activity</p>
          ) : (
            <div className="flow-root">
              <ul className="-mb-8">
                {stats.recentActivity.map((activity, activityIdx) => (
                  <li key={activity.id}>
                    <div className="relative pb-8">
                      {activityIdx !== stats.recentActivity.length - 1 ? (
                        <span
                          className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                          aria-hidden="true"
                        />
                      ) : null}
                      <div className="relative flex space-x-3">
                        <div>
                          <span className={`
                            h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white
                            ${activity.status === 'active' 
                              ? 'bg-green-500' 
                              : 'bg-gray-500'
                            }
                          `}>
                            <ClockIcon className="h-5 w-5 text-white" />
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                          <div>
                            <p className="text-sm text-gray-500">
                              {activity.action} utility{' '}
                              <span className="font-medium text-gray-900">
                                {activity.name}
                              </span>
                            </p>
                          </div>
                          <div className="text-right text-sm whitespace-nowrap text-gray-500">
                            <time dateTime={activity.time}>
                              {new Date(activity.time).toLocaleDateString()}
                            </time>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
      
      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            
              href="/admin/utilities/create"
              className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300"
            >
              <div>
                <span className="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 group-hover:bg-blue-100">
                  <BuildingOfficeIcon className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium">
                  <span className="absolute inset-0" aria-hidden="true" />
                  Add New Utility
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  Onboard a new water utility to the platform
                </p>
              </div>
            </a>
            
            
              href="/admin/utilities"
              className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300"
            >
              <div>
                <span className="rounded-lg inline-flex p-3 bg-green-50 text-green-700 group-hover:bg-green-100">
                  <CheckCircleIcon className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium">
                  <span className="absolute inset-0" aria-hidden="true" />
                  Manage Utilities
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  View and manage all registered utilities
                </p>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}