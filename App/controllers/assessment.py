from App.models import Assessment
from App.models import Course
from App.database import db

def add_assessment(course_code: str, given_date: str, end_date: str, category: str) -> bool:
    existing_assessment = Assessment.query.filter_by(course_code=course_code, given_date=given_date).first()
    if existing_assessment is not None: 
        return False
    new_assessment = Assessment(course_code=course_code, given_date=given_date, end_date=end_date, category=category)
    db.session.add(new_assessment)
    db.session.commit()
    return True

def get_assessments() -> list[Assessment]:
    return Assessment.query.all()

def get_assessment_type(id: int) -> str | None:
    assessment = Assessment.query.filter_by(id=id).first()
    return assessment.category.name

def get_assessment_by_id(id: int) -> Assessment | None:
    return Assessment.query.get(id)

def get_course(assessment_id: int) -> Course | None:
    assessment = Assessment.query.filter_by(id = id)
    if assessment:
        course = Course.query.filter_by(course_code = assessment.course_code)

def get_assessments_by_course(course_code: str) -> list[Assessment] | None:
    return Assessment.query.filter_by(course_code=course_code).all()

def get_assessments_by_level(level:int)->list[Assessment] | None:
    courses = Course.query.filter_by(level=level).all()
    assessments: list[Assessment] = []
    for course in courses:
        assessments.extend(course.assessments)
    return assessments

def delete_assessment(assessment_id: int) -> bool:
    assessment = Assessment.query.filter_by(id = assessment_id).first()
    if assessment:
        db.session.delete(assessment)
        db.session.commit()
        return True
    return False

# def get_clashes():
    # return CourseAssessment.query.filter_by(clash_detected=True).all()
