from . import db
from .base_model import BaseModel

class Teacher(BaseModel):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    # Relação 1-N com turmas (Course)
    courses = db.relationship("Course", backref="teacher", lazy=True)

    def __repr__(self):
        return f"<Teacher {self.nome}>"