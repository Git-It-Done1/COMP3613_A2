import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, Student, Staff, Shortlist, InternshipPosition, Employer)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()

    # Create Employers------------------------------------------------------------------------------------------------------------------
    employers = [
        Employer("Alice Johnson", "alice@techcorp.com", "TechCorp"),
        Employer("Bob Smith", "bob@innovate.com", "InnovateX"),
        Employer("Carol Lee", "carol@webworks.com", "WebWorks"),
        Employer("David Kim", "david@nextgen.com", "NextGen")
    ]
    db.session.add_all(employers)
    db.session.commit()


    # Create Internship Positions------------------------------------------------------------------------------------------------------------------

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


    # Create Students------------------------------------------------------------------------------------------------------------------

    students = [
        Student("John Doe", "john@student.com", "Computer Science", 3.6),
        Student("Jane Smith", "jane@student.com", "Information Technology", 3.8),
        Student("Michael Brown", "michael@student.com", "Software Engineering", 3.5),
        Student("Emily Davis", "emily@student.com", "Computer Science", 3.9),
        Student("Chris Wilson", "chris@student.com", "Data Science", 3.7),
        Student("Laura Johnson", "laura@student.com", "Information Systems", 3.4),
        Student("Daniel Lee", "daniel@student.com", "Software Engineering", 3.3),
        Student("Sophia Martinez", "sophia@student.com", "Computer Science", 3.85),
        Student("Kevin Garcia", "kevin@student.com", "Data Science", 3.6),
        Student("Olivia Taylor", "olivia@student.com", "Information Technology", 3.75),
    ]
    db.session.add_all(students)
    db.session.commit()


    # Create Staff------------------------------------------------------------------------------------------------------------------

    staff_members = [
        Staff("Dr. Alan Turing", "alan@university.com", "Computer Science"),
        Staff("Dr. Grace Hopper", "grace@university.com", "Software Engineering"),
    ]
    
    db.session.add_all(staff_members)
    db.session.commit()

# User Commands------------------------------------------------------------------------------------------------------------------------
@app.cli.command("create-position", help="Create an internship position")
def create_position():
    employer_id = input("Employer ID: ")
    employer = Employer.query.get(employer_id)
    if not employer:
        print("Invalid employer ID")
        return
    
    title = input("Title: ")
    description = input("Description: ")
    requirements = input("Requirements: ")
    department = input("Department: ")
    location = input("Location: ")
    
    employer.create_position(title, description, requirements, department, location)
    print(f"Position created!")

@app.cli.command("shortlist-student", help="Add student to position shortlist")
def shortlist_student():
    staff_id = input("Staff ID: ")
    student_id = input("Student ID: ")
    position_id = input("Position ID: ")
    
    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    position = InternshipPosition.query.get(position_id)
    
    if not all([staff, student, position]):
        print("Invalid ID")
        return
    
    staff.add_to_shortlist(student, position)
    print("Student shortlisted!")

@app.cli.command("review-student", help="Accept/reject student from shortlist")
def review_student():
    employer_id = input("Employer ID: ")
    shortlist_id = input("Shortlist ID: ")
    decision = input("Decision (accept/reject): ")
    
    employer = Employer.query.get(employer_id)
    shortlist = Shortlist.query.get(shortlist_id)
    
    if not employer or not shortlist:
        print("Invalid ID")
        return
    
    employer.review_shortlist_entry(shortlist, decision.capitalize())
    print("Decision saved!")

@app.cli.command("my-shortlists", help="View my shortlisted positions")
def my_shortlists():
    student_id = input("Student ID: ")
    student = Student.query.get(student_id)
    
    if not student:
        print("Invalid student ID")
        return
    
    for s in student.shortlists:
        print(f"{s.position.title} at {s.position.employer.company} - {s.employer_decision}")

# Quick lookup commands
@app.cli.command("positions", help="Show all positions")
def positions():
    for p in InternshipPosition.query.filter_by(is_active=True).all():
        print(f"{p.position_id}: {p.title} ({p.employer.company})")

@app.cli.command("students", help="Show all students")
def students():
    for s in Student.query.all():
        print(f"{s.student_id}: {s.name}")

@app.cli.command("employers", help="Show all employers")
def employers():
    for e in Employer.query.all():
        print(f"{e.employer_id}: {e.name} ({e.company})")

@app.cli.command("staff", help="Show all staff")
def staff():
    for s in Staff.query.all():
        print(f"{s.staff_id}: {s.name}")

@app.cli.command("shortlists", help="Show all shortlists")
def shortlists():
    for s in Shortlist.query.all():
        print(f"{s.shortlist_id}: {s.student.name} -> {s.position.title} ({s.employer_decision})")

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    
@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StaffUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    
@test.command("employer", help="Run Employer tests")
@click.argument("type", default="all")
def employer_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "EmployerUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "EmployerIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    
@test.command("internship_position", help="Run InternshipPosition tests")
@click.argument("type", default="all")
def internship_position_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "InternshipPositionUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "InternshipPositionIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    
@test.command("shortlist", help="Run Shortlist tests")
@click.argument("type", default="all")
def shortlist_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ShortlistUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ShortlistIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    
app.cli.add_command(test)