import React, { useMemo, useState } from 'react';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import './styles/App.css';

function App() {
  const storedSession = localStorage.getItem('local-ai-session-id');
  const storedDevice = localStorage.getItem('local-ai-device-id');
  const [sessionId, setSessionId] = useState(storedSession);
  const [deviceId, setDeviceId] = useState(storedDevice);

  const initialPath = useMemo(() => window.location.pathname, []);

  const handleLoginSuccess = (newSessionId, newDeviceId) => {
    localStorage.setItem('local-ai-session-id', newSessionId);
    localStorage.setItem('local-ai-device-id', newDeviceId);
    setSessionId(newSessionId);
    setDeviceId(newDeviceId);
    window.history.pushState({}, '', `/chat/${newDeviceId}`);
  };

  const handleLogout = () => {
    localStorage.removeItem('local-ai-session-id');
    setSessionId(null);
    window.history.pushState({}, '', '/');
  };

  return (
    <div className="app">
      {!sessionId ? (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      ) : (
        <ChatPage
          sessionId={sessionId}
          deviceId={deviceId}
          initialPath={initialPath}
          onLogout={handleLogout}
        />
      )}
    </div>
  );
}

export default App;
