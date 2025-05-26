// distro-frontend/src/app/(admin)/admin/invitations/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '../../../../contexts/AuthContext';
import api from '../../../../lib/api';
import { Button } from '../../../../components/common/Button';
import { LoadingSpinner } from '../../../../components/common/LoadingSpinner';
import { useRouter } from 'next/navigation';

interface Invitation {
  id: string;
  email: string;
  role: string;
  invited_by_name: string;
  is_valid: boolean;
  is_accepted: boolean;
  created_on: string;
  expires_on: string;
}

export default function InvitationManagementPage() {
  const { user, isLoading } = useAuth();
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [fetching, setFetching] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!user || !['admin', 'supervisor'].includes(user.role)) {
      router.push('/dashboard');
      return;
    }

    const fetchInvitations = async () => {
      setFetching(true);
      try {
        const response = await api.get('/users/invitations/');
        setInvitations(response.data.results || []);
      } catch (err: any) {
        setError(err.response?.data?.error || 'Failed to fetch invitations');
      } finally {
        setFetching(false);
      }
    };
    fetchInvitations();
  }, [user, router]);

  const handleResendInvitation = async (invitationId: string) => {
    try {
      await api.post(`/users/invitations/${invitationId}/resend/`);
      setInvitations(invitations.map(inv => 
        inv.id === invitationId ? { ...inv, expires_on: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString() } : inv
      ));
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to resend invitation');
    }
  };

  if (isLoading || fetching) return <LoadingSpinner />;
  if (!user) return null;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Invitation Management</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invited By</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {invitations.map((inv) => (
              <tr key={inv.id}>
                <td className="px-6 py-4 whitespace-nowrap">{inv.email}</td>
                <td className="px-6 py-4 whitespace-nowrap">{inv.role}</td>
                <td className="px-6 py-4 whitespace-nowrap">{inv.invited_by_name}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {inv.is_accepted ? 'Accepted' : inv.is_valid ? 'Pending' : 'Expired'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {!inv.is_accepted && inv.is_valid && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleResendInvitation(inv.id)}
                    >
                      Resend
                    </Button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}