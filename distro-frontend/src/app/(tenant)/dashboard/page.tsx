// distro-frontend/src/app/(tenant)/dashboard/page.tsx
'use client';

import { useAuth } from '../../../contexts/AuthContext';
import { LocationTracker } from '../../../components/common/LocationTracker';
import { LoadingSpinner } from '../../../components/common/LoadingSpinner';

export default function DashboardPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!user) return null;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <p>Welcome, {user.full_name || user.email}!</p>
      {user.role === 'field_tech' && <LocationTracker />}
    </div>
  );
}