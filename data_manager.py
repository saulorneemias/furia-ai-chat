import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
import os

class DataManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_schedules()
        
    def setup_schedules(self):
        # Atualiza a cada 30 minutos
        self.scheduler.add_job(self.update_matches, 'interval', minutes=30)
        self.scheduler.add_job(self.update_team_stats, 'interval', hours=1)
        self.scheduler.start()
    
    def update_matches(self):
        try:
            response = requests.get(f"{Config.HLTV_API}/matches")
            data = response.json()
            
            # Filtra apenas jogos da FURIA
            furia_matches = [m for m in data if m['team1'] == 'FURIA' or m['team2'] == 'FURIA']
            
            with open('data/cache/matches.json', 'w') as f:
                json.dump(furia_matches, f)
                
        except Exception as e:
            print(f"Erro ao atualizar jogos: {e}")
    
    def update_team_stats(self):
        try:
            response = requests.get(f"{Config.SPORTDATA_API}/teams/furia")
            data = response.json()
            
            with open('data/cache/team_stats.json', 'w') as f:
                json.dump(data, f)
                
        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")
    
    def get_current_data(self, data_type):
        try:
            with open(f'data/cache/{data_type}.json') as f:
                return json.load(f)
        except:
            return None