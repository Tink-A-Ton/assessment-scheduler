import logging
from typing import Any, Generator
import unittest
from flask import Flask
from flask.testing import FlaskClient
import pytest
from ...main import create_app
from ...database import create_db, db
from ...controllers.semester import create_semester
from ...models.domain.semester import Semester

LOGGER: logging.Logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="module")
def empty_db() -> Generator[FlaskClient, logging.Logger, None]:
    app: Flask = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"}
    )
    create_db()
    yield app.test_client()
    db.drop_all()


class SemesterIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test database and Flask application context."""
        self.start_date: str = "2024-01-01"
        self.end_date: str = "2024-06-30"
        self.semester_number: int = 1
        self.max_exams: int = 10

    def test_create_semester(self) -> None:
        create_semester(
            self.start_date, self.end_date, self.semester_number, self.max_exams
        )
        semester: Semester = Semester.query.get(1)
        self.assertIsNotNone(semester)
        self.assertEqual(semester.start_date, self.start_date)
        self.assertEqual(semester.end_date, self.end_date)
        self.assertEqual(semester.semester_number, self.semester_number)
        self.assertEqual(semester.max_exams, self.max_exams)
