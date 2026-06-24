from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.bebedero import Bebedero
    from app.models.imagen import Imagen


class MonitoreoDiario(Base):
    __tablename__ = "monitoreo_diario"
    __table_args__ = (UniqueConstraint("bebedero_id", "fecha", name="uq_bebedero_fecha"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bebedero_id: Mapped[int] = mapped_column(
        ForeignKey("bebederos.id", ondelete="CASCADE"), nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    nivel_agua_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    distancia_sensor_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    cobertura_capsulas_porciento: Mapped[float | None] = mapped_column(Float, nullable=True)
    sensor_ultrasound: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    camera_activa: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    analyzer_activo: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    config_ok: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    bebedero: Mapped[Bebedero] = relationship(back_populates="monitoreos")
    imagenes: Mapped[list[Imagen]] = relationship(back_populates="monitoreo")
