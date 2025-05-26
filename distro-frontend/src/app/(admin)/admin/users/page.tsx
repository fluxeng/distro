// distro-frontend/src/app/(admin)/admin/users/create/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '../../../../../lib/api';
import { Button } from '../../../../../components/common/Button';
import { LoadingSpinner } from '../../../../../components/common/LoadingSpinner';

const schema = z.object({
  email: z.string().email('Invalid email address'),
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  phone_number: z.string().optional(),
  role: z.enum(['admin', 'supervisor', 'field_tech', 'customer_service']),
  send_invitation: z.boolean().default(true),
});

type FormData = z.infer<typeof schema>;

export default function CreateUserPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.post('/users/users/', data);
      router.push('/admin/users');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create user');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-6">Create User</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            id="email"
            type="email"
            {...register('email')}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
          {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
        </div>
        <div>
          <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
            First Name
          </label>
          <input
            id="first_name"
            {...register('first_name')}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
          {errors.first_name && <p className="text-red-500 text-sm mt-1">{errors.first_name.message}</p>}
        </div>
        <div>
          <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
            Last Name
          </label>
          <input
            id="last_name"
            {...register('last_name')}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
          {errors.last_name && <p className="text-red-500 text-sm mt-1">{errors.last_name.message}</p>}
        </div>
        <div>
          <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700">
            Phone Number
          </label>
          <input
            id="phone_number"
            {...register('phone_number')}
            className="mt-1 bundle w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
          {errors.phone_number && <p className="text-red-500 text-sm mt-1">{errors.phone_number.message}</p>}
        </div>
        <div>
          <label htmlFor="role" className="block text-sm font-medium text-gray-700">
            Role
          </label>
          <select
            id="role"
            {...register('role')}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          >
            <option value="admin">Administrator</option>
            <option value="supervisor">Supervisor</option>
            <option value="field_tech">Field Technician</option>
            <option value="customer_service">Customer Service</option>
          </select>
          {errors.role && <p className="text-red-500 text-sm mt-1">{errors.role.message}</p>}
        </div>
        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              {...register('send_invitation')}
              className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">Send invitation email</span>
          </label>
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <Button type="submit" disabled={isLoading} className="w-full">
          {isLoading ? <LoadingSpinner /> : 'Create User'}
        </Button>
      </form>
    </div>
  );
}