// distro-frontend/src/components/common/LocationTracker.tsx
'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../lib/api';
import { Button } from './Button';

export const LocationTracker: React.FC = () => {
  const { user } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isTracking, setIsTracking] = useState(false);

  useEffect(() => {
    if (!user?.location_tracking_consent || user.role !== 'field_tech') return;

    const updateLocation = () => {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            await api.post('/users/update_location/', {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
            });
          } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to update location');
          }
        },
        (err) => {
          setError(err.message);
        }
      );
    };

    if (isTracking) {
      updateLocation();
      const interval = setInterval(updateLocation, 60000); // Update every minute
      return () => clearInterval(interval);
    }
  }, [user, isTracking]);

  if (!user || user.role !== 'field_tech' || !user.location_tracking_consent) return null;

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h3 className="text-lg font-medium mb-2">Location Tracking</h3>
      {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
      <Button
        onClick={() => setIsTracking(!isTracking)}
        variant={isTracking ? 'destructive' : 'default'}
      >
        {isTracking ? 'Stop Tracking' : 'Start Tracking'}
      </Button>
    </div>
  );
};