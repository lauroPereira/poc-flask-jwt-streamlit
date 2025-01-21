from models.course_model import Course
from models import db

class CourseService:
    @staticmethod
    def list_all_courses():
        return Course.query.all()

    @staticmethod
    def create_course(nome: str, descricao: str) -> Course:
        new_course = Course(nome=nome, descricao=descricao)
        db.session.add(new_course)
        db.session.commit()
        return new_course

    @staticmethod
    def get_course_by_id(course_id: int) -> Course:
        return Course.query.get(course_id)

    @staticmethod
    def update_course(course_id: int, nome: str, descricao: str) -> Course:
        course = Course.query.get(course_id)
        if not course:
            return None
        course.nome = nome
        course.descricao = descricao
        db.session.commit()
        return course

    @staticmethod
    def delete_course(course_id: int) -> bool:
        course = Course.query.get(course_id)
        if not course:
            return False
        db.session.delete(course)
        db.session.commit()
        return True