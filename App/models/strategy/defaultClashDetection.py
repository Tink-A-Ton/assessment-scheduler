from datetime import date, timedelta
from ..courseAssessment import CourseAssessment
from ..semester import Semester
from .clashDetection import ClashDetection


class DefaultClashDetection(ClashDetection):
    def detect_clash(self, new_assessment: CourseAssessment) -> bool:
        clash = 0
        sem: Semester = Semester.query.order_by(Semester.id.desc()).first()
        max_assessments: int = sem.max_assessments
        print(max_assessments)

        compare_code: str = new_assessment.course_code.replace(" ", "")
        all_assessments: list[CourseAssessment] = CourseAssessment.query.all()

        if not new_assessment.end_date:  # dates not set yet
            return False

        relevant_assessments: list[CourseAssessment] = [
            a
            for a in all_assessments
            if a.course_code.replace(" ", "")[4] == compare_code[4]
            and a.id != new_assessment.id
            and a.start_date is not None
        ]

        sunday, saturday = get_week_range(new_assessment.end_date.isoformat())
        for assessment in relevant_assessments:
            due_date = assessment.end_date
            if sunday <= due_date <= saturday:
                clash += 1

        return clash >= max_assessments


def get_week_range(iso_date_str) -> tuple[date, date]:
    date_obj: date = date.fromisoformat(iso_date_str)
    day_of_week: int = date_obj.weekday()

    if day_of_week != 6:
        days_to_subtract: int = (day_of_week + 1) % 7
    else:
        days_to_subtract = 0

    sunday_date: date = date_obj - timedelta(days=days_to_subtract)
    saturday_date: date = sunday_date + timedelta(days=6)
    return sunday_date, saturday_date
