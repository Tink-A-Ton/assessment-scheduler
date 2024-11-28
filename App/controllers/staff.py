from App.models import Staff, Course
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from ..models import Instructor


def create_staff(id, email, password, first_name, last_name, position) -> Staff | None:
    try:
        staff: Staff = Staff(id, email, password, first_name, last_name, position)
        db.session.add(staff)
        db.session.commit()
        return staff
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error creating staff: {e}")
        return None


def add_course_instructor(staff_id, course_code) -> Instructor:
    instructor: Instructor | None = Instructor.query.filter_by(
        staff_id=staff_id, course_code=course_code
    ).first()
    if instructor is not None:
        return instructor
    instructor = Instructor(staff_id, course_code)
    db.session.add(instructor)
    db.session.commit()
    return instructor


def get_registered_courses(staff_id) -> list[Course]:
    course_listing: list[Instructor] = Instructor.query.filter_by(staff_id=staff_id).all()
    instructor_courses: list[Course] = []
    for listing in course_listing:
        instructor_courses.append(Course.query.get(listing.course_code))
    return instructor_courses
