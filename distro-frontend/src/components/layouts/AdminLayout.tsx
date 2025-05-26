// distro-frontend/src/components/layouts/AdminLayout.tsx
'use client';

import { AdminHeader } from '../navigation/AdminHeader';
import { AdminSidebar } from '../navigation/AdminSidebar';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-gray-100">
      <AdminSidebar />
      <div className="flex-1 flex flex-col">
        <AdminHeader />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}