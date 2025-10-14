from App.database import db
from App.models import InternshipPosition


def create_position(title, description, requirements, department, location, employer):
    position = InternshipPosition(title=title, description=description, requirements=requirements, department=department, location=location, employer=employer)
    db.session.add(position)
    db.session.commit()
    return position


def deactivate_position(position):
    position.deactivate()
    db.session.commit()
    return position

def get_position_by_id(position_id):
    return InternshipPosition.query.get(position_id)

def get_positions_by_employer(employer_id):
    return InternshipPosition.query.filter_by(employer_id=employer_id)

    

