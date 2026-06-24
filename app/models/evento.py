from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import GravedadEvento
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.bebedero import Bebedero


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bebedero_id: Mapped[int] = mapped_column(
        ForeignKey("bebederos.id", ondelete="CASCADE"), nullable=False
    )
    tipo_evento: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    gravedad: Mapped[GravedadEvento] = mapped_column(
        SAEnum(GravedadEvento, name="gravedad_evento"), nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    resuelta: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    fecha_resolucion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    bebedero: Mapped[Bebedero] = relationship(back_populates="eventos")
