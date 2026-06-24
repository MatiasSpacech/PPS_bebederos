from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import TokenPayload, get_current_user, require_roles
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.recursos import ClienteResumen, EstablecimientoResumen
from app.services.recursos_service import (
    get_cliente_detalle,
    get_my_cliente_detalle,
    list_establecimientos_visible_for_user,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/dashboard")
def dashboard(payload: TokenPayload = Depends(require_roles("cliente"))) -> dict[str, object]:
    return {
        "message": "Panel de cliente",
        "user": payload.model_dump(),
    }


@router.get("/me", response_model=ClienteResumen)
def my_detail(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("cliente")),
) -> ClienteResumen:
    return get_my_cliente_detalle(db, current_user)


@router.get("/{cliente_id}", response_model=ClienteResumen)
def client_detail(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario", "cliente")),
) -> ClienteResumen:
    return get_cliente_detalle(db, current_user, cliente_id)


@router.get("/mis-establecimientos", response_model=list[EstablecimientoResumen])
def my_establishments(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("cliente")),
) -> list[EstablecimientoResumen]:
    return list_establecimientos_visible_for_user(db, current_user)
