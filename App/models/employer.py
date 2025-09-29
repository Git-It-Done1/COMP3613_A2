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

    def create_position(self, title, description, requirements, department, location):
        position = InternshipPosition(
            title=title,
            description=description,
            requirements=requirements,
            department=department,
            location=location,
            employer=self
        )
        db.session.add(position)
        db.session.commit()
        return position

    def review_shortlist_entry(self, entry, decision):
        entry.set_employer_decision(decision)
        db.session.commit()