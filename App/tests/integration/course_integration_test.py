import logging
from typing import Generator, Optional
import unittest

from flask import Flask
from flask.testing import FlaskClient
import pytest
from ...main import create_app
from ...database import create_db, db
from ...controllers.course import create_course, delete_course, edit_course, get_courses
from ...models.domain.course import Course

LOGGER: logging.Logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="module")
def empty_db() -> Generator[FlaskClient, logging.Logger, None]:
    app: Flask = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"}
    )
    create_db()
    yield app.test_client()
    db.drop_all()


class CourseIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test database and Flask application context."""
        self.course_code: str = "COMP1601"
        self.course_title: str = "Introduction to Computer Programming I"
        self.level: int = 1
        self.semester_id: int = 1
        create_course(self.course_code, self.course_title, self.level, self.semester_id)

    def test_create_course(self) -> None:
        """Test course creation functionality."""
        create_course("COMP1602", "Intro to computer programming II", 1, 2)
        course: Course = Course.query.get("COMP1602")
        self.assertIsNotNone(course)
        self.assertEqual(course.course_code, "COMP1602", "Course code mismatch")
        self.assertEqual(
            course.course_title,
            "Intro to computer programming II",
            "Course title mismatch",
        )
        self.assertEqual(course.level, 1, "Course level mismatch")
        self.assertEqual(course.semester_id, 2, "Course semester mismatch")

    def test_get_courses(self) -> None:
        """Test course retrieval functionality."""
        create_course("COMP1602", "Intro to computer programming II", 1, 2)
        courses: list[Course] = get_courses()
        self.assertTrue(len(courses) >= 1, "Expected one course to be present")
        create_course("COMP1602", "Introduction to Computer Programming II", 1, 2)
        courses: list[Course] = get_courses()
        self.assertTrue(len(courses) >= 1, "Expected two courses to be present")

    def test_edit_course(self) -> None:
        """Test course editing functionality."""
        course: Course = Course.query.get(self.course_code)
        self.assertIsNotNone(course)
        self.assertEqual(course.course_title, self.course_title)
        edit_course(self.course_code, "Intro to Computer Programming", self.level)
        course: Course = Course.query.get(self.course_code)
        self.assertIsNotNone(course)
        self.assertEqual(course.course_title, "Intro to Computer Programming")

    def test_delete_course(self) -> None:
        """Test course deletion functionality."""
        course: Optional[Course] = Course.query.get(self.course_code)
        self.assertIsNotNone(course, "Course COMP1601 should exist")
        self.assertTrue(
            delete_course(self.course_code), "Course COMP1601 should be deleted"
        )
        self.assertIsNone(
            Course.query.get(self.course_code),
            "Course COMP1601 should not exist after deletion",
        )
