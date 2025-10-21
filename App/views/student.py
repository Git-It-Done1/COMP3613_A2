from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from App.controllers.student import *

student_bp = Blueprint("student", __name__, url_prefix="/api/students")

@student_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    return jsonify(get_all_students_json()), 200

@student_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
def get_one(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return jsonify(error="Not found"), 404
    return jsonify(student.to_dict()), 200

@student_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    data = request.json
    student = create_student(data['name'], data['email'], data['major'], data['gpa'])
    return jsonify(student.to_dict()), 201

@student_bp.route("/shortlist", methods=["POST"])
@jwt_required()
def shortlist():
    data = request.json
    try:
        entry = shortlist_student(data["staff_id"], data["student_id"], data["position_id"])
        return jsonify(shortlist_id=entry.shortlist_id), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400

@student_bp.route("/<int:student_id>/shortlists", methods=["GET"])
@jwt_required()
def get_shortlists(student_id):
    try:
        shortlists = get_my_shortlists(student_id)
        return jsonify([{
            "position": s.position.title,
            "employer": s.position.employer.company,
            "decision": s.employer_decision
        } for s in shortlists]), 200
    except ValueError as e:
        return jsonify(error=str(e)), 404

