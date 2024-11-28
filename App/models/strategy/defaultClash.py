from datetime import date, timedelta
from ...controllers.assessment import get_assessments
from ..courseAssessment import CourseAssessment
from ..semester import Semester
from .clashDetection import ClashDetection


class DefaultClash(ClashDetection):
    def detect_clash(self, new_assessment: CourseAssessment) -> bool:
        if not new_assessment.end_date:
            return False

        semester: Semester = Semester.query.order_by(Semester.id.desc()).first()
        max_assessments: int = semester.max_assessments
        course_prefix: str = new_assessment.course_code.replace(" ", "")[4]
        sunday, saturday = self.get_week_range(new_assessment.end_date.isoformat())

        relevant_assessments: list[CourseAssessment] = [
            assessment
            for assessment in get_assessments()
            if assessment.course_code.replace(" ", "")[4] == course_prefix
            and assessment.id != new_assessment.id
            and assessment.start_date
        ]

        clashes: int = sum(sunday <= a.end_date <= saturday for a in relevant_assessments)
        return clashes >= max_assessments

    def get_week_range(self, date_str: str) -> tuple[date, date]:
        """Sunday - Saturday Week"""
        input_date: date = date.fromisoformat(date_str)
        start_of_week: date = input_date - timedelta(days=(input_date.weekday() + 1) % 7)
        end_of_week: date = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week
