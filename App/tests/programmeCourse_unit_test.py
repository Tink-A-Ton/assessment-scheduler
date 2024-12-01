import logging,unittest
from App.models.domain.programmeCourse import ProgrammeCourse

LOGGER: logging.Logger = logging.getLogger(__name__)

class ProgrammeCourseUnitTests(unittest.TestCase):
    def test_new_programme_course(self) -> None:
        new_programme_course = ProgrammeCourse(course_code="3600", programme_id=1)
        self.assertIsInstance(new_programme_course, ProgrammeCourse, "new_programme_course should be an instance of ProgrammeCourse")
        self.assertEqual(new_programme_course.course_code, "3600", "Course Code Mismatch")
        self.assertEqual(new_programme_course.programme_id, 1, "Programme ID Mismatch") 

    def test_programme_course_to_json(self) -> None:
        new_programme_course = ProgrammeCourse(course_code="3600", programme_id=1)
        programme_course_json: dict[str, str | int] = new_programme_course.to_json()
        expected_json: dict[str, str | int] = {"course_code": "3600", "programme_id": 1}
        self.assertEqual(programme_course_json, expected_json, "Programme Course JSON does not match expected fields or values")
