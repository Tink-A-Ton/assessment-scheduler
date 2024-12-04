from typing import Optional
from ..models import User, Admin
from ..database import db


def get_user(id: int) -> Optional[User]:
    user: Optional[User] = User.query.get(id)
    if user is None:
        return None
    return user


def get_user_by_email(email: str) -> Optional[User]:
    user: Optional[User] = User.query.filter_by(email=email).first()
    if user is None:
        return None
    return user


def is_admin(id: int) -> bool:
    return Admin.query.get(id)


def is_admin_account(email: str) -> bool:
    return Admin.query.filter_by(email=email).first()


def update_password(id: int, password: str) -> None:
    user: User = User.query.get(id)
    user.set_password(password)
    db.session.commit()
