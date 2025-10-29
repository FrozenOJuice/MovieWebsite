// frontend/components/ProtectedRoute.tsx
'use client'

import { useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { getCurrentUser } from '@/lib/auth'

interface ProtectedRouteProps {
  children: ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [authorized, setAuthorized] = useState(false)

  useEffect(() => {
    async function verify() {
      const user = await getCurrentUser()
      if (!user) {
        router.replace('/login')
      } else {
        setAuthorized(true)
      }
      setLoading(false)
    }
    verify()
  }, [router])

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '4rem' }}>Loading...</div>
  }

  return authorized ? <>{children}</> : null
}
