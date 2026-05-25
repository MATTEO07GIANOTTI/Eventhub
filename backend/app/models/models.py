from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100))
    role = db.Column(db.String(20), default="user", nullable=False)
    banned = db.Column(db.Boolean, default=False)

    bookings = db.relationship("Booking", backref="user", lazy=True)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    venue = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    cover_image = db.Column(db.String(255))
    organizer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    organizer = db.relationship("User", backref="events")

    bookings = db.relationship("Booking", backref="event", lazy=True)
    reviews = db.relationship("Review", backref="event", lazy=True)

    @property
    def available_seats(self):
        return self.capacity - len(self.bookings)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
