from App.database import db

class Shortlist(db.Model):
    __tablename__ = 'shortlists'
    
    shortlist_id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('internship_positions.position_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    status = db.Column(db.String(20), default="Pending")
    employer_decision = db.Column(db.String(20), default="Undecided")

    student = db.relationship('Student', backref=db.backref('shortlists', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('shortlists', lazy=True))
    position = db.relationship('InternshipPosition', backref=db.backref('shortlists', lazy=True))

    def __init__(self, student, position, staff, status="Pending", employer_decision="Undecided"):
        self.student = student
        self.position = position
        self.staff = staff
        self.status = status
        self.employer_decision = employer_decision

    def set_employer_decision(self, decision):
        self.employer_decision = decision
        db.session.commit()