from . import db
from .base_model import BaseModel

class Course(BaseModel):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)

    def __repr__(self):
        return f"<Course {self.nome}>"
