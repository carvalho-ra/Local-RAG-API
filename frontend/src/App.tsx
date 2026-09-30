import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [isThinking, setIsThinking] = useState(false)

  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadMessage, setUploadMessage] = useState('')

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

  async function handleUpload(event: React.SyntheticEvent) {
    event.preventDefault()

    if (!file) {
      setUploadMessage('Selecione um arquivo.')
      return
    }

    setIsUploading(true)
    setUploadMessage('Enviando arquivo...')

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Erro ${response.status}: ${errorText}`)
      }

      const data = await response.json()

      if (data.error) {
        setUploadMessage(data.error)
        return
      }

      setUploadMessage(data.message)
      setFile(null)
    } catch (error) {
      console.error('Erro ao enviar arquivo:', error)
      setUploadMessage('Não foi possível enviar o arquivo.')
    } finally {
      setIsUploading(false)
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
            disabled={isThinking}
          />

          <button type="submit" disabled={isThinking}>
            Perguntar
          </button>
        </form>
      </section>

      <section className="upload-section">
        <form onSubmit={handleUpload} className="upload-form">
          <input
            type="file"
            accept=".pdf,.md,.txt"
            onChange={(event) => {
              setFile(event.target.files?.[0] ?? null)
              setUploadMessage('')
            }}
            disabled={isUploading}
          />

          <button type="submit" disabled={!file || isUploading}>
            {isUploading ? 'Enviando...' : 'Enviar documento'}
          </button>
        </form>

        {file && (
          <p className="upload-file">
            Arquivo selecionado: {file.name}
          </p>
        )}

        {uploadMessage && (
          <p className="upload-message">
            {uploadMessage}
          </p>
        )}
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
