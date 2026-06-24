from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.enums import RoleName
from app.models.bebedero import Bebedero
from app.models.cliente import Cliente
from app.models.establecimiento import Establecimiento
from app.models.veterinario import Veterinario
from app.models.usuario import Usuario
from app.schemas.recursos import BebederoResumen, ClienteResumen, EstablecimientoResumen, VeterinarioDetalle
from app.schemas.usuario import UsuarioPublic


def _usuario_public(user: Usuario) -> UsuarioPublic:
    return UsuarioPublic.model_validate(user)


def _can_view_cliente(user: Usuario, cliente: Cliente) -> bool:
    if user.rol == RoleName.admin:
        return True
    if user.rol == RoleName.veterinario and user.veterinario is not None:
        return cliente.veterinario_id == user.veterinario.id
    if user.rol == RoleName.cliente and user.cliente is not None:
        return cliente.id == user.cliente.id
    return False


def _can_view_veterinario(user: Usuario, veterinario: Veterinario) -> bool:
    if user.rol == RoleName.admin:
        return True
    if user.rol == RoleName.veterinario and user.veterinario is not None:
        return veterinario.id == user.veterinario.id
    return False


def list_clientes_visible_for_user(db: Session, user: Usuario) -> list[ClienteResumen]:
    statement = (
        select(Cliente)
        .options(
            selectinload(Cliente.usuario),
            selectinload(Cliente.establecimientos).selectinload(Establecimiento.bebederos),
        )
        .order_by(Cliente.id)
    )
    if user.rol == RoleName.veterinario and user.veterinario is not None:
        statement = statement.where(Cliente.veterinario_id == user.veterinario.id)
    elif user.rol == RoleName.cliente and user.cliente is not None:
        statement = statement.where(Cliente.id == user.cliente.id)
    clientes = db.scalars(statement).unique().all()
    return [_cliente_resumen(cliente) for cliente in clientes]


def get_cliente_detalle(db: Session, user: Usuario, cliente_id: int) -> ClienteResumen:
    statement = (
        select(Cliente)
        .options(
            selectinload(Cliente.usuario),
            selectinload(Cliente.establecimientos).selectinload(Establecimiento.bebederos),
        )
        .where(Cliente.id == cliente_id)
    )
    cliente = db.scalars(statement).unique().one_or_none()
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    if not _can_view_cliente(user, cliente):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver este cliente")
    return _cliente_resumen(cliente)


def get_my_cliente_detalle(db: Session, user: Usuario) -> ClienteResumen:
    if user.cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no tiene perfil de cliente")
    return get_cliente_detalle(db, user, user.cliente.id)


def get_veterinario_detalle(db: Session, user: Usuario, veterinario_id: int) -> VeterinarioDetalle:
    statement = (
        select(Veterinario)
        .options(
            selectinload(Veterinario.usuario),
            selectinload(Veterinario.clientes).selectinload(Cliente.usuario),
            selectinload(Veterinario.clientes).selectinload(Cliente.establecimientos).selectinload(Establecimiento.bebederos),
        )
        .where(Veterinario.id == veterinario_id)
    )
    veterinario = db.scalars(statement).unique().one_or_none()
    if veterinario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinario no encontrado")
    if not _can_view_veterinario(user, veterinario):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver este veterinario")
    return VeterinarioDetalle(
        id=veterinario.id,
        usuario_id=veterinario.usuario_id,
        nombre=veterinario.usuario.nombre,
        especialidad=veterinario.especialidad,
        telefono=veterinario.telefono,
        ubicacion=veterinario.ubicacion,
        foto_perfil=veterinario.foto_perfil,
        fecha_creacion=veterinario.fecha_creacion,
        clientes=[_cliente_resumen(cliente) for cliente in veterinario.clientes],
    )


def get_my_veterinario_detalle(db: Session, user: Usuario) -> VeterinarioDetalle:
    if user.veterinario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no tiene perfil de veterinario")
    return get_veterinario_detalle(db, user, user.veterinario.id)


def list_establecimientos_visible_for_user(
    db: Session,
    user: Usuario,
    cliente_id: int | None = None,
) -> list[EstablecimientoResumen]:
    statement = (
        select(Establecimiento)
        .options(selectinload(Establecimiento.bebederos))
        .join(Cliente)
        .order_by(Establecimiento.id)
    )
    if user.rol == RoleName.veterinario and user.veterinario is not None:
        statement = statement.where(Cliente.veterinario_id == user.veterinario.id)
    elif user.rol == RoleName.cliente and user.cliente is not None:
        statement = statement.where(Establecimiento.cliente_id == user.cliente.id)
    if cliente_id is not None:
        statement = statement.where(Establecimiento.cliente_id == cliente_id)
        if user.rol == RoleName.veterinario and user.veterinario is not None:
            statement = statement.where(Cliente.veterinario_id == user.veterinario.id)
        elif user.rol == RoleName.cliente and user.cliente is not None:
            statement = statement.where(Establecimiento.cliente_id == user.cliente.id)
    establecimientos = db.scalars(statement).unique().all()
    return [_establecimiento_resumen(establecimiento) for establecimiento in establecimientos]


def _cliente_resumen(cliente: Cliente) -> ClienteResumen:
    return ClienteResumen(
        id=cliente.id,
        razon_social=cliente.razon_social,
        telefono=cliente.telefono,
        contacto_principal=cliente.contacto_principal,
        usuario=_usuario_public(cliente.usuario),
        establecimientos=[_establecimiento_resumen(item) for item in cliente.establecimientos],
    )


def _establecimiento_resumen(establecimiento: Establecimiento) -> EstablecimientoResumen:
    return EstablecimientoResumen(
        id=establecimiento.id,
        nombre=establecimiento.nombre,
        ubicacion=establecimiento.ubicacion,
        fecha_creacion=establecimiento.fecha_creacion,
        bebederos=[BebederoResumen.model_validate(bebedero) for bebedero in establecimiento.bebederos],
    )
