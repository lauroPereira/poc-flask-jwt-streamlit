from . import db

students_courses = db.Table(
    'students_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True)
)
