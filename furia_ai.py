import openai
from config import Config
from conversation_manager import ConversationManager
from data_manager import DataManager

class FuriaAI:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.conversation = ConversationManager()
        self.data_manager = DataManager()
        self.context = Config.AI_CONTEXT
    
    def _build_prompt(self, chat_id, user_message):
        history = self.conversation.get_history(chat_id)
        current_data = self._get_relevant_data(user_message)
        
        messages = [
            {"role": "system", "content": self.context + current_data}
        ]
        
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _get_relevant_data(self, query):
        """Extrai dados relevantes baseado na consulta"""
        query_lower = query.lower()
        
        data_snippets = []
        matches = self.data_manager.get_current_data('matches')
        stats = self.data_manager.get_current_data('team_stats')
        
        if any(word in query_lower for word in ["jogo", "partida", "calendário"]):
            if matches:
                next_match = matches[0]
                data_snippets.append(f"PRÓXIMO JOGO: {next_match['event']} - vs {next_match['opponent']} em {next_match['date']}")
        
        if any(word in query_lower for word in ["estatística", "performance", "rating"]):
            if stats:
                data_snippets.append(f"ESTATÍSTICAS RECENTES: Rating {stats['rating']} | Win rate {stats['winRate']}%")
        
        return "\n".join(data_snippets) if data_snippets else "Sem dados específicos para esta consulta."
    
    def generate_response(self, chat_id, user_message):
        try:
            messages = self._build_prompt(chat_id, user_message)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=250
            )
            
            ai_response = response.choices[0].message.content
            
            # Atualiza histórico
            self.conversation.add_message(chat_id, "user", user_message)
            self.conversation.add_message(chat_id, "assistant", ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"🐆 Oops! Erro ao gerar resposta: {str(e)}"