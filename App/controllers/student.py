from App.models import Student, Staff, Shortlist, InternshipPosition
from App.database import db

def get_student_by_id(student_id):
    """Return a student by ID"""
    return db.session.get(Student, student_id)

def get_all_students():
    """Return all students"""
    return Student.query.all()

def get_all_students_json():
    """Return all students as a list of dicts"""
    students = get_all_students()
    return [s.to_dict() for s in students]

def create_student(name, email, major, gpa):
    """Create a new student"""
    student = Student(name=name, email=email, major=major, gpa=gpa)
    db.session.add(student)
    db.session.commit()
    return student

def shortlist_student(staff_id, student_id, position_id):
    """Staff shortlists a student for a position"""
    staff = Staff.query.get(staff_id)
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

def get_my_shortlists(student_id):
    """Return a student's shortlist entries"""
    student = get_student_by_id(student_id)
    if not student:
        raise ValueError("Invalid student ID")
    return student.shortlists

def review_student(employer_id, shortlist_id, decision):
    """Employer reviews a student from a shortlist"""
    from App.controllers.employer import review_shortlist_entry
    return review_shortlist_entry(employer_id, shortlist_id, decision)