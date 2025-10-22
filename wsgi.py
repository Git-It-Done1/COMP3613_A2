# wsgi.py
import click, pytest, sys
from flask.cli import AppGroup
from App.database import db, get_migrate
from App.models import User, Student, Staff, Shortlist, InternshipPosition, Employer
from App.main import create_app
from App.controllers import create_user, get_all_users_json, get_all_users, initialize

app = create_app()
migrate = get_migrate(app)


# ==================== Core Functionality Commands ====================

@app.cli.command("create-position", help="Create an internship position")
def create_position_cmd():
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
    
    position = InternshipPosition(title, description, requirements, department, location, employer)
    db.session.add(position)
    db.session.commit()
    print(f"Position created with ID: {position.position_id}")


@app.cli.command("shortlist-student", help="Add student to position shortlist")
def shortlist_student_cmd():
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
def review_student_cmd():
    employer_id = input("Employer ID: ")
    shortlist_id = input("Shortlist ID: ")
    decision = input("Decision (Accepted/Rejected/Pending): ")
    
    employer = Employer.query.get(employer_id)
    shortlist = Shortlist.query.get(shortlist_id)
    
    if not employer or not shortlist:
        print("Invalid ID")
        return
    
    # Verify employer owns this position
    if shortlist.position.employer_id != employer.employer_id:
        print("Error: Employer does not own this position")
        return
    
    shortlist.set_employer_decision(decision)
    db.session.commit()
    print(f"Decision saved: {decision}")


@app.cli.command("my-shortlists", help="View my shortlisted positions")
def my_shortlists_cmd():
    student_id = input("Student ID: ")
    student = Student.query.get(student_id)
    
    if not student:
        print("Invalid student ID")
        return
    
    if not student.shortlists:
        print("No shortlists found")
        return
    
    print(f"\nShortlists for {student.name}:")
    print(f"{'Position':<30} {'Company':<20} {'Decision':<15}")
    print("-" * 65)
    for s in student.shortlists:
        print(f"{s.position.title:<30} {s.position.employer.company:<20} {s.employer_decision:<15}")


# ==================== Quick Lookup Commands ====================

@app.cli.command("positions", help="Show all positions")
def positions_cmd():
    positions = InternshipPosition.query.filter_by(is_active=True).all()
    if not positions:
        print("No active positions found")
        return
    
    print(f"\n{'ID':<5} {'Title':<30} {'Company':<20} {'Location':<15}")
    print("-" * 70)
    for p in positions:
        print(f"{p.position_id:<5} {p.title:<30} {p.employer.company:<20} {p.location:<15}")


@app.cli.command("students", help="Show all students")
def students_cmd():
    students = Student.query.all()
    if not students:
        print("No students found")
        return
    
    print(f"\n{'ID':<5} {'Name':<25} {'Major':<25} {'GPA':<5}")
    print("-" * 60)
    for s in students:
        print(f"{s.student_id:<5} {s.name:<25} {s.major:<25} {s.gpa:<5}")


@app.cli.command("employers", help="Show all employers")
def employers_cmd():
    employers = Employer.query.all()
    if not employers:
        print("No employers found")
        return
    
    print(f"\n{'ID':<5} {'Name':<25} {'Company':<20}")
    print("-" * 50)
    for e in employers:
        print(f"{e.employer_id:<5} {e.name:<25} {e.company:<20}")


@app.cli.command("staff", help="Show all staff")
def staff_cmd():
    staff = Staff.query.all()
    if not staff:
        print("No staff found")
        return
    
    print(f"\n{'ID':<5} {'Name':<25} {'Department':<20}")
    print("-" * 50)
    for s in staff:
        print(f"{s.staff_id:<5} {s.name:<25} {s.department:<20}")


@app.cli.command("shortlists", help="Show all shortlists")
def shortlists_cmd():
    shortlists = Shortlist.query.all()
    if not shortlists:
        print("No shortlists found")
        return
    
    print(f"\n{'ID':<5} {'Student':<25} {'Position':<30} {'Decision':<15}")
    print("-" * 75)
    for s in shortlists:
        print(f"{s.shortlist_id:<5} {s.student.name:<25} {s.position.title:<30} {s.employer_decision:<15}")


# ==================== User Commands ====================

user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)


# ==================== Run Server ====================

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
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
    
