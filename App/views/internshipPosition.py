from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from App.controllers.internshipPosition import *

position_bp = Blueprint("position", __name__, url_prefix="/api/positions")

@position_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    data = request.json
    position = create_position(
        data['title'], data['description'], data['requirements'],
        data['department'], data['location'], data['employer_id']
    )
    return jsonify(position_id=position.position_id, title=position.title), 201

@position_bp.route("/<int:position_id>", methods=["GET"])
@jwt_required()
def get_one(position_id):
    position = get_position_by_id(position_id)
    if not position:
        return jsonify(error="Not found"), 404
    return jsonify(
        position_id=position.position_id,
        title=position.title,
        description=position.description,
        department=position.department
    ), 200

@position_bp.route("/employer/<int:employer_id>", methods=["GET"])
@jwt_required()
def by_employer(employer_id):
    positions = get_positions_by_employer(employer_id)
    return jsonify([{"position_id": p.position_id, "title": p.title} for p in positions]), 200


