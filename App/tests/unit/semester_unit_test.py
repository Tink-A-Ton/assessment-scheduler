import logging,unittest
from App.models.domain.semester import Semester

LOGGER: logging.Logger = logging.getLogger(__name__)

class SemesterUnitTests(unittest.TestCase):
    def test_new_semester(self) -> None:
        new_semester: Semester = Semester("2024-01-01", "2024-06-30", 1, 10)
        self.assertIsInstance(new_semester, Semester, "new_semester should be an instance of Semester")
        self.assertEqual(new_semester.start_date, "2024-01-01", "Start Date Mismatch")
        self.assertEqual(new_semester.end_date, "2024-06-30", "End Date Mismatch")
        self.assertEqual(new_semester.semester_number, 1, "Semester Number Mismatch")
        self.assertEqual(new_semester.max_exams, 10, "Max Exams Mismatch")

    def test_semester_to_json(self) -> None:
        new_semester: Semester = Semester("2024-01-01", "2024-06-30", 1, 10)
        semester_json: dict[str, str | int] = new_semester.to_json()
        del semester_json['id']
        expected_json: dict[str, str | int] = {
            "start_date": "2024-01-01",
            "end_date": "2024-06-30",
            "semester_number": 1,
            "max_exams": 10
        }
        self.assertEqual(semester_json, expected_json, "Semester JSON does not match expected fields or values")
    