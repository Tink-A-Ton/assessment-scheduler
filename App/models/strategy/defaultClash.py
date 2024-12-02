from ..domain import Exam, Course
from .clashDetection import ClashDetection


class DefaultClash(ClashDetection):
    """
    Detects clashes where exams for courses of the same academic level
    cannot overlap in time.
    """
    def detect_clash(self, new_exam: Exam) -> bool:
        course_level: int = Course.query.get(new_exam.course_code).level
        relevant_exams: list[Exam] = Exam.query.filter(
            Exam.start_date == new_exam.start_date,
            Exam.id != new_exam.id,
        ).all()

        return any(
            Course.query.get(exam.course_code).level == course_level
            and (
                new_exam.start_time <= exam.end_time
                and new_exam.end_time >= exam.start_time
            )
            for exam in relevant_exams
        )
