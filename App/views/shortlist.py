from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from App.models import Shortlist

shortlist_bp = Blueprint("shortlist", __name__, url_prefix="/api/shortlists")

@shortlist_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    entries = Shortlist.query.all()
    return jsonify([{
        "shortlist_id": s.shortlist_id,
        "student": s.student.name,
        "position": s.position.title,
        "decision": s.employer_decision
    } for s in entries]), 200