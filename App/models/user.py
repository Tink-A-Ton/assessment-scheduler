from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(120), nullable=False)

    def __init__(self, id: int, email: str, password: str) -> None:
        self.id = id
        self.email = email
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def to_json(self) -> dict[str, str | int]:
        return {"id": self.id, "password": self.password, "email": self.email}
