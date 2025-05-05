import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # APIs externas
    HLTV_API = "https://hltv-api.vercel.app/api"
    SPORTDATA_API = os.getenv('SPORTDATA_API')
    
    # Contexto do assistente
    AI_CONTEXT = """
    Você é o FURIA FanBot, assistente virtual para torcedores da FURIA Esports (CS:GO). 
    Personalidade: entusiasmada, detalhista e bem-informada.
    
    Diretrizes:
    1. Priorize informações dos dados fornecidos
    2. Mantenha respostas entre 1-3 parágrafos
    3. Use emojis relevantes (🐆, 🔥, 🎉)
    4. Considere o histórico da conversa
    """