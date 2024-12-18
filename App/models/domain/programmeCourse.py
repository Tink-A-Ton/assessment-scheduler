from ...database import db


class ProgrammeCourse(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code: str = db.Column(db.String(9), db.ForeignKey("course.course_code"))
    programme_id: int = db.Column(db.Integer, db.ForeignKey("programme.id"))

    def __init__(self, course_code: str, programme_id: int) -> None:
        self.course_code = course_code
        self.programme_id = programme_id

    def to_json(self) -> dict[str, str | int]:
        return {"course_code": self.course_code, "programme_id": self.programme_id}
