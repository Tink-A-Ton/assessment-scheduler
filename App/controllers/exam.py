from App.models import Exam
from App.models import Course
from App.database import db
from datetime import date, time


def add_exam(
    course_code: str,
    start_date: date,
    start_time: time,
    end_time: time,
    clash_detected: bool,
) -> Exam:
    exam_exist: Exam = Exam.query.filter_by(
        course_code=course_code, start_date=start_date
    ).first()
    if exam_exist is not None:
        return exam_exist
    exam = Exam(
        course_code=course_code,
        start_date=start_date,
        start_time=start_time,
        end_time=end_time,
        clash_detected=clash_detected,
    )
    db.session.add(exam)
    db.session.commit()
    return exam


def get_exams() -> list[Exam]:
    return Exam.query.all()


def get_exam(id: int) -> Exam | None:
    return Exam.query.get(id)


def get_exam_course(id: int) -> Course | None:
    exam = Exam.query.get(id)
    if exam:
        course: Course | None = Course.query.get(exam.course_code)
        if course:
            return course
    return None


def get_exams_by_course(course_code: str) -> list[Exam]:
    return Exam.query.filter_by(course_code=course_code).all()


def get_exams_by_level(level: int) -> list[Exam]:
    courses = Course.query.filter_by(level=level).all()
    exams: list[Exam] = []
    for course in courses:
        exams.extend(course.exams)
    return exams


def delete_exam_by_id(exam_id: int) -> bool:
    exam: Exam | None = get_exam(exam_id)
    if exam:
        db.session.delete(exam)
        db.session.commit()
        return True
    return False


def get_clashes() -> list[Exam]:
    return Exam.query.filter_by(clash_detected=True).all()
