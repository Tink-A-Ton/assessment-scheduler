from App.database import db


class CourseInstructor(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id: int = db.Column(db.Integer, db.ForeignKey("staff.id"))
    course_code: str = db.Column(db.String(120), db.ForeignKey("course.course_code"))

    def __init__(self, staff_id: int, course_code: str) -> None:
        self.staff_id = staff_id
        self.course_code = course_code

    def to_json(self) -> dict[str, str | int]:
        return {
            "id": self.id,
            "staff_id": self.staff_id,
            "course_code": self.course_code,
        }
