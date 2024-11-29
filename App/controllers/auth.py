from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager
from ..models import User
from .user import get_user


def login_user(id: int, password: str) -> str | None:
    user: User | None = get_user(id)
    if user and user.check_password(password):
        return create_access_token(identity=user.id)
    return None


def setup_jwt(app: Flask) -> JWTManager:
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user_id: int) -> int:
        """Return the user ID as the identity for the JWT."""
        return user_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> User | None:
        """Retrieve the User object based on the ID in the JWT."""
        identity = jwt_data["sub"]
        return get_user(identity)

    return jwt
