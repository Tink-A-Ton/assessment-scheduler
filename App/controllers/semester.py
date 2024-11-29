from App.models import Semester
from App.database import db
from App.models import Course


def add_semester(start_date, end_date, semester_number, max_exams) -> Semester:
    new_sem = Semester(
        start_date=start_date,
        end_date=end_date,
        semester_number=semester_number,
        max_exams=max_exams,
    )
    db.session.add(new_sem)
    db.session.commit()
    return new_sem

def get_courses_offered(semester_id: int) -> list[Course]:
    semester: Semester | None = Semester.query.get(semester_id)
    if semester is None:
        return []
    return semester.courses_offered