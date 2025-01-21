from flask import Blueprint, render_template, request, redirect, url_for, session
from services.course_service import CourseService

course_bp = Blueprint('course_bp', __name__)

def check_adm_role():
    """
    Verifica se o usuário atual é 'adm'.
    Caso não seja, retornamos False para negar acesso.
    """
    return session.get('role') == 'adm'


@course_bp.route('/adm/courses', methods=['GET'])
def adm_courses_list():
    """
    Lista todas as turmas, com botões de Adicionar, Editar, Excluir.
    Somente 'adm' pode acessar.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    courses = CourseService.list_all_courses()
    
    return render_template('course_list.html', courses=courses)


@course_bp.route('/adm/courses/new', methods=['GET', 'POST'])
def adm_courses_new():
    """
    Página para adicionar nova turma.
    - GET: exibe o formulário vazio.
    - POST: cria a turma no DB e redireciona para a lista.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    if request.method == 'GET':
        # Renderiza formulário vazio
        return render_template('course_form.html', course=None, action='new')

    # POST
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')

    if not nome:
        return "Nome é obrigatório", 400

    CourseService.create_course(nome, descricao)
    return redirect(url_for('course_bp.adm_courses_list'))


@course_bp.route('/adm/courses/<int:course_id>/edit', methods=['GET', 'POST'])
def adm_courses_edit(course_id):
    """
    Página para editar os dados da turma.
    - GET: exibe formulário pré-preenchido.
    - POST: salva alterações e redireciona para a lista.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    course = CourseService.get_course_by_id(course_id)
    if not course:
        return "Turma não encontrada", 404

    if request.method == 'GET':
        # Exibe formulário pré-preenchido
        return render_template('course_form.html', course=course, action='edit')

    # POST (atualizar)
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')

    if not nome:
        return "Nome é obrigatório", 400

    CourseService.update_course(course_id, nome, descricao)
    return redirect(url_for('course_bp.adm_courses_list'))


@course_bp.route('/adm/courses/<int:course_id>/delete', methods=['POST'])
def adm_courses_delete(course_id):
    """
    A rota 'POST' para excluir a turma.
    Ao excluir, redirecionamos de volta para a lista.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    deleted = CourseService.delete_course(course_id)
    if not deleted:
        return "Turma não encontrada", 404

    return redirect(url_for('course_bp.adm_courses_list'))