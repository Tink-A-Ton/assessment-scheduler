from datetime import date, time
import logging,unittest
from ...models.strategy import DefaultClash
from ...controllers.exam import create_exam
from ...models.domain.exam import Exam
LOGGER: logging.Logger = logging.getLogger(__name__)

class DefaultClashIntegrationTests(unittest.TestCase):
    # def test_detect_clash(self) -> None:
    #     default_clash = DefaultClash()
    #     exam: Exam = create_exam("COMP1601", date(2024, 2, 1), time(9, 0), time(11, 0))
    #     create_exam("COMP1602", date(2024, 2, 1), time(11, 0), time(13, 0))
    #     self.assertTrue(default_clash.detect_clash(exam))
    # TODO implement