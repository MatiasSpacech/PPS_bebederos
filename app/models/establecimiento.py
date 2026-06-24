from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.bebedero import Bebedero
    from app.models.cliente import Cliente


class Establecimiento(Base):
    __tablename__ = "establecimientos"
    __table_args__ = (UniqueConstraint("cliente_id", "nombre", name="uq_cliente_nombre"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    ubicacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    cliente: Mapped[Cliente] = relationship(back_populates="establecimientos")
    bebederos: Mapped[list[Bebedero]] = relationship(back_populates="establecimiento")
