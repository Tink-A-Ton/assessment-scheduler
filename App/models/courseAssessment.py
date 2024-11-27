from App.database import db
from datetime import datetime, date, time


class CourseAssessment(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code: str = db.Column(
        db.String(9), db.ForeignKey("course.course_code"), nullable=False
    )
    start_date: date = db.Column(db.Date, nullable=True)
    end_date: date = db.Column(db.Date, nullable=True)
    start_time: time = db.Column(db.Time, nullable=True)
    end_time: time = db.Column(db.Time, nullable=True)
    clash_detected: bool = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        course_code: str,
        start_date: date,
        end_date: date,
        start_time: time,
        end_time: time,
        clash_detected: bool,
    ) -> None:
        self.course_code = course_code
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.clash_detected = clash_detected

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "course_code": self.course_code,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "clash_detected": self.clash_detected,
        }
