# Backend - FastAPI Server

Production-grade FastAPI server for local Ollama AI chat platform.

## 🚀 Features

- **FastAPI Framework** - High performance async API
- **SQLAlchemy ORM** - SQLite database management
- **Ollama Integration** - Direct Ollama API communication
- **Model Routing** - Intelligent model selection based on prompt analysis
- **Session Management** - Per-session chat history
- **API Logging** - Request/response logging for debugging
- **CORS Support** - Cross-origin access for frontend

## 📁 Directory Structure

```
app/
├── main.py              # FastAPI application
├── database/
│   ├── config.py        # SQLAlchemy config
│   └── data/            # SQLite database (auto-created)
├── models/
│   └── database.py      # SQLAlchemy models
├── routers/
│   ├── auth.py          # Authentication endpoints
│   └── chat.py          # Chat endpoints
├── schemas/
│   └── requests.py      # Pydantic schemas
└── utils/
    ├── ollama_manager.py # Ollama communication
    ├── router.py        # Model routing logic
    └── managers.py      # Business logic
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```
OLLAMA_API_URL=http://localhost:11434
API_KEY=thoovara@hari
DEBUG=True
```

### Database

SQLite automatically creates at:
```
app/database/data/chat.db
```

## 📡 API Documentation

### Authentication

**Login**
```
POST /api/auth/login
{
  "api_key": "thoovara@hari"
}

Response:
{
  "success": true,
  "session_id": "uuid-string",
  "message": "Welcome! Session..."
}
```

### Chat

**Send Message**
```
POST /api/chat/send
{
  "message": "Explain Python",
  "session_id": "uuid",
  "model": "phi3",
  "auto_mode": false
}

Response:
{
  "response": "Python is a...",
  "model_used": "phi3",
  "session_id": "uuid",
  "tokens_used": 152
}
```

**Get Status**
```
GET /api/chat/status

Response:
{
  "current_model": "phi3",
  "available_models": ["phi3", "llama3", "mistral", ...],
  "is_running": true
}
```

**Switch Model**
```
POST /api/chat/switch-model
{
  "model": "llama3",
  "session_id": "uuid"
}

Response:
{
  "success": true,
  "current_model": "llama3",
  "message": "Switched to llama3"
}
```

**Get Chat History**
```
GET /api/chat/history/{session_id}

Response:
{
  "messages": [
    {
      "id": 1,
      "user_message": "Hello",
      "ai_response": "Hi there!",
      "model_used": "phi3",
      "timestamp": "2024-06-07T..."
    }
  ],
  "session_id": "uuid"
}
```

## 🤖 Model Manager

### Supported Models

- ✅ **phi3** (Default) - Fast, general purpose
- ✅ **llama3** - Reasoning, complex tasks
- ✅ **mistral** - Fast responses, summaries
- ✅ **deepseek-coder** - Code generation & debugging
- ✅ **llava** - Vision (if needed)
- ❌ **tinyllama** - FORBIDDEN

### Model Switching Logic

1. **Unload Previous Model** - Free RAM before loading new
2. **Load New Model** - Verify availability
3. **Generate Response** - Use active model
4. **Keep Alive** - 30-minute timeout before unloading

### Smart Router

**Prompt Classification:**

```python
ModelRouter.classify_prompt(prompt) -> model_name
```

Classification algorithm:
- Counts matching keywords in prompt
- Returns model with highest score
- Falls back to phi3 if no matches

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  api_key VARCHAR UNIQUE,
  created_at DATETIME,
  last_login DATETIME,
  is_active BOOLEAN
)
```

### Chat Messages Table
```sql
CREATE TABLE chat_messages (
  id INTEGER PRIMARY KEY,
  session_id VARCHAR,
  user_message TEXT,
  ai_response TEXT,
  model_used VARCHAR,
  timestamp DATETIME,
  tokens_used INTEGER
)
```

### Sessions Table
```sql
CREATE TABLE sessions (
  id VARCHAR PRIMARY KEY,
  user_api_key VARCHAR,
  created_at DATETIME,
  last_activity DATETIME,
  model_history TEXT
)
```

### API Logs Table
```sql
CREATE TABLE api_logs (
  id INTEGER PRIMARY KEY,
  endpoint VARCHAR,
  method VARCHAR,
  api_key VARCHAR,
  status_code INTEGER,
  timestamp DATETIME,
  response_time_ms INTEGER
)
```

## 🔐 Security

### API Key Validation

All endpoints (except /docs) require valid API key:
```python
# app/utils/managers.py
VALID_API_KEY = "thoovara@hari"
```

### CORS Configuration

```python
# app/main.py
CORSMiddleware(allow_origins=["*"], ...)
```

## 📊 Logging

Logs are written to console with format:
```
2024-06-07 17:00:00 - app.routers.chat - INFO - 💬 New message
```

## 🚀 Running Server

### Development
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Docker
```bash
docker build -t local-ai-backend .
docker run -p 8000:8000 local-ai-backend
```

## 🧪 Testing

### Manual API Testing

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key": "thoovara@hari"}'

# Send Message
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "session_id": "uuid",
    "model": "phi3"
  }'

# Get Status
curl http://localhost:8000/api/chat/status
```

### Interactive Docs

Open browser:
```
http://localhost:8000/docs
```

## 🔧 Troubleshooting

### Ollama Not Connecting

```python
# Check OLLAMA_API in ollama_manager.py
OLLAMA_API = "http://localhost:11434"
```

### Database Locked

```bash
# SQLite sometimes locks on concurrent writes
# Solution: Use connection pooling
```

### Model Loading Slow

```bash
# Monitor Ollama
ollama ps

# Check available RAM
free -h
```

## 📈 Performance

**Benchmarks** (on CPU):
- phi3: 5-10 tokens/sec
- llama3: 3-5 tokens/sec
- mistral: 8-12 tokens/sec
- deepseek-coder: 4-6 tokens/sec

**RAM Usage:**
- phi3: ~2-3 GB
- llama3: ~8 GB
- mistral: ~7 GB
- deepseek-coder: ~15 GB

## 🔄 Model Lifecycle

```
1. Model Requested (auto_mode or manual switch)
   ↓
2. Validate Model (not forbidden)
   ↓
3. Switch Model (unload previous)
   ↓
4. Load Model (verify availability)
   ↓
5. Generate Response
   ↓
6. Save to Database
   ↓
7. Keep Alive (30 min timeout)
```

---

For full documentation, see main [README.md](../README.md)
