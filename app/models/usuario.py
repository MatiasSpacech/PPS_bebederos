from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import RoleName
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.veterinario import Veterinario


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RoleName] = mapped_column(
        SAEnum(RoleName, name="rol_usuario"), nullable=False, index=True
    )
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    fecha_ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    veterinario: Mapped[Veterinario | None] = relationship(back_populates="usuario", uselist=False)
    cliente: Mapped[Cliente | None] = relationship(back_populates="usuario", uselist=False)
