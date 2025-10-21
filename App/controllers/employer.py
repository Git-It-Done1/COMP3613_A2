from App.models import Employer, Shortlist
from App.database import db

def create_employer(name, email, company):
    employer = Employer(name=name, email=email, company=company)
    db.session.add(employer)
    db.session.commit()
    return employer

def review_shortlist_entry(employer_id, shortlist_id, decision):
    """Employer reviews a shortlist entry"""
    employer = get_employer_by_id(employer_id)
    if not employer:
        raise ValueError("Invalid employer ID")
    
    entry = Shortlist.query.get(shortlist_id)
    if not entry:
        raise ValueError("Invalid shortlist ID")
    
    if entry.position.employer_id != employer_id:
        raise ValueError("Employer does not own this position")
    
    entry.set_employer_decision(decision)
    db.session.commit()
    return entry

def get_employer_by_id(employer_id):
    return db.session.get(Employer, employer_id)

def get_employer_by_email(email):
    return Employer.query.filter_by(email=email).first() 
    