import csv
from io import StringIO
from flask import Blueprint, jsonify, Response
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from app.extensions import db
from app.models.models import User, Event, Booking, Review
from app.utils.auth import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/users")
@jwt_required()
@role_required("admin")
def users():
    records = User.query.all()
    return jsonify([{"id": u.id, "email": u.email, "role": u.role, "banned": u.banned} for u in records])


@admin_bp.patch("/users/<int:user_id>/promote")
@jwt_required()
@role_required("admin")
def promote(user_id):
    user = User.query.get_or_404(user_id)
    user.role = "organizer"
    db.session.commit()
    return jsonify({"message": "Promoted"})


@admin_bp.get("/reviews/flagged")
@jwt_required()
@role_required("admin")
def flagged_reviews():
    flagged = Review.query.filter_by(flagged=True).all()
    return jsonify([{"id": r.id, "comment": r.comment, "rating": r.rating} for r in flagged])


@admin_bp.get("/dashboard")
@jwt_required()
@role_required("organizer", "admin")
def dashboard():
    stats = (
        db.session.query(
            Event.id,
            Event.title,
            func.count(Booking.id).label("bookings"),
            (func.count(Booking.id) * Event.price).label("revenue"),
            func.coalesce(func.avg(Review.rating), 0).label("avg_rating"),
        )
        .outerjoin(Booking, Booking.event_id == Event.id)
        .outerjoin(Review, Review.event_id == Event.id)
        .group_by(Event.id)
        .all()
    )
    return jsonify([
        {"event_id": s.id, "title": s.title, "bookings": s.bookings, "revenue": s.revenue, "avg_rating": round(float(s.avg_rating), 2)}
        for s in stats
    ])


@admin_bp.get("/events/<int:event_id>/attendees.csv")
@jwt_required()
@role_required("organizer", "admin")
def attendees_csv(event_id):
    event = Event.query.get_or_404(event_id)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "email", "city"])
    for booking in event.bookings:
        writer.writerow([booking.user.full_name, booking.user.email, booking.user.city])
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename=event_{event_id}_attendees.csv"})
