from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import TokenPayload, get_current_user, require_roles
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.bebederos import BebederoDetalle
from app.services.bebederos_service import get_bebedero_detalle

router = APIRouter(prefix="/bebederos", tags=["bebederos"])


@router.get("/{bebedero_id}", response_model=BebederoDetalle)
def read_bebedero(
    bebedero_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    _: TokenPayload = Depends(require_roles("veterinario", "cliente")),
) -> BebederoDetalle:
    return get_bebedero_detalle(db, current_user, bebedero_id)
