import os, csv
from datetime import date, datetime
from werkzeug.utils import secure_filename
from ..models import Admin
from .exam import get_exam, get_exams
from ..models import Exam
from .course import create_course
from ..database import db


def allow_override(id: int) -> None:
    exam: Exam | None = get_exam(id)
    if exam:
        exam.clash_detected = False


def deny_override(id: int) -> None:
    exam: Exam | None = get_exam(id)
    if not exam:
        return
    exam.clash_detected = False
    exam.start_date = None
    exam.start_time = None
    exam.end_time = None
    db.session.commit()


def process_file(file) -> None:
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
                int(row["Semester"]),
            )


def get_search_results(day: str | None) -> list[Exam]:
    if not day:
        return []
    start_date: date = datetime.strptime(day, "%Y-%m-%d").date()
    return [a for a in get_exams() if start_date <= a.start_date]


def create_admin(id, email, password) -> Admin:
    admin: Admin = Admin(id, email, password)
    db.session.add(admin)
    db.session.commit()
    return admin
