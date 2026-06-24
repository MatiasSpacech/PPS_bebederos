from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.enums import RoleName
from app.crud.usuarios import create_user, get_by_email, touch_last_access
from app.models.usuario import Usuario
from app.schemas.auth import AccessToken, LoginRequest, RegisterRequest


class AuthenticationError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )


def build_access_token(user: Usuario, settings: Settings) -> AccessToken:
    token_payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.rol.value,
        "nombre": user.nombre,
    }
    token = create_access_token(token_payload, settings)
    return AccessToken(access_token=token)


def authenticate_user(db: Session, credentials: LoginRequest, settings: Settings) -> AccessToken:
    user = get_by_email(db, credentials.email)
    if user is None or not user.activo:
        raise AuthenticationError()
    if not verify_password(credentials.password, user.password_hash):
        raise AuthenticationError()
    touch_last_access(db, user)
    return build_access_token(user, settings)


def register_user(db: Session, credentials: RegisterRequest, settings: Settings) -> AccessToken:
    if credentials.rol != RoleName.cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El registro público solo permite crear clientes",
        )
    if get_by_email(db, credentials.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese email",
        )
    user = Usuario(
        email=credentials.email,
        password_hash=get_password_hash(credentials.password),
        nombre=credentials.nombre,
        rol=credentials.rol,
        activo=True,
    )
    create_user(db, user)
    db.commit()
    db.refresh(user)
    return build_access_token(user, settings)


def seed_password(password: str) -> str:
    return get_password_hash(password)
