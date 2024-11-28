from ..domain.course import Course
from ..domain.exam import Exam
from .clashDetection import ClashDetection
from ..domain.programmeCourse import ProgrammeCourse


class ProgrammeLevelClash(ClashDetection):
    """
    Prevents exam clashes within the same programme for courses on the same day.
    """

    def detect_clash(self, new_exam: Exam) -> bool:
        programmes: list[ProgrammeCourse] = ProgrammeCourse.query.filter_by(
            course_code=new_exam.course_code
        ).all()
        exam_course: Course = Course.query.get(new_exam.course_code)
        programme_courses: list[ProgrammeCourse] = []
        for programme in programmes:
            programme_courses.extend(
                ProgrammeCourse.query.filter_by(programme_id=programme.programme_id).all()
            )
        level_courses: list[Course] = Course.query.filter_by(
            level=exam_course.level
        ).all()
        programme_level_courses: list[Course] = [
            course
            for course in level_courses
            for programme_course in programme_courses
            if course.course_code == programme_course.course_code
        ]
        programme_exams: list[Exam] = []
        for course in programme_level_courses:
            programme_exams.extend(
                Exam.query.filter_by(course_code=course.course_code).all()
            )
        for exam in programme_exams:
            if exam.start_date == new_exam.start_date and exam.id != new_exam.id:
                return True
        return False
