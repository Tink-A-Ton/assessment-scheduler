from App.database import db


class CourseInstructor(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id: int = db.Column(db.Integer, db.ForeignKey("staff.id"))
    courseCode: str = db.Column(db.String(120), db.ForeignKey("course.courseCode"))

    def __init__(self, staff_id: int, courseCode: str) -> None:
        self.staff_id = staff_id
        self.courseCode = courseCode

    def to_json(self) -> dict[str, str | int]:
        return {
            "id": self.id,
            "staff_id": self.staff_id,
            "courseCode": self.courseCode,
        }