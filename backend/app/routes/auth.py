from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.models import User
from app.schemas.schemas import RegisterSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
register_schema = RegisterSchema()


@auth_bp.post("/register")
def register():
    payload = register_schema.load(request.get_json())
    if User.query.filter_by(email=payload["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(email=payload["email"], full_name=payload["full_name"], city=payload.get("city"))
    user.set_password(payload["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered"}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"message": "Invalid credentials"}), 401

    access = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh = create_refresh_token(identity=str(user.id))
    return jsonify({"access_token": access, "refresh_token": refresh, "role": user.role})


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"access_token": token})
