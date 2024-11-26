from App.models import Staff
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from App.models.courseInstructor import CourseInstructor


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


def add_course_instructor(staff_id, course_code) -> CourseInstructor:
    instructor: CourseInstructor | None = CourseInstructor.query.filter_by(
        staff_id=staff_id, course_code=course_code
    ).first()
    if instructor is not None:
        return instructor
    instructor = CourseInstructor(staff_id, course_code)
    db.session.add(instructor)
    db.session.commit()
    return instructor


def get_registered_courses(staff_id):
    course_listing = CourseInstructor.query.filter_by(staff_id=staff_id).all()
    return course_listing
