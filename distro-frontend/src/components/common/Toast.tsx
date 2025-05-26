// distro-frontend/src/components/common/Toast.tsx
'use client';

import { useEffect, useState } from 'react';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

interface ToastProps {
  message: string;
  type: 'success' | 'error';
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`fixed bottom-4 right-4 p-4 rounded-md shadow-md ${
      type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white flex items-center`}>
      {type === 'success' ? (
        <CheckCircleIcon className="w-6 h-6 mr-2" />
      ) : (
        <XCircleIcon className="w-6 h-6 mr-2" />
      )}
      <span>{message}</span>
    </div>
  );
};