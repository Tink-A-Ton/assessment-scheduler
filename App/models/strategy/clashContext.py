from .utils import PREDEFINED_RULES
from .clashDetection import ClashDetection
from ..courseAssessment import CourseAssessment


class ClashContext:
    def __init__(self) -> None:
        self.selected_strategies: list[ClashDetection] = []
        self.selected_strategies.append(PREDEFINED_RULES["rule0"]())

    def add_rule(self, rule_name: str) -> None:
        if rule_name in PREDEFINED_RULES:
            strategy_class = PREDEFINED_RULES[rule_name]
            self.selected_strategies.append(strategy_class())
        else:
            raise ValueError(f"Unknown rule: {rule_name}")

    def detect_clash(self, assessment: CourseAssessment) -> bool:
        for strategy in self.selected_strategies:
            if strategy.detect_clash(assessment):
                return True
        return False