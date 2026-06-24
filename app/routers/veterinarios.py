from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import TokenPayload, get_current_user, require_roles
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.recursos import ClienteResumen, EstablecimientoResumen, VeterinarioDetalle
from app.services.recursos_service import (
    get_my_veterinario_detalle,
    get_veterinario_detalle,
    list_clientes_visible_for_user,
    list_establecimientos_visible_for_user,
)

router = APIRouter(prefix="/veterinarios", tags=["veterinarios"])


@router.get("/dashboard")
def dashboard(payload: TokenPayload = Depends(require_roles("veterinario"))) -> dict[str, object]:
    return {
        "message": "Panel de veterinario",
        "user": payload.model_dump(),
    }


@router.get("/me", response_model=VeterinarioDetalle)
def my_detail(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario")),
) -> VeterinarioDetalle:
    return get_my_veterinario_detalle(db, current_user)


@router.get("/{veterinario_id}", response_model=VeterinarioDetalle)
def veterinarian_detail(
    veterinario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario")),
) -> VeterinarioDetalle:
    return get_veterinario_detalle(db, current_user, veterinario_id)


@router.get("/clientes", response_model=list[ClienteResumen])
def my_clients(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario")),
) -> list[ClienteResumen]:
    return list_clientes_visible_for_user(db, current_user)


@router.get("/clientes/{cliente_id}/establecimientos", response_model=list[EstablecimientoResumen])
def client_establishments(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario")),
) -> list[EstablecimientoResumen]:
    return list_establecimientos_visible_for_user(db, current_user, cliente_id=cliente_id)
