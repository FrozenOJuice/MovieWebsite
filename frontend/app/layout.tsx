// frontend/app/layout.tsx
import './globals.css'
import { ReactNode } from 'react'
import Link from 'next/link'

export const metadata = {
  title: 'WatchWorthy',
  description: 'Discover and review your favorite movies',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="navbar">
          <div className="nav-container">
            {/* ✅ Logo now links to homepage */}
            <Link href="/" className="logo">
              WatchWorthy
            </Link>

            <nav>
              <Link href="/about">About</Link>
              <Link href="/login">Login</Link>
              <Link href="/register" className="btn-primary">Sign Up</Link>
            </nav>
          </div>
        </header>

        <main>{children}</main>

        <footer className="footer">
          <p>© {new Date().getFullYear()} WatchWorthy. All rights reserved.</p>
        </footer>
      </body>
    </html>
  )
}
