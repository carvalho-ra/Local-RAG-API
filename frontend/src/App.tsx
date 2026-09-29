import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')

  async function handleSubmit(event: React.SyntheticEvent) {
    event.preventDefault()

    const response = await fetch('/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    })

    const data = await response.json()

    setAnswer(data.answer)
  }

  return (
    <main className="app">
      <header className="header">
        <div className="brand">
          <span className="signature">&gt;_</span>
          <span className="brand-name">Local RAG</span>
        </div>

        <span className="status">  
          <span className="status-dot" />
          API online
        </span>
      </header>

      <section className="hero">
        <h1>Local RAG</h1>
        <p>Faça perguntas sobre seus documentos.</p>
      </section>

      <section className="question-section">
        <form onSubmit={handleSubmit} className="question-form">
          <input
            type="text"
            placeholder="Digite sua pergunta..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />

          <button type="submit">Perguntar</button>
        </form>
      </section>

      {answer && (
        <section className="answer-section">
          <span className="section-label">RESPOSTA</span>

          <div className="answer-card">
            <p>{answer}</p>
          </div>
        </section>
      )}
    </main>
  )
}

export default App