from App.models import Staff, Student, InternshipPosition, Shortlist
from App.database import db

def create_staff(name, email, department):
    staff = Staff(name=name, email=email, department=department)
    db.session.add(staff)
    db.session.commit()
    return staff

def get_staff_by_id(staff_id):
    return db.session.get(Staff, staff_id)

def add_to_shortlist(staff_id, student_id, position_id):
    """Staff adds a student to shortlist for a position"""
    staff = get_staff_by_id(staff_id)
    student = Student.query.get(student_id)
    position = InternshipPosition.query.get(position_id)
    
    if not all([staff, student, position]):
        raise ValueError("Invalid staff, student, or position ID")
    
    shortlist_entry = Shortlist(
        student=student,
        position=position,
        staff=staff,
        status="Pending"
    )
    db.session.add(shortlist_entry)
    db.session.commit()
    return shortlist_entry