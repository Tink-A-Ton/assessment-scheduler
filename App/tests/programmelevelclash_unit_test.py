import unittest, logging
from App.models.domain import ProgrammeCourse, Exam
from App.models.strategy import ProgrammeLevelClash

LOGGER: logging.Logger = logging.getLogger(__name__)

class ProgrammeLevelClashUnitTests(unittest.TestCase):
    def test_new_programmelevelclash(self) -> None:
        programme_level_clash = ProgrammeLevelClash()
        self.assertIsInstance(programme_level_clash, ProgrammeLevelClash, "programme_level_clash should be an instance of ProgrammeLevelClash")

    def test_detect_clash(self) -> None:
        programme_level_clash = ProgrammeLevelClash()
        programme_course1: ProgrammeCourse = ProgrammeCourse("COMP1601", 1)
        programme_course2: ProgrammeCourse = ProgrammeCourse("INFO1601", 1)
        exam1: Exam = Exam("COMP1601", "2024-01-01", "10:00", "11:00", False)
        exam2: Exam = Exam("INFO1601", "2024-01-01", "10:00", "11:00", False)
        self.assertTrue(programme_level_clash.detect_clash(exam1))
        self.assertFalse(programme_level_clash.detect_clash(exam2))
