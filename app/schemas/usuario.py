from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.enums import RoleName


class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str
    rol: RoleName
    activo: bool = True


class UsuarioPublic(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UsuarioMe(UsuarioPublic):
    fecha_creacion: datetime | None = None
    fecha_ultimo_acceso: datetime | None = None
