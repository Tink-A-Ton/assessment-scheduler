from App.models import User, Admin


def get_user(id: str) -> User | None:
    user: User | None = User.query.get(id)
    if user is None:
        return None
    return user


def is_admin(id: int) -> bool:
    return Admin.query.get(id)
