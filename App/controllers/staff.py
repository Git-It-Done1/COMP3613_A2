from App.models import Staff
from App.models import Shortlist
from App.database import db


def create_staff(name, email, department):
    staff = Staff(name=name, email=email, department=department)
    db.session.add(staff)
    db.session.commit()
    return staff

def get_staff_by_id(staff_id):
    return Staff.query.get(staff_id) 

def add_to_shortlist(self, student, position):
    shortlist_entry = Shortlist(student=student, position=position, staff=self, status="Pending")
    db.session.add(shortlist_entry)
    db.session.commit()
    return shortlist_entry

