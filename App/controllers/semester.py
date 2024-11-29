from App.models import Semester
from App.database import db
from App.models import Course


def add_semester(start_date, end_date, semester_number, max_exams) -> Semester:
    semester = Semester(start_date, end_date, semester_number, max_exams)
    db.session.add(semester)
    db.session.commit()
    return semester


def get_courses_offered(semester_id: int) -> list[Course]:
    semester: Semester = Semester.query.get(semester_id)
    return semester.courses_offered
