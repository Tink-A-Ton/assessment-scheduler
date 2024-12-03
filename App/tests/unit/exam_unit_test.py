from datetime import date, time
import logging,unittest
from ...models.domain.exam import Exam

LOGGER: logging.Logger = logging.getLogger(__name__)

class ExamUnitTests(unittest.TestCase):
    def test_new_exam(self) -> None:
        new_exam: Exam = Exam("3600", date.today(), time(10, 0), time(12, 0), False)
        self.assertEqual(new_exam.course_code, "3600", "Course Code Mismatch")
        self.assertEqual(new_exam.start_date, date.today(), "Start Date Mismatch")
        self.assertEqual(new_exam.start_time, time(10, 0), "Start Time Mismatch")
        self.assertEqual(new_exam.end_time, time(12, 0), "End Time Mismatch")
        self.assertFalse(new_exam.clash_detected, "Clash Detected should be False")

    def test_exam_to_json(self) -> None:
        new_exam: Exam = Exam("3600", date(2024,1,1), time(10, 0), time(12, 0), False)
        exam_json: dict[str, str | int | bool] = new_exam.to_json()
        del exam_json['id']
        expected_json: dict[str, str | int | bool] = {
            "course_code": "3600",
            "start_date": "2024-01-01",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "clash_detected": False
        }
        self.assertEqual(exam_json, expected_json, "Exam JSON does not match expected fields or values")

