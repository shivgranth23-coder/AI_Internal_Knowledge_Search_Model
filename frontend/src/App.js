import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import SearchBox from './components/SearchBox';
import ResultDisplay from './components/ResultDisplay';
import StatusBar from './components/StatusBar';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState(null);
  const [indexed, setIndexed] = useState(false);

  // Check system status on mount
  useEffect(() => {
    checkStatus();
    // Check every 5 seconds
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const checkStatus = async () => {
    try {
      const response = await axios.get('/status');
      setStatus(response.data);
      setIndexed(response.data.database.total_documents > 0);
      setError(null);
    } catch (err) {
      setError('Cannot connect to API. Make sure backend is running on http://localhost:8000');
      setStatus(null);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    if (!indexed) {
      setError('Documents not indexed yet. Please index documents first.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('/search', {
        query: query,
        top_k: 5,
        temperature: 0.7,
        max_tokens: 500
      });

      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || 'Search failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error during search. Check that Ollama is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleIndexDocuments = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/index');
      
      if (response.data.success) {
        setIndexed(true);
        setError(`Successfully indexed ${response.data.chunks_created} chunks from ${response.data.documents_processed} documents`);
        await checkStatus();
      } else {
        setError(response.data.error || 'Indexing failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error during indexing');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>📚 PDF Knowledge Search</h1>
        <p>Ask questions about your internal documents</p>
      </header>

      <StatusBar status={status} indexed={indexed} />

      <main className="container">
        <div className="search-section">
          <SearchBox 
            query={query}
            setQuery={setQuery}
            onSearch={handleSearch}
            loading={loading}
            onIndexDocuments={handleIndexDocuments}
            indexed={indexed}
          />

          {error && <div className="error-message">{error}</div>}

          {result && <ResultDisplay result={result} />}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Searching your documents...</p>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>Powered by FastAPI + Ollama + RAG Architecture</p>
      </footer>
    </div>
  );
}

export default App;
