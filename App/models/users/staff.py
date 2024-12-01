from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.relationships import Relationship
from ...database import db
from .instructor import Instructor
from ..utils import Position
from .user import User


class Staff(User):
    id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    position: Mapped[Position] = mapped_column(db.Enum(Position), nullable=False)
    courses: Relationship[Instructor] = relationship("Instructor", backref="staff")

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
