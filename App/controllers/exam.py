from App.models.utils import parse_date, parse_time
from ..models import Exam
from ..database import db


def create_exam(
    course_code: str, start_date, start_time, end_time, clash: bool = False
) -> Exam:
    exam_exist: Exam = Exam.query.filter_by(
        course_code=course_code,
        start_date=start_date,
    ).first()
    if exam_exist is not None:
        return exam_exist
    exam = Exam(course_code, start_date, start_time, end_time, clash)
    db.session.add(exam)
    db.session.commit()
    return exam


def get_exams_by_course(course_code: str) -> list[Exam]:
    return Exam.query.filter_by(course_code=course_code).all()


def get_clashes() -> list[Exam]:
    return Exam.query.filter_by(clash_detected=True).all()


def get_exams() -> list[Exam]:
    return Exam.query.all()


def get_exam(id: int) -> Exam | None:
    return Exam.query.get(id)


def get_exams_json() -> list[dict[str, str]]:
    return [exam.to_json() for exam in get_exams()]


def update_exam(id: int, start_date, start_time, end_time) -> Exam | None:
    exam: Exam | None = get_exam(id)
    if exam is None:
        return None
    exam.start_date = parse_date(start_date)
    exam.start_time = parse_time(start_time)
    exam.end_time = parse_time(end_time)
    db.session.commit()
    return exam


def delete_exam(exam_id: int) -> bool:
    exam: Exam | None = get_exam(exam_id)
    if exam is None:
        return False
    db.session.delete(exam)
    db.session.commit()
    from .clash import recheck_nearby_clashes

    recheck_nearby_clashes(exam.start_date)
    return True
