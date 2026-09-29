import { useState } from 'react'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')

  function handleSubmit(event: React.SyntheticEvent) {
    event.preventDefault()
    setAnswer(question)
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