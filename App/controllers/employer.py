from App.models import Employer, InternshipPosition
from App.database import db


def create_employer(name, email, company):
    employer = Employer(name=name, email=email, company=company)
    db.session.add(employer)
    db.session.commit()
    return employer


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
    return entry

def get_employer_by_id(employer_id):
    return Employer.query.get(employer_id)

def get_employer_by_email(email):
    return Employer.query.filter_by(email=email).first()