import os, csv
from datetime import date, datetime
from typing import Optional
from werkzeug.utils import secure_filename
from ..models import Admin
from .exam import get_exam
from ..models import Exam
from .course import create_course
from ..database import db
from .semester import get_semester


def allow_override(id: int) -> None:
    exam: Optional[Exam] = get_exam(id)
    if exam:
        exam.clash_detected = False
        db.session.commit()


def deny_override(id: int) -> None:
    exam: Optional[Exam] = get_exam(id)
    if not exam:
        return
    exam.clash_detected = False
    exam.start_date = None
    exam.start_time = None
    exam.end_time = None
    db.session.commit()


def process_file(file) -> None:
    semester: dict[str, str | int] = get_semester()
    filename: str = secure_filename(file.filename)
    file.save(os.path.join("App/uploads", filename))
    fpath: str = "App/uploads/" + filename
    with open(fpath, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            create_course(
                row["Course Code"],
                row["Course Title"],
                int(row["Level"]),
                semester.id,
            )


def create_admin(id, email, password) -> Admin:
    admin: Admin = Admin(id, email, password)
    db.session.add(admin)
    db.session.commit()
    return admin
