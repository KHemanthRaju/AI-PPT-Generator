import React, { useState } from 'react';

import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt';

  const extractTopicAndUrls = (text) => {
    const lines = text.split('\n');
    const topic = lines[0];
    const urls = text.match(/https?:\/\/[^\s]+/g) || [];
    const slideMatch = text.toLowerCase().match(/(\d+)\s*slides?/);
    const slideCount = slideMatch ? parseInt(slideMatch[1]) : 6;
    return { topic, urls, slideCount };
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const { topic, urls, slideCount } = extractTopicAndUrls(input);
      
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description: topic,
          urls: urls,
          slide_count: slideCount
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();

      let assistantContent = '';
      if (data.download_url) {
        assistantContent = `✅ PowerPoint created successfully!\n\n[📥 Download PowerPoint](${data.download_url})`;
      } else {
        assistantContent = 'Slides generated! Download functionality requires local processing.';
      }

      // Add slide preview
      if (data.slides) {
        assistantContent += '\n\n**📋 Slide Preview:**\n';
        data.slides.slides.forEach((slide, i) => {
          assistantContent += `\n**${i + 1}. ${slide.title}**\n`;
          slide.content.forEach(bullet => {
            assistantContent += `• ${bullet}\n`;
          });
        });
      }

      setMessages(prev => [...prev, { role: 'assistant', content: assistantContent }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Error: ${error.response?.data?.error || error.message}` 
      }]);
    }

    setLoading(false);
    setInput('');
  };

  return (
    <div className="app">
      <div className="header">
        <h1>🤖 AI PowerPoint Generator</h1>
      </div>
      
      <div className="chat-container">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content.split('\n').map((line, j) => (
                <div key={j}>
                  {line.includes('[📥 Download PowerPoint]') ? (
                    <a href={line.match(/\((.*?)\)/)[1]} target="_blank" rel="noopener noreferrer" className="download-link">
                      📥 Download PowerPoint
                    </a>
                  ) : line}
                </div>
              ))}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message assistant">
            <div className="message-content">Generating PowerPoint...</div>
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Create a presentation about AI trends with these URLs: https://example.com"
          className="chat-input"
        />
        <button onClick={sendMessage} disabled={loading} className="send-button">
          Send
        </button>
      </div>
    </div>
  );
}

export default App;