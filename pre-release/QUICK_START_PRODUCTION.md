# 🚀 Quick Start - Production System

**Status:** ✅ FULLY OPERATIONAL  
**Last Verified:** 2026-06-07

## 🎯 Current System State

```
Backend:  http://0.0.0.0:8000  ✅ RUNNING
Ollama:   http://localhost:11434  ✅ RUNNING
Database: SQLite chat.db  ✅ READY
Tests:    23/23 PASSED  ✅
```

## 🔐 Login Credentials

```
API Key: thoovara@hari
```

## �� Quick Test

### 1. Login and Get Session ID

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key": "thoovara@hari"}'
```

Response:
```json
{
  "session_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "message": "Welcome! Session..."
}
```

### 2. Check Available Models

```bash
curl http://localhost:8000/api/chat/status
```

Response:
```json
{
  "current_model": "phi3",
  "available_models": ["phi3", "llama3", "mistral", "deepseek-coder", "llava"],
  "is_loading": false
}
```

### 3. Send a Chat Message

```bash
curl -X POST http://localhost:8000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is 2+2?",
    "session_id": "<YOUR_SESSION_ID>",
    "auto_mode": false
  }'
```

Response:
```json
{
  "response": "2 + 2 = 4",
  "model_used": "phi3",
  "tokens_used": 15
}
```

## 🌐 Network Access

### From Local Machine
```
http://localhost:8000
```

### From Other Devices
Find your IP:
```bash
hostname -I
```

Then access from other device:
```
http://<YOUR_IP>:8000
```

## 📝 Notes

- phi3 is the default model on startup
- Only ONE model can be active at a time
- All chat history persisted in SQLite
- Sessions isolated per login

For detailed documentation, see README.md

---

**Status:** ✅ Production Ready  
**Test Results:** 23/23 Passed
