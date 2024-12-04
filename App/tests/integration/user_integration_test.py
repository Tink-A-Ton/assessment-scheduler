from datetime import date, time
import logging
from typing import Generator, Optional
import unittest

from flask import Flask
from flask.testing import FlaskClient
import pytest
from ...controllers import add_instructor, get_staff_exams, create_course
from ...controllers import create_admin, login_user, create_staff, create_exam
from ...models.users.instructor import Instructor
from ...models.users.staff import Staff
from ...models.utils import Position
from ...models import Admin
from ...main import create_app
from ...database import create_db, db

LOGGER: logging.Logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="module")
def empty_db() -> Generator[FlaskClient, logging.Logger, None]:
    app: Flask = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"}
    )
    create_db()
    yield app.test_client()
    db.drop_all()


class UserIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test database and Flask application context."""
        self.staff_id = 81603567
        self.admin_id = 99999999
        self.password = "password123"
        self.admin_password = "adminpass"
        self.email = "test@mail.com"
        self.admin_email = "admin@mail.com"

    def test_login(self) -> None:
        """Test user login functionality."""
        create_staff(
            self.staff_id,
            self.email,
            self.password,
            "John",
            "Doe",
            Position.LECTURER.value,
        )
        token: Optional[str] = login_user(self.email, self.password)
        self.assertIsNotNone(
            token, "Expected a token to be returned upon successful login"
        )

    def test_create_admin(self) -> None:
        """Test admin creation functionality."""
        create_admin(self.admin_id, self.admin_email, self.admin_password)
        admin: Admin = Admin.query.get(self.admin_id)
        self.assertIsNotNone(admin)
        self.assertEqual(admin.email, self.admin_email)

    def test_create_staff(self) -> None:
        """Test staff creation functionality."""
        create_staff(
            self.staff_id,
            self.email,
            self.password,
            "John",
            "Doe",
            Position.LECTURER.value,
        )
        staff: Staff = Staff.query.get(self.staff_id)
        self.assertIsNotNone(staff)
        self.assertEqual(staff.email, self.email)

    def test_get_staff_exams(self) -> None:
        """Test staff exams retrieval functionality."""
        create_staff(
            self.staff_id,
            self.email,
            self.password,
            "John",
            "Doe",
            Position.LECTURER.value,
        )
        create_course("COMP1601", "Introduction to Computer Programming I", 1, 1)
        create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
        add_instructor(self.staff_id, "COMP1601")
        exams: list[dict] = get_staff_exams(self.staff_id)
        self.assertEqual(len(exams), 1)

    def test_add_instructor(self) -> None:
        """Test instructor addition functionality."""
        create_staff(
            self.staff_id,
            self.email,
            self.password,
            "John",
            "Doe",
            Position.LECTURER.value,
        )
        create_course("COMP1601", "Introduction to Computer Programming I", 1, 1)
        add_instructor(self.staff_id, "COMP1601")
        instructor: Instructor = Instructor.query.filter_by(
            staff_id=self.staff_id, course_code="COMP1601"
        ).first()
        self.assertIsNotNone(instructor, "Instructor should be added to the course")
