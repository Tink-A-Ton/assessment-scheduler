from App.models import CourseAssessment
from App.models import Course
from App.database import db
from datetime import date, time


def add_assessment(
    course_code: str,
    start_date: date,
    end_date: date,
    start_time: time,
    end_time: time,
    clash_detected: bool,
) -> bool:
    existing_assessment = CourseAssessment.query.filter_by(
        course_code=course_code, start_date=start_date
    ).first()
    if existing_assessment is not None:
        return False
    new_assessment = CourseAssessment(
        course_code=course_code,
        start_date=start_date,
        end_date=end_date,
        start_time=start_time,
        end_time=end_time,
        clash_detected=clash_detected,
    )
    db.session.add(new_assessment)
    db.session.commit()
    return True


def get_assessments() -> list[CourseAssessment]:
    return CourseAssessment.query.all()


def get_assessment_by_id(id: int) -> CourseAssessment | None:
    return CourseAssessment.query.get(id)


def get_course(assessment_type: int) -> Course | None:
    assessment = CourseAssessment.query.get(id)
    if assessment:
        course: Course = Course.query.get(assessment.course_code)
        if course:
            return course
    return None


def get_assessments_by_course(course_code: str) -> list[CourseAssessment]:
    return CourseAssessment.query.filter_by(course_code=course_code).all()


def get_assessments_by_level(level: int) -> list[CourseAssessment]:
    courses = Course.query.filter_by(level=level).all()
    assessments: list[CourseAssessment] = []
    for course in courses:
        assessments.extend(course.assessments)
    return assessments


def delete_assessment_by_id(assessment_id: int) -> bool:
    assessment: CourseAssessment | None = get_assessment_by_id(assessment_id)
    if assessment:
        db.session.delete(assessment)
        db.session.commit()
        return True
    return False


# def get_clashes():
# return CourseAssessment.query.filter_by(clash_detected=True).all()
