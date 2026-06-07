# ⚡ Quick Start Guide

Get the Local AI Chat Platform running in 5 minutes!

## Prerequisites

- **Ollama** installed and running (`ollama serve`)
- **Python 3.11+** 
- **Node.js 18+**

## Step 1: Prepare Ollama Models (One-time)

```bash
ollama pull phi3
ollama pull llama3
ollama pull mistral
ollama pull deepseek-coder
ollama pull llava
```

Keep Ollama running in a separate terminal:
```bash
ollama serve
```

## Step 2: Start Backend

```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Start Frontend

In a new terminal:

```bash
cd frontend
npm install
npm start
```

Browser opens automatically at `http://localhost:3000`

## Step 4: Login & Chat

1. **API Key:** `thoovara@hari`
2. **Click Login**
3. **Start chatting!** 💬

## Verify Everything Works

### Check Backend
```bash
curl http://localhost:8000/
# Should return API info
```

### Check Ollama
```bash
curl http://localhost:11434/api/tags
# Should list available models
```

### Check Frontend
Open browser: `http://localhost:3000`

---

## Common Issues

### "Cannot connect to Ollama"

**Problem:** Backend can't reach Ollama

**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# Check connection
curl http://localhost:11434/
```

### "Port 8000 already in use"

**Solution:**
```bash
# Change port in backend startup
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### "Models not found"

**Solution:**
```bash
ollama pull phi3
ollama pull llama3
# etc...
```

### "npm start fails"

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## Next Steps

1. **Read Full Documentation** → [README.md](README.md)
2. **Backend Docs** → [backend/README.md](backend/README.md)
3. **Frontend Docs** → [frontend/README.md](frontend/README.md)
4. **API Swagger** → http://localhost:8000/docs

---

## Docker Quick Start

```bash
docker-compose up -d

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Ollama: http://localhost:11434
```

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│         User Browser                 │
│    http://localhost:3000             │
├─────────────────────────────────────┤
│       React Frontend (Port 3000)     │
│  - Login interface                   │
│  - Chat UI with animations           │
│  - Model selector                    │
├─────────────────────────────────────┤
│   FastAPI Backend (Port 8000)        │
│  - /api/auth/login                   │
│  - /api/chat/send                    │
│  - Model routing logic               │
│  - SQLite database                   │
├─────────────────────────────────────┤
│   Ollama (Port 11434)                │
│  - phi3, llama3, mistral, etc.       │
│  - Local model inference             │
└─────────────────────────────────────┘
```

## Features Highlight

✅ **ChatGPT-style UI** - Modern dark theme with animations
✅ **Multi-model support** - Switch between phi3, llama3, mistral, etc.
✅ **Smart routing** - Auto-select best model for your question
✅ **Chat history** - Persistent database of conversations
✅ **Local network** - Access from any device on WiFi
✅ **No cloud** - 100% local, all data stays on your machine

## Keyboard Shortcuts

- **Enter** - Send message
- **Shift + Enter** - New line
- **Ctrl/Cmd + L** - Toggle sidebar

## Tips

1. **First time slow?** - First inference loads the model, it will cache after
2. **Want to switch models?** - Click model name in sidebar, previous model unloads automatically
3. **Auto mode?** - Enable it to let the system pick the best model for each question
4. **Check history?** - All messages are saved in SQLite database

---

## Support

### Docs
- Main README: [README.md](README.md)
- Backend API: [backend/README.md](backend/README.md)
- Frontend UI: [frontend/README.md](frontend/README.md)

### Debug Mode

**Backend:**
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

**Frontend:**
```bash
REACT_APP_DEBUG=true npm start
```

Open DevTools (F12) to see logs and API calls.

---

## Production Deployment

See [README.md - Production Deployment](README.md#-production-deployment) section

---

**Happy Chatting! 🚀**

Questions? Check the main [README.md](README.md)
