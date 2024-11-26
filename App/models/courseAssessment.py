from App.database import db
from datetime import datetime, date, time


class CourseAssessment(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code: str = db.Column(
        db.String(9), db.ForeignKey("course.course_code"), nullable=False
    )
    assessment_id: int = db.Column(
        db.Integer, db.ForeignKey("assessment.id"), nullable=False
    )
    start_date: date = db.Column(db.Date, nullable=True)
    end_date: date = db.Column(db.Date, nullable=True)
    start_time: time = db.Column(db.Time, nullable=True)
    end_time: time = db.Column(db.Time, nullable=True)
    clash_detected: bool = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        course_code: str,
        assessment_id: int,
        start_date: date,
        end_date: date,
        start_time: time,
        end_time: time,
        clash_detected: bool,
    ) -> None:
        self.course_code = course_code
        self.assessment_id = assessment_id
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.clash_detected = clash_detected

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "course_code": self.course_code,
            "assessment_id": self.assessment_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "clash_detected": self.clash_detected,
        }
