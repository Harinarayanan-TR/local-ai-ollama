import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || `${window.location.origin}/api`;

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth API
export const login = async (apiKey, deviceId) => {
  try {
    const response = await apiClient.post('/auth/login', {
      api_key: apiKey,
      device_id: deviceId,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Chat API
export const sendMessage = async (message, sessionId, model = 'phi3', autoMode = false) => {
  try {
    const response = await apiClient.post('/chat/send', {
      message,
      session_id: sessionId,
      model,
      auto_mode: autoMode,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getStatus = async () => {
  try {
    const response = await apiClient.get('/chat/status');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const switchModel = async (model, sessionId) => {
  try {
    const response = await apiClient.post('/chat/switch-model', {
      model,
      session_id: sessionId,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getHistory = async (sessionId) => {
  try {
    const response = await apiClient.get(`/chat/history/${sessionId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};
