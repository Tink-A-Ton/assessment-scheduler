from datetime import date, time
from flask import Flask
from flask.testing import FlaskClient
import logging, unittest
from typing import Generator
import pytest
from App.main import create_app
from App.database import db, create_db
from App.controllers import (
    create_exam,
    get_exams_by_course,
    delete_exam,
    get_clashes,
    get_exams,
    get_exam,
)
from App.models import Exam, Course

LOGGER: logging.Logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="function")
def empty_db() -> Generator[FlaskClient, None, None]:
    app: Flask = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
            "JWT_SECRET_KEY": "test-key",
            "SECRET_KEY": "test-key",
        }
    )
    create_db()
    yield app.test_client()
    db.drop_all()

class ExamIntegrationTests(unittest.TestCase):
    def setUp(self) -> None: 
        self.exam_id: int = 1
        self.course_code: str = "COMP1601"
        self.start_date: date = date.today()
        self.start_time: time = time(10, 0)
        self.end_time: time = time(12, 0)
        self.clash: bool = False

    def test_create_exam(self) -> None:
        exam: Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time, self.clash)
        self.assertIsNotNone(exam, "Exam should not be None")
        self.assertEqual(exam.id, self.exam_id, "Exam ID mismatch")
        self.assertEqual(exam.course_code, self.course_code, "Course Code mismatch")
        self.assertEqual(exam.start_date, self.start_date, "Start Date mismatch")
        self.assertEqual(exam.start_time, self.start_time, "Start Time mismatch")
        self.assertEqual(exam.end_time, self.end_time, "End Time mismatch")
        self.assertEqual(exam.clash_detected, self.clash, "Clash Detected mismatch")


    def test_get_exams_by_course(self) -> None:
        exam: Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time, self.clash)
        exams_by_course: list[Exam] = get_exams_by_course(exam.course_code)
        self.assertEqual(len(exams_by_course), 1, "Number of exams by course mismatch")
        self.assertEqual(exams_by_course[0].id, exam.id, "Exam ID mismatch")
    
    def test_delete_exam(self) -> None:
        exam : Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time, self.clash)
        deleted: bool = delete_exam(exam.id)
        self.assertTrue(deleted, "Exam deletion should succeed")

    def test_get_clashes(self) -> None:
        exam: Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time, True)
        db.session.commit()
        clashes: list[Exam] = get_clashes()
        self.assertEqual(len(clashes), 1, "Number of clashes mismatch")
        self.assertEqual(clashes[0].id, exam.id, "Clash ID mismatch")

    def test_get_exams(self) -> None:
        exam: Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time, self.clash)
        exams: list[Exam] = get_exams()
        assert exams is not None
        self.assertEqual(len(exams), 1, "Number of exams mismatch")
        self.assertEqual(exams[0].id, exam.id, "Exam ID mismatch")

    def test_get_exam(self) -> None:
        exam: Exam = create_exam(self.course_code, self.start_date, self.start_time, self.end_time, self.clash)
        exam_by_id: Exam | None = get_exam(exam.id)
        assert exam_by_id is not None
        self.assertEqual(exam_by_id.id, exam.id, "Exam ID mismatch")

