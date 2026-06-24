from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.crud.usuarios import get_by_id
from app.db.session import get_db
from app.models.usuario import Usuario

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


class TokenPayload(BaseModel):
    user_id: int
    email: str
    role: str
    nombre: str | None = None


def get_current_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = decode_access_token(token, settings)
        user_id = payload.get("sub")
        email = payload.get("email")
        role = payload.get("role")
        nombre = payload.get("nombre")
        if user_id is None or email is None or role is None:
            raise ValueError("Token incompleto")
        return TokenPayload(
            user_id=int(user_id),
            email=email,
            role=role,
            nombre=nombre,
        )
    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


def get_current_user(
    payload: TokenPayload = Depends(get_current_payload),
    db: Session = Depends(get_db),
) -> Usuario:
    user = get_by_id(db, payload.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el usuario",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*allowed_roles: str) -> Callable:
    def dependency(payload: TokenPayload = Depends(get_current_payload)) -> TokenPayload:
        if payload.role == "admin":
            return payload
        if allowed_roles and payload.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso",
            )
        return payload

    return dependency


require_admin = require_roles("admin")
