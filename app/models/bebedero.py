from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.establecimiento import Establecimiento
    from app.models.evento import Evento
    from app.models.imagen import Imagen
    from app.models.monitoreo_diario import MonitoreoDiario


class Bebedero(Base):
    __tablename__ = "bebederos"
    __table_args__ = (UniqueConstraint("establecimiento_id", "nombre", name="uq_establecimiento_nombre"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    establecimiento_id: Mapped[int] = mapped_column(
        ForeignKey("establecimientos.id", ondelete="CASCADE"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    ubicacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    puerto: Mapped[int] = mapped_column(Integer, nullable=False, default=8000)
    cobertura_objetivo: Mapped[float] = mapped_column(Float, nullable=False, default=80.0)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ultima_medicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    establecimiento: Mapped[Establecimiento] = relationship(back_populates="bebederos")
    monitoreos: Mapped[list[MonitoreoDiario]] = relationship(back_populates="bebedero")
    imagenes: Mapped[list[Imagen]] = relationship(back_populates="bebedero")
    eventos: Mapped[list[Evento]] = relationship(back_populates="bebedero")
