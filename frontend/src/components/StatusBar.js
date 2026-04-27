import React from 'react';
import './StatusBar.css';

function StatusBar({ status, indexed }) {
  if (!status) {
    return (
      <div className="status-bar error">
        <div className="status-content">
          <span className="status-icon">⚠️</span>
          <span className="status-text">Backend API not connected</span>
        </div>
      </div>
    );
  }

  const ollamaStatus = status.ollama?.connected ? 'connected' : 'disconnected';
  const ollamaClass = status.ollama?.connected ? 'success' : 'warning';
  const indexStatus = indexed ? 'indexed' : 'not-indexed';
  const indexClass = indexed ? 'success' : 'warning';

  return (
    <div className="status-bar">
      <div className="status-grid">
        <div className={`status-item ${ollamaClass}`}>
          <span className="status-icon">🤖</span>
          <div className="status-info">
            <p className="status-label">Ollama LLM</p>
            <p className="status-value">{ollamaStatus}</p>
          </div>
        </div>

        <div className={`status-item ${indexClass}`}>
          <span className="status-icon">📚</span>
          <div className="status-info">
            <p className="status-label">Documents</p>
            <p className="status-value">
              {status.database.total_documents} chunks indexed
            </p>
          </div>
        </div>

        <div className="status-item info">
          <span className="status-icon">📍</span>
          <div className="status-info">
            <p className="status-label">Documents Folder</p>
            <p className="status-value">{status.documents_directory.split('\\').pop()}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StatusBar;
