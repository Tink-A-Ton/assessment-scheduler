from types import new_class
from ..course import Course
from ..courseAssessment import CourseAssessment
from ..semester import Semester
from .clashDetection import ClashDetection
from ..courseProgramme import CourseProgramme

class ProgrammeLevelClash(ClashDetection):
    """
    This class implements the programme clash detection strategy such that exams for
    courses of the same programme cannot schedule exams on the same day.
    """
    def detect_clash(self, new_assessment: CourseAssessment) -> bool:
        programmes: list[CourseProgramme] = CourseProgramme.query.filter_by(course_code=new_assessment.course_code).all()
        assessment_course: Course = Course.query.get(new_assessment.course_code)
        programme_courses: list[CourseProgramme] = []
        for programme in programmes:
            programme_courses.extend(
                CourseProgramme.query.filter_by(programme_id=programme.programme_id).all()
            )
        level_courses: list[Course] = Course.query.filter_by(level=assessment_course.level).all()
        programme_level_courses: list[Course] = [
            course
            for course in level_courses
            for programme_course in programme_courses
            if course.course_code == programme_course.course_code
        ]
        programme_assessments: list[CourseAssessment] = []
        for course in programme_level_courses:
            programme_assessments.extend(
                CourseAssessment.query.filter_by(course_code=course.course_code).all()
            )
        for assessment in programme_assessments:
            if assessment.start_date == new_assessment.start_date and assessment.id != new_assessment.id:
                return True
        return False