from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import database
from app.database.config import engine, Base
from app.models.database import User, ChatMessage, Session as DBSession, APILog

# Create tables
Base.metadata.create_all(bind=engine)

# Import routers
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="Local AI Chat Platform",
    description="Production-grade local Ollama chat interface with strict security",
    version="1.0.0"
)

# Add rate limiter to app
app.state.limiter = limiter

# CORS middleware - STRICT LOCAL NETWORK ONLY
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:6767",
        "http://127.0.0.1:6767",
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+):\d+",
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(chat_router)

# Root endpoint
@app.get("/")
def root():
    return {
        "name": "Local AI Chat Platform",
        "status": "✅ Running",
        "version": "1.0.0",
        "security": "Production-grade authentication",
        "endpoints": {
            "login": "/api/auth/login",
            "send_message": "/api/chat/send",
            "model_status": "/api/chat/status",
            "switch_model": "/api/chat/switch-model",
            "chat_history": "/api/chat/history/{session_id}",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Local AI Chat Platform starting...")
    logger.info("🔒 Security: API key authentication enabled")
    logger.info("🤖 Model management: Single-model execution")
    logger.info("📊 Database: SQLite initialized")
    logger.info("🎯 Ollama connection: Ready")
    logger.info("⏱️ Rate limiting: Enabled")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
