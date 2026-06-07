from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    api_key: str
    device_id: Optional[str] = None

class LoginResponse(BaseModel):
    success: bool
    session_id: str
    device_id: str
    message: str

class ChatRequest(BaseModel):
    message: str
    session_id: str
    model: Optional[str] = "phi3"
    auto_mode: bool = True

class ChatResponse(BaseModel):
    response: str
    model_used: str
    session_id: str
    tokens_used: Optional[int] = 0
    blocked: bool = False

class ModelStatus(BaseModel):
    current_model: str
    available_models: list
    model_ids: dict
    is_loading: bool
    busy: bool

class ModelSwitchRequest(BaseModel):
    model: str
    session_id: str

class HistoryResponse(BaseModel):
    messages: list
    session_id: str
