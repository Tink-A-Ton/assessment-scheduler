import logging,unittest
from App.models.domain.programme import Programme

LOGGER: logging.Logger = logging.getLogger(__name__)

class ProgrammeUnitTests(unittest.TestCase):
    def test_new_programme(self) -> None:
        new_programme = Programme("Computer Science")
        self.assertEqual(new_programme.name, "Computer Science", "Programme Name Mismatch")

    def test_programme_to_json(self) -> None:
        new_programme: Programme = Programme("Computer Science")
        programme_json: dict[str, str | int] = new_programme.to_json()
        del programme_json['id']
        expected_json: dict[str, str | int] = {
            "name": "Computer Science"
        }
        self.assertEqual(programme_json, expected_json, "Programme JSON does not match expected fields or values")
