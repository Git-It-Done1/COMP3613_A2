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
        """Return all shortlists for this student"""
        return self.shortlists
    
    def to_dict(self):
        """Convert student to dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'major': self.major,
            'gpa': float(self.gpa)
        }
    
    def __repr__(self):
        return f'<Student {self.student_id}: {self.name}>'

