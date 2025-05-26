import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/contexts/AuthContext'
import { TenantProvider } from '@/contexts/TenantContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Distro V1 - Water Utility Management',
  description: 'Digital twin platform for water utilities with integrated customer support',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <TenantProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </TenantProvider>
      </body>
    </html>
  )
}