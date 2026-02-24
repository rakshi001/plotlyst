import { useState, type FormEvent } from 'react'
import './App.css'

const GENRES = [
  'Fantasy',
  'Sci-Fi',
  'Mystery',
  'Romance',
  'Horror',
  'Adventure',
  'Historical Fiction',
]

interface StoryResult {
  title: string
  story: string
  characters: string[]
  world: string
}

function App() {
  const [genre, setGenre] = useState(GENRES[0])
  const [characters, setCharacters] = useState('')
  const [setting, setSetting] = useState('')
  const [theme, setTheme] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<StoryResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ genre, characters, setting, theme }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Server error')
      }
      const data: StoryResult = await res.json()
      setResult(data)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-wrapper">
      <header className="app-header">
        <h1 className="app-title">✦ Plotlyst</h1>
        <p className="app-subtitle">AI-powered story generation at your fingertips</p>
      </header>

      <main className="main-content">
        <section className="form-section card">
          <h2 className="section-heading">Craft Your Story</h2>
          <form onSubmit={handleSubmit} className="story-form">
            <div className="form-group">
              <label htmlFor="genre">Genre</label>
              <select
                id="genre"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                required
              >
                {GENRES.map((g) => (
                  <option key={g} value={g}>{g}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="characters">Characters</label>
              <input
                id="characters"
                type="text"
                placeholder="e.g. a brave knight and a wise wizard"
                value={characters}
                onChange={(e) => setCharacters(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="setting">Setting</label>
              <input
                id="setting"
                type="text"
                placeholder="e.g. medieval kingdom"
                value={setting}
                onChange={(e) => setSetting(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="theme">Theme</label>
              <input
                id="theme"
                type="text"
                placeholder="e.g. redemption and sacrifice"
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="generate-btn" disabled={loading}>
              {loading ? (
                <span className="btn-loading">
                  <span className="spinner" /> Generating…
                </span>
              ) : (
                '✦ Generate Story'
              )}
            </button>
          </form>
        </section>

        {error && (
          <div className="error-banner" role="alert">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <section className="result-section">
            <div className="result-title-block card">
              <p className="result-label">Your Story</p>
              <h2 className="result-title">{result.title}</h2>
            </div>

            <div className="result-grid">
              <div className="card world-card">
                <h3 className="card-heading">🌍 World</h3>
                <p className="world-text">{result.world}</p>
              </div>

              <div className="card characters-card">
                <h3 className="card-heading">👤 Characters</h3>
                <ul className="characters-list">
                  {result.characters.map((c, i) => (
                    <li key={i} className="character-chip">{c}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="card story-card">
              <h3 className="card-heading">📖 Story</h3>
              <div className="story-text">
                {result.story.split('\n\n').map((para, i) => (
                  <p key={i}>{para}</p>
                ))}
              </div>
            </div>
          </section>
        )}
      </main>

      <footer className="app-footer">
        <p>Built with Plotlyst — where every story begins</p>
      </footer>
    </div>
  )
}

export default App
