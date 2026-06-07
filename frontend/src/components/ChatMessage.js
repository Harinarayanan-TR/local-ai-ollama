import React from 'react';
import '../styles/ChatMessage.css';

function ChatMessage({ message }) {
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  return (
    <div className="message-pair">
      <div className="message user-message">
        <div className="message-content">
          <p>{message.user}</p>
        </div>
        <span className="message-time">{formatTime(message.timestamp)}</span>
      </div>

      <div className="message ai-message">
        <div className="message-header">
          <span className={`model-label ${message.blocked ? 'blocked' : ''}`}>{message.model}</span>
        </div>
        <div className="message-content">
          <p>{message.ai}</p>
        </div>
        <span className="message-time">{formatTime(message.timestamp)}</span>
      </div>
    </div>
  );
}

export default ChatMessage;
