import click
from flask.cli import AppGroup
from App.database import db
from App.models import Employer, InternshipPosition, Student, Staff

init_cli = AppGroup("init", help="Database initialization commands")

def initialize():
    db.create_all()
    print("Database tables created.")

@init_cli.command("db", help="Creates and initializes the database with seed data")
def init_db():
    initialize()  

    # Create Employers
    employers = [
        Employer("Alice Johnson", "alice@techcorp.com", "TechCorp"),
        Employer("Bob Smith", "bob@innovate.com", "InnovateX"),
        Employer("Carol Lee", "carol@webworks.com", "WebWorks"),
        Employer("David Kim", "david@nextgen.com", "NextGen")
    ]
    db.session.add_all(employers)
    db.session.commit()

    # Create Internship Positions
    positions = [
        InternshipPosition("Software Intern", "Work on backend APIs", "Python, SQL", "IT", "Remote", employers[0]),
        InternshipPosition("Frontend Developer", "Build React UIs", "JavaScript, React", "IT", "Office", employers[0]),
        InternshipPosition("Data Analyst Intern", "Analyze datasets", "Python, Excel", "Data", "Remote", employers[1]),
        InternshipPosition("Marketing Intern", "Assist campaigns", "Social Media, Content", "Marketing", "Office", employers[1]),
        InternshipPosition("QA Tester", "Test web applications", "Selenium, Manual Testing", "QA", "Remote", employers[2]),
        InternshipPosition("DevOps Intern", "Support cloud infrastructure", "AWS, Docker", "IT", "Office", employers[3]),
    ]
    db.session.add_all(positions)
    db.session.commit()

    # Create Students
    students = [
        Student("John Doe", "john@student.com", "Computer Science", 3.6),
        Student("Jane Smith", "jane@student.com", "Information Technology", 3.8),
        Student("Michael Brown", "michael@student.com", "Software Engineering", 3.5),
        Student("Emily Davis", "emily@student.com", "Computer Science", 3.9),
    ]
    db.session.add_all(students)
    db.session.commit()

    # Create Staff
    staff_members = [
        Staff("Dr. Alan Turing", "alan@university.com", "Computer Science"),
        Staff("Dr. Grace Hopper", "grace@university.com", "Software Engineering"),
    ]
    db.session.add_all(staff_members)
    db.session.commit()

    print("Database initialized successfully.")