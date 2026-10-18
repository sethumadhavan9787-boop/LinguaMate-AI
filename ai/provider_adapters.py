import os
import json
import logging
from typing import Dict, Any, List, Optional
from config import Config

logger = logging.getLogger(__name__)

class BaseAIAdapter:
    """Base class for all provider-independent AI adapters."""
    def __init__(self, name: str):
        self.name = name

    def is_available(self) -> bool:
        return False

    def check_grammar(self, sentence: str) -> Optional[Dict[str, Any]]:
        return None

    def generate_conversation_reply(self, message: str, topic: str, level: str, history: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        return None

    def generate_quiz_questions(self, category: str, count: int) -> Optional[List[Dict[str, Any]]]:
        return None


class OfflineFallbackAdapter(BaseAIAdapter):
    """
    100% Free, zero-dependency offline fallback adapter.
    Uses rule-based linguistics and local question/dialogue banks.
    """
    def __init__(self):
        super().__init__("Offline Curated Engine")

    def is_available(self) -> bool:
        return True


class GeminiAdapter(BaseAIAdapter):
    """
    Google Gemini Free-Tier Adapter using standard requests.
    Supports gemini-1.5-flash or gemini-2.0-flash without heavy SDK dependencies.
    """
    def __init__(self, api_key: str):
        super().__init__("Google Gemini (Free-Tier)")
        self.api_key = api_key

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def generate_text(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        if not self.is_available():
            return None
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
        }
        try:
            res = requests.post(url, json=payload, timeout=8)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}")
        return None


class GroqAdapter(BaseAIAdapter):
    """
    Groq Fast Free-Tier Adapter using Groq Cloud API.
    Uses open models like llama-3.1-8b-instant.
    """
    def __init__(self, api_key: str):
        super().__init__("Groq Cloud (Free-Tier)")
        self.api_key = api_key

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def generate_text(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        if not self.is_available():
            return None
        import requests
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"Groq API call failed: {e}")
        return None


def get_ai_adapter() -> BaseAIAdapter:
    """Factory method to return the active configured AI adapter."""
    provider = Config.AI_PROVIDER
    
    if provider == "gemini" and Config.GEMINI_API_KEY:
        adapter = GeminiAdapter(Config.GEMINI_API_KEY)
        if adapter.is_available():
            return adapter
            
    if provider == "groq" and Config.GROQ_API_KEY:
        adapter = GroqAdapter(Config.GROQ_API_KEY)
        if adapter.is_available():
            return adapter
            
    # Default to Offline Curated Fallback
    return OfflineFallbackAdapter()
