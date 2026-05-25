from datetime import datetime, timedelta, timezone
import pytest
from app import create_app
from app.extensions import db
from app.models.models import User, Event


@pytest.fixture
def client():
    class TestConfig:
        TESTING = True
        SECRET_KEY = "test"
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_SECRET_KEY = "test-jwt"

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def register_and_login(client, email="user@test.com", password="Password123"):
    client.post("/api/auth/register", json={"email": email, "password": password, "full_name": "Mario Rossi"})
    r = client.post("/api/auth/login", json={"email": email, "password": password})
    return r.get_json()["access_token"]


def test_register_and_login(client):
    res = client.post("/api/auth/register", json={"email": "a@a.com", "password": "Password123", "full_name": "A"})
    assert res.status_code == 201
    login = client.post("/api/auth/login", json={"email": "a@a.com", "password": "Password123"})
    assert login.status_code == 200
    assert "access_token" in login.get_json()


def test_booking_capacity_check(client):
    with client.application.app_context():
        organizer = User(email="org@test.com", full_name="Org", role="organizer")
        organizer.set_password("Password123")
        db.session.add(organizer)
        db.session.flush()
        e = Event(title="Concerto", description="d", category="concert", city="Rome", venue="Hall", date=datetime.now(timezone.utc)+timedelta(days=1), price=10, capacity=1, organizer_id=organizer.id)
        db.session.add(e)
        db.session.commit()

    token = register_and_login(client)
    h = {"Authorization": f"Bearer {token}"}
    first = client.post("/api/events/1/book", headers=h)
    second = client.post("/api/events/1/book", headers=h)
    assert first.status_code == 201
    assert second.status_code == 400


def test_review_only_after_event(client):
    with client.application.app_context():
        organizer = User(email="org2@test.com", full_name="Org2", role="organizer")
        organizer.set_password("Password123")
        db.session.add(organizer)
        db.session.flush()
        e = Event(title="Workshop", description="d", category="workshop", city="Milan", venue="Lab", date=datetime.now(timezone.utc)+timedelta(days=2), price=0, capacity=3, organizer_id=organizer.id)
        db.session.add(e)
        db.session.commit()

    token = register_and_login(client, email="u2@test.com")
    h = {"Authorization": f"Bearer {token}"}
    client.post("/api/events/1/book", headers=h)
    res = client.post("/api/events/1/reviews", headers=h, json={"rating": 5, "comment": "Bellissimo evento"})
    assert res.status_code == 400
