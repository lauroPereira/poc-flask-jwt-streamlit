from flask import Blueprint, render_template, request, redirect, url_for, session
from services.auth_service import AuthService

ui_bp = Blueprint('ui_bp', __name__)

@ui_bp.route('/')
def home():
    """
    Página inicial após login bem-sucedido.
    Se não estiver logado, redireciona para /login.
    """
    if 'user_id' not in session:
        return redirect(url_for('ui_bp.login'))
    # Se estiver logado, exibe Hello World
    return render_template('home.html')

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
        # Salvamos na sessão
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('ui_bp.home'))
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
    password = request.form.get('password')

    if not username or not password:
        return "Dados incompletos", 400

    # Verifica se usuário já existe
    from models.user_model import User
    existing = User.query.filter_by(username=username).first()
    if existing:
        return "Nome de usuário já está em uso", 400

    # Cria usuário
    AuthService.create_user(username, password)
    return redirect(url_for('ui_bp.login'))