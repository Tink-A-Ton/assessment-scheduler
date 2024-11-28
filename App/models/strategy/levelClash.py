from ..course import Course
from ..courseAssessment import CourseAssessment
from ..semester import Semester
from .clashDetection import ClashDetection


class LevelClash(ClashDetection):
    """
    This class implements the level clash detection strategy such that exams for
    courses of the same academic level cannot have overlapping time slots.
    """
    def detect_clash(self, new_assessment: CourseAssessment) -> bool:
        sem: Semester = Semester.query.order_by(Semester.id.desc()).first()

        scheduled_assessments: list[CourseAssessment] = CourseAssessment.query.filter_by(
            start_date=new_assessment.start_date)
        course_level: int = Course.query.get(new_assessment.course_code).level
        relevant_assessments: list[CourseAssessment] = [
            assessment
            for assessment in scheduled_assessments
            if Course.query.get(assessment.course_code).level == course_level
            and assessment.id != new_assessment.id
        ]
        
        for assessment in relevant_assessments:
            if new_assessment.start_time >= assessment.start_time and new_assessment.start_time <= assessment.end_time:
                return True
            if new_assessment.end_time >= assessment.start_time and new_assessment.end_time <= assessment.end_time:
                return True
        return False