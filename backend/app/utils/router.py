import re
import logging

logger = logging.getLogger(__name__)

class ModelRouter:
    """Conservative model routing that defaults to phi3."""
    
    CODING_KEYWORDS = [
        "code", "function", "script", "python", "javascript", "java", "cpp", "rust",
        "debug", "error", "bug", "algorithm", "data structure", "api", "sql", "html",
        "css", "framework", "library", "package", "module", "class", "variable"
    ]
    
    REASONING_KEYWORDS = [
        "deep analysis", "long reasoning", "complex reasoning", "prove", "derive",
        "mathematical proof", "multi-step", "architecture review"
    ]
    
    FAST_KEYWORDS = [
        "summarize this long text", "rewrite", "draft", "polish"
    ]

    VISION_KEYWORDS = ["image", "photo", "screenshot", "visual", "picture", "diagram"]
    
    @staticmethod
    def classify_prompt(prompt: str) -> str:
        """Classify prompt to determine best model"""
        prompt_lower = prompt.lower()
        
        coding_score = sum(1 for kw in ModelRouter.CODING_KEYWORDS if kw in prompt_lower)
        reasoning_score = sum(1 for kw in ModelRouter.REASONING_KEYWORDS if kw in prompt_lower)
        fast_score = sum(1 for kw in ModelRouter.FAST_KEYWORDS if kw in prompt_lower)
        vision_score = sum(1 for kw in ModelRouter.VISION_KEYWORDS if kw in prompt_lower)
        
        if vision_score >= 2:
            logger.info(f"🔀 Classification: VISION (score: {vision_score})")
            return "llava"
        if coding_score >= 2 and coding_score > reasoning_score:
            logger.info(f"🔀 Classification: CODING (score: {coding_score})")
            return "deepseek-coder"
        if reasoning_score >= 1:
            logger.info(f"🔀 Classification: REASONING (score: {reasoning_score})")
            return "llama3"
        if fast_score >= 1:
            logger.info(f"🔀 Classification: WRITING (score: {fast_score})")
            return "mistral"
        logger.info(f"🔀 Classification: DEFAULT")
        return "phi3"
    
    @staticmethod
    def route(prompt: str, auto_mode: bool = False, current_model: str = "phi3") -> str:
        """Route prompt to best model"""
        if not auto_mode:
            return current_model
        
        best_model = ModelRouter.classify_prompt(prompt)
        logger.info(f"✅ Routed to: {best_model}")
        return best_model
