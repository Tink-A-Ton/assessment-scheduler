from ..models import Semester
from ..database import db


def create_semester(
    start_date: str, end_date: str, semester_number: int, max_exams: int
) -> Semester:
    semester = Semester(start_date, end_date, semester_number, max_exams)
    db.session.add(semester)
    db.session.commit()
    return semester


def get_semester() -> dict[str, str | int]:
    semester: Semester = Semester.query.order_by(Semester.id.desc()).first()
    return semester.to_json()
