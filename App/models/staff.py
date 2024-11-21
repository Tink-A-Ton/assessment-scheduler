from App.database import db
from .position import Position
from .user import User


class Staff(User):
    id: int = db.Column(db.Integer, primary_key=True)
    first_name: str = db.Column(db.String(120), nullable=False)
    last_name: str = db.Column(db.String(120), nullable=False)
    position: Position = db.Column(db.Enum(Position), nullable=False)
    courses = db.relationship("CourseInstructor", backref="staff", lazy="joined")

    def __init__(self, id, email, password, first_name, last_name, position) -> None:
        super().__init__(id, email, password)
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
