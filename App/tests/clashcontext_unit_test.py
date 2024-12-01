import logging
import unittest
from App.models.strategy.defaultClash import DefaultClash
from App.models.strategy.levelClash import LevelClash
from App.models.strategy.clashContext import ClashContext

LOGGER: logging.Logger = logging.getLogger(__name__)

class ClashContextUnitTests(unittest.TestCase):
    def test_new_clash_context(self) -> None:
        new_clash_context = ClashContext()
        self.assertIsInstance(new_clash_context, ClashContext, "new_clash_context should be an instance of ClashContext")
        self.assertEqual(len(new_clash_context.selected_strategies), 1, "selected_strategies should have rule0 as a default first element")
        self.assertIsInstance(new_clash_context.selected_strategies[0], DefaultClash, "first element should be an instance of DefaultClash")

    def test_add_rule(self) -> None:
        new_clash_context = ClashContext()
        new_clash_context.add_rule("rule1")
        self.assertIsInstance(new_clash_context.selected_strategies[1], LevelClash, "selected_strategies should have rule1 as the second element")

    def test_detect_clash(self) -> None:
        new_clash_context = ClashContext()
        