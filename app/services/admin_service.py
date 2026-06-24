from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import RoleName
from app.core.security import get_password_hash
from app.crud.usuarios import create_user, get_by_email, get_by_id
from app.models.bebedero import Bebedero
from app.models.cliente import Cliente
from app.models.establecimiento import Establecimiento
from app.models.evento import Evento
from app.models.imagen import Imagen
from app.models.monitoreo_diario import MonitoreoDiario
from app.models.usuario import Usuario
from app.models.veterinario import Veterinario
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


def _ensure_unique_email(db: Session, email: str) -> None:
    if get_by_email(db, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese email",
        )


def _ensure_active_user(user: Usuario | None, message: str) -> Usuario:
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return user


def create_veterinario(db: Session, payload: VeterinarioCreateRequest) -> VeterinarioAdminResponse:
    _ensure_unique_email(db, payload.email)
    user = Usuario(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        nombre=payload.nombre,
        rol=RoleName.veterinario,
        activo=payload.activo,
    )
    create_user(db, user)
    veterinarian = Veterinario(
        usuario=user,
        especialidad=payload.especialidad,
        telefono=payload.telefono,
        ubicacion=payload.ubicacion,
        foto_perfil=payload.foto_perfil,
    )
    db.add(veterinarian)
    db.commit()
    db.refresh(user)
    db.refresh(veterinarian)
    return VeterinarioAdminResponse(
        usuario=UsuarioPublic.model_validate(user),
        veterinario_id=veterinarian.id,
        especialidad=veterinarian.especialidad,
        telefono=veterinarian.telefono,
        ubicacion=veterinarian.ubicacion,
        foto_perfil=veterinarian.foto_perfil,
    )


def create_cliente(db: Session, payload: ClienteCreateRequest) -> ClienteAdminResponse:
    _ensure_unique_email(db, payload.email)
    veterinarian = db.get(Veterinario, payload.veterinario_id)
    if veterinarian is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinario no encontrado")
    if veterinarian.usuario.activo is False or veterinarian.usuario.rol != RoleName.veterinario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario indicado no es veterinario",
        )
    user = Usuario(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        nombre=payload.nombre,
        rol=RoleName.cliente,
        activo=payload.activo,
    )
    create_user(db, user)
    client = Cliente(
        usuario=user,
        veterinario_id=payload.veterinario_id,
        razon_social=payload.razon_social,
        telefono=payload.telefono,
        contacto_principal=payload.contacto_principal,
    )
    db.add(client)
    db.commit()
    db.refresh(user)
    db.refresh(client)
    return ClienteAdminResponse(
        usuario=UsuarioPublic.model_validate(user),
        cliente_id=client.id,
        veterinario_id=client.veterinario_id,
        razon_social=client.razon_social,
        telefono=client.telefono,
        contacto_principal=client.contacto_principal,
    )


def update_user_status(db: Session, user_id: int, payload: UsuarioEstadoUpdate) -> UsuarioPublic:
    user = _ensure_active_user(get_by_id(db, user_id), "Usuario no encontrado")
    user.activo = payload.activo
    db.commit()
    db.refresh(user)
    return UsuarioPublic.model_validate(user)


def get_admin_summary(db: Session) -> AdminSummary:
    total_usuarios = db.scalar(select(func.count()).select_from(Usuario)) or 0
    total_usuarios_activos = db.scalar(select(func.count()).select_from(Usuario).where(Usuario.activo.is_(True))) or 0
    total_usuarios_inactivos = total_usuarios - total_usuarios_activos
    total_admins = db.scalar(select(func.count()).select_from(Usuario).where(Usuario.rol == RoleName.admin)) or 0
    total_veterinarios = db.scalar(select(func.count()).select_from(Veterinario)) or 0
    total_clientes = db.scalar(select(func.count()).select_from(Cliente)) or 0
    total_establecimientos = db.scalar(select(func.count()).select_from(Establecimiento)) or 0
    total_bebederos = db.scalar(select(func.count()).select_from(Bebedero)) or 0
    total_bebederos_activos = db.scalar(select(func.count()).select_from(Bebedero).where(Bebedero.estado.is_(True))) or 0
    total_monitoreos = db.scalar(select(func.count()).select_from(MonitoreoDiario)) or 0
    total_imagenes = db.scalar(select(func.count()).select_from(Imagen)) or 0
    total_eventos = db.scalar(select(func.count()).select_from(Evento)) or 0
    total_eventos_pendientes = db.scalar(select(func.count()).select_from(Evento).where(Evento.resuelta.is_(False))) or 0
    return AdminSummary(
        total_usuarios=total_usuarios,
        total_usuarios_activos=total_usuarios_activos,
        total_usuarios_inactivos=total_usuarios_inactivos,
        total_admins=total_admins,
        total_veterinarios=total_veterinarios,
        total_clientes=total_clientes,
        total_establecimientos=total_establecimientos,
        total_bebederos=total_bebederos,
        total_bebederos_activos=total_bebederos_activos,
        total_monitoreos=total_monitoreos,
        total_imagenes=total_imagenes,
        total_eventos=total_eventos,
        total_eventos_pendientes=total_eventos_pendientes,
    )


def init_admin(db: Session, payload: InitAdminRequest) -> UsuarioPublic:
    """Crear el primer usuario admin. Solo funciona si no existe ningún admin en la BD."""
    # Verificar que no exista ningún admin
    existing_admin = db.query(Usuario).filter(Usuario.rol == RoleName.admin).first()
    if existing_admin is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario administrador",
        )

    # Verificar que el email sea único
    _ensure_unique_email(db, payload.email)

    # Crear usuario admin
    user = Usuario(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        nombre=payload.nombre,
        rol=RoleName.admin,
        activo=True,
    )
    create_user(db, user)
    db.commit()
    db.refresh(user)

    return UsuarioPublic.model_validate(user)
