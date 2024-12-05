from datetime import date, time
import logging
import unittest
from ...models.strategy import ProgrammeLevelClash, LevelClash, ClashContext, DefaultClash
from ...controllers import create_course, create_exam, create_semester
from ...main import create_app
from ...database import db
from ...models.domain import Exam, ProgrammeCourse

LOGGER: logging.Logger = logging.getLogger(__name__)


class ClashIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test database and Flask application context."""
        self.app = create_app(
            {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"}
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        create_course("COMP1601", "Programming I", 1, 1)
        create_course("COMP1602", "Programming II", 1, 1)
        create_course("COMP3602", "Theory of Computation", 3, 1)
        create_course("COMP1603", "Programming III", 3, 1)
        create_semester("2024-01-01", "2024-06-30", 1, 2)
        prog_course1 = ProgrammeCourse("COMP1601", 1)
        prog_course2 = ProgrammeCourse("COMP1602", 1)
        db.session.add(prog_course1)
        db.session.add(prog_course2)
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_remove_rule(self) -> None:
        new_clash_context = ClashContext()
        length: int = len(new_clash_context.strategies)
        self.assertGreater(length, 0, "strategies should have atleast one rule")
        new_clash_context.remove_rule("rule0")
        self.assertEqual(
            len(new_clash_context.strategies),
            length - 1,
            "strategies should have one less rule after removing one",
        )

    def test_clash_context(self) -> None:
        new_clash_context = ClashContext()
        exam1: Exam = create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
        exam2: Exam = create_exam("COMP1602", date(2024, 2, 1), time(12, 0), time(14, 0))
        self.assertTrue(
            new_clash_context.detect_clash(exam2),
            "Expected programme level clash for same day, same course",
        )
        new_clash_context.remove_rule("rule2")
        exam1: Exam = create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
        exam2: Exam = create_exam("COMP1602", date(2024, 2, 1), time(12, 0), time(14, 0))
        self.assertFalse(
            new_clash_context.detect_clash(exam2),
            "Expected no clash for same day after removing rule2",
        )
        exam3: Exam = create_exam("COMP1603", date(2024, 2, 1), time(10, 0), time(12, 0))
        self.assertTrue(new_clash_context.detect_clash(exam3), "Expected level clash")
        new_clash_context.remove_rule("rule1")
        exam3: Exam = create_exam("COMP1603", date(2024, 2, 1), time(10, 0), time(12, 0))
        self.assertFalse(
            new_clash_context.detect_clash(exam3),
            "Expected no clash after removing rule1",
        )
        exam1: Exam = create_exam("COMP1602", date(2024, 2, 2), time(9, 0), time(11, 0))
        exam2: Exam = create_exam("COMP1601", date(2024, 2, 2), time(9, 0), time(11, 0))
        self.assertTrue(new_clash_context.detect_clash(exam2), "Expected default clash")

    def test_default_clash(self) -> None:
        default_clash = DefaultClash()
        exam1: Exam = create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
        create_exam("COMP3602", date(2024, 2, 1), time(10, 0), time(12, 0))
        self.assertFalse(
            default_clash.detect_clash(exam1),
            "Expected no clash for different level overlapping exams",
        )
        create_exam("COMP1602", date(2024, 2, 2), time(9, 0), time(11, 0))
        self.assertFalse(
            default_clash.detect_clash(exam1),
            "Expected no clash for exams on different dates",
        )
        create_exam("COMP1602", date(2024, 2, 1), time(10, 0), time(12, 0))
        self.assertTrue(
            default_clash.detect_clash(exam1),
            "Expected clash for same level overlapping exam times",
        )
        create_exam("COMP1602", date(2024, 2, 1), time(9, 0), time(11, 0))
        self.assertTrue(
            default_clash.detect_clash(exam1),
            "Expected clash for exams at exactly the same time",
        )

    def test_level_clash(self) -> None:
        level_clash = LevelClash()
        exam1: Exam = create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
        self.assertFalse(level_clash.detect_clash(exam1), "Expected no clash")
        exam2: Exam = create_exam("COMP1602", date(2024, 2, 1), time(12, 0), time(14, 0))
        self.assertFalse(level_clash.detect_clash(exam2), "Expected no clash")
        exam3: Exam = create_exam("COMP1603", date(2024, 2, 1), time(10, 0), time(12, 0))
        self.assertTrue(level_clash.detect_clash(exam3), "Expected clash")

    def test_program_level_clash(self) -> None:
        program_clash = ProgrammeLevelClash()
        exam1: Exam = create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
        self.assertFalse(
            program_clash.detect_clash(exam1), "Expected no clash for first exam"
        )
        exam2: Exam = create_exam("COMP1602", date(2024, 2, 1), time(14, 0), time(16, 0))
        self.assertTrue(
            program_clash.detect_clash(exam2),
            "Expected clash for same day, same programme and level",
        )
        exam3: Exam = create_exam("COMP1602", date(2024, 2, 2), time(9, 0), time(11, 0))
        self.assertFalse(
            program_clash.detect_clash(exam3), "Expected no clash for different day"
        )
