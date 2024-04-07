import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .palette import Palette


class Color(Base):
    __tablename__ = "colors"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )
    hex_color: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )

    palette_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("palettes.id"))
    palette: Mapped["Palette"] = relationship(back_populates="colors")
