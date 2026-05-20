from src.config import SETTINGS
from src.energy_system import _ENGINE, EnergyFlows, Session

with Session(_ENGINE) as db:
    ef = EnergyFlows.load_from_database(db)
    ef.save_to_database(db)

if __name__ == "__main__":
    print(SETTINGS)

""" 
"192.168.2.187:11434"
curl http://192.168.2.187:11434/api/chat -d '{"model": "mistral","messages": [{ "role": "user", "content": "Hello!" }]}'
"""
