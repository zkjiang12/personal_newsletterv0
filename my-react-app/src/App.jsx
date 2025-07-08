import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [info, setInfo] = useState("")
  const [loading, setLoading] = useState(false)
  const [storedResponses, setStoredResponses] = useState([])
  const [selectedResponse, setSelectedResponse] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const callBackend = async()=>{
    try{
      setLoading(true)
      console.log('fetching')
      const response = await fetch('https://newsletter-backend-aged-voice-3775.fly.dev/')
      // const response = await fetch('http://127.0.0.1:8080/')
      const json = await response.json()
      console.log(json)
      setInfo(json.content)
      setSelectedResponse(null) // Clear selected response when getting new content
      
      // Refresh stored responses after getting new content
      fetchStoredResponses()
      
      // Close sidebar on mobile after action
      setSidebarOpen(false)
    }catch(err){
      console.log("error :( ", err)
    } finally {
      setLoading(false)
    }
  }

  const fetchStoredResponses = async () => {
    try {
      // const response = await fetch('http://127.0.0.1:8080/supabase')
      const response = await fetch('https://newsletter-backend-aged-voice-3775.fly.dev/supabase')
      const json = await response.json()
      console.log('Stored responses:', json.data)
      
      // Process the list of content strings into proper response objects
      const processedResponses = (json.data || []).map((content, index) => {
        // Extract title from content using ### format
        let title = "Untitled Response";
        if (content && typeof content === 'string') {
          const pattern = /### (.*?) ###/;
          const match = content.match(pattern);
          if (match) {
            title = match[1].trim();
          } else {
            // Fallback: use first line as title
            const firstLine = content.split('\n')[0].trim();
            if (firstLine) {
              title = firstLine.length > 60 ? firstLine.substring(0, 60) + '...' : firstLine;
            }
          }
        }
        
        return {
          id: index + 1, // Create a simple ID based on index
          title: title,
          content: content,
          created_at: null, // No timestamp available
          preview: content && typeof content === 'string' ? 
            (content.length > 150 ? content.substring(0, 150) + '...' : content) : 
            'No content'
        };
      });
      
      setStoredResponses(processedResponses);
    } catch (err) {
      console.log("Error fetching stored responses:", err)
    }
  }

  const handleResponseClick = (response) => {
    setSelectedResponse(response)
    setInfo(response.content)
    // Close sidebar on mobile after selection
    setSidebarOpen(false)
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
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

  const getPreviewText = (response) => {
    // Use the processed preview 
    if (response.preview) {
      return response.preview;
    }
    
    // Fallback
    if (!response.content) return 'No content';
    const firstLine = response.content.split('\n')[0];
    return firstLine.length > 50 ? firstLine.substring(0, 50) + '...' : firstLine;
  }

  const getTitle = (response) => {
    // Use the processed title
    if (response.title && response.title !== 'Untitled Response') {
      return response.title.length > 60 ? response.title.substring(0, 60) + '...' : response.title;
    }
    
    return 'Untitled Response';
  }

  useEffect(()=>{
    fetchStoredResponses()
  },[])

  // Prevent body scroll when sidebar is open on mobile
  useEffect(() => {
    if (sidebarOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    // Cleanup function to reset when component unmounts
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [sidebarOpen])

  return (
    <>
      <div className='app-container'>
        {/* Mobile Menu Button */}
        <button className="mobile-menu-btn" onClick={toggleSidebar}>
          <div className="hamburger">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </button>

        {/* Sidebar Overlay for mobile */}
        {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)}></div>}

        {/* Side Panel */}
        <div className={`sidebar ${sidebarOpen ? 'sidebar-open' : ''}`}>
          <div className="sidebar-header">
            <h3>Saved Responses</h3>
            <div className="sidebar-controls">
              <button onClick={fetchStoredResponses} className="refresh-btn">
                Refresh
              </button>
              <button className="close-btn mobile-only" onClick={() => setSidebarOpen(false)}>
                ×
              </button>
            </div>
          </div>
          <div className="stored-responses">
            {storedResponses.length === 0 ? (
              <p className="no-responses">No saved responses yet</p>
            ) : (
              storedResponses.map((response, index) => (
                <div 
                  key={response.id || index} 
                  className={`response-item ${selectedResponse?.id === response.id ? 'selected' : ''}`}
                  onClick={() => handleResponseClick(response)}
                >
                  <div className="response-preview">
                    <div className="response-date">
                      {getTitle(response)}
                    </div>
                    <div className="response-text">
                      {getPreviewText(response)}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Main Content */}
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
      </div>
    </>
  )
}

export default App
