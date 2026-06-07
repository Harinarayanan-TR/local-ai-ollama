# 📡 API Reference

Complete API documentation for Local AI Chat Platform with examples.

## Base URL

```
Development: http://localhost:8000
Production: http://{your-ip}:8000
```

## Authentication

All endpoints (except `/` and `/docs`) require valid API key.

**Credentials:**
```
API Key: thoovara@hari
```

---

## 🔑 Authentication Endpoints

### POST `/api/auth/login`

Authenticate with API key and create a session.

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "thoovara@hari"
  }'
```

**Request Body:**
```json
{
  "api_key": "thoovara@hari"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Welcome! Session 550e8400... created"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid API key"
}
```

**Status Codes:**
- `200` - Login successful
- `401` - Invalid API key
- `422` - Validation error

---

## 💬 Chat Endpoints

### POST `/api/chat/send`

Send a message and get AI response.

**Request:**
```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum computing",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "model": "phi3",
    "auto_mode": false
  }'
```

**Request Body:**
```json
{
  "message": "Explain quantum computing",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "model": "phi3",
  "auto_mode": false
}
```

**Parameters:**
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `message` | string | Yes | - | User query |
| `session_id` | string | Yes | - | From login response |
| `model` | string | No | "phi3" | Model to use |
| `auto_mode` | boolean | No | false | Auto-route to best model |

**Response (200 OK):**
```json
{
  "response": "Quantum computing harnesses quantum mechanical phenomena...",
  "model_used": "phi3",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "tokens_used": 124
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Session not found"
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Error generating response"
}
```

**Status Codes:**
- `200` - Success
- `404` - Session not found
- `500` - Generation error

**Examples:**

1. **Standard Query:**
```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python?",
    "session_id": "YOUR_SESSION_ID",
    "model": "phi3"
  }'
```

2. **Coding Question (Manual Model):**
```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a Python function to sort a list",
    "session_id": "YOUR_SESSION_ID",
    "model": "deepseek-coder"
  }'
```

3. **With Auto Routing:**
```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Debug my code",
    "session_id": "YOUR_SESSION_ID",
    "auto_mode": true
  }'
