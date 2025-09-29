from App.database import db

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    major = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Numeric(3,2), nullable=False)

    def __init__(self, name, email, major, gpa):
        self.name = name
        self.email = email
        self.major = major
        self.gpa = gpa

    def view_my_shortlists(self):
        return self.shortlists