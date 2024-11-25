from App.database import db
import enum
from datetime import datetime


class Category(enum.Enum):
    EXAM = "Exam"
    ASSIGNMENT = "Assignment"
    QUIZ = "Quiz"
    PROJECT = "Project"
    DEBATE = "Debate"
    PRESENTATION = "Presentation"
    ORALEXAM = "Oral Exam"
    PARTICIPATION = "Participation"


class Assessment(db.Model):
    id: int = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    course_code: str = db.Column(db.String(9), db.ForeignKey("course.course_code"))
    given_date: datetime = db.Column(db.DateTime, nullable=False)
    end_date: datetime = db.Column(db.DateTime, nullable=False)
    category: Category = db.Column(db.Enum(Category), nullable=False)

    def __init__(
        self,
        courseCode: str,
        given_date: datetime,
        end_date: datetime,
        category: Category,
    ) -> None:
        self.courseCode = courseCode
        self.given_date = given_date
        self.end_date = end_date
        self.category = category

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "courseCode": self.courseCode,
            "given_date": self.given_date,
            "end_date": self.end_date,
            "category": self.category,
        }
