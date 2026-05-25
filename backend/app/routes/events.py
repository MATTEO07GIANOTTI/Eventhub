import os
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.models import Event, Booking, Review
from app.schemas.schemas import EventSchema, ReviewSchema
from app.utils.auth import role_required
from app.tasks.notifications import send_booking_confirmation

events_bp = Blueprint("events", __name__, url_prefix="/api/events")
event_schema = EventSchema()
review_schema = ReviewSchema()


@events_bp.get("")
def list_events():
    query = Event.query
    if category := request.args.get("category"):
        query = query.filter_by(category=category)
    if city := request.args.get("city"):
        query = query.filter_by(city=city)
    events = query.order_by(Event.date.asc()).all()
    return jsonify([
        {
            "id": e.id,
            "title": e.title,
            "category": e.category,
            "city": e.city,
            "date": e.date.isoformat(),
            "price": e.price,
            "available_seats": e.available_seats,
            "cover_image": e.cover_image,
        }
        for e in events
    ])


@events_bp.post("")
@jwt_required()
@role_required("organizer", "admin")
def create_event():
    form_data = event_schema.load(request.form.to_dict())
    image = request.files.get("cover_image")
    image_path = None
    if image:
        os.makedirs("uploads", exist_ok=True)
        image_path = f"uploads/{datetime.now().timestamp()}_{image.filename}"
        image.save(image_path)

    event = Event(**form_data, organizer_id=int(get_jwt_identity()), cover_image=image_path)
    db.session.add(event)
    db.session.commit()
    return jsonify({"id": event.id}), 201


@events_bp.post("/<int:event_id>/book")
@jwt_required()
@role_required("user", "organizer", "admin")
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    uid = int(get_jwt_identity())
    if Booking.query.filter_by(event_id=event_id, user_id=uid).first():
        return jsonify({"message": "Already booked"}), 400
    if event.available_seats <= 0:
        return jsonify({"message": "Event sold out"}), 400

    booking = Booking(user_id=uid, event_id=event_id)
    db.session.add(booking)
    db.session.commit()
    send_booking_confirmation(booking.user.email, event.title)
    return jsonify({"message": "Booking confirmed"}), 201


@events_bp.post("/<int:event_id>/reviews")
@jwt_required()
def add_review(event_id):
    payload = review_schema.load(request.get_json())
    event = Event.query.get_or_404(event_id)
    if event.date > datetime.now(timezone.utc):
        return jsonify({"message": "Event not ended yet"}), 400
    uid = int(get_jwt_identity())
    if not Booking.query.filter_by(event_id=event_id, user_id=uid).first():
        return jsonify({"message": "Only attendees can review"}), 403

    review = Review(user_id=uid, event_id=event_id, **payload)
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review added"}), 201


@events_bp.get("/cover/<path:filename>")
def get_cover(filename):
    return send_from_directory("uploads", filename)
