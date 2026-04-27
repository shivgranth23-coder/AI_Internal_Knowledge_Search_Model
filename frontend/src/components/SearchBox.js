import React from 'react';
import './SearchBox.css';

function SearchBox({ query, setQuery, onSearch, loading, onIndexDocuments, indexed }) {
  return (
    <div className="search-box-container">
      <form onSubmit={onSearch} className="search-form">
        <div className="input-wrapper">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your documents..."
            disabled={loading || !indexed}
            className="search-input"
          />
          <button 
            type="submit" 
            disabled={loading || !indexed}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      <div className="action-buttons">
        <button
          onClick={onIndexDocuments}
          disabled={loading}
          className={`index-button ${indexed ? 'indexed' : ''}`}
        >
          {loading ? 'Indexing...' : indexed ? '✓ Documents Indexed' : 'Index Documents'}
        </button>
      </div>

      <div className="help-text">
        <p>💡 <strong>Tip:</strong> Try asking questions like:</p>
        <ul>
          <li>"What are the key concepts in product management?"</li>
          <li>"Summarize the AI-enhanced product framework"</li>
          <li>"What is the go-to-market strategy?"</li>
        </ul>
      </div>
    </div>
  );
}

export default SearchBox;
