from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import TokenPayload, require_admin
from app.db.session import get_db
from app.schemas.admin import (
    AdminSummary,
    ClienteAdminResponse,
    ClienteCreateRequest,
    InitAdminRequest,
    UsuarioEstadoUpdate,
    VeterinarioAdminResponse,
    VeterinarioCreateRequest,
)
from app.schemas.usuario import UsuarioPublic
from app.services.admin_service import (
    create_cliente,
    create_veterinario,
    get_admin_summary,
    init_admin,
    update_user_status,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/init", response_model=UsuarioPublic, status_code=201)
def initialize_admin(payload: InitAdminRequest, db: Session = Depends(get_db)) -> UsuarioPublic:
    """Crear el primer usuario administrador. Solo funciona si no existe ningún admin."""
    return init_admin(db, payload)


@router.get("/dashboard")
def dashboard(payload: TokenPayload = Depends(require_admin)) -> dict[str, object]:
    return {
        "message": "Panel de administrador",
        "user": payload.model_dump(),
    }


@router.get("/summary", response_model=AdminSummary)
def summary(
    db: Session = Depends(get_db),
    _: TokenPayload = Depends(require_admin),
) -> AdminSummary:
    return get_admin_summary(db)


@router.post("/veterinarios", response_model=VeterinarioAdminResponse, status_code=201)
def create_veterinarian(
    payload: VeterinarioCreateRequest,
    db: Session = Depends(get_db),
    _: TokenPayload = Depends(require_admin),
) -> VeterinarioAdminResponse:
    return create_veterinario(db, payload)


@router.post("/clientes", response_model=ClienteAdminResponse, status_code=201)
def create_client(
    payload: ClienteCreateRequest,
    db: Session = Depends(get_db),
    _: TokenPayload = Depends(require_admin),
) -> ClienteAdminResponse:
    return create_cliente(db, payload)


@router.patch("/usuarios/{user_id}/estado", response_model=UsuarioPublic)
def update_status(
    user_id: int,
    payload: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    _: TokenPayload = Depends(require_admin),
) -> UsuarioPublic:
    return update_user_status(db, user_id, payload)
