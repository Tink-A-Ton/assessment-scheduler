from datetime import date, time
import logging,unittest

from ...models.domain.exam import Exam
from ...models.strategy import ClashContext
from ...controllers.exam import create_exam
from ...controllers.course import create_course
from ...database import db
from ... import create_app
LOGGER: logging.Logger = logging.getLogger(__name__)

class ClashContextIntegrationTests(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_remove_rule(self) -> None:
        new_clash_context = ClashContext()
        length: int = len(new_clash_context.strategies)
        self.assertGreater(length, 0, "strategies should have atleast one rule")
        new_clash_context.remove_rule("rule0")
        self.assertEqual(len(new_clash_context.strategies), length - 1, "strategies should have one less rule after removing one")

    def test_clash_context_detect_clash(self) -> None:
        """Test that clash detection works correctly with multiple rules."""
        new_clash_context = ClashContext()
        exam1: Exam = create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
        exam2: Exam = create_exam("COMP3602", date(2024, 2, 1), time(10, 0), time(12, 0))
        create_course("COMP1601", "Programming I",1, 1)
        create_course("COMP3602", "Programming II", 1, 1)
        result: bool = new_clash_context.detect_clash(exam2)
        self.assertTrue(result, "Should detect a clash between overlapping exams")
        self.assertTrue(exam2.clash_detected, "Exam clash_detected flag should be set to True")
