import React, { useState } from 'react';
import { login } from '../utils/api';
import '../styles/Login.css';

function LoginPage({ onLoginSuccess }) {
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const getDeviceId = () => {
    const existing = localStorage.getItem('local-ai-device-id');
    if (existing) return existing;
    const generated = crypto.randomUUID();
    localStorage.setItem('local-ai-device-id', generated);
    return generated;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await login(apiKey, getDeviceId());
      if (response.success) {
        onLoginSuccess(response.session_id, response.device_id);
      }
    } catch (err) {
      setError(err.detail || 'Login failed. Please check your API key.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <main className="login-card">
        <div className="login-header">
          <p className="login-kicker">Local WiFi AI</p>
          <h1>Sign in</h1>
          <p>Private Ollama chat for this network.</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="apiKey">API Key</label>
            <input
              type="password"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your API key"
              disabled={loading}
              className="form-input"
            />
          </div>

          {error && <div className="error-message">❌ {error}</div>}

          <button
            type="submit"
            disabled={loading || !apiKey}
            className="login-button"
          >
            {loading ? 'Authenticating...' : 'Login'}
          </button>
        </form>

      </main>
    </div>
  );
}

export default LoginPage;
