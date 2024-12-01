import unittest, logging
from App.models.strategy.defaultClash import DefaultClash

LOGGER: logging.Logger = logging.getLogger(__name__)

class DefaultClashUnitTests(unittest.TestCase):
    def test_detect_clash(self) -> None:
        default_clash = DefaultClash()
        self.assertIsInstance(default_clash, DefaultClash, "default_clash should be an instance of DefaultClash")
        # continue