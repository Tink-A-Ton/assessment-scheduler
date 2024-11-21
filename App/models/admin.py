from .user import User


class Admin(User):
    def __init__(self, id, email, password) -> None:
        super().__init__(id, email, password)
