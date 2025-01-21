from flask import Blueprint, render_template, request, redirect, url_for, session
from services.auth_service import AuthService
from models import db
from models.user_model import User

ui_bp = Blueprint('ui_bp', __name__)

@ui_bp.route('/')
def index():
    """
    Página inicial após login bem-sucedido.
    Se não estiver logado, redireciona para /login.
    Caso contrário retorna os dados de username, email e role para a página home
    """
    
    if 'user_id' not in session:
        return redirect(url_for('ui_bp.login'))
    
    user = User.query.get(session['user_id'])
    
    if not user:
        return redirect(url_for('ui_bp.logout'))

    return render_template('home.html', 
                           username=user.username, 
                           email=user.email, 
                           role=user.role)

@ui_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Exibe tela de login (GET).
    Tenta autenticar usuário (POST).
    """
    
    if request.method == 'GET':
        return render_template('login.html')

    # POST
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return "Usuário e senha são obrigatórios", 400

    user = AuthService.authenticate_user(username, password)
    if user:
        # Salvamos dados na sessão
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        session['role'] = user.role
        return redirect(url_for('ui_bp.index'))
    else:
        return "Credenciais inválidas", 401

@ui_bp.route('/logout')
def logout():
    """
    Remove dados de sessão para 'deslogar'.
    """
    session.clear()
    return redirect(url_for('ui_bp.login'))

@ui_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Formulário de cadastro de usuário (nome de usuário e senha).
    """
    if request.method == 'GET':
        return render_template('register.html')

    # POST
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')  # 'aluno', 'professor', 'adm', etc.

    if not all([username, email, password, role]):
        return "Dados incompletos", 400

    # Verifica se usuário já existe
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return "Nome de usuário já em uso", 400
    
    # Verifica se o e-mail já existe
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return "E-mail já em uso", 400

    # Cria usuário
    AuthService.create_user(username, email, password, role)
    return redirect(url_for('ui_bp.login'))