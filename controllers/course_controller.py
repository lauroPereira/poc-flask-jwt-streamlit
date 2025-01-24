from flask import Blueprint, render_template, request, redirect, url_for, session
from services.course_service import CourseService
from services.teacher_service import TeacherService

course_bp = Blueprint('course_bp', __name__)

def check_adm_role():
    """
    Verifica se o usuário atual é 'adm'.
    Caso não seja, retornamos False para negar acesso.
    """
    return session.get('role') == 'adm'


@course_bp.route('/courses', methods=['GET'])
def courses_list():
    """
    Lista todas as turmas, com botões de Adicionar, Editar, Excluir.
    Somente 'adm' pode acessar.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    courses = CourseService.list_all_courses()
    
    return render_template('course_list.html', courses=courses)


@course_bp.route('/courses/new', methods=['GET', 'POST'])
def courses_new():
    """
    Página para adicionar nova turma.
    - GET: exibe o formulário vazio.
    - POST: cria a turma no DB e redireciona para a lista.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    if request.method == 'GET':
        
        teachers = TeacherService.list_all_teachers()
        
        # Renderiza formulário vazio
        return render_template(
            'course_form.html', 
            course=None, 
            action='new',
            teachers=teachers
        )

    # POST
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')

    if not nome:
        return "Nome é obrigatório", 400

    teacher_id = request.form.get('teacher_id')
    CourseService.create_course(nome, descricao, teacher_id)
    return redirect(url_for('course_bp.courses_list'))


@course_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
def courses_edit(course_id):
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
        
        teachers = TeacherService.list_all_teachers()
        
        # Exibe formulário pré-preenchido
        return render_template(
            'course_form.html', 
            course=course, 
            action='edit', 
            teachers=teachers
        )

    # POST (atualizar)
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')

    if not nome:
        return "Nome é obrigatório", 400
    
    teacher_id = request.form.get('teacher_id')

    CourseService.update_course(course_id, nome, descricao, teacher_id)
    return redirect(url_for('course_bp.courses_list'))


@course_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
def courses_delete(course_id):
    """
    A rota 'POST' para excluir a turma.
    Ao excluir, redirecionamos de volta para a lista.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    deleted = CourseService.delete_course(course_id)
    if not deleted:
        return "Turma não encontrada", 404

    return redirect(url_for('course_bp.courses_list'))