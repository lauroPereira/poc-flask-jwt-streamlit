import bcrypt
from models.user_model import User
from models import db

class AuthService:
    @staticmethod
    def create_user(username: str, password: str) -> User:
        """
        Cria novo usuário no banco, retornando o objeto User.
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_str = hashed.decode('utf-8')

        new_user = User(username=username, password=hashed_str)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def authenticate_user(username: str, password: str) -> User:
        """
        Verifica se o username existe e a senha está correta.
        Retorna o objeto User se credenciais forem válidas, senão None.
        """
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        return None