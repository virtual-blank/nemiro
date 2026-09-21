import enum
import uuid
from typing import TYPE_CHECKING

from database.db import Base
from database.mixins import TimeStampMixin, Uuid7PkMixin
from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.users.models import User


class MemberRoleEnum(str, enum.Enum):
    VIEWER = "VIEWER"
    EDITOR = "EDITOR"
    ADMIN = "ADMIN"


class Board(Uuid7PkMixin, TimeStampMixin, Base):
    __tablename__ = "boards"

    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    is_public: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship("User", back_populates="boards", passive_deletes=True, lazy="raise_on_sql")


class BoardMember(Uuid7PkMixin, TimeStampMixin, Base):
    __tablename__ = "board_members"

    board_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("boards.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[MemberRoleEnum]
