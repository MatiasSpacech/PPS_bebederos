from fastapi import FastAPI

from app.core.config import get_settings
from app.routers import admin, auth, bebederos, clientes, establecimientos, health, veterinarios

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend FastAPI para administración de bebederos, monitoreo y roles.",
)

app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(admin.router, prefix=settings.api_v1_prefix)
app.include_router(bebederos.router, prefix=settings.api_v1_prefix)
app.include_router(establecimientos.router, prefix=settings.api_v1_prefix)
app.include_router(veterinarios.router, prefix=settings.api_v1_prefix)
app.include_router(clientes.router, prefix=settings.api_v1_prefix)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "docs": "/docs",
        "status": "ready",
    }
