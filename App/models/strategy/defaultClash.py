from ..utils import get_week_range
from ...controllers.exam import get_exams
from ..domain.exam import Exam
from ..domain.semester import Semester
from .clashDetection import ClashDetection


class DefaultClash(ClashDetection):
    def detect_clash(self, new_exam: Exam) -> bool:
        if not new_exam.start_date:
            return False

        semester: Semester = Semester.query.order_by(Semester.id.desc()).first()
        max_exams: int = semester.max_exams
        course_prefix: str = new_exam.course_code.replace(" ", "")[4]
        sunday, saturday = get_week_range(new_exam.start_date.isoformat())

        relevant_exams: list[Exam] = [
            exam
            for exam in get_exams()
            if exam.course_code.replace(" ", "")[4] == course_prefix
            and exam.id != new_exam.id
            and exam.start_date
        ]

        clashes: int = sum(sunday <= a.start_date <= saturday for a in relevant_exams)
        return clashes >= max_exams
