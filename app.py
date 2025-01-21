from flask import Flask, session
from config import Config
from models import db
from controllers.auth_controller import ui_bp
from controllers.course_controller import course_bp
from controllers.teacher_controller import teacher_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Configurar secret key para session
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    app.register_blueprint(ui_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(teacher_bp)
    
    @app.context_processor
    def inject_user_data():
        user_name = session.get('username')
        user_email = session.get('email')
        user_role = session.get('role')
        return {
            'username': user_name,
            'email': user_email,
            'role': user_role
        }

    return app


if __name__ == "__main__":
    flask_app = create_app()
    
    with flask_app.app_context():
        # Cria as tabelas, caso não existam
        db.create_all()
        
    flask_app.run(debug=True)
    
    