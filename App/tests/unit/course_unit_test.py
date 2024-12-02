import logging,unittest
from ...models.domain.course import Course

LOGGER: logging.Logger = logging.getLogger(__name__)

class CourseUnitTests(unittest.TestCase):
    def test_new_course(self) -> None:
        new_course: Course = Course("COMP3602", 1, "Theory of Computation", 3)
        self.assertEqual(new_course.course_code, "COMP3602", "Course Code Mismatch")
        self.assertEqual(new_course.semester_id, 1, "Semester ID Mismatch")
        self.assertEqual(new_course.course_title, "Theory of Computation", "Course Title Mismatch")
        self.assertEqual(new_course.level, 3, "Course Level Mismatch")

    def test_course_to_json(self) -> None:
        new_course: Course = Course("COMP3602", 1, "Theory of Computation", 3)
        course_json: dict[str, str | int] = new_course.to_json()
        expected_json: dict[str, str | int] = {"course_code": "COMP3602", "semester_id": 1, "course_title": "Theory of Computation", "level": 3}
        self.assertEqual(course_json, expected_json, "Course JSON does not match expected fields or values")
