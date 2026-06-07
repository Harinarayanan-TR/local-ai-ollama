import React, { useState } from 'react';
import '../styles/Sidebar.css';

function Sidebar({ currentModel, autoMode, onAutoModeToggle, onModelSwitch, onLogout, status, disabled }) {
  const [expanded, setExpanded] = useState(false);

  const models = ['phi3', 'deepseek-coder', 'mistral', 'llama3', 'llava'];
  const modelIds = status?.model_ids || {
    phi3: 'M01',
    'deepseek-coder': 'M02',
    mistral: 'M03',
    llama3: 'M04',
    llava: 'M05',
  };

  return (
    <div className={`sidebar ${expanded ? 'expanded' : 'collapsed'}`}>
      <button
        className="toggle-button"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? '✕' : '☰'}
      </button>

      {expanded && (
        <div className="sidebar-content">
          <div className="sidebar-section">
            <h3>Models</h3>
            <div className="model-list">
              {models.map((model) => (
                <button
                  key={model}
                  className={`model-button ${model === currentModel ? 'active' : ''}`}
                  onClick={() => onModelSwitch(model)}
                  disabled={disabled}
                >
                  <span className="model-name">{model}</span>
                  <span className="model-id">{modelIds[model]}</span>
                  {model === currentModel && <span className="active-indicator">✓</span>}
                </button>
              ))}
            </div>
          </div>

          <div className="sidebar-section">
            <div className="auto-mode-toggle">
              <label htmlFor="autoMode">Auto select</label>
              <input
                type="checkbox"
                id="autoMode"
                checked={autoMode}
                onChange={onAutoModeToggle}
              />
            </div>
          </div>

          {status && (
            <div className="sidebar-section">
              <h3>Status</h3>
              <div className="status-info">
                <p>
                  <strong>Current:</strong> {status.current_model}
                </p>
                <p className={status.busy ? 'offline' : 'running'}>
                  <strong>Queue:</strong> {status.busy ? 'Busy' : 'Ready'}
                </p>
              </div>
            </div>
          )}

          <button onClick={onLogout} className="logout-button">
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

export default Sidebar;
