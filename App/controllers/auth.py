from typing import Optional
from flask import Flask
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from flask_jwt_extended import create_access_token, get_jwt
from ..models import User
from .user import get_user, is_admin
from functools import wraps


def login_user(email: str, password: str) -> Optional[str]:
    user: Optional[User] = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        role: str = "Admin" if is_admin(user.id) else "Staff"
        return create_access_token(identity=user.id, additional_claims={"role": role})
    return None


def setup_jwt(app: Flask) -> JWTManager:
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user_id: int) -> int:
        """Return the user ID as the identity for the JWT."""
        return user_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> Optional[User]:
        """Retrieve the User object based on the ID in the JWT."""
        identity = jwt_data["sub"]
        return get_user(identity)

    return jwt


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != role:
                return {"msg": "Unauthorized"}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper
