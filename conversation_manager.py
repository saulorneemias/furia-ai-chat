import redis
from config import Config
import json
from datetime import timedelta

class ConversationManager:
    def __init__(self):
        self.redis = redis.from_url(Config.REDIS_URL)
        
    def _get_key(self, chat_id):
        return f"furia_chat:{chat_id}"
    
    def get_history(self, chat_id):
        key = self._get_key(chat_id)
        history = self.redis.get(key)
        return json.loads(history) if history else []
    
    def add_message(self, chat_id, role, content):
        key = self._get_key(chat_id)
        history = self.get_history(chat_id)
        
        history.append({"role": role, "content": content})
        
        # Mantém apenas as últimas 6 mensagens para contexto
        if len(history) > 6:
            history = history[-6:]
        
        self.redis.setex(key, timedelta(hours=24), json.dumps(history))
    
    def clear_history(self, chat_id):
        self.redis.delete(self._get_key(chat_id))