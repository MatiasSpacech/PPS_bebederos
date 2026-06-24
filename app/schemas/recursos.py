from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.usuario import UsuarioPublic


class BebederoResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    ubicacion: str | None = None
    estado: bool
    ultima_medicion: datetime | None = None


class EstablecimientoResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    ubicacion: str | None = None
    fecha_creacion: datetime
    bebederos: list[BebederoResumen] = []


class EstablecimientoDetalle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    cliente_razon_social: str
    nombre: str
    ubicacion: str | None = None
    fecha_creacion: datetime
    bebederos: list[BebederoResumen] = []


class ClienteResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    razon_social: str
    telefono: str | None = None
    contacto_principal: str | None = None
    usuario: UsuarioPublic
    establecimientos: list[EstablecimientoResumen] = []


class VeterinarioDetalle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    nombre: str
    especialidad: str | None = None
    telefono: str | None = None
    ubicacion: str | None = None
    foto_perfil: str | None = None
    fecha_creacion: datetime
    clientes: list[ClienteResumen] = []
