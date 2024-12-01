import logging,unittest
from App.models.strategy import ClashContext

LOGGER: logging.Logger = logging.getLogger(__name__)

class ClashContextUnitTests(unittest.TestCase):
    def test_new_clash_context(self) -> None:
        new_clash_context = ClashContext()  
        self.assertIsInstance(new_clash_context, ClashContext, "new_clash_context should be an instance of ClashContext")
        length = len(new_clash_context.strategies)
        self.assertGreater(length, 0, "strategies should have at least one rule")

    def test_remove_rule(self) -> None:
        new_clash_context = ClashContext()
        length: int = len(new_clash_context.strategies)
        self.assertGreater(length, 0, "strategies should have atleast one rule")
        new_clash_context.remove_rule("rule0")
        self.assertEqual(len(new_clash_context.strategies), length - 1, "strategies should have one less rule after removing one")
