from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user
from flask_admin import Admin
from flask import flash, redirect, url_for, request
from App.database import db
from App.models import User

class AdminView(ModelView):
    @jwt_required()
    def is_accessible(self):
        return current_user is not None and current_user.user_type == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        flash("Login as admin to access this page")
        return redirect(url_for('auth_views.login', next=request.url))

def setup_admin(app):
    admin = Admin(app, name='Internship System', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))
