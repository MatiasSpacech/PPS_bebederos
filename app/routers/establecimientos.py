from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import TokenPayload, get_current_user, require_roles
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.recursos import BebederoResumen, EstablecimientoDetalle
from app.services.bebederos_service import get_establecimiento_detalle, list_bebederos_for_establecimiento

router = APIRouter(prefix="/establecimientos", tags=["establecimientos"])


@router.get("/{establecimiento_id}/bebederos", response_model=list[BebederoResumen])
def establishment_bebederos(
    establecimiento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario", "cliente")),
) -> list[BebederoResumen]:
    return list_bebederos_for_establecimiento(db, current_user, establecimiento_id)


@router.get("/{establecimiento_id}", response_model=EstablecimientoDetalle)
def establishment_detail(
    establecimiento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario", "cliente")),
) -> EstablecimientoDetalle:
    return get_establecimiento_detalle(db, current_user, establecimiento_id)
