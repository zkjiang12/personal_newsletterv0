import { useState } from 'react'
import './App.css'

function App() {
  const [info, setInfo] = useState("")
  const [loading, setLoading] = useState(false)

  const callBackend = async()=>{
    try{
      setLoading(true)
      console.log('fetching')
      const response = await fetch('https://newsletter-backend-aged-voice-3775.fly.dev/')
      const json = await response.json()
      console.log(json)
      setInfo(json.content)
    }catch(err){
      console.log("error :( ", err)
    } finally {
      setLoading(false)
    }
  }

  const formatText = (text) => {
    if (!text) return '';
    
    return text
      .split('\n')
      .map(line => {
        // Handle headers
        if (line.startsWith('###')) {
          return `<h3>${line.replace('###', '').trim()}</h3>`;
        }
        
        // Handle bullet points
        if (line.trim().startsWith('*')) {
          return `<div class="bullet-point">${line.replace(/^\s*\*\s*/, '• ')}</div>`;
        }
        
        // Handle bold text
        if (line.includes('**')) {
          const boldFormatted = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
          return `<div class="text-line">${boldFormatted}</div>`;
        }
        
        // Regular text
        if (line.trim()) {
          return `<div class="text-line">${line}</div>`;
        }
        
        // Empty line
        return '<div class="space"></div>';
      })
      .join('');
  };

  return (
    <>
      <div className='main-container'>
        <div className="title-container">
          <h1>Personalized Newsletter</h1>
          <p>Stay up to date with AI + Robotics research</p>
          <button 
            onClick={callBackend} 
            disabled={loading}
            className={loading ? 'loading' : ''}
          >
            {loading ? 'Updating...' : 'Update Me'}
          </button>
        </div>
        <div className="info">
          {loading ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Searching for latest research...</p>
            </div>
          ) : (
            <div className="content">
              <div 
                className="newsletter-content" 
                dangerouslySetInnerHTML={{ __html: formatText(info) }}
              />
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default App
