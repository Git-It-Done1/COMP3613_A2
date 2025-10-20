from App.database import db

class Employer(db.Model):
    __tablename__ = 'employers'
    
    employer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    company = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, company):
        self.name = name
        self.email = email
        self.company = company
    
    def to_dict(self):
        """Convert employer to dictionary"""
        return {
            'employer_id': self.employer_id,
            'name': self.name,
            'email': self.email,
            'company': self.company
        }
    
    def __repr__(self):
        return f'<Employer {self.employer_id}: {self.name} - {self.company}>'