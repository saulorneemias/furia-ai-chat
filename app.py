import os
import logging
import random
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv
import ollama

# Configurações iniciais
load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Dados estáticos da FURIA
FURIA_DATA = {
    "elenco": {
        "jogadores": [
            {"nome": "KSCERATO", "funcao": "Entry Fragger", "rating": 1.24},
            {"nome": "yuurih", "funcao": "Rifler", "rating": 1.18},
            {"nome": "arT", "funcao": "IGL/Capitão", "rating": 1.10},
            {"nome": "saffee", "funcao": "AWPer", "rating": 1.15},
            {"nome": "chelo", "funcao": "Support", "rating": 1.08}
        ],
        "tecnico": "guerri"
    },
    "proximos_jogos": [
        {"adversario": "Team Vitality", "data": "25/05", "horario": "19:00", "torneio": "ESL Pro League"},
        {"adversario": "Natus Vincere", "data": "01/06", "horario": "16:00", "torneio": "BLAST Premier"}
    ]
}

RESPOSTAS = {
    "start": "🐆🔥 *FURIA FanBot* 🔥🐆\n\nPergunte sobre jogadores, próximos jogos ou resultados!",
    "elenco": "👥 *Elenco FURIA* 👥\n" + "\n".join(
        f"➡ {p['nome']} ({p['funcao']}) | Rating: {p['rating']}" 
        for p in FURIA_DATA["elenco"]["jogadores"]
    ),
    "proximos_jogos": "🗓️ *Próximos Jogos*\n" + "\n".join(
        f"⚔️ vs {j['adversario']} ({j['torneio']})\n⏰ {j['data']} às {j['horario']} BRT" 
        for j in FURIA_DATA["proximos_jogos"]
    ),
    "motivacional": [
        "🎉 VAMO JUNTÃO! #DIADEFURIA",
        "🔥 ESSE ANO É NOSSO!",
        "🐆 FURIA É GUERREIRA!"
    ]
}

def generate_ai_response(prompt: str) -> str:
    """Gera resposta usando Ollama com contexto da FURIA (versão síncrona)"""
    try:
        response = ollama.chat(
            model='llama3.2:latest',  # Altere para o modelo que aparece no seu 'ollama list'
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    Você é o FURIA FanBot, um assistente virtual que responde como torcedor animado.
                    Dados atuais: {FURIA_DATA}
                    Regras:
                    - Responda em português brasileiro
                    - Seja breve e animado
                    - Use emojis quando apropriado
                    - Mantenha o foco em CS:GO/FURIA/VALORANT/LEAGUE OF LEGENDS
                    
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={'temperature': 0.7, 'num_predict': 100}
        )
        return response['message']['content']
    except Exception as e:
        logging.error(f"Erro Ollama: {e}")
        return None

async def get_static_response(prompt: str) -> str:
    """Fallback com respostas estáticas"""
    prompt_lower = prompt.lower()
    
    if any(p["nome"].lower() in prompt_lower for p in FURIA_DATA["elenco"]["jogadores"]):
        return RESPOSTAS["elenco"]
    elif any(t in prompt_lower for t in ["jogo", "partida", "calendário"]):
        return RESPOSTAS["proximos_jogos"]
    elif any(t in prompt_lower for t in ["vamo", "bora", "furia"]):
        return random.choice(RESPOSTAS["motivacional"])
    else:
        return "🤖 Pergunte sobre: /jogadores, /proximojogos"

# Handlers do Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RESPOSTAS["start"], parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    
    # Chamada assíncrona da função síncrona
    loop = asyncio.get_event_loop()
    ai_response = await loop.run_in_executor(None, generate_ai_response, user_input)
    
    if ai_response:
        # Limita a resposta para evitar erros no Telegram
        await update.message.reply_text(ai_response[:400], parse_mode="Markdown")
        return
    
    # Fallback estático
    static_response = await get_static_response(user_input)
    await update.message.reply_text(static_response, parse_mode="Markdown")

def setup_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jogadores", 
        lambda u,c: u.message.reply_text(RESPOSTAS["elenco"], parse_mode="Markdown")))
    application.add_handler(CommandHandler("proximojogos", 
        lambda u,c: u.message.reply_text(RESPOSTAS["proximos_jogos"], parse_mode="Markdown")))
    
    # Mensagens genéricas
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return application

# Rotas Flask
@app.route('/webhook', methods=['POST'])
async def webhook():
    application = setup_bot()
    update = Update.de_json(request.get_json(), application.bot)
    await application.process_update(update)
    return jsonify(status="success")

@app.route('/')
def health_check():
    return "🐆 FURIA FanBot Online - Use /start no Telegram"

if __name__ == '__main__':
    # Verifica conexão com Ollama
    try:
        models = ollama.list()
        logging.info(f"Modelos Ollama disponíveis: {[m['name'] for m in models['models']]}")
        logging.info("Bot pronto para receber mensagens!")
    except Exception as e:
        logging.error(f"Falha ao conectar no Ollama: {e}")
        logging.warning("O bot usará apenas respostas estáticas")

    bot = setup_bot()
    bot.run_polling()