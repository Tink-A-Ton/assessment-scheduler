from App.database import db
import enum


class Category(enum.Enum):
    EXAM = "Exam"
    ASSIGNMENT = "Assignment"
    QUIZ = "Quiz"
    PROJECT = "Project"
    DEBATE = "Debate"
    PRESENTATION = "Presentation"
    ORALEXAM = "Oral Exam"
    PARTICIPATION = "Participation"


class AssessmentType(db.Model):
    id: int = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    category = db.Column(db.Enum(Category), nullable=False)

    def __init__(self, category) -> None:
        self.category = Category(category)

    def to_json(self) -> dict[str, int | Category]:
        return {"id": self.id, "category": self.category.name}
