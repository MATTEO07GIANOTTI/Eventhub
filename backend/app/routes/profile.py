from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.models import User, Booking

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.get("")
@jwt_required()
def me():
    user = User.query.get_or_404(int(get_jwt_identity()))
    return jsonify({"email": user.email, "full_name": user.full_name, "city": user.city, "role": user.role})


@profile_bp.patch("")
@jwt_required()
def update_profile():
    user = User.query.get_or_404(int(get_jwt_identity()))
    data = request.get_json()
    user.full_name = data.get("full_name", user.full_name)
    user.city = data.get("city", user.city)
    db.session.commit()
    return jsonify({"message": "Profile updated"})


@profile_bp.get("/tickets")
@jwt_required()
def tickets():
    uid = int(get_jwt_identity())
    my_bookings = Booking.query.filter_by(user_id=uid).all()
    return jsonify([
        {
            "event": b.event.title,
            "date": b.event.date.isoformat(),
            "qr_payload": f"EVENT:{b.event_id}|USER:{b.user_id}|BOOKING:{b.id}",
        }
        for b in my_bookings
    ])
