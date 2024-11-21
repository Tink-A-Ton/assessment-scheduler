from App.database import db


class Programme(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(120), nullable=False)
    courses = db.relationship("CourseProgramme")

    def __init__(self, name) -> None:
        self.name = name

    def to_json(self) -> dict[str, str | int]:
        return {"id": self.id, "name": self.name}
