from datetime import date, time
import logging,unittest
from App.models.domain.exam import Exam

LOGGER: logging.Logger = logging.getLogger(__name__)

class ExamUnitTests(unittest.TestCase):
    def test_new_exam(self) -> None:
        new_exam = Exam(course_code="3600", start_date=date.today(), start_time=time(10, 0), end_time=time(12, 0), clash_detected=False)
        self.assertIsInstance(new_exam, Exam, "new_exam should be an instance of Exam")
        self.assertEqual(new_exam.course_code, "3600", "Course Code Mismatch")
        self.assertEqual(new_exam.start_date, date.today(), "Start Date Mismatch")
        self.assertEqual(new_exam.start_time, time(10, 0), "Start Time Mismatch")
        self.assertEqual(new_exam.end_time, time(12, 0), "End Time Mismatch")
        self.assertFalse(new_exam.clash_detected, "Clash Detected should be False")

    def test_exam_to_json(self) -> None:
        new_exam :Exam = Exam(course_code="3600", start_date=date.today(), start_time=time(10, 0), end_time=time(12, 0), clash_detected=False)
        exam_json: dict[str, str | int | bool] = new_exam.to_json()
        del exam_json['id']
        expected_json: dict[str, str | int | bool] = {
            "course_code": "3600",
            "start_date": date.today().isoformat(),
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "clash_detected": False
        }
        self.assertEqual(exam_json, expected_json, "Exam JSON does not match expected fields or values")

