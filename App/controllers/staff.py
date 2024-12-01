from .exam import get_exams_by_course
from .course import get_course
from ..models import Staff, Course, Instructor
from ..database import db
from sqlalchemy.exc import SQLAlchemyError


def create_staff(
    id: int, email: str, password: str, first_name: str, last_name: str, position: str
) -> bool:
    try:
        staff: Staff = Staff(id, email, password, first_name, last_name, position)
        db.session.add(staff)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error creating staff: {e}")
        return False


def add_instructor(staff_id: int, course_code: str) -> None:
    instructor: Instructor | None = Instructor.query.filter_by(
        staff_id=staff_id, course_code=course_code
    ).first()
    if instructor is not None:
        return
    instructor = Instructor(staff_id, course_code)
    db.session.add(instructor)
    db.session.commit()


def get_staff(id: int) -> Staff:
    return Staff.query.get(id)


def get_instructors(staff_id: int) -> list[Instructor]:
    return Instructor.query.filter_by(staff_id=staff_id).all()


def get_registered_courses(staff_id) -> list[Course]:
    return [get_course(staff.course_code) for staff in get_instructors(staff_id)]


def get_staff_exams(staff_id) -> list[dict]:
    return [
        assessment.to_json()
        for course in get_registered_courses(staff_id)
        for assessment in get_exams_by_course(course.course_code)
    ]


def get_staff_courses(staff_id: int) -> list[dict]:
    return [course.to_json() for course in get_registered_courses(staff_id)]
