from App.database import db

class InternshipPosition(db.Model):
    __tablename__ = 'internship_positions'
    
    position_id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.employer_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    employer = db.relationship('Employer', backref=db.backref('positions', lazy=True))

    def __init__(self, title, description, requirements, department, location, employer, is_active=True):
        self.title = title
        self.description = description
        self.requirements = requirements
        self.department = department
        self.location = location
        self.is_active = is_active
        self.employer = employer

    def deactivate(self):
        self.is_active = False
        db.session.commit()