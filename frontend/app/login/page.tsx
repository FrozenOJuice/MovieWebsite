'use client'

import { useState } from 'react'
import Link from 'next/link'
import { postData } from '../api'
import './login.css'

export default function LoginPage() {
  const [formData, setFormData] = useState({ identifier: '', password: '' })
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    setMessage('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.identifier || !formData.password) {
      setMessage('Please enter your username/email and password.')
      setStatus('error')
      return
    }

    setStatus('loading')
    try {
      // OAuth2PasswordRequestForm requires "username" field name in backend
      const payload = new URLSearchParams()
      payload.append('username', formData.identifier)
      payload.append('password', formData.password)

      const res = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: payload
      })

      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Login failed.')

      // Store access token
      localStorage.setItem('access_token', data.access_token)

      setStatus('success')
      setMessage('Login successful!')
      console.log('✅ Logged in:', data)

      // Optional redirect
      // window.location.href = '/dashboard'
    } catch (err: any) {
      setStatus('error')
      setMessage(err.message)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Login to WatchWorthy</h1>
        <form onSubmit={handleSubmit} className="auth-form">
          <input
            name="identifier"
            type="text"
            placeholder="Username or Email"
            value={formData.identifier}
            onChange={handleChange}
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <button type="submit" disabled={status === 'loading'}>
            {status === 'loading' ? 'Logging in...' : 'Login'}
          </button>
        </form>

        {message && (
          <p className={status === 'success' ? 'success' : 'error'}>
            {message}
          </p>
        )}

        <p className="switch-link">
          Don't have an account? <Link href="/register">Register here</Link>
        </p>
      </div>
    </div>
  )
}
