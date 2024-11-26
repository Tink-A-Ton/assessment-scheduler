from sqlalchemy.orm import Mapped, mapped_column, relationship
from App.database import db
from .position import Position
from .user import User

class Staff(User):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    position: Mapped[Position] = mapped_column(db.Enum(Position), nullable=False)
    courses = relationship("CourseInstructor", backref="staff", lazy="joined")

    def __init__(
        self,
        id: int,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        position: str,
    ) -> None:
        super().__init__(id, email, password)
        self.first_name = first_name
        self.last_name = last_name
        self.position = Position(position)
