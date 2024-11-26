from App.database import db


class Course(db.Model):
    course_code: str = db.Column(db.String(9), primary_key=True)
    semester_id: int = db.Column(db.Integer, nullable=False)
    course_title: str = db.Column(db.String(120), nullable=False)
    level: int = db.Column(db.Integer, nullable=False)
    Assessments = db.relationship("Assessment", backref="course", lazy="joined")

    def __init__(
        self, course_code: str, semester_id: int, course_title: str, level: int
    ) -> None:
        self.course_code = course_code
        self.semester_id = semester_id
        self.course_title = course_title
        self.level = level

    def to_json(self) -> dict[str, str | int]:
        return {
            "course_code": self.course_code,
            "semester_id": self.semester_id,
            "course_title": self.course_title,
            "level": self.level,
        }
