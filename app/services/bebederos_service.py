from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.enums import RoleName
from app.models.bebedero import Bebedero
from app.models.establecimiento import Establecimiento
from app.models.monitoreo_diario import MonitoreoDiario
from app.models.usuario import Usuario
from app.schemas.bebederos import BebederoDetalle, ImagenDetalle, MonitoreoDetalle
from app.schemas.recursos import BebederoResumen, EstablecimientoDetalle


def get_bebedero_detalle(db: Session, user: Usuario, bebedero_id: int) -> BebederoDetalle:
    statement = (
        select(Bebedero)
        .options(
            selectinload(Bebedero.establecimiento).selectinload(Establecimiento.cliente),
            selectinload(Bebedero.monitoreos).selectinload(MonitoreoDiario.imagenes),
        )
        .where(Bebedero.id == bebedero_id)
    )
    bebedero = db.scalars(statement).unique().one_or_none()
    if bebedero is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bebedero no encontrado")
    if not _can_view_bebedero(user, bebedero):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver este bebedero")
    return _to_detalle(bebedero)


def list_bebederos_for_establecimiento(
    db: Session,
    user: Usuario,
    establecimiento_id: int,
) -> list[BebederoResumen]:
    statement = (
        select(Establecimiento)
        .options(selectinload(Establecimiento.bebederos), selectinload(Establecimiento.cliente))
        .where(Establecimiento.id == establecimiento_id)
    )
    establecimiento = db.scalars(statement).unique().one_or_none()
    if establecimiento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establecimiento no encontrado")
    if not _can_view_establecimiento(user, establecimiento):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver este establecimiento")
    return [BebederoResumen.model_validate(bebedero) for bebedero in establecimiento.bebederos]


def get_establecimiento_detalle(
    db: Session,
    user: Usuario,
    establecimiento_id: int,
) -> EstablecimientoDetalle:
    statement = (
        select(Establecimiento)
        .options(selectinload(Establecimiento.bebederos), selectinload(Establecimiento.cliente))
        .where(Establecimiento.id == establecimiento_id)
    )
    establecimiento = db.scalars(statement).unique().one_or_none()
    if establecimiento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establecimiento no encontrado")
    if not _can_view_establecimiento(user, establecimiento):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver este establecimiento")
    return EstablecimientoDetalle(
        id=establecimiento.id,
        cliente_id=establecimiento.cliente_id,
        cliente_razon_social=establecimiento.cliente.razon_social,
        nombre=establecimiento.nombre,
        ubicacion=establecimiento.ubicacion,
        fecha_creacion=establecimiento.fecha_creacion,
        bebederos=[BebederoResumen.model_validate(bebedero) for bebedero in establecimiento.bebederos],
    )


def _can_view_bebedero(user: Usuario, bebedero: Bebedero) -> bool:
    if user.rol == RoleName.admin:
        return True
    if user.rol == RoleName.veterinario and user.veterinario is not None:
        return bebedero.establecimiento.cliente.veterinario_id == user.veterinario.id
    if user.rol == RoleName.cliente and user.cliente is not None:
        return bebedero.establecimiento.cliente_id == user.cliente.id
    return False


def _can_view_establecimiento(user: Usuario, establecimiento: Establecimiento) -> bool:
    if user.rol == RoleName.admin:
        return True
    if user.rol == RoleName.veterinario and user.veterinario is not None:
        return establecimiento.cliente.veterinario_id == user.veterinario.id
    if user.rol == RoleName.cliente and user.cliente is not None:
        return establecimiento.cliente_id == user.cliente.id
    return False


def _to_detalle(bebedero: Bebedero) -> BebederoDetalle:
    monitoreos = sorted(bebedero.monitoreos, key=lambda item: (item.fecha, item.timestamp), reverse=True)
    return BebederoDetalle(
        id=bebedero.id,
        establecimiento_id=bebedero.establecimiento_id,
        establecimiento_nombre=bebedero.establecimiento.nombre,
        nombre=bebedero.nombre,
        ubicacion=bebedero.ubicacion,
        ip_address=bebedero.ip_address,
        puerto=bebedero.puerto,
        cobertura_objetivo=bebedero.cobertura_objetivo,
        estado=bebedero.estado,
        ultima_medicion=bebedero.ultima_medicion,
        fecha_creacion=bebedero.fecha_creacion,
        monitoreos=[
            MonitoreoDetalle(
                id=monitoreo.id,
                fecha=monitoreo.fecha,
                timestamp=monitoreo.timestamp,
                nivel_agua_cm=monitoreo.nivel_agua_cm,
                distancia_sensor_cm=monitoreo.distancia_sensor_cm,
                cobertura_capsulas_porciento=monitoreo.cobertura_capsulas_porciento,
                sensor_ultrasound=monitoreo.sensor_ultrasound,
                camera_activa=monitoreo.camera_activa,
                analyzer_activo=monitoreo.analyzer_activo,
                config_ok=monitoreo.config_ok,
                error_message=monitoreo.error_message,
                imagenes=[
                    ImagenDetalle.model_validate(imagen)
                    for imagen in sorted(monitoreo.imagenes, key=lambda item: item.fecha_captura, reverse=True)
                ],
            )
            for monitoreo in monitoreos
        ],
    )
