# Bebederos API

Backend en FastAPI para administrar usuarios, veterinarios, clientes, establecimientos, bebederos y monitoreo.

## Stack

- FastAPI
- SQLAlchemy 2.x
- MySQL / MariaDB
- JWT con access token
- Passlib + bcrypt para hashing de contraseñas

## Estructura

- `app/core`: configuración, seguridad y dependencias.
- `app/db`: base ORM y sesión de base de datos.
- `app/models`: modelos SQLAlchemy del esquema.
- `app/schemas`: contratos Pydantic de entrada y salida.
- `app/crud`: acceso a datos.
- `app/services`: lógica de autenticación y negocio.
- `app/routers`: rutas API.

## Arranque

1. Crear un archivo `.env` con la URL de base de datos y el secreto JWT.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Ejecutar `uvicorn app.main:app --reload`.

## Endpoints disponibles

- `POST /api/v1/auth/register`: crea una cuenta de `cliente` y devuelve un JWT.
- `POST /api/v1/auth/login`: autentica y devuelve un JWT.
- `GET /api/v1/auth/me`: devuelve el usuario autenticado.
- `GET /api/v1/admin/summary`: resumen global con métricas de usuarios, recursos y eventos.
- `POST /api/v1/admin/veterinarios`: crea un usuario veterinario y su perfil.
- `POST /api/v1/admin/clientes`: crea un usuario cliente y lo asigna a un veterinario.
- `PATCH /api/v1/admin/usuarios/{user_id}/estado`: activa o desactiva un usuario.
- `GET /api/v1/clientes/me`: devuelve el detalle del cliente autenticado.
- `GET /api/v1/clientes/{cliente_id}`: devuelve el detalle de un cliente con sus establecimientos.
- `GET /api/v1/veterinarios/me`: devuelve el detalle del veterinario autenticado.
- `GET /api/v1/veterinarios/{veterinario_id}`: devuelve el detalle de un veterinario con sus clientes.
- `GET /api/v1/establecimientos/{establecimiento_id}`: devuelve el detalle del establecimiento y sus bebederos.
- `GET /api/v1/establecimientos/{establecimiento_id}/bebederos`: lista los bebederos de un establecimiento con control de acceso por rol.
- `GET /api/v1/bebederos/{bebedero_id}`: devuelve el detalle del bebedero con monitoreos e imágenes.

## Nota de diseño

La autorización está pensada por rol:

- `admin`: acceso total.
- `veterinario`: acceso a sus clientes y sus recursos.
- `cliente`: acceso solo a sus establecimientos y bebederos.

Eventos y monitoreo quedan en modo lectura para esta primera etapa.
