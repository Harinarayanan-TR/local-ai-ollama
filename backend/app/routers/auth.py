from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database.config import get_db
from app.schemas.requests import LoginRequest, LoginResponse
from app.utils.managers import AuthManager
import time
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """API key based login with secure authentication"""
    start_time = time.time()
    
    if not AuthManager.verify_api_key(request.api_key):
        logger.warning(f"❌ Login failed: Invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Create or get user
    user = AuthManager.get_or_create_user(request.api_key, db)
    
    # Create new session
    device_id = request.device_id or str(uuid.uuid4())
    session_id = AuthManager.create_session(request.api_key, db, device_id)
    
    response_time = int((time.time() - start_time) * 1000)
    logger.info(f"✅ User logged in successfully ({response_time}ms)")
    
    return LoginResponse(
        success=True,
        session_id=session_id,
        device_id=device_id,
        message=f"Welcome! Session {session_id[:8]}... created"
    )
