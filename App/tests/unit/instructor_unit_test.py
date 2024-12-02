import logging,unittest
from ...models.users.instructor import Instructor

LOGGER: logging.Logger = logging.getLogger(__name__)

class InstructorUnitTests(unittest.TestCase):
    def test_new_instructor(self) -> None:
        new_instructor: Instructor = Instructor(610000000, "COMP3600")
        self.assertEqual(new_instructor.staff_id, 610000000, "Instructor Staff ID Mismatch")
        self.assertEqual(new_instructor.course_code, "COMP3600", "Instructor Course Code Mismatch")
    
    def test_instructor_to_json(self) -> None:
        new_instructor: Instructor = Instructor(610000000, "COMP3600")
        instructor_json: dict[str, str | int] = new_instructor.to_json()
        del instructor_json['id']
        expected_json: dict[str, str | int] = {
            "staff_id": 610000000,
            "course_code": "COMP3600"
        }
        self.assertEqual(instructor_json, expected_json, "Instructor JSON does not match expected fields or values")
