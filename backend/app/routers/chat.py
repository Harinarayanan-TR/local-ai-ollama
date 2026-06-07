from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
import logging
from app.database.config import get_db
from app.schemas.requests import ChatRequest, ChatResponse, ModelStatus, ModelSwitchRequest, HistoryResponse
from app.utils.ollama_manager import ollama_manager
from app.utils.router import ModelRouter
from app.utils.managers import AuthManager, MessageManager, LogManager
from app.models.database import Session as DBSession

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"]
)

@router.post("/send", response_model=ChatResponse)
def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    """Send message and get AI response"""
    start_time = time.time()
    
    # Verify session exists
    session = db.query(DBSession).filter(DBSession.id == request.session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    logger.info(f"💬 New message: {request.message[:50]}...")
    
    try:
        target_model = ModelRouter.route(
            request.message,
            auto_mode=request.auto_mode,
            current_model=request.model or "phi3"
        )
        response_text, tokens, model_used, blocked = ollama_manager.generate_response_locked(
            request.message,
            target_model
        )
        
        MessageManager.save_message(
            request.session_id,
            request.message,
            response_text,
            model_used,
            tokens,
            db
        )
        
        response_time = int((time.time() - start_time) * 1000)
        
        # Log request
        LogManager.log_request(
            "/api/chat/send",
            "POST",
            "api_key",
            200,
            response_time,
            db
        )
        
        return ChatResponse(
            response=response_text,
            model_used=model_used,
            session_id=request.session_id,
            tokens_used=tokens,
            blocked=blocked
        )
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        response_time = int((time.time() - start_time) * 1000)
        LogManager.log_request("/api/chat/send", "POST", "api_key", 500, response_time, db)
        
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=ModelStatus)
def get_status():
    """Get current model status"""
    return ModelStatus(**ollama_manager.get_status())

@router.post("/switch-model")
def switch_model(request: ModelSwitchRequest, db: Session = Depends(get_db)):
    """Manually switch to a specific model"""
    logger.info(f"🔀 Manual switch requested: {request.model}")

    session = db.query(DBSession).filter(DBSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not ollama_manager.validate_model(request.model):
        raise HTTPException(status_code=400, detail=f"Invalid model: {request.model}")
    
    if ollama_manager.get_status()["busy"]:
        return {
            "success": False,
            "current_model": ollama_manager.current_model,
            "message": ollama_manager.busy_message(ollama_manager.current_model),
            "model_ids": ollama_manager.model_ids,
        }

    success = ollama_manager.switch_model(request.model)
    
    if not success:
        logger.error(f"❌ Failed to switch to {request.model}")
        raise HTTPException(status_code=500, detail=f"Failed to switch to model: {request.model}")
    
    logger.info(f"✅ Successfully switched to {request.model}")
    return {
        "success": True,
        "current_model": ollama_manager.current_model,
        "message": f"Switched to {request.model}"
    }

@router.get("/history/{session_id}")
def get_history(session_id: str, db: Session = Depends(get_db)):
    """Get chat history for session"""
    messages = MessageManager.get_session_history(session_id, db)
    
    return HistoryResponse(
        messages=[{
            "id": msg.id,
            "user_message": msg.user_message,
            "ai_response": msg.ai_response,
            "model_used": msg.model_used,
            "timestamp": msg.timestamp.isoformat()
        } for msg in messages],
        session_id=session_id
    )
