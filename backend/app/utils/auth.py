from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.models import User


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.banned:
                return jsonify({"message": "Unauthorized"}), 403
            if user.role not in roles:
                return jsonify({"message": "Insufficient role"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
