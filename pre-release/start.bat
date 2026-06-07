@echo off
REM Local AI Chat Platform - Development Startup Script (Windows)

echo.
echo ===================================================
echo 🚀 Local AI Chat Platform - Setup Script
echo ===================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 18+
    exit /b 1
)

echo ✅ Python found: 
python --version

echo ✅ Node.js found: 
node --version

echo.
echo 🔧 Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo ✅ Backend ready

echo.
echo 🔧 Setting up frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing dependencies...
    call npm install -q
)

echo ✅ Frontend ready

echo.
echo ===================================================
echo 🎉 Setup Complete!
echo ===================================================
echo.
echo 📝 To start the application:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python -m uvicorn app.main:app --reload --host 0.0.0.0
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm start
echo.
echo Requirements:
echo   ✓ Ollama running on http://localhost:11434
echo   ✓ Models pulled (phi3, llama3, mistral, deepseek-coder)
echo.
echo Access:
echo   🌐 Frontend: http://localhost:3000
echo   🔌 Backend: http://localhost:8000
echo   📚 Docs: http://localhost:8000/docs
echo.
echo Default API Key: thoovara@hari
echo ===================================================
echo.
pause
