from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.core.enums import RoleName
from app.schemas.usuario import UsuarioPublic


class VeterinarioCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nombre: str
    especialidad: str | None = None
    telefono: str | None = None
    ubicacion: str | None = None
    foto_perfil: str | None = None
    activo: bool = True


class ClienteCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nombre: str
    veterinario_id: int
    razon_social: str
    telefono: str | None = None
    contacto_principal: str | None = None
    activo: bool = True


class InitAdminRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nombre: str


class UsuarioEstadoUpdate(BaseModel):
    activo: bool


class VeterinarioAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario: UsuarioPublic
    veterinario_id: int
    especialidad: str | None = None
    telefono: str | None = None
    ubicacion: str | None = None
    foto_perfil: str | None = None


class ClienteAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario: UsuarioPublic
    cliente_id: int
    veterinario_id: int
    razon_social: str
    telefono: str | None = None
    contacto_principal: str | None = None


class AdminSummary(BaseModel):
    total_usuarios: int
    total_usuarios_activos: int
    total_usuarios_inactivos: int
    total_admins: int
    total_veterinarios: int
    total_clientes: int
    total_establecimientos: int
    total_bebederos: int
    total_bebederos_activos: int
    total_monitoreos: int
    total_imagenes: int
    total_eventos: int
    total_eventos_pendientes: int
