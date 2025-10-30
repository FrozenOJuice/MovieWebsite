'use client'

import { useState } from 'react'
import Link from 'next/link'
import { postData } from '../api'
import './register.css'

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'member'
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [serverMessage, setServerMessage] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    setErrors(prev => ({ ...prev, [name]: '' }))
    setServerMessage('')
  }

  const validateForm = () => {
    const newErrors: Record<string, string> = {}
    if (!formData.username.trim()) newErrors.username = 'Username is required'
    if (!formData.email.includes('@')) newErrors.email = 'Valid email required'
    if (formData.password.length < 6) newErrors.password = 'Password must be at least 6 characters'
    if (formData.password !== formData.confirmPassword) newErrors.confirmPassword = 'Passwords do not match'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!validateForm()) return
    setStatus('loading')
    try {
      const payload = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: formData.role
      }
      const res = await postData('/auth/register', payload)
      console.log('✅ Registered:', res)
      setStatus('success')
      setServerMessage('Registration successful! You can now log in.')
    } catch (err: any) {
      console.error(err)
      setStatus('error')
      setServerMessage(err.message)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Create an Account</h1>
        <form onSubmit={handleSubmit} className="auth-form">
          <input name="username" placeholder="Username" value={formData.username} onChange={handleChange} />
          {errors.username && <p className="error">{errors.username}</p>}

          <input name="email" placeholder="Email" type="email" value={formData.email} onChange={handleChange} />
          {errors.email && <p className="error">{errors.email}</p>}

          <input name="password" placeholder="Password" type="password" value={formData.password} onChange={handleChange} />
          {errors.password && <p className="error">{errors.password}</p>}

          <input name="confirmPassword" placeholder="Confirm Password" type="password" value={formData.confirmPassword} onChange={handleChange} />
          {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}

          <select name="role" value={formData.role} onChange={handleChange}>
            <option value="member">Member</option>
            <option value="critic">Critic</option>
          </select>

          <button type="submit" disabled={status === 'loading'}>
            {status === 'loading' ? 'Registering...' : 'Register'}
          </button>

          {serverMessage && (
            <p className={status === 'success' ? 'success' : 'error'}>
              {serverMessage}
            </p>
          )}
        </form>
        <p className="switch-link">
          Already have an account? <Link href="/login">Login here</Link>
        </p>
      </div>
    </div>
  )
}
