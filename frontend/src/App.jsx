import { useState } from 'react'
import './App.css'

function App() {
  const [email, setEmail] = useState("")
  const [subject, setSubject] = useState("")
  const [body, setBody] = useState("")
  const [analysis, setAnalysis] = useState(null)

async function handleAddClick(){
    const response = await fetch("http://127.0.0.1:8000/analysis", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
  },
        body: JSON.stringify({email,subject,body }),
        })
    const data = await response.json()
    setAnalysis(data)
    }
   return (
    <>
    <div className="form">
        <h1>Phishing Radar </h1>
        <label> Email <input placeholder = "email" value={email} onChange={e => setEmail(e.target.value)} /> </label>
        <label> Subject<input placeholder = "subject" value={subject} onChange={e => setSubject(e.target.value)} /> </label>
        <label> Body<textarea placeholder = "body" value={body} onChange={e => setBody(e.target.value)} /> </label>
          <button onClick={handleAddClick}>
            Add
          </button>
    </div>
    <div className="result">
        {analysis && <p>{analysis.explanation}</p>}
        {analysis && <p>{analysis.is_a_threat ? "⚠️ Phishing" : "✅ Safe"}</p>}
        {analysis && <ul>{analysis.signals.map((signal, index) => <li key={index}>{signal}</li>)}</ul>}
        {analysis && <p>{analysis.official_email ? analysis.official_email : null}</p>}
    </div>

    </>
  );
}

export default App
