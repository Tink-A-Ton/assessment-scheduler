from typing import Optional
from ..models import Course
from ..database import db


def create_course(course_code: str, course_title: str, level: int, semester: int) -> bool:
    course_exist: Optional[Course] = Course.query.get(course_code)
    if course_exist:
        return False
    course = Course(course_code, semester, course_title, level)
    db.session.add(course)
    db.session.commit()
    return True


def get_courses() -> list[Course]:
    return Course.query.all()


def get_course(course_code: str) -> Optional[Course]:
    return Course.query.get(course_code)


def edit_course(course_code: str, course_title: str, level: int) -> Optional[Course]:
    course: Optional[Course] = get_course(course_code)
    if course is None:
        return None
    course.course_title = course_title
    course.level = level
    db.session.commit()
    return course


def delete_course(course_code: str) -> bool:
    course: Optional[Course] = get_course(course_code)
    if course is None:
        return False
    db.session.delete(course)
    db.session.commit()
    return True


def get_available_courses(staff_courses) -> list[Course]:
    return [c for c in get_courses() if c not in staff_courses]
