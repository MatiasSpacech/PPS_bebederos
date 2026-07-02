from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import mimetypes

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.imagen import Imagen
from app.models.usuario import Usuario
from app.core.enums import RoleName

router = APIRouter(tags=["imagenes"])


@router.get("/imagenes/{imagen_id}", response_class=FileResponse)
def serve_imagen(
    imagen_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    imagen = db.get(Imagen, imagen_id)
    if imagen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")

    bebedero = imagen.bebedero
    # RBAC: same rules as bebedero viewing
    if current_user.rol == RoleName.admin:
        pass
    elif current_user.rol == RoleName.veterinario and getattr(current_user, "veterinario", None) is not None:
        if bebedero.establecimiento.cliente.veterinario_id != current_user.veterinario.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver esta imagen")
    elif current_user.rol == RoleName.cliente and getattr(current_user, "cliente", None) is not None:
        if bebedero.establecimiento.cliente_id != current_user.cliente.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver esta imagen")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para ver esta imagen")

    file_path = imagen.ruta_filesystem
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Archivo de imagen no encontrado en el servidor")

    media_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(path=file_path, media_type=media_type or "application/octet-stream", filename=imagen.nombre_archivo)
