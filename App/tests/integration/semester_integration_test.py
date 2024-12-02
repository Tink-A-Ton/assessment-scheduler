import logging
from typing import Any
import unittest
from App.main import create_app
from App.database import db
from App.controllers.semester import create_semester
from App.models.domain.semester import Semester

LOGGER: logging.Logger = logging.getLogger(__name__)

class SemesterIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test database and Flask application context."""
        self.app: Any = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client: Any = self.app.test_client()
        self.app_context: Any = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.start_date: str = "2024-01-01"
        self.end_date: str = "2024-06-30"
        self.semester_number: int = 1
        self.max_exams: int = 10

    def tearDown(self) -> None:
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_semester(self)-> None:
        create_semester(self.start_date, self.end_date, self.semester_number, self.max_exams)
        semester: Semester = Semester.query.get(1)
        self.assertIsNotNone(semester)
        self.assertEqual(semester.start_date, self.start_date)
        self.assertEqual(semester.end_date, self.end_date)
        self.assertEqual(semester.semester_number, self.semester_number)
        self.assertEqual(semester.max_exams, self.max_exams)
