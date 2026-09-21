from typing import TYPE_CHECKING

from database.db import Base
from database.mixins import TimeStampMixin, Uuid7PkMixin
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.boards.models import Board


class User(Uuid7PkMixin, TimeStampMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(16), unique=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    boards: Mapped[list["Board"]] = relationship(back_populates="user", lazy="raise_on_sql")
