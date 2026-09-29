import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [isThinking, setIsThinking] = useState(false)

  async function handleSubmit(event: React.SyntheticEvent) {
    event.preventDefault()

    setIsThinking(true)

    try {
      const response = await fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Erro ${response.status}: ${errorText}`)
      }

      const data = await response.json()

      setAnswer(data.answer)
    } catch (error) {
      console.error('Erro ao consultar a API:', error)
      setAnswer('Não foi possível obter uma resposta da API.')
    } finally {
      setIsThinking(false)
    }
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

      {isThinking && (
        <section className="answer-section">
          <span className="section-label">PENSANDO...</span>
        </section>
      )}

      {answer && !isThinking && (
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