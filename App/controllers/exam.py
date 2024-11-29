from ..models import Course, Exam
from ..database import db
from datetime import date, time
from .course import get_course


def create_exam(
    course_code: str, start_date: date, start_time: time, end_time: time, clash: bool
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


def get_exam_by_course(id: int) -> Course | None:
    exam: Exam | None = get_exam(id)
    if exam is None:
        return None
    return get_course(exam.course_code)


def get_exams_by_course(course_code: str) -> list[Exam]:
    return Exam.query.filter_by(course_code=course_code).all()


def delete_exam(exam_id: int) -> bool:
    exam: Exam | None = get_exam(exam_id)
    if exam is None:
        return False
    db.session.delete(exam)
    db.session.commit()
    return True


def get_clashes() -> list[Exam]:
    return Exam.query.filter_by(clash_detected=True).all()


def get_exams() -> list[Exam]:
    return Exam.query.all()


def get_exam(id: int) -> Exam | None:
    return Exam.query.get(id)


def edit_exam(id: int, start_date, start_time, end_time) -> None | Exam:
    exam: Exam | None = get_exam(id)
    if exam is None:
        return None
    exam.start_date = start_date
    exam.start_time = start_time
    exam.end_time = end_time
    db.session.commit()
    return exam
