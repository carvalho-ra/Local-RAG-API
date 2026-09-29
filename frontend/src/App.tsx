import { useState } from 'react'

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
      body: JSON.stringify({question})
    })

    const data = await response.json()

    setAnswer(data.answer)
  }

  return (
    <main>
      <h1>Local RAG</h1>
      <p>Faça perguntas sobre seus documentos.</p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Digite sua pergunta..."
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
        />
        <button type="submit">Perguntar</button>
      </form>

      {answer && <p>{answer}</p>}
    </main>
  )
}

export default App