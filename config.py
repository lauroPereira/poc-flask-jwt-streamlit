import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'a71ee98c2973dd95cd21f51be60a36dc35992f077dea2afc431aeff6edf1800a' # Gere uma chave unica para manter sua aplicacao segura
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False