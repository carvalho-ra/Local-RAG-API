import { useEffect, useRef, useState } from 'react'
import './App.css'

type Document = {
  id: number
  filename: string
  created_at: string
}

type Message = {
  role: 'user' | 'assistant'
  content: string
}

function App() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [conversationId, setConversationId] = useState<number | null>(null)
  const [isThinking, setIsThinking] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadMessage, setUploadMessage] = useState('')

  const [documents, setDocuments] = useState<Document[]>([])

  async function loadDocuments() {
    try {
      const response = await fetch('/documents')

      if (!response.ok) {
        throw new Error(`Erro ${response.status}`)
      }

      const data = await response.json()
      setDocuments(data)
    } catch (error) {
      console.error('Erro ao carregar documentos:', error)
    }
  }

  useEffect(() => {
    async function loadInitialDocuments() {
      try {
        const response = await fetch('/documents')

        if (!response.ok) {
          throw new Error(`Erro ${response.status}`)
        }

        const data = await response.json()
        setDocuments(data)
      } catch (error) {
        console.error('Erro ao carregar documentos:', error)
      }
    }

    loadInitialDocuments()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSubmit(event: React.SyntheticEvent) {
    event.preventDefault()

    setIsThinking(true)

    try {
      const response = await fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          conversation_id: conversationId,
        }),
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Erro ${response.status}: ${errorText}`)
      }

      const data = await response.json()

      setConversationId(data.conversation_id)

      setMessages((currentMessages) => [
        ...currentMessages,
        { role: 'user', content: question },
        { role: 'assistant', content: data.answer },
      ])

      setQuestion('')
    } catch (error) {
      console.error('Erro ao consultar a API:', error)

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: 'assistant',
          content: 'Não foi possível obter uma resposta da API.',
        },
      ])
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
    setUploadMessage('Processando documento...')

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

      await loadDocuments()
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

      <div className="workspace">
        <aside className="documents-panel">
          <div className="documents-header">
            <span className="section-label">DOCUMENTOS</span>
          </div>

          <div className="documents-list">
            {documents.length === 0 ? (
              <p className="empty-documents">
                Nenhum documento.
              </p>
            ) : (
              documents.map((document) => (
                <div key={document.id} className="document-item">
                  <span className="document-icon">📄</span>
                  <span className="document-name">
                    {document.filename}
                  </span>
                </div>
              ))
            )}
          </div>

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
              {file.name}
            </p>
          )}

          {uploadMessage && (
            <p className="upload-message">
              {uploadMessage}
            </p>
          )}
        </aside>

        <section className="chat-panel">
          <section className="conversation-section">
            <span className="section-label">CONVERSA</span>

            <div className="conversation">
              <div className="messages">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`message ${message.role}`}
                  >
                    <span className="message-role">
                      {message.role === 'user' ? 'Você' : 'RAG'}
                    </span>

                    <div className="answer-card">
                      <p>{message.content}</p>
                    </div>
                  </div>
                ))}

                <div ref={messagesEndRef} />
              </div>
            </div>
          </section>

          {isThinking && (
            <section className="thinking">
              <span className="section-label">PENSANDO...</span>
            </section>
          )}

          <section className="question-section">
            <form onSubmit={handleSubmit} className="question-form">
              <input
                type="text"
                placeholder="Digite sua pergunta..."
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                disabled={isThinking}
              />

              <button
                type="submit"
                disabled={isThinking || !question.trim()}
              >
                Perguntar
              </button>
            </form>
          </section>
        </section>
      </div>
    </main>
  )
}

export default App