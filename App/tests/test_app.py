import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Shortlist, Staff, Employer, InternshipPosition, shortList
from App.controllers import (
    create_user,
    get_all_users_json,
    get_user,
    get_user_by_username,
    update_user,
    create_staff,
    create_employer,
    create_position,
    add_to_shortlist,
    create_shortlist_entry,
    get_shortlist_by_id,
    review_shortlist_entry,
    get_employer_by_id,
    get_employer_by_email,
    get_position_by_id,
    deactivate_position,
    get_positions_by_employer,
    update_employer_decision,
    get_shortlists_by_staff,
    get_shortlists_by_position
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("John Doe", "john@student.com", "BSc Computer Science (General)", 3.6)
        assert student.name == "John Doe"
        assert student.gpa == 3.6

    def test_student_shortlists(self):
        student = Student("John Doe", "john@student.com", "BSc Computer Science (General)", 3.6)
        shortLists = student.view_my_shortlists()
        assert shortLists == []

class StaffUnitTests(unittest.TestCase):
    def test_create_staff(self):
        staff = Staff("Dr. Smith", "smith@uni.edu", "DCIT")
        assert staff.name == "Dr. Smith"
        assert staff.department == "DCIT"

class EmployerUnitTests(unittest.TestCase):
    def test_create_employer(self):
        employer = Employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        assert employer.name == "Alice Johnson"
        assert employer.company == "TechCorp"

class InternshipPositionUnitTests(unittest.TestCase):
    def test_create_position(self):
        employer = Employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        position = InternshipPosition("Frontend Dev", "Build UIs", "React", "IT", "Office", employer)
        assert position.title == "Frontend Dev"
        assert position.is_active == True

class ShortlistUnitTests(unittest.TestCase):
    def test_create_shortlist_entry(self):
        student = Student("John Doe", "john@student.com", "BSc Computer Science (General)", 3.6)
        staff = Staff("Dr. Smith", "smith@uni.edu", "DCIT")
        employer = Employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        position = InternshipPosition("Frontend Dev", "Build UIs", "React", "IT", "Office", employer)
        shortlist = Shortlist(student, position, staff, "Pending", "Undecided")
        assert shortlist.student == student
        shortlist.status == "Pending"

    def test_set_employer_decision(self):
        student = Student("John Doe", "john@student.com", "BSc Computer Science (General)", 3.6)
        staff = Staff("Dr. Smith", "smith@uni.edu", "DCIT")
        employer = Employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        position = InternshipPosition("Frontend Dev", "Build UIs", "React", "IT", "Office", employer)
        shortlist_entry = Shortlist(student, position, staff, "Pending", "Undecided")
        shortlist_entry.set_employer_decision("Accepted")
        assert shortlist_entry.employer_decision == "Accepted"

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class StaffIntegrationTests(unittest.TestCase):
    def test_staff_add_to_shortlist(self):
        staff = create_staff("Dr. Smith", "smith@uni.edu", "DCIT")
        student = Student("John Doe", "john@student.com", "BSc Computer Science (General)", 3.6)
        db.session.add(student)
        db.session.commit()
        employer = create_employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        position = create_position("Frontend Dev", "Build UIs", "React", "IT", "Office", employer.employer_id)
        shortlist_entry = add_to_shortlist(staff.staff_id, student.student_id, position.position_id)
        assert shortlist_entry.student_id == student.student_id and shortlist_entry.status == "Pending"

class EmployerIntegrationTests(unittest.TestCase):
    def test_employer_create_position(self):
        employer = create_employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        position = create_position("Frontend Dev", "Build UIs", "React", "IT", "Office", employer.employer_id)
        assert position != None and position.employer_id == employer.employer_id

    def test_employer_review_shortlist_entry(self):
        student = Student("John Doe", "john@student.com", "BSc Computer Science (General)", 3.6)
        staff = create_staff("Dr. Smith", "smith@uni.edu", "DCIT")
        employer = get_employer_by_id(1)
        position = create_position("Frontend Dev", "Build UIs", "React", "IT", "Office", employer.employer_id)
        entry = create_shortlist_entry(student, position, staff)
        shortlist_entry = review_shortlist_entry(employer.employer_id, get_shortlist_by_id(1).shortlist_id, "Accepted")
        assert shortlist_entry.employer_decision == "Accepted"

    def test_get_employer_by_id(self):
        employer = get_employer_by_id(1)
        assert employer.email == "alice@techcorp.com"

    def test_get_employer_by_email(self):
        employer = get_employer_by_email("alice@techcorp.com")
        assert employer.email == "alice@techcorp.com"

    def test_get_employer_by_email_not_found(self):
        employer = get_employer_by_email("john@techcorp.com")
        assert employer == None

class InternshipPositionIntegrationTests(unittest.TestCase):
    def test_deactivate_position(self):
        employer = create_employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        position = create_position("Frontend Dev", "Build UIs", "React", "IT", "Office", employer.employer_id)
        position = get_position_by_id(1)
        position = deactivate_position(position.position_id)
        assert position.is_active == False

    def test_get_position_by_id(self):
        position = get_position_by_id(1)
        assert position.title == "Frontend Dev"

    def test_get_positions_by_employer(self):
        positions = get_positions_by_employer(1)
        assert positions != None

class ShortlistIntegrationTests(unittest.TestCase):
    def test_create_shortlist_entry(self):
        staff = create_staff("Dr. Smith", "smith@uni.edu", "DCIT")
        student = Student("John Doe", "john@student.com", "BSc Computer Science (General)", 3.6)
        employer = create_employer("Alice Johnson", "alice@techcorp.com", "TechCorp")
        position = create_position("Frontend Dev", "Build UIs", "React", "IT", "Office", employer.employer_id)
        entry = create_shortlist_entry(student, position, staff)
        assert entry != None and entry.student_id == student.student_id and entry.position_id == position.position_id and entry.staff_id == staff.staff_id

    def test_update_employer_decision(self):
        entry = get_shortlist_by_id(1)
        entry = update_employer_decision(entry.shortlist_id, "Accepted")
        assert entry.employer_decision == "Accepted"

    def test_get_shortlist_by_id(self):
        entry = get_shortlist_by_id(1)
        assert entry != None

    def test_get_shortlists_by_staff(self):
        entries = get_shortlists_by_staff(1)
        assert entries != None

    def test_get_shortlists_by_position(self):
        entries = get_shortlists_by_position(1)
        assert entries != None
        

