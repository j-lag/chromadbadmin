import os
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
