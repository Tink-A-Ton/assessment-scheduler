from datetime import date
from App.database import db


class Semester(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date: date = db.Column(db.Date, nullable=False)
    end_date: date = db.Column(db.Date, nullable=False)
    semester_number: int = db.Column(db.Integer, nullable=False)
    max_assessments: int = db.Column(db.Integer, nullable=False)
    coursesOffered = db.relationship("Course", backref="semester", lazy="joined")

    def __init__(
        self,
        start_date: date,
        end_date: date,
        semester_number: int,
        max_assessments: int,
    ) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.semester_number = semester_number
        self.max_assessments = max_assessments

    def to_json(self) -> dict[str, int | str | date]:
        return {
            "id": self.id,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "semesterNumber": self.semester_number,
            "maxAssessments": self.max_assessments,
        }
