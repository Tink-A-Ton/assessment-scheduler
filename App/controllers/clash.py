from .exam import Exam
from ..models import ClashContext


def detect_exam_clash(exam: Exam, rule1, rule2) -> bool:
    context = ClashContext()
    if rule1:
        context.add_rule("rule1")
    if rule2:
        context.add_rule("rule2")
    return context.detect_clash(exam)
