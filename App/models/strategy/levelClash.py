from ..course import Course
from ..courseAssessment import CourseAssessment
from .clashDetection import ClashDetection


class LevelClash(ClashDetection):
    """
    Detects clashes where exams for courses of the same academic level
    cannot overlap in time.
    """

    def detect_clash(self, new_assessment: CourseAssessment) -> bool:
        course_level: int = Course.query.get(new_assessment.course_code).level
        relevant_assessments: list[CourseAssessment] = CourseAssessment.query.filter(
            CourseAssessment.start_date == new_assessment.start_date,
            CourseAssessment.id != new_assessment.id,
        ).all()

        return any(
            Course.query.get(assessment.course_code).level == course_level
            and (
                new_assessment.start_time <= assessment.end_time
                and new_assessment.end_time >= assessment.start_time
            )
            for assessment in relevant_assessments
        )
