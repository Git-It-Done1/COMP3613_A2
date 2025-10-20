from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.controllers import create_user, get_all_users_json, get_user

user_views = Blueprint('user_views', __name__, url_prefix='/api/users')

@user_views.route('/', methods=['GET'])
@jwt_required()
def get_users():
    return jsonify(get_all_users_json()), 200

@user_views.route('/', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify(id=user.id, username=user.username), 201
