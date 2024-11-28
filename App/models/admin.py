from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.properties import MappedColumn
from .user import User


class Admin(User):
    id: MappedColumn[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    def __init__(self, id, email, password) -> None:
        super().__init__(id, email, password)