```

---

### GET `/api/chat/status`

Get current model status and available models.

**Request:**
```bash
curl http://localhost:8000/api/chat/status
```

**Response (200 OK):**
```json
{
  "current_model": "phi3",
  "available_models": [
    "phi3",
    "llama3",
    "mistral",
    "deepseek-coder",
    "llava"
  ],
  "is_running": true
}
```

**Status Codes:**
- `200` - Success

---

### POST `/api/chat/switch-model`

Manually switch to a different model.

**Request:**
```bash
curl -X POST http://localhost:8000/api/chat/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Request Body:**
```json
{
  "model": "llama3",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Parameters:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `model` | string | Yes | phi3, llama3, mistral, deepseek-coder, llava |
| `session_id` | string | Yes | From login response |

**Response (200 OK):**
```json
{
  "success": true,
  "current_model": "llama3",
  "message": "Switched to llama3"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Invalid model: tinyllama"
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Failed to switch model"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid model
- `500` - Switch failed

**Examples:**

1. **Switch to Reasoning Model:**
```bash
curl -X POST http://localhost:8000/api/chat/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "session_id": "YOUR_SESSION_ID"
  }'
```

2. **Switch to Coding Model:**
```bash
curl -X POST http://localhost:8000/api/chat/switch-model \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-coder",
    "session_id": "YOUR_SESSION_ID"
  }'
```

---

### GET `/api/chat/history/{session_id}`

Get chat history for a session.

**Request:**
```bash
curl "http://localhost:8000/api/chat/history/550e8400-e29b-41d4-a716-446655440000"
```

**Path Parameters:**
| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| `session_id` | string | Yes | From login response |

**Response (200 OK):**
```json
{
  "messages": [
    {
      "id": 1,
      "user_message": "What is Python?",
      "ai_response": "Python is a high-level programming language...",
      "model_used": "phi3",
      "timestamp": "2024-06-07T17:45:30.123456"
    },
    {
      "id": 2,
      "user_message": "Write a function to calculate factorial",
      "ai_response": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)",
      "model_used": "deepseek-coder",
      "timestamp": "2024-06-07T17:46:15.654321"
    }
  ],
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Session not found"
}
```

**Status Codes:**
- `200` - Success
- `404` - Session not found

**Query Parameters:**
Optional parameters for pagination:
```
?limit=50     # Default: 50 messages
?offset=0     # Default: 0
```

**Example with Pagination:**
```bash
curl "http://localhost:8000/api/chat/history/YOUR_SESSION_ID?limit=20&offset=0"
```

---

## 🔌 Complete Workflow Example

### 1. Login
```bash
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key": "thoovara@hari"}' | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)

echo "Session: $SESSION_ID"
```

### 2. Check Status
```bash
curl http://localhost:8000/api/chat/status
```

### 3. Send Message
```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Hello!\",
    \"session_id\": \"$SESSION_ID\",
    \"model\": \"phi3\"
  }"
```

### 4. Switch Model
```bash
curl -X POST http://localhost:8000/api/chat/switch-model \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"llama3\",
    \"session_id\": \"$SESSION_ID\"
  }"
```

### 5. Get History
```bash
curl "http://localhost:8000/api/chat/history/$SESSION_ID"
```

---

## 🚨 Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| `200` | Success | Request processed successfully |
| `400` | Bad Request | Invalid model name |
| `401` | Unauthorized | Invalid API key |
| `404` | Not Found | Session doesn't exist |
| `422` | Validation Error | Missing required field |
| `500` | Server Error | Ollama connection failed |

### Error Handling Best Practices

**JavaScript/Axios:**
```javascript
try {
  const response = await sendMessage(message, sessionId);
  console.log(response.response);
} catch (error) {
  if (error.response?.status === 401) {
    console.log('Invalid API key');
  } else if (error.response?.status === 404) {
    console.log('Session not found');
  } else {
    console.log('Error:', error.response?.data?.detail);
  }
}
```

**Python/Requests:**
```python
try:
    response = requests.post(
        'http://localhost:8000/api/chat/send',
        json={...}
    )
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"Error: {e.response.status_code} - {e.response.json()['detail']}")
```

---

## 📊 Response Fields Explained

### ChatResponse
```json
{
  "response": "The AI-generated text response",
  "model_used": "phi3",
  "session_id": "uuid-string",
  "tokens_used": 150
}
```

**Fields:**
- `response` - Generated text from the model
- `model_used` - Which model generated this
- `session_id` - Your session identifier
- `tokens_used` - Number of tokens consumed

### ChatMessage (from history)
```json
{
  "id": 1,
  "user_message": "What is AI?",
  "ai_response": "AI is...",
  "model_used": "phi3",
  "timestamp": "2024-06-07T17:45:30.123456"
}
```

**Fields:**
- `id` - Message ID in database
- `user_message` - Your question
- `ai_response` - Model's response
- `model_used` - Model that answered
- `timestamp` - ISO 8601 timestamp

---

## 🧪 Testing

### Using Postman

1. **Create Collection:** "Local AI Chat"
2. **Add Requests:**
   - `POST /api/auth/login`
   - `POST /api/chat/send`
   - `GET /api/chat/status`
   - `POST /api/chat/switch-model`
   - `GET /api/chat/history/{session_id}`

3. **Set Variables:**
   ```
   {{base_url}} = http://localhost:8000
   {{session_id}} = (extracted from login response)
   {{api_key}} = thoovara@hari
   ```

### Using cURL

```bash
#!/bin/bash

# Login
echo "🔐 Logging in..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key": "thoovara@hari"}')

SESSION_ID=$(echo $RESPONSE | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)
echo "Session: $SESSION_ID"

# Send message
echo "💬 Sending message..."
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Hello, how are you?\",
    \"session_id\": \"$SESSION_ID\",
    \"model\": \"phi3\"
  }"
```

---

## 📝 Notes

- API responses include timestamp information
- Chat history is persistent per session
- Models are unloaded after 30 minutes of inactivity
- Only one model can be active at a time
- Token counts are approximate

---

For more information, see [README.md](README.md)
