from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user, create_access_token
from App.controllers.user import get_user_by_username

auth_views = Blueprint('auth_views', __name__, url_prefix='/api')

@auth_views.route('/login', methods=['POST'])
def login():
    data = request.json
    user = get_user_by_username(data['username'])
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token), 200
    return jsonify(error="Invalid credentials"), 401

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify():
    return jsonify(user_id=current_user.id, username=current_user.username), 200