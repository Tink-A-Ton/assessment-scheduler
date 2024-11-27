from App.models import User, Admin, Staff


def get_user(id: str) -> User | None:
    user: User | None = Admin.query.get(id) or Staff.query.get(id)
    if user is None:
        return None
    return user

def get_user_by_email(email: str) -> User | None:
    user: User | None = Admin.query.filter_by(email=email).first() or Staff.query.filter_by(email=email).first()
    if user is None:
        return None
    return user

def is_admin(id: int) -> bool:
    return Admin.query.get(id)
