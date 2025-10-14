from App.database import db
from App.models.internshipPosition import InternshipPosition

class Employer(db.Model):
    __tablename__ = 'employers'
    
    employer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    company = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, company):
        self.name = name
        self.email = email
        self.company = company

   