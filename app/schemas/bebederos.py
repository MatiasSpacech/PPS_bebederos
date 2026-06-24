from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ImagenDetalle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_archivo: str
    ruta_filesystem: str
    fecha_captura: datetime
    tamano_bytes: int | None = None
    checksum: str | None = None


class MonitoreoDetalle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: date
    timestamp: datetime
    nivel_agua_cm: float | None = None
    distancia_sensor_cm: float | None = None
    cobertura_capsulas_porciento: float | None = None
    sensor_ultrasound: bool | None = None
    camera_activa: bool | None = None
    analyzer_activo: bool | None = None
    config_ok: bool | None = None
    error_message: str | None = None
    imagenes: list[ImagenDetalle] = Field(default_factory=list)


class BebederoDetalle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    establecimiento_id: int
    establecimiento_nombre: str
    nombre: str
    ubicacion: str | None = None
    ip_address: str | None = None
    puerto: int
    cobertura_objetivo: float
    estado: bool
    ultima_medicion: datetime | None = None
    fecha_creacion: datetime
    monitoreos: list[MonitoreoDetalle] = Field(default_factory=list)
