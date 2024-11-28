from ..course import Course
from ..courseAssessment import CourseAssessment
from .clashDetection import ClashDetection
from ..courseProgramme import CourseProgramme


class ProgrammeLevelClash(ClashDetection):
    """
    Prevents exam clashes within the same programme for courses on the same day.
    """

    def detect_clash(self, new_assessment: CourseAssessment) -> bool:
        assessment_course: Course = Course.query.get(new_assessment.course_code)
        level_courses: list[Course] = Course.query.filter_by(
            level=assessment_course.level
        ).all()
        programme_courses: list[CourseProgramme] = CourseProgramme.query.filter_by(
            course_code=new_assessment.course_code
        ).all()
        programme_level_courses: list[Course] = [
            course
            for course in level_courses
            if course.course_code in [pc.course_code for pc in programme_courses]
        ]
        return any(
            assessment.start_date == new_assessment.start_date
            and assessment.id != new_assessment.id
            for course in programme_level_courses
            for assessment in CourseAssessment.query.filter_by(
                course_code=course.course_code
            ).all()
        )
