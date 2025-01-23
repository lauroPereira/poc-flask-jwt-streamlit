from models.student_model import Student
from models import db

class StudentService:
    @staticmethod
    def list_all_students():
        return Student.query.all()

    @staticmethod
    def create_student(nome: str, email: str) -> Student:
        new_student = Student(nome=nome, email=email)
        db.session.add(new_student)
        db.session.commit()
        return new_student

    @staticmethod
    def get_student_by_id(student_id: int) -> Student:
        return Student.query.get(student_id)

    @staticmethod
    def update_student(student_id: int, nome: str, email: str) -> Student:
        student = Student.query.get(student_id)
        if not student:
            return None
        student.nome = nome
        student.email = email
        db.session.commit()
        return student

    @staticmethod
    def delete_student(student_id: int) -> bool:
        student = Student.query.get(student_id)
        if not student:
            return False
        db.session.delete(student)
        db.session.commit()
        return True
