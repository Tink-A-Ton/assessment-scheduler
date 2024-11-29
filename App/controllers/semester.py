from datetime import date
from App.models import Semester
from App.database import db
from App.models import Course


def create_semester(
    start_date: str, end_date: str, semester_number: int, max_exams: int
) -> Semester:
    semester = Semester(start_date, end_date, semester_number, max_exams)
    db.session.add(semester)
    db.session.commit()
    return semester


def get_courses_offered(semester_id: int) -> list[Course]:
    semester: Semester = Semester.query.get(semester_id)
    return semester.courses_offered


def get_semester() -> dict[str, str]:
    semester: Semester = Semester.query.order_by(Semester.id.desc()).first()
    return {
        "start": semester.start_date,
        "end": semester.end_date,
    }
