// distro-frontend/src/components/navigation/AdminSidebar.tsx
'use client';

import { useAuth } from '../../contexts/AuthContext';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { HomeIcon, UsersIcon, MailIcon } from '@heroicons/react/24/outline';

export const AdminSidebar: React.FC = () => {
  const { user } = useAuth();
  const pathname = usePathname();

  if (!user) return null;

  const navItems = [
    { name: 'Dashboard', href: '/admin/dashboard', icon: HomeIcon },
    ...(user.permissions.includes('view_all_users')
      ? [{ name: 'Users', href: '/admin/users', icon: UsersIcon }]
      : []),
    ...(user.permissions.includes('view_all_users')
      ? [{ name: 'Invitations', href: '/admin/invitations', icon: MailIcon }]
      : []),
  ];

  return (
    <div className="w-64 bg-white shadow-md">
      <div className="p-4">
        <h2 className="text-xl font-bold">Admin Panel</h2>
      </div>
      <nav className="mt-4">
        {navItems.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={`flex items-center p-4 text-gray-700 hover:bg-gray-100 ${
              pathname === item.href ? 'bg-gray-100' : ''
            }`}
          >
            <item.icon className="w-6 h-6 mr-3" />
            {item.name}
          </Link>
        ))}
      </nav>
    </div>
  );
};