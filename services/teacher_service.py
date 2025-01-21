from models.teacher_model import Teacher
from models import db

class TeacherService:
    @staticmethod
    def list_all_teachers():
        return Teacher.query.all()

    @staticmethod
    def create_teacher(nome: str, email: str) -> Teacher:
        new_teacher = Teacher(nome=nome, email=email)
        db.session.add(new_teacher)
        db.session.commit()
        return new_teacher

    @staticmethod
    def get_teacher_by_id(teacher_id: int) -> Teacher:
        return Teacher.query.get(teacher_id)

    @staticmethod
    def update_teacher(teacher_id: int, nome: str, email: str) -> Teacher:
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return None
        teacher.nome = nome
        teacher.email = email
        db.session.commit()
        return teacher

    @staticmethod
    def delete_teacher(teacher_id: int) -> bool:
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return False
        db.session.delete(teacher)
        db.session.commit()
        return True
