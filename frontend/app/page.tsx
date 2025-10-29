// frontend/app/page.tsx
import './page.css'

export default function HomePage() {
  return (
    <section className="landing">
      <div className="landing-content">
        <h2>Welcome to WatchWorthy</h2>
        <p>
          Your go-to platform for honest movie reviews and ratings — where
          every opinion matters.  
          <br />
          Join now to explore, review, and share your thoughts.
        </p>

        <div className="landing-buttons">
          <a href="/login" className="btn-primary">Login</a>
          <a href="/register" className="btn-outline">Register</a>
        </div>
      </div>
    </section>
  )
}
