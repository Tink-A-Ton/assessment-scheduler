from datetime import date, datetime
from werkzeug.utils import secure_filename
import os, csv
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


def get_search_results(day: str) -> list[Exam]:
    start_date: date = datetime.strptime(day, "%Y-%m-%d").date()
    search_results: list[Exam] = []
    for a in get_exams():
        if start_date <= a.start_date:
            search_results.append(a)
    return search_results
