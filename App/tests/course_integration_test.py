from flask import Flask
from flask.testing import FlaskClient
import logging, unittest
from typing import Generator
import pytest
from App.main import create_app
from App.database import db, create_db
from App.models import Course
from App.controllers import (
    create_course,
    get_course,
    get_courses,
    get_courses_by_level,
    delete_course,
    edit_course,
)

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

class CourseIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.course_code: str = "COMP1601"
        self.semester_id: int = 1
        self.course_title: str = "Introduction to Programming"
        self.level: int = 1


    def test_create_course(self) -> None:
        created: bool = create_course(self.course_code, self.course_title, self.level, self.semester_id)
        self.assertTrue(created, "Course creation should succeed")
        course: Course | None = get_course(self.course_code)
        assert course is not None
        self.assertEqual(course.course_code, self.course_code, "Course code mismatch")
        self.assertEqual(course.course_title, self.course_title, "Course title mismatch")
        self.assertEqual(course.level, self.level, "Course level mismatch")
        self.assertEqual(course.semester_id, self.semester_id, "Course semester ID mismatch")

    def test_get_courses(self) -> None:
        create_course(self.course_code, self.course_title, self.level, self.semester_id)
        create_course("COMP2611", "Data Structures and Algorithms", 1, 1)
        courses: list[Course] = get_courses()
        self.assertGreater(len(courses), 0, "Expected atleast one course in total")
        course: Course = courses[-1]
        assert course is not None
        self.assertEqual(course.course_code, "COMP2611", "Course code mismatch")
        self.assertEqual(course.course_title, "Data Structures and Algorithms", "Course title mismatch")
        self.assertEqual(course.level, 1, "Course level mismatch")
        self.assertEqual(course.semester_id, 1, "Course semester ID mismatch")

    def test_edit_course(self) -> None:
        create_course(self.course_code, self.course_title, self.level, self.semester_id)
        updated: Course | None = edit_course(self.course_code,2, "Data Structures and Algorithms", 2)
        assert updated is not None
        self.assertEqual(updated.course_code, self.course_code, "Course code mismatch")
        self.assertEqual(updated.course_title, "Data Structures and Algorithms", "Course title mismatch")
        self.assertEqual(updated.level, 2, "Course level mismatch")
        self.assertEqual(updated.semester_id, 2, "Course semester ID mismatch")

    def test_get_courses_by_level(self) -> None:
        create_course(self.course_code, self.course_title, self.level, self.semester_id)
        create_course("COMP2611", "Data Structures and Algorithms", 2, 1)
        create_course("COMP2603", "Object-Oriented Programming I", 2, 2)
        create_course("COMP2601", "Computer Architecture", 2, 1)
        courses: list[Course] | None = get_courses_by_level(2)
        assert courses is not None
        self.assertGreater(len(courses), 0, "Expected atleast one course in total")
        course: Course = courses[-1]
        self.assertEqual(course.course_code, "COMP2601", "Course code mismatch")
        self.assertEqual(course.course_title, "Computer Architecture", "Course title mismatch")

    def test_delete_course(self) -> None:
        create_course(self.course_code, self.course_title, self.level, self.semester_id)
        deleted: bool = delete_course(self.course_code)
        self.assertTrue(deleted, "Course deletion should succeed")
        course: Course | None = get_course(self.course_code)
        self.assertIsNone(course, "Course should not exist after deletion")

    