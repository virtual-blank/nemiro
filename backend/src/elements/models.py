import enum
import uuid

from database.db import Base
from database.mixins import TimeStampMixin, Uuid7PkMixin
from sqlalchemy import ForeignKey, Integer, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class ElementTypeEnum(str, enum.Enum):
    SHAPE = "SHAPE"
    TEXT = "TEXT"
    ARROW = "ARROW"
    IMAGE = "IMAGE"


class Element(Uuid7PkMixin, TimeStampMixin, Base):
    __tablename__ = "elements"

    board_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("boards.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(25))
    type: Mapped[ElementTypeEnum]
    x: Mapped[float]
    y: Mapped[float]
    z_index: Mapped[int]  # Слой наложения, определяет какой элемент выше
    width: Mapped[float]
    height: Mapped[float]
    rotation: Mapped[float]

    payload: Mapped[dict] = mapped_column(JSONB)
    version: Mapped[int] = mapped_column(Integer, default=1)
