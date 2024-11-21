from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __abstract__ = True
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(120), nullable=False, unique=True)
    password: str = db.Column(db.String(120), nullable=False)

    def __init__(self, id: int, email: str, password: str) -> None:
        self.id: int = id
        self.email: str = email
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    def to_json(self) -> dict[str, str | int]:
        return {"id": self.id, "password": self.password, "email": self.email}
