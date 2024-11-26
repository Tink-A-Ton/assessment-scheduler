from App.models import Course
from App.models import Assessment
from App.database import db

def add_course(course_code: str, course_title: str, level: int, semester: int) -> bool:
    existing_course = Course.query.filter_by(course_code=course_code).first()
    if existing_course is not None:
        return False
    new_course = Course(course_code=course_code, semester_id=semester, course_title=course_title, level=level)
    db.session.add(new_course)
    db.session.commit()
    return True

def get_all_courses() -> list[Course]:
    return Course.query.all() 

def get_course(course_code: str) -> Course | None:
    return Course.query.filter_by(course_code=course_code).first()

def edit_course(course_code: str, semester_id: int, course_title: str, level: int) -> Course | None:
    existing_course = Course.query.filter_by(course_code=course_code).first()
    if existing_course:
        existing_course.semester_id = semester_id
        existing_course.course_title = course_title
        existing_course.level = level
        db.session.add(existing_course)
        db.session.commit()
        return existing_course
    return None    

def get_course_level(course_code: str) -> int | None:
    course = Course.query.filter_by(course_code=course_code).first()
    if course:
        return course.level
    return None

def get_courses_by_level(level: int) -> list[Course] | None:
    return Course.query.filter_by(level = level).all()


def delete_course(course_code: str) -> bool:
    course_to_delete = Course.query.filter_by(course_code=course_code).first()
    if course_to_delete:
        db.session.delete(course_to_delete)
        db.session.commit()
        return True
    return False