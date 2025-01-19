from flask import Flask
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Configurar secret key para session
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    return app

if __name__ == "__main__":
    flask_app = create_app()
    
    with flask_app.app_context():
        # Cria as tabelas, caso não existam
        db.create_all()
        
    flask_app.run(debug=True)