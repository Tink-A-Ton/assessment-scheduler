import unittest, logging
from App.models.strategy.levelClash import LevelClash
from models.domain.exam import Exam

LOGGER: logging.Logger = logging.getLogger(__name__)

class LevelClashUnitTests(unittest.TestCase):
    def test_new_levelclash(self) -> None:
        level_clash = LevelClash()
        self.assertIsInstance(level_clash, LevelClash, "level_clash should be an instance of LevelClash")
        
    def test_detect_clash(self) -> None:
        level_clash = LevelClash()
        exam1: Exam = Exam("COMP1601", "2024-01-01", "10:00", "11:00", False)
        exam2: Exam = Exam("INFO1601", "2024-01-01", "10:00", "11:00", False)
        self.assertTrue(level_clash.detect_clash(exam1))
        self.assertFalse(level_clash.detect_clash(exam2))


