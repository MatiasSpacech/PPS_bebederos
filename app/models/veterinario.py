from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.usuario import Usuario


class Veterinario(Base):
    __tablename__ = "veterinarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    especialidad: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ubicacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    foto_perfil: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    usuario: Mapped[Usuario] = relationship(back_populates="veterinario")
    clientes: Mapped[list[Cliente]] = relationship(back_populates="veterinario")
