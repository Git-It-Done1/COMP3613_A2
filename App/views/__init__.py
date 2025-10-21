from .auth import auth_views
from .user import user_views
from .student import student_bp
from .staff import staff_bp
from .employer import employer_bp
from .internshipPosition import position_bp
from .shortlist import shortlist_bp
from .index import index_views
from .admin import setup_admin

views = [index_views, auth_views, user_views, student_bp, staff_bp, employer_bp, position_bp, shortlist_bp]


