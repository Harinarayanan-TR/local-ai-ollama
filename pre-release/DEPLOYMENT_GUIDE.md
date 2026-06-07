# 🚀 Deployment Guide

Complete guide to run the Local AI Chat Platform locally and in production.

## Prerequisites

### For All Deployments
- **Ollama** installed and running
- Models pulled: `phi3`, `llama3`, `mistral`, `deepseek-coder`, `llava`

### For Development
- Python 3.11+
- Node.js 18+
- npm or yarn

### For Production
- Docker
- Docker Compose
- Linux server (recommended)

---

## 🏃 Development Setup (5 Minutes)

### Step 1: Start Ollama
```bash
ollama serve
```

Keep this running in a separate terminal.

### Step 2: Start Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Start Frontend

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Step 4: Login & Test

1. Open http://localhost:3000
2. Enter API key: `thoovara@hari`
3. Click "Login"
4. Start chatting! 💬

---

## 🐳 Docker Development

### Quick Start

```bash
docker-compose up -d
```

This starts:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **Ollama:** http://localhost:11434

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop All Services

```bash
docker-compose down
```

---

## 🌍 Production Deployment

### Server Requirements

**Minimum:**
- 4GB RAM
- 2 CPU cores
- 20GB disk space

**Recommended:**
- 16GB+ RAM
- 4+ CPU cores
- 50GB+ disk space (for models)

### Step 1: Deploy to Server

```bash
# Clone or copy project to server
scp -r project/ user@server:/app/

# SSH into server
ssh user@server
cd /app/project
```

### Step 2: Pull Models on Server

```bash
ollama pull phi3
ollama pull llama3
ollama pull mistral
ollama pull deepseek-coder
ollama pull llava
```

Keep Ollama running:
```bash
nohup ollama serve > /var/log/ollama.log 2>&1 &
```

### Step 3: Update Configuration

Edit `.env` file:
```bash
cp backend/.env.example backend/.env

# Update values:
OLLAMA_API_URL=http://localhost:11434
API_KEY=your_secure_api_key_here
DEBUG=False
```

### Step 4: Start with Docker Compose

```bash
docker-compose -f docker-compose.yml up -d

# Verify
docker-compose ps
```

### Step 5: Setup Reverse Proxy (nginx)

Create `/etc/nginx/sites-available/ai-chat`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000/api;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/ai-chat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Security Checklist

### Before Going Live

- [ ] Change default API key
- [ ] Set DEBUG=False
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Enable database backups
- [ ] Review CORS settings
- [ ] Add rate limiting
- [ ] Set up monitoring

### Firewall Setup (Ubuntu)

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 📊 Monitoring & Maintenance

### Check Services Status

```bash
docker-compose ps
docker stats
```

### View Logs

```bash
# Backend logs
docker logs project_backend_1 -f

# Frontend logs
docker logs project_frontend_1 -f
```

### Database Backup

```bash
# Backup database
mkdir -p ./backups
cp backend/app/database/data/chat.db ./backups/chat_$(date +%Y%m%d).db
```

---

## 🔄 Scaling

### Database Optimization

For production with PostgreSQL:

```python
# In database/config.py
DATABASE_URL = "postgresql://user:password@localhost:5432/ai_chat"
```

### Backend Instances

Use multiple backend containers with load balancing:

```yaml
# docker-compose.yml
services:
  backend1:
    build: ./backend
    ports:
      - "8001:8000"
  backend2:
    build: ./backend
    ports:
      - "8002:8000"
```

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Check Python version
python3 --version  # Should be 3.11+

# Check port usage
lsof -i :8000
```

### Frontend Won't Build

```bash
# Clear npm cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

### Ollama Connection Error

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags
```

### Database Issues

```bash
# Backup and reset
cp backend/app/database/data/chat.db ./backup.db
rm backend/app/database/data/chat.db

# Will recreate automatically
```

---

## 📈 Performance Tuning

### Backend Production

```bash
# Using gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend Optimization

```bash
npm run build

# Serve optimized build
serve -s build
```

---

## 📝 Backup Strategy

### Daily Backups

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/ai-chat"
mkdir -p $BACKUP_DIR

DATE=$(date +%Y%m%d_%H%M%S)
cp /app/project/backend/app/database/data/chat.db $BACKUP_DIR/chat_$DATE.db

# Keep last 30 days
find $BACKUP_DIR -name "chat_*.db" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

---

## 📞 Deployment Support

### Resources

- **Setup Guide:** QUICK_START.md
- **Full Docs:** README.md
- **Architecture:** PROJECT_SUMMARY.md
- **API Reference:** API_REFERENCE.md

### Verification Steps

1. Test backend: `curl http://localhost:8000/`
2. Test frontend: Open browser to port 3000
3. Test Ollama: `curl http://localhost:11434/api/tags`
4. Test API: Use Swagger UI at `/docs`

---

**Ready to deploy! 🚀**

For more details, see README.md and QUICK_START.md
