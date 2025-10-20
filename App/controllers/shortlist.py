from App.models import Shortlist
from App.database import db

def create_shortlist_entry(student, position, staff, status="Pending"):
    shortlist_entry = Shortlist(
        student=student,
        position=position,
        staff=staff,
        status=status
    )
    db.session.add(shortlist_entry)
    db.session.commit()
    return shortlist_entry

def update_employer_decision(shortlist_id, decision):
    shortlist_entry = get_shortlist_by_id(shortlist_id)
    if not shortlist_entry:
        raise ValueError("Invalid shortlist ID")
    shortlist_entry.set_employer_decision(decision)
    db.session.commit()
    return shortlist_entry

def get_shortlist_by_id(shortlist_id):
    return db.session.get(Shortlist, shortlist_id)

def get_shortlists_by_staff(staff_id):
    return Shortlist.query.filter_by(staff_id=staff_id).all()

def get_shortlists_by_position(position_id):
    return Shortlist.query.filter_by(position_id=position_id).all()
