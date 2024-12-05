from datetime import date, timedelta
from typing import Optional
from .exam import Exam
from ..database import db


def detect_exam_clash(
    exam: Exam, rule1: Optional[str] = None, rule2: Optional[str] = None
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


def recheck_nearby_clashes(start_date: Optional[date]) -> None:
    if start_date is None:
        return
    range_start: date = start_date - timedelta(weeks=1)
    range_end: date = start_date + timedelta(weeks=2)
    nearby_exams: list[Exam] = Exam.query.filter(
        Exam.start_date.between(range_start, range_end)
    ).all()
    from ..models import ClashContext

    clash_context = ClashContext()
    for exam in nearby_exams:
        clash_context.detect_clash(exam)
    db.session.commit()
