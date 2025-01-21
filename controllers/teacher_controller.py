# controllers/teacher_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from services.teacher_service import TeacherService
from services.course_service import CourseService

teacher_bp = Blueprint('teacher_bp', __name__)

def check_adm_role():
    return session.get('role') == 'adm'

@teacher_bp.route('/adm/teachers', methods=['GET'])
def teachers_list():
    """
    Lista todos os professores, com botão de Adicionar, Editar, Excluir.
    Somente 'adm' pode acessar.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    teachers = TeacherService.list_all_teachers()
    return render_template('teacher_list.html', teachers=teachers)

@teacher_bp.route('/adm/teachers/new', methods=['GET', 'POST'])
def teachers_new():
    """
    Página para adicionar novo professor.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    if request.method == 'GET':
        return render_template('teacher_form.html', teacher=None, action='new')

    # POST
    nome = request.form.get('nome')
    email = request.form.get('email')

    if not nome or not email:
        return "Nome e email são obrigatórios", 400

    TeacherService.create_teacher(nome, email)
    return redirect(url_for('teacher_bp.teachers_list'))

@teacher_bp.route('/adm/teachers/<int:teacher_id>/edit', methods=['GET', 'POST'])
def teachers_edit(teacher_id):
    """
    Edita dados de um professor existente.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    teacher = TeacherService.get_teacher_by_id(teacher_id)
    if not teacher:
        return "Professor não encontrado", 404

    if request.method == 'GET':
        return render_template('teacher_form.html', teacher=teacher, action='edit')

    # POST - atualizar
    nome = request.form.get('nome')
    email = request.form.get('email')
    if not nome or not email:
        return "Nome e email são obrigatórios", 400

    TeacherService.update_teacher(teacher_id, nome, email)
    return redirect(url_for('teacher_bp.teachers_list'))

@teacher_bp.route('/adm/teachers/<int:teacher_id>/delete', methods=['POST'])
def teachers_delete(teacher_id):
    """
    Exclui um professor, caso ele exista.
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    deleted = TeacherService.delete_teacher(teacher_id)
    if not deleted:
        return "Professor não encontrado", 404

    return redirect(url_for('teacher_bp.teachers_list'))

@teacher_bp.route('/adm/teachers/<int:teacher_id>/courses', methods=['GET'])
def teachers_courses(teacher_id):
    """
    Opcional: Mostra as turmas associadas a um determinado professor
    (com relationship 1->N).
    """
    if not check_adm_role():
        return "Acesso negado - apenas administrador", 403

    teacher = TeacherService.get_teacher_by_id(teacher_id)
    if not teacher:
        return "Professor não encontrado", 404

    # teacher.courses é a lista de turmas relacionadas
    return render_template('teacher_courses.html', teacher=teacher)
