from App.database import db
from App.models.shortList import Shortlist

class Staff(db.Model):
    __tablename__ = 'staff'
    
    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, department):
        self.name = name
        self.email = email
        self.department = department

    def add_to_shortlist(self, student, position):
        shortlist_entry = Shortlist(student=student, position=position, staff=self, status="Pending")
        db.session.add(shortlist_entry)
        db.session.commit()
        return shortlist_entry