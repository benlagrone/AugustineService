// src/App.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function Message({ role, message, persona }) {
  return (
    <div className={`message ${role === 'user' ? 'user-message' : 'assistant-message'}`}>
      <span className="message-role">{role === 'user' ? 'You' : persona}:</span>
      <p>{message}</p>
    </div>
  );
}

function ChatControls({ persona, setPersona, mode, setMode, onTestMemory, hasMessages }) {
  return (
    <div className="controls">
      <label>
        Persona:
        <select value={persona} onChange={(e) => setPersona(e.target.value)}>
          <option value="Augustine">Augustine</option>
          <option value="Freud">Freud</option>
        </select>
      </label>
      
      <label>
        Mode:
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="conversation">Conversation</option>
          <option value="reference">Reference</option>
        </select>
      </label>

      <button 
        onClick={onTestMemory} 
        disabled={!hasMessages}
        className="memory-test-btn"
      >
        Test Memory
      </button>
    </div>
  );
}

function ChatInput({ query, setQuery, onSubmit, loading }) {
  return (
    <form onSubmit={onSubmit} className="input-form">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
        disabled={loading}
      />
      <button type="submit" disabled={loading}>Send</button>
    </form>
  );
}

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState('');
  const [persona, setPersona] = useState('Augustine');
  const [mode, setMode] = useState('conversation');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (messageText) => {
    setLoading(true);
    try {
      const res = await axios.post('/api/chat', {
        question: messageText,
        mode: mode,
        persona: persona,
        session_id: sessionId
      });

      if (!sessionId && res.data.session_id) {
        setSessionId(res.data.session_id);
      }

      setMessages(prev => [...prev, { role: 'assistant', message: res.data.response }]);
      return true;
    } catch (error) {
      console.error('Error fetching response:', error);
      setError('Error fetching response');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setError('');
    const messageText = query.trim();
    setQuery('');
    setMessages(prev => [...prev, { role: 'user', message: messageText }]);
    
    await sendMessage(messageText);
  };

  const testMemory = async () => {
    if (loading || messages.length < 2) return;

    const memoryTestQuestion = "What did we discuss in our previous messages?";
    setMessages(prev => [...prev, { role: 'user', message: memoryTestQuestion }]);
    await sendMessage(memoryTestQuestion);
  };

  return (
    <div className="App">
      <h1>Chat with Augustine</h1>
      
      {sessionId && (
        <div className="session-info">
          Session ID: {sessionId}
        </div>
      )}

      <ChatControls 
        persona={persona}
        setPersona={setPersona}
        mode={mode}
        setMode={setMode}
        onTestMemory={testMemory}
        hasMessages={messages.length >= 2}
      />

      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <Message 
              key={index}
              role={msg.role}
              message={msg.message}
              persona={persona}
            />
          ))}
          {loading && (
            <div className="message assistant-message">
              <span className="message-role">{persona}:</span>
              <p className="typing-indicator">Thinking...</p>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <ChatInput 
          query={query}
          setQuery={setQuery}
          onSubmit={handleSubmit}
          loading={loading}
        />
      </div>

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;