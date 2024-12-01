from datetime import date, time
from flask import Flask
from flask.testing import FlaskClient
import logging, unittest
from typing import Generator
import pytest
from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Staff, Instructor, Course, Exam
from App.controllers import (
    get_user,
    get_user_by_email,
    create_staff,
    update_password,
    create_admin,
    get_staff,
    login_user,
    is_admin,
    is_admin_account,
    add_instructor,
    get_instructors,
    get_registered_courses,
    get_search_results,
    allow_override,
    deny_override,
    create_exam,
    get_staff_exams,
    get_exam,
    get_staff_courses,
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

class UserIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.staff_id: int = 81603567
        self.admin_id: int = 99999999
        self.password: str = "password123"
        self.admin_password: str = "adminpass"
        self.email: str = "test@mail.com"
        self.admin_email: str = "admin@mail.com"

    def test_get_user(self) -> None:
        user: User | None = get_user(self.staff_id)
        self.assertIsNone(user, "Expected no user for the staff ID")

    def test_get_user_by_email(self) -> None:
        user: User | None = get_user_by_email(self.email)
        self.assertIsNone(user, "Expected no user for the email")

    def test_update_password(self) -> None:
        create_staff(self.staff_id, self.email, self.password, "John", "Doe", "Lecturer")
        update_password(self.staff_id, "newpassword")
        staff: Staff | None = get_staff(self.staff_id)
        assert staff is not None
        self.assertTrue(staff.check_password("newpassword"))

    def test_create_staff(self) -> None:
        created: bool = create_staff(
            self.staff_id,
            self.email,
            self.password,
            "John",
            "Doe",
            "Lecturer"
        )
        self.assertTrue(created, "Staff creation should succeed")
        staff: Staff | None = get_staff(self.staff_id)
        self.assertIsNotNone(staff, "Expected to retrieve a Staff object")
        self.assertEqual(staff.id, self.staff_id, "Staff ID mismatch")
        self.assertEqual(staff.email, self.email, "Staff email mismatch")
        self.assertEqual(staff.first_name, "John", "Staff first name mismatch")
        self.assertEqual(staff.last_name, "Doe", "Staff last name mismatch")

    def test_create_admin(self) -> None:
        admin: Admin | None = create_admin(self.admin_id, self.admin_email, self.admin_password)
        self.assertIsNotNone(admin, "Expected to create an Admin object")
        self.assertTrue(
            is_admin(self.admin_id),
            "Expected admin status to be True for created admin"
        )
        self.assertTrue(
            is_admin_account(self.admin_email),
            "Expected email to be recognized as admin account"
        )

    def test_staff_login(self) -> None:
        created: bool = create_staff(
            self.staff_id,
            self.email,
            self.password,
            "John",
            "Doe",
            "Lecturer"
        )
        self.assertTrue(created, "Staff creation failed")
        staff_token: str | None = login_user(self.email, self.password)
        self.assertIsNotNone(
            staff_token,
            "Expected a token to be returned upon successful staff login"
        )

    def test_admin_login(self) -> None:
        admin: Admin = create_admin(self.admin_id, self.admin_email, self.admin_password)
        self.assertIsNotNone(admin, "Admin creation failed")
        admin_token: str | None = login_user(self.admin_email, self.admin_password)
        self.assertIsNotNone(
            admin_token,
            "Expected a token to be returned upon successful admin login"
        )

    def test_invalid_login(self) -> None:
        token: str | None = login_user("invalid@mail.com", "wrongpass")
        self.assertIsNone(token, "Expected None for invalid login credentials")
    
    def test_is_admin(self) -> None:
        create_admin(self.admin_id, self.admin_email, self.admin_password)
        admin: bool = is_admin(self.admin_id)
        self.assertTrue(admin, "Expected to retrieve an Admin object")

    def test_is_admin_account(self) -> None:
        create_admin(self.admin_id, self.admin_email, self.admin_password)
        admin: bool = is_admin_account(self.admin_email)
        self.assertTrue(admin, "Expected to retrieve an Admin object")

    def test_add_instructor(self) -> None:
        create_staff(self.staff_id, self.email, self.password, "John", "Doe", "Lecturer")
        add_instructor(self.staff_id, "COMP1511")
        instructor: Instructor | None = get_instructors(self.staff_id)[0]
        assert instructor is not None
        self.assertEqual(instructor.staff_id, self.staff_id, "Instructor staff ID mismatch")
        self.assertEqual(instructor.course_code, "COMP1511", "Instructor course code mismatch")

    def test_get_instructors(self) -> None:
        create_staff(self.staff_id, self.email, self.password, "John", "Doe", "Lecturer")
        instructors: list[Instructor] = get_instructors(self.staff_id)
        self.assertEqual(len(instructors), 0, "Expected no instructors for the staff")

    def test_get_registered_courses(self) -> None:
        create_staff(self.staff_id, self.email, self.password, "John", "Doe", "Lecturer")
        courses: list[Course] = get_registered_courses(self.staff_id)
        self.assertEqual(len(courses), 0, "Expected no courses for the staff")

    def test_get_search_results(self) -> None:
        results: list[Exam] = get_search_results("2024-11-30")
        self.assertEqual(len(results), 0, "Expected no exams for the search results")

    def test_allow_override(self) -> None:
        create_exam("COMP1511", date.today(), time(10, 0), time(12, 0), False)
        allow_override(1)
        exam: Exam | None = get_exam(1)
        assert exam is not None
        self.assertFalse(exam.clash_detected, "Expected clash detection to be False")
        self.assertIsNotNone(exam.start_date, "Expected start date to be not None")
        self.assertIsNotNone(exam.start_time, "Expected start time to be not None")
        self.assertIsNotNone(exam.end_time, "Expected end time to be not None")

    def test_deny_override(self) -> None:
        create_exam("COMP1511", date.today(), time(10, 0), time(12, 0), False)
        deny_override(1)
        exam: Exam | None = get_exam(1)
        assert exam is not None
        self.assertFalse(exam.clash_detected, "Expected clash detection to be False")
        self.assertIsNone(exam.start_date, "Expected start date to be None")
        self.assertIsNone(exam.start_time, "Expected start time to be None")
        self.assertIsNone(exam.end_time, "Expected end time to be None")

    def test_get_staff_exams(self) -> None:
        exams: list[dict] = get_staff_exams(self.staff_id)
        self.assertEqual(len(exams), 0, "Expected no exams for the staff")

    def test_get_staff_courses(self) -> None:
        courses: list[dict] = get_staff_courses(self.staff_id)
        self.assertEqual(len(courses), 0, "Expected no courses for the staff")
