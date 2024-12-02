from datetime import date, time
import logging
import unittest
import pytest 
from typing import Any, Generator
from flask import Flask 
from flask.testing import FlaskClient 

from ...models.domain.exam import Exam
from ...main import create_app
from ...database import db,create_db
from ...controllers.course import create_course
from ...controllers.clash import detect_exam_clash
from ...controllers.exam import create_exam, delete_exam, get_exam, update_exam, get_exams, get_exam, get_clashes
LOGGER: logging.Logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="module")
def empty_db() -> Generator[FlaskClient, logging.Logger, None]:
    app: Flask = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"}
    )
    create_db()
    yield app.test_client()
    db.drop_all()


class ExamIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test database and Flask application context."""
        self.course_code: str = "COMP1601"
        self.level: int = 1
        self.start_date: date = date(2024, 2, 1)
        self.start_time: time = time(9, 0)
        self.end_time: time = time(11, 0)
        self.clash_detected: bool = False

    def test_create_exam(self) -> None:
        """Test exam creation functionality."""
        exam: Exam = create_exam(
            self.course_code, self.start_date, self.start_time, self.end_time
        )
        self.assertIsNotNone(exam, "Expected an exam to be created")
        self.assertEqual(exam.course_code, self.course_code, "Course code mismatch")
        self.assertEqual(exam.start_date, self.start_date, "Start date mismatch")
        self.assertEqual(exam.start_time, self.start_time, "Start time mismatch")
        self.assertEqual(exam.end_time, self.end_time, "End time mismatch")

    def test_update_exam(self) -> None:
        """Test exam update functionality."""
        exam: Exam = create_exam(
            self.course_code, self.start_date, self.start_time, self.end_time
        )
        updated_exam: Exam | None = update_exam(
            exam.id, date.today().isoformat(), "10:00:00", "12:00:00"
        )
        assert updated_exam is not None, "Expected exam to be updated"
        self.assertEqual(
            updated_exam.start_date, date.today(), "Start date not updated correctly"
        )

    def test_get_exams(self) -> None:
        """Test exam retrieval functionality."""
        exams: list[Exam] = get_exams()
        create_exam("COMP3603", self.start_date, self.start_time, self.end_time)
        create_exam("COMP3602", date(2024, 12, 5), time(13, 0), time(15, 0))
        exams = get_exams()
        self.assertGreaterEqual(len(exams), 2, "Expected 2 exams")

    def test_delete_exam(self) -> None:
        exam: Exam = create_exam(
            self.course_code, self.start_date, self.start_time, self.end_time
        )
        self.assertIsNotNone(exam, "Expected exam to be created")
        exam_id: int = exam.id
        fetched_exam: Exam | None = get_exam(exam_id)
        self.assertIsNotNone(fetched_exam, "Expected exam to exist")
        delete_exam(exam_id)
        fetched_exam = get_exam(exam_id)
        self.assertIsNone(fetched_exam, "Expected exam to be deleted")

    def test_get_clashes(self) -> None:
        create_exam(self.course_code, self.start_date, self.start_time, self.end_time)
        create_course("COMP3602", "Theory of Computation", 1, 2)
        create_course("COMP1601", "Introduction to Computer Programming", 1, 2)
        detect_exam_clash(
            create_exam("COMP3602", self.start_date, self.start_time, self.end_time)
        )
        clashes: list[Exam] = get_clashes()
        self.assertGreaterEqual(len(clashes), 1, "Expected at least 1 clash")
