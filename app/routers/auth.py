from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import get_current_payload, get_current_user
from app.db.session import get_db
from app.schemas.auth import AccessToken, LoginRequest, RegisterRequest, TokenPayload
from app.schemas.usuario import UsuarioMe
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AccessToken)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> AccessToken:
    return authenticate_user(db, credentials, get_settings())


@router.post("/register", response_model=AccessToken, status_code=201)
def register(
    credentials: RegisterRequest,
    db: Session = Depends(get_db),
) -> AccessToken:
    return register_user(db, credentials, get_settings())


@router.get("/me", response_model=UsuarioMe)
def read_me(current_user=Depends(get_current_user)) -> UsuarioMe:
    return UsuarioMe.model_validate(current_user)
