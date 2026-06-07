import React, { useCallback, useState, useEffect, useRef } from 'react';
import { sendMessage, getStatus, getHistory, switchModel } from '../utils/api';
import Sidebar from '../components/Sidebar';
import ChatMessage from '../components/ChatMessage';
import '../styles/ChatPage.css';

function ChatPage({ sessionId, deviceId, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentModel, setCurrentModel] = useState('phi3');
  const [autoMode, setAutoMode] = useState(true);
  const [status, setStatus] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadStatus = useCallback(async () => {
    try {
      const data = await getStatus();
      setStatus(data);
      setCurrentModel(data.current_model);
    } catch (error) {
      console.error('Failed to load status:', error);
    }
  }, []);

  const loadHistory = useCallback(async () => {
    try {
      const data = await getHistory(sessionId);
      const formattedMessages = data.messages.map(msg => ({
        id: msg.id,
        type: 'message_pair',
        user: msg.user_message,
        ai: msg.ai_response,
        model: msg.model_used,
        timestamp: msg.timestamp,
      }));
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  }, [sessionId]);

  useEffect(() => {
    loadStatus();
    loadHistory();
  }, [loadStatus, loadHistory]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || loading) return;

    const userMessage = inputValue;
    setInputValue('');
    setLoading(true);

    try {
      const response = await sendMessage(
        userMessage,
        sessionId,
        currentModel,
        autoMode
      );

      const newMessage = {
        id: Date.now(),
        type: 'message_pair',
        user: userMessage,
        ai: response.response,
        model: response.model_used,
        blocked: response.blocked,
        timestamp: new Date().toISOString(),
      };

      setMessages((existingMessages) => [...existingMessages, newMessage]);
      setCurrentModel(response.model_used);

      if (autoMode) {
        loadStatus();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleModelSwitch = async (model) => {
    try {
      await switchModel(model, sessionId);
      setCurrentModel(model);
      loadStatus();
    } catch (error) {
      console.error('Failed to switch model:', error);
      alert('Failed to switch model');
    }
  };

  return (
    <div className="chat-container">
      <Sidebar
        currentModel={currentModel}
        autoMode={autoMode}
        onAutoModeToggle={() => setAutoMode(!autoMode)}
        onModelSwitch={handleModelSwitch}
        onLogout={onLogout}
        status={status}
        disabled={loading}
      />

      <div className="chat-main">
        <div className="chat-header">
          <div>
            <p className="device-label">Device {deviceId?.slice(0, 8)}</p>
            <h1>Local AI Chat</h1>
          </div>
          <div className="model-indicator">
            <span className="model-badge">
              {currentModel.toUpperCase()} {autoMode && 'AUTO'}
            </span>
          </div>
        </div>

        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <h2>Start a private local chat</h2>
              <p>Start a conversation by typing a message below</p>
            </div>
          ) : (
            messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="chat-input-form">
          <div className="input-wrapper">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask me anything..."
              disabled={loading}
              className="chat-input"
            />
            <button
              type="submit"
              disabled={loading || !inputValue.trim()}
              className="send-button"
            >
              {loading ? '⏳' : '➤'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ChatPage;
