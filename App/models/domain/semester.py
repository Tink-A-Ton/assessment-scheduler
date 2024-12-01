from ...database import db


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date: str = db.Column(db.String(100), nullable=False)
    end_date: str = db.Column(db.String(100), nullable=False)
    semester_number: int = db.Column(db.Integer, nullable=False)
    max_exams: int = db.Column(db.Integer, nullable=False)
    courses_offered = db.relationship("Course", backref="semester", lazy="joined")

    def __init__(
        self,
        start_date: str,
        end_date: str,
        semester_number: int,
        max_exams: int,
    ) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.semester_number = semester_number
        self.max_exams = max_exams

    def to_json(self) -> dict[str, int | str]:
        return {
            "id": self.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "semester_number": self.semester_number,
            "max_exams": self.max_exams,
        }
