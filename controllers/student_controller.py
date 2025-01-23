from flask import Blueprint, render_template, request, redirect, url_for, session
from services.student_service import StudentService

student_bp = Blueprint('student_bp', __name__)

def check_some_role():
    """
    Se quiser checar permissão no futuro (p.e. admin).
    Por ora, vamos permitir livre acesso.
    """
    return True

@student_bp.route('/students', methods=['GET'])
def students_list():
    if not check_some_role():
        return "Acesso negado", 403

    students = StudentService.list_all_students()
    return render_template('student_list.html', students=students)

@student_bp.route('/students/new', methods=['GET', 'POST'])
def students_new():
    if not check_some_role():
        return "Acesso negado", 403

    if request.method == 'GET':
        return render_template('student_form.html', student=None, action='new')

    # POST
    nome = request.form.get('nome')
    email = request.form.get('email')

    if not nome or not email:
        return "Nome e email são obrigatórios", 400

    StudentService.create_student(nome, email)
    return redirect(url_for('student_bp.students_list'))

@student_bp.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def students_edit(student_id):
    if not check_some_role():
        return "Acesso negado", 403

    student = StudentService.get_student_by_id(student_id)
    if not student:
        return "Aluno não encontrado", 404

    if request.method == 'GET':
        return render_template('student_form.html', student=student, action='edit')

    # POST (atualizar)
    nome = request.form.get('nome')
    email = request.form.get('email')
    if not nome or not email:
        return "Nome e email são obrigatórios", 400

    StudentService.update_student(student_id, nome, email)
    return redirect(url_for('student_bp.students_list'))

@student_bp.route('/students/<int:student_id>/delete', methods=['POST'])
def students_delete(student_id):
    if not check_some_role():
        return "Acesso negado", 403

    deleted = StudentService.delete_student(student_id)
    if not deleted:
        return "Aluno não encontrado", 404

    return redirect(url_for('student_bp.students_list'))
