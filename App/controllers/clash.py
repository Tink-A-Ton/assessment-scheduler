from .exam import Exam
from ..database import db


def detect_exam_clash(
    exam: Exam, rule1: str | None = None, rule2: str | None = None
) -> bool:
    from ..models import ClashContext

    context = ClashContext()
    if rule1 is None:
        context.remove_rule("rule1")
    if rule2 is None:
        context.remove_rule("rule2")
    clash: bool = context.detect_clash(exam)
    db.session.commit()
    return clash
