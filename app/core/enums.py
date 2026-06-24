from enum import Enum


class RoleName(str, Enum):
    admin = "admin"
    veterinario = "veterinario"
    cliente = "cliente"


class GravedadEvento(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"
