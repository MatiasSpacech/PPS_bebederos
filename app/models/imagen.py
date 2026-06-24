from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.bebedero import Bebedero
    from app.models.monitoreo_diario import MonitoreoDiario


class Imagen(Base):
    __tablename__ = "imagenes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    monitoreo_id: Mapped[int] = mapped_column(
        ForeignKey("monitoreo_diario.id", ondelete="CASCADE"), nullable=False
    )
    bebedero_id: Mapped[int] = mapped_column(
        ForeignKey("bebederos.id", ondelete="CASCADE"), nullable=False
    )
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    ruta_filesystem: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_captura: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    tamano_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)

    monitoreo: Mapped[MonitoreoDiario] = relationship(back_populates="imagenes")
    bebedero: Mapped[Bebedero] = relationship(back_populates="imagenes")
