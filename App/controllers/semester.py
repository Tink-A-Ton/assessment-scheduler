from ..models import Semester
from ..database import db


def create_semester(
    start_date: str, end_date: str, semester_number: int, max_exams: int
) -> Semester:
    semester = Semester(start_date, end_date, semester_number, max_exams)
    db.session.add(semester)
    db.session.commit()
    return semester


def get_semester() -> Semester:
    return Semester.query.order_by(Semester.id.desc()).first()


def get_semester_json() -> dict[str, str | int]:
    semester: Semester = get_semester()
    return semester.to_json()
