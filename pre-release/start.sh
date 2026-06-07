#!/bin/bash

# Local AI Chat Platform - Development Startup Script

set -e

echo "🚀 Starting Local AI Chat Platform..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Make sure Ollama is running on port 11434"
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Backend setup
echo -e "${BLUE}🔧 Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

pip install -q -r requirements.txt

echo -e "${GREEN}✅ Backend ready${NC}"
echo ""

# Frontend setup
echo -e "${BLUE}🔧 Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install -q
fi

echo -e "${GREEN}✅ Frontend ready${NC}"
echo ""

# Summary
echo -e "${YELLOW}════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo -e "${BLUE}To start the application:${NC}"
echo ""
echo -e "${GREEN}Terminal 1 - Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  python -m uvicorn app.main:app --reload --host 0.0.0.0"
echo ""
echo -e "${GREEN}Terminal 2 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm start"
echo ""
echo -e "${BLUE}Requirements:${NC}"
echo "  ✓ Ollama running on http://localhost:11434"
echo "  ✓ Models pulled (phi3, llama3, mistral, deepseek-coder)"
echo ""
echo -e "${BLUE}Access:${NC}"
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔌 Backend API: http://localhost:8000"
echo "  📚 API Docs: http://localhost:8000/docs"
echo ""
echo -e "${BLUE}Default Credentials:${NC}"
echo "  API Key: thoovara@hari"
echo ""
echo -e "${YELLOW}════════════════════════════════════════════${NC}"
