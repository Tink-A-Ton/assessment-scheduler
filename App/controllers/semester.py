from App.models import Semester
from App.database import db


def add_sem(start_date, end_date, semester_number, max_assessments) -> Semester:
    new_sem = Semester(
        start_date=start_date,
        end_date=end_date,
        semester_number=semester_number,
        max_assessments=max_assessments,
    )
    db.session.add(new_sem)
    db.session.commit()
    return new_sem
