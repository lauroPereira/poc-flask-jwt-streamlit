from . import db
from .base_model import BaseModel
from .student_course_model import students_courses

class Student(BaseModel):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    # Relação muitos-para-muitos com Course
    courses = db.relationship(
        "Course",
        secondary=students_courses,
        back_populates="students"
    )

    def __repr__(self):
        return f"<Student {self.nome}>"
