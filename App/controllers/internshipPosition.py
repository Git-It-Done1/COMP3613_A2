from App.database import db
from App.models import InternshipPosition, Employer

def create_position(title, description, requirements, department, location, employer_id):
    """Create a new internship position"""
    employer = db.session.get(Employer, employer_id)
    if not employer:
        raise ValueError("Invalid employer ID")
    
    position = InternshipPosition(
        title=title,
        description=description,
        requirements=requirements,
        department=department,
        location=location,
        employer=employer
    )
    db.session.add(position)
    db.session.commit()
    return position

def deactivate_position(position_id):
    position = get_position_by_id(position_id)
    if not position:
        raise ValueError("Invalid position ID")
    position.deactivate()
    db.session.commit()
    return position

def get_position_by_id(position_id):
    return db.session.get(InternshipPosition, position_id)

def get_positions_by_employer(employer_id):
    return InternshipPosition.query.filter_by(employer_id=employer_id).all()
    