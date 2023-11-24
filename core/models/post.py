from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    _user_back_populate = "posts"
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default=""
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, body={self.body!r}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)
