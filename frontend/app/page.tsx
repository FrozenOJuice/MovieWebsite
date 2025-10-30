'use client'

import Link from 'next/link'
import './page.css'

export default function HomePage() {
  return (
    <div className="home-container">
      <header className="home-header">
        <Link href="/" className="logo">
          WatchWorthy
        </Link>
        <nav className="nav-links">
          <Link href="/register" className="btn btn-register">Register</Link>
          <Link href="/login" className="btn btn-login">Login</Link>
        </nav>
      </header>

      <main className="home-main">
        <div className="welcome">
          <h1>Welcome to WatchWorthy</h1>
          <p>Your hub for movie reviews, ratings, and discussions.</p>
          <div className="action-buttons">
            <Link href="/register" className="btn-primary">Get Started</Link>
            <Link href="/login" className="btn-secondary">Sign In</Link>
          </div>
        </div>
      </main>

      <footer className="home-footer">
        <p>© 2025 WatchWorthy. All rights reserved.</p>
      </footer>
    </div>
  )
}
