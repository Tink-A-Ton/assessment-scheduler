import logging,unittest
from App.models.utils import Position
from App.models.users import User, Admin, Staff

LOGGER: logging.Logger = logging.getLogger(__name__)

class UserUnitTests(unittest.TestCase):
    def test_new_user(self) -> None:
        new_user = User(816031000, "user@mail.com", "userpass")
        self.assertIsInstance(new_user, User, "new_user should be an instance of User")
        self.assertEqual(new_user.id, 816031000, "User ID Mismatch")
    
    def test_password_hash(self) -> None:
        new_user: User = User(816031000, "user@mail.com", "userpass")
        self.assertNotEqual(new_user.password, "userpass", "Password should not be stored in plaintext")

    def test_check_password(self)-> None:
        new_user: User = User(816031000, "user@mail.com", "userpass")
        self.assertTrue(new_user.check_password("userpass"),"Password Mismatch")

    def test_user_to_json(self) -> None:
        new_user: User = User(816031000, "user@mail.com", "userpass")
        user_json: dict[str, str | int] = new_user.to_json()
        expected_json: dict[str, str | int] = {"id": 816031000, "email": "user@mail.com"}
        self.assertEqual(user_json, expected_json, "User JSON does not match expected fields or values")

    def test_new_admin(self)->None:
        new_admin: Admin = Admin(816031001, "admin@mail.com", "adminpass")
        self.assertIsInstance(new_admin, Admin, "new_admin should be an instance of Admin")
        self.assertEqual(new_admin.id, 816031001, "Admin ID Mismatch")
        self.assertEqual(new_admin.email, "admin@mail.com", "Admin Email Mismatch")

    def test_new_staff(self) -> None:
        new_staff = Staff(11111111, "jane@mail.com", "password", "Jane", "Doe", "Part-Time Tutor")
        self.assertIsInstance(new_staff, Staff, "new_staff should be an instance of Staff")
        self.assertEqual(new_staff.id, 11111111, "Staff ID Mismatch")
        self.assertEqual(new_staff.email, "jane@mail.com", "Staff Email Mismatch")
        self.assertEqual(new_staff.first_name, "Jane", "Staff First Name Mismatch")
        self.assertEqual(new_staff.last_name, "Doe", "Staff Last Name Mismatch")
        self.assertEqual(new_staff.position, Position.PTTUTOR, "Staff Position Mismatch")

        # this class is fine, no need for isInstance assertion