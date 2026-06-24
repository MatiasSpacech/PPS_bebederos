from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import RoleName
from app.schemas.usuario import UsuarioPublic


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nombre: str
    rol: RoleName = RoleName.cliente


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    user_id: int
    email: EmailStr
    role: RoleName
    nombre: str | None = None


class MeResponse(UsuarioPublic):
    model_config = ConfigDict(from_attributes=True)
