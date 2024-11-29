from ..models import User, Admin
from ..database import db


def get_user(id: int) -> User | None:
    user: User | None = User.query.get(id)
    if user is None:
        return None
    return user


def get_user_by_email(email: str) -> User | None:
    user: User | None = User.query.filter_by(email=email).first()
    if user is None:
        return None
    return user


def is_admin(id: int) -> bool:
    return Admin.query.get(id)


def create_admin(id, email, password) -> Admin:
    admin: Admin = Admin(id, email, password)
    db.session.add(admin)
    db.session.commit()
    return admin
