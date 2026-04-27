import React from 'react';
import './ResultDisplay.css';

function ResultDisplay({ result }) {
  return (
    <div className="result-container">
      <div className="result-header">
        <h2>🤖 Answer</h2>
      </div>

      <div className="answer-box">
        <p className="answer-text">{result.answer}</p>
      </div>

      {result.sources && result.sources.length > 0 && (
        <div className="sources-section">
          <h3>📄 Sources</h3>
          <div className="sources-list">
            {result.sources.map((source, index) => (
              <div key={index} className="source-item">
                <div className="source-icon">📖</div>
                <div className="source-details">
                  <p className="source-name">{source.source}</p>
                  <p className="source-meta">
                    Chunk #{source.chunk_index}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {result.metadata && (
        <div className="metadata-section">
          <details>
            <summary>📊 Metadata & Performance</summary>
            <div className="metadata-content">
              {result.metadata.model && (
                <p><strong>Model:</strong> {result.metadata.model}</p>
              )}
              {result.metadata.prompt_tokens && (
                <p><strong>Prompt Tokens:</strong> {result.metadata.prompt_tokens}</p>
              )}
              {result.metadata.response_tokens && (
                <p><strong>Response Tokens:</strong> {result.metadata.response_tokens}</p>
              )}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}

export default ResultDisplay;
