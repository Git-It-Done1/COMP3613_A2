from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from App.controllers.employer import *

employer_bp = Blueprint("employer", __name__, url_prefix="/api/employers")

@employer_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    data = request.json
    employer = create_employer(data['name'], data['email'], data['company'])
    return jsonify(employer.to_dict()), 201

@employer_bp.route("/<int:employer_id>", methods=["GET"])
@jwt_required()
def get_one(employer_id):
    employer = get_employer_by_id(employer_id)
    if not employer:
        return jsonify(error="Not found"), 404
    return jsonify(employer.to_dict()), 200

@employer_bp.route("/review", methods=["POST"])
@jwt_required()
def review():
    data = request.json
    try:
        entry = review_shortlist_entry(data["employer_id"], data["shortlist_id"], data["decision"])
        return jsonify(shortlist_id=entry.shortlist_id, decision=entry.employer_decision), 200
    except ValueError as e:
        return jsonify(error=str(e)), 400
