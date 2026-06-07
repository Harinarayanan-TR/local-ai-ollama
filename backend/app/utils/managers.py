import uuid
import logging
import bcrypt
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import User, ChatMessage, Session as DBSession, APILog

logger = logging.getLogger(__name__)

class AuthManager:
    """Secure API key authentication with bcrypt hashing"""
    
    # Store hashed API key for thoovara@hari
    # Hash generated: bcrypt.hashpw(b"thoovara@hari", bcrypt.gensalt()).decode()
    VALID_API_KEY_HASH = "$2b$12$...placeholder_hash..."
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key using bcrypt"""
        return bcrypt.hashpw(api_key.encode(), bcrypt.gensalt()).decode()
    
    @staticmethod
    def verify_api_key(api_key: str, hashed_key: str = None) -> bool:
        """Verify API key against hash (or hardcoded default)"""
        # Default API key for development
        if api_key == "thoovara@hari":
            logger.info("✅ API key verified (default)")
            return True
        
        # In production, verify against hashed key
        if hashed_key:
            try:
                return bcrypt.checkpw(api_key.encode(), hashed_key.encode())
            except Exception as e:
                logger.error(f"❌ Error verifying API key: {e}")
                return False
        
        logger.warning("❌ Invalid API key attempted")
        return False
    
    @staticmethod
    def create_session(api_key: str, db: Session, device_id: str = None) -> str:
        """Create or reuse a chat session bound to one device."""
        if not device_id:
            device_id = str(uuid.uuid4())

        existing = db.query(DBSession).filter(DBSession.device_id == device_id).first()
        if existing:
            existing.last_activity = datetime.utcnow()
            db.commit()
            logger.info(f"✅ Existing device session reused: {existing.id[:8]}...")
            return existing.id
        
        session_id = str(uuid.uuid4())
        new_session = DBSession(
            id=session_id,
            user_api_key=api_key,
            device_id=device_id,
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow()
        )
        
        db.add(new_session)
        db.commit()
        logger.info(f"✅ New session created: {session_id[:8]}...")
        return session_id
    
    @staticmethod
    def get_or_create_user(api_key: str, db: Session) -> User:
        """Get existing user or create new one"""
        user = db.query(User).filter(User.api_key == api_key).first()
        
        if not user:
            user = User(api_key=api_key)
            db.add(user)
            db.commit()
            logger.info(f"✅ New user created")
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user

class MessageManager:
    """Manage chat messages"""
    
    @staticmethod
    def save_message(session_id: str, user_msg: str, ai_response: str, 
                    model: str, tokens: int, db: Session):
        """Save chat message to database"""
        message = ChatMessage(
            session_id=session_id,
            user_message=user_msg,
            ai_response=ai_response,
            model_used=model,
            timestamp=datetime.utcnow(),
            tokens_used=tokens
        )
        
        db.add(message)
        db.commit()
        logger.info(f"💾 Message saved ({tokens} tokens)")
    
    @staticmethod
    def get_session_history(session_id: str, db: Session, limit: int = 50):
        """Get chat history for session"""
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
        
        return list(reversed(messages))

class LogManager:
    """Log API requests"""
    
    @staticmethod
    def log_request(endpoint: str, method: str, api_key: str, 
                   status_code: int, response_time_ms: int, db: Session):
        """Log API request"""
        log = APILog(
            endpoint=endpoint,
            method=method,
            api_key=api_key,
            status_code=status_code,
            timestamp=datetime.utcnow(),
            response_time_ms=response_time_ms
        )
        
        db.add(log)
        db.commit()
