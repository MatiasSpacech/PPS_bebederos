from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.establecimiento import Establecimiento
    from app.models.usuario import Usuario
    from app.models.veterinario import Veterinario


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    veterinario_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarios.id", ondelete="RESTRICT"), nullable=False
    )
    razon_social: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contacto_principal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    usuario: Mapped[Usuario] = relationship(back_populates="cliente")
    veterinario: Mapped[Veterinario] = relationship(back_populates="clientes")
    establecimientos: Mapped[list[Establecimiento]] = relationship(
        back_populates="cliente"
    )
