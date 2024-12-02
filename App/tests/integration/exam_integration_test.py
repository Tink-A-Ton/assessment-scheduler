from datetime import date, time
import os
import logging
import unittest
from typing import Any

from ...models.domain.exam import Exam
from ...main import create_app
from ...database import db
from ...controllers.exam import create_exam, delete_exam, get_exam, update_exam, get_exams, get_exam, get_clashes
LOGGER: logging.Logger = logging.getLogger(__name__)

class ExamIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test database and Flask application context."""
        self.app: Any = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client: Any = self.app.test_client()
        self.app_context: Any = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.course_code: str = "COMP1601"
        self.start_date: date = date(2024, 2, 1)
        self.start_time: time = time(9, 0)
        self.end_time: time = time(11, 0)
        self.clash_detected: bool = False

    def tearDown(self) -> None:
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_exam(self) -> None:
        """Test exam creation functionality."""
        exam: Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time)
        self.assertIsNotNone(exam, "Expected an exam to be created")
        self.assertEqual(exam.course_code, self.course_code, "Course code mismatch")
        self.assertEqual(exam.start_date, self.start_date, "Start date mismatch")
        self.assertEqual(exam.start_time, self.start_time, "Start time mismatch")
        self.assertEqual(exam.end_time, self.end_time, "End time mismatch")

    
    # def test_update_exam(self) -> None:
    #     """Test exam update functionality."""
    #     exam: Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time)
    #     updated_exam: Exam | None = update_exam(exam.id, date.today(), self.start_time, self.end_time)
    #     assert updated_exam is not None, "Expected exam to be updated"
    #     self.assertEqual(updated_exam.start_date, date.today(), "Start date not updated correctly")
    # TODO fix

    def test_get_exams(self) -> None:
        """Test exam retrieval functionality."""
        exams: list[Exam] = get_exams()
        self.assertEqual(len(exams), 0)
        create_exam(self.course_code, self.start_date, self.start_time, self.end_time)
        create_exam("COMP3602", date(2024,12,5), time(13,0), time(15,0))
        exams = get_exams()
        self.assertEqual(len(exams), 2, "Expected 2 exams")

    def test_delete_exam(self) -> None:
        create_exam(self.course_code, self.start_date, self.start_time, self.end_time)
        exam: Exam | None = get_exam(1)
        self.assertIsNotNone(exam, "Expected exam to exist")
        delete_exam(1)
        exam = get_exam(1)
        self.assertIsNone(exam, "Expected exam to be deleted")

    # def test_get_clashes(self) -> None:
    #     """Test clash retrieval functionality."""
    #     create_exam(self.course_code, self.start_date, self.start_time, self.end_time)
    #     create_exam("COMP3602", self.start_date, self.start_time, self.end_time)
    #     clashes: list[Exam] = get_clashes()
    #     self.assertEqual(len(clashes), 1, "Expected at least 1 clash")
    # TODO fix