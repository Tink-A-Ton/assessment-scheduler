from enum import Enum
from App.database import db
from .user import User


class Position(Enum):
    PTINSTRUCTOR = "Part-Time Instructor"
    INSTRUCTOR = "Instructor"
    HOD = "Head of Department"
    LECTURER = "Lecturer"
    TA = "Teaching Assistant"
    TUTOR = "Tutor"
    PTTUTOR = "Part-Time Tutor"


class Staff(User):
    id: int = db.Column(db.Integer, primary_key=True)
    firstName: str = db.Column(db.String(120), nullable=False)
    lastName: str = db.Column(db.String(120), nullable=False)
    position: Position = db.Column(db.Enum(Position), nullable=False)
    courses = db.relationship("CourseInstructor", backref="staff", lazy="joined")

    def __init__(self, id, email, password, firstName, lastName, position):
        super().__init__(id, email, password)
        self.firstName = firstName
        self.lastName = lastName
        self.position = position

    def to_json(self) -> dict[str, str | int | list]:
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "position": self.position.name,
            "email": self.email,
            "courses": [course.to_json() for course in self.courses],
        }
