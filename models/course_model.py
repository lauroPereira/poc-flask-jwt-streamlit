from . import db
from .base_model import BaseModel
from .student_course_model import students_courses  # importa a tabela intermediária

class Course(BaseModel):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    
    students = db.relationship(
        "Student",                  # Nome da classe que vamos relacionar
        secondary=students_courses, # tabela intermediária
        back_populates="courses"    # propriedade do outro lado (em Student)
    )

    def __repr__(self):
        return f"<Course {self.nome}>"
