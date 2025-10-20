import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Shortlist, Staff, Employer, InternshipPosition, shortList
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
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


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

