import os
import threading
import requests
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_API = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
DEFAULT_MODEL = "phi3"

class OllamaManager:
    def __init__(self):
        self.current_model = DEFAULT_MODEL
        self.model_ids = {
            "phi3": "M01",
            "deepseek-coder": "M02",
            "mistral": "M03",
            "llama3": "M04",
            "llava": "M05",
        }
        self.available_models = list(self.model_ids.keys())
        self.forbidden_models = ["tinyllama"]
        self._generation_lock = threading.Lock()
    
    def validate_model(self, model_name: str) -> bool:
        """Validate if model is allowed to use"""
        if model_name in self.forbidden_models:
            logger.error(f"❌ Model {model_name} is forbidden")
            return False
        return model_name in self.available_models
    
    def unload_model(self, model_name: str) -> bool:
        """Unload a model from RAM"""
        try:
            logger.info(f"🔄 Unloading model: {model_name}")
            requests.post(
                f"{OLLAMA_API}/api/generate",
                json={"model": model_name, "stream": False, "keep_alive": 0}
                ,
                timeout=30,
            )
            logger.info(f"✅ Unloaded {model_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Error unloading {model_name}: {e}")
            return False
    
    def load_model(self, model_name: str) -> bool:
        """Check if model is available/loadable"""
        try:
            response = requests.get(f"{OLLAMA_API}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"].split(":")[0] for m in models]
                return model_name in model_names
            return False
        except Exception as e:
            logger.error(f"❌ Error checking model {model_name}: {e}")
            return False
    
    def switch_model(self, new_model: str) -> bool:
        """Switch from current model to new model"""
        if not self.validate_model(new_model):
            return False
        
        if new_model == self.current_model:
            return True
        
        logger.info(f"🔀 Switching: {self.current_model} → {new_model}")
        
        # Unload previous model
        self.unload_model(self.current_model)
        
        # Verify new model is available
        if not self.load_model(new_model):
            logger.error(f"❌ Model {new_model} not available")
            self.current_model = DEFAULT_MODEL
            return False
        
        self.current_model = new_model
        logger.info(f"✅ Now using: {self.current_model}")
        return True
    
    def busy_message(self, requested_model: str = None) -> str:
        model = requested_model or self.current_model
        model_id = self.model_ids.get(model, self.model_ids[DEFAULT_MODEL])
        return f"UNABLE TO LOAD MODEL. PLEASE CONTINUE THE CONVERSATION WITH MODEL ID: {model_id}"

    def prepare_model(self, requested_model: str) -> tuple[bool, str]:
        """Switch models only when the generation lock is held."""
        if not self.validate_model(requested_model):
            requested_model = DEFAULT_MODEL

        if requested_model != self.current_model:
            if not self.switch_model(requested_model):
                return False, self.busy_message(self.current_model)

        return True, requested_model

    def generate_response_locked(self, prompt: str, model: Optional[str] = None) -> tuple[str, int, str, bool]:
        """Generate one response at a time to protect host memory and CPU."""
        requested_model = model or DEFAULT_MODEL
        if not self.validate_model(requested_model):
            requested_model = DEFAULT_MODEL

        if not self._generation_lock.acquire(blocking=False):
            return self.busy_message(self.current_model), 0, self.current_model, True

        try:
            ok, model = self.prepare_model(requested_model)
            if not ok:
                return self.busy_message(self.current_model), 0, self.current_model, True

            logger.info(f"💬 Generating with {model}: {prompt[:50]}...")
            response = requests.post(
                f"{OLLAMA_API}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "keep_alive": "30m"
                },
                timeout=300,
            )
            
            if response.status_code == 200:
                data = response.json()
                text = data.get("response", "")
                tokens = data.get("eval_count", 0)
                logger.info(f"✅ Generated response ({tokens} tokens)")
                return text, tokens, self.current_model, False

            logger.error(f"❌ API error: {response.status_code}")
            return "Error generating response from Ollama.", 0, self.current_model, False
        except Exception as e:
            logger.error(f"❌ Exception in generate_response: {e}")
            return f"Error: {str(e)}", 0, self.current_model, False
        finally:
            self._generation_lock.release()

    def generate_response(self, prompt: str, model: Optional[str] = None) -> tuple:
        text, tokens, _model, _blocked = self.generate_response_locked(prompt, model)
        return text, tokens

    def reset_runtime_state(self):
        """Unload all managed models and return scheduler state to phi3."""
        for model_name in self.available_models:
            self.unload_model(model_name)
        self.current_model = DEFAULT_MODEL
    
    def get_status(self) -> dict:
        """Get current model status"""
        return {
            "current_model": self.current_model,
            "available_models": self.available_models,
            "model_ids": self.model_ids,
            "is_loading": self.load_model(self.current_model),
            "busy": self._generation_lock.locked(),
        }

ollama_manager = OllamaManager()
