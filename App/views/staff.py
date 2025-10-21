from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from App.controllers.staff import *

staff_bp = Blueprint("staff", __name__, url_prefix="/api/staff")

@staff_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    data = request.json
    staff = create_staff(data['name'], data['email'], data['department'])
    return jsonify(staff_id=staff.staff_id, name=staff.name), 201

@staff_bp.route("/<int:staff_id>", methods=["GET"])
@jwt_required()
def get_one(staff_id):
    staff = get_staff_by_id(staff_id)
    if not staff:
        return jsonify(error="Not found"), 404
    return jsonify(staff_id=staff.staff_id, name=staff.name, department=staff.department), 200

@staff_bp.route("/shortlist", methods=["POST"])
@jwt_required()
def shortlist():
    data = request.json
    try:
        entry = add_to_shortlist(data["staff_id"], data["student_id"], data["position_id"])
        return jsonify(shortlist_id=entry.shortlist_id), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400

