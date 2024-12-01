from .ruleSet import PREDEFINED_RULES
from .clashDetection import ClashDetection
from ..domain.exam import Exam


class ClashContext:
    def __init__(self) -> None:
        self.strategies: dict[str, ClashDetection] = {
            rule_name: rule() for rule_name, rule in PREDEFINED_RULES.items()
        }

    def remove_rule(self, rule_name: str) -> None:
        if rule_name in self.strategies:
            del self.strategies[rule_name]
        else:
            raise ValueError(f"Rule '{rule_name}' does not exist or is not enabled.")

    def detect_clash(self, exam: Exam) -> bool:
        exam.clash_detected = any(s.detect_clash(exam) for s in self.strategies.values())
        return exam.clash_detected
