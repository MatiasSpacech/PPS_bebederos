# Ejemplos de Uso de la API

## Flujo completo de bootstrap

### Paso 1: Crear el primer admin

```bash
curl -X POST http://localhost:8000/api/v1/admin/init \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@bebederos.com",
    "password": "AdminSecure123!",
    "nombre": "Juan Admin"
  }'
```

**Respuesta (201)**:
```json
{
  "email": "admin@bebederos.com",
  "nombre": "Juan Admin",
  "rol": "admin",
  "activo": true,
  "fecha_creacion": "2026-06-22T10:30:00"
}
```

### Paso 2: Login como admin

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@bebederos.com",
    "password": "AdminSecure123!"
  }'
```

**Respuesta (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Guardar el `access_token` como `$ADMIN_TOKEN` para requests posteriores.

### Paso 3: Ver dashboard del admin

```bash
curl -X GET http://localhost:8000/api/v1/admin/dashboard \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

**Respuesta (200)**:
```json
{
  "message": "Panel de administrador",
  "user": {
    "user_id": 1,
    "email": "admin@bebederos.com",
    "role": "admin",
    "nombre": "Juan Admin"
  }
}
```

### Paso 4: Ver resumen de métricas

```bash
curl -X GET http://localhost:8000/api/v1/admin/summary \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

**Respuesta (200)**:
```json
{
  "total_usuarios": 1,
  "total_usuarios_activos": 1,
  "total_usuarios_inactivos": 0,
  "total_admins": 1,
  "total_veterinarios": 0,
  "total_clientes": 0,
  "total_establecimientos": 0,
  "total_bebederos": 0,
  "total_bebederos_activos": 0,
  "total_monitoreos": 0,
  "total_imagenes": 0,
  "total_eventos": 0,
  "total_eventos_pendientes": 0
}
```

## Crear veterinarios

### Paso 5: Admin crea un veterinario

```bash
curl -X POST http://localhost:8000/api/v1/admin/veterinarios \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "vet1@bebederos.com",
    "password": "VetPass123!",
    "nombre": "Dr. Carlos López",
    "especialidad": "Rumiantes",
    "telefono": "+34-666-777-888",
    "ubicacion": "Madrid",
    "foto_perfil": "https://example.com/vet1.jpg",
    "activo": true
  }'
```

**Respuesta (201)**:
```json
{
  "usuario": {
    "email": "vet1@bebederos.com",
    "nombre": "Dr. Carlos López",
    "rol": "veterinario",
    "activo": true,
    "fecha_creacion": "2026-06-22T10:35:00"
  },
  "veterinario_id": 1,
  "especialidad": "Rumiantes",
  "telefono": "+34-666-777-888",
  "ubicacion": "Madrid",
  "foto_perfil": "https://example.com/vet1.jpg"
}
```

Guardar `veterinario_id` = 1 para crear clientes asignados a este veterinario.

## Crear clientes

### Paso 6: Admin crea un cliente asignado al veterinario

```bash
curl -X POST http://localhost:8000/api/v1/admin/clientes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "granja@example.com",
    "password": "GranjaPass123!",
    "nombre": "Juan Granjero",
    "veterinario_id": 1,
    "razon_social": "Granja Pérez S.L.",
    "telefono": "+34-666-999-888",
    "contacto_principal": "Juan Pérez",
    "activo": true
  }'
```

**Respuesta (201)**:
```json
{
  "usuario": {
    "email": "granja@example.com",
    "nombre": "Juan Granjero",
    "rol": "cliente",
    "activo": true,
    "fecha_creacion": "2026-06-22T10:40:00"
  },
  "cliente_id": 1,
  "veterinario_id": 1,
  "razon_social": "Granja Pérez S.L.",
  "telefono": "+34-666-999-888",
  "contacto_principal": "Juan Pérez"
}
```

## Acceso como veterinario

### Paso 7: Veterinario hace login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "vet1@bebederos.com",
    "password": "VetPass123!"
  }'
```

**Respuesta (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Guardar el token como `$VET_TOKEN`.

### Paso 8: Veterinario ve su perfil

```bash
curl -X GET http://localhost:8000/api/v1/veterinarios/me \
  -H "Authorization: Bearer $VET_TOKEN"
```

**Respuesta (200)**:
```json
{
  "usuario": {
    "email": "vet1@bebederos.com",
    "nombre": "Dr. Carlos López",
    "rol": "veterinario",
    "activo": true,
    "fecha_creacion": "2026-06-22T10:35:00"
  },
  "veterinario_id": 1,
  "especialidad": "Rumiantes",
  "telefono": "+34-666-777-888",
  "ubicacion": "Madrid",
  "foto_perfil": "https://example.com/vet1.jpg"
}
```

### Paso 9: Veterinario ve sus clientes

```bash
curl -X GET http://localhost:8000/api/v1/veterinarios/clientes \
  -H "Authorization: Bearer $VET_TOKEN"
```

**Respuesta (200)**:
```json
{
  "clientes": [
    {
      "usuario": {
        "email": "granja@example.com",
        "nombre": "Juan Granjero",
        "rol": "cliente",
        "activo": true
      },
      "cliente_id": 1,
      "razon_social": "Granja Pérez S.L.",
      "telefono": "+34-666-999-888",
      "contacto_principal": "Juan Pérez"
    }
  ]
}
```

### Paso 10: Veterinario ve establecimientos de un cliente

```bash
curl -X GET http://localhost:8000/api/v1/veterinarios/1/clientes/1/establecimientos \
  -H "Authorization: Bearer $VET_TOKEN"
```

**Respuesta (200)**:
```json
{
  "establecimientos": []
}
```

(Vacío porque el cliente aún no ha creado establecimientos)

## Acceso como cliente

### Paso 11: Cliente hace login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "granja@example.com",
    "password": "GranjaPass123!"
  }'
```

**Respuesta (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Guardar el token como `$CLIENT_TOKEN`.

### Paso 12: Cliente ve su perfil

```bash
curl -X GET http://localhost:8000/api/v1/clientes/me \
  -H "Authorization: Bearer $CLIENT_TOKEN"
```

**Respuesta (200)**:
```json
{
  "usuario": {
    "email": "granja@example.com",
    "nombre": "Juan Granjero",
    "rol": "cliente",
    "activo": true
  },
  "cliente_id": 1,
  "veterinario_id": 1,
  "razon_social": "Granja Pérez S.L.",
  "telefono": "+34-666-999-888",
  "contacto_principal": "Juan Pérez"
}
```

### Paso 13: Cliente ve sus establecimientos

```bash
curl -X GET http://localhost:8000/api/v1/clientes/mis-establecimientos \
  -H "Authorization: Bearer $CLIENT_TOKEN"
```

**Respuesta (200)**:
```json
{
  "establecimientos": []
}
```

## Error: Cliente intenta acceder a recurso ajeno

### Crear segundo cliente (sin asignación al vet)

```bash
curl -X POST http://localhost:8000/api/v1/admin/clientes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "otra_granja@example.com",
    "password": "OtraPass123!",
    "nombre": "Otra Granja",
    "veterinario_id": 1,
    "razon_social": "Otra Granja S.L.",
    "telefono": "+34-666-111-222",
    "activo": true
  }'
```

Guardar `cliente_id` = 2.

### Cliente 1 intenta ver cliente 2

```bash
curl -X GET http://localhost:8000/api/v1/clientes/2 \
  -H "Authorization: Bearer $CLIENT_TOKEN"
```

**Respuesta (403)**:
```json
{
  "detail": "No tienes permiso para acceder a este recurso"
}
```

## Registro de nuevo cliente (sin admin)

### Cliente se auto-registra

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo_cliente@example.com",
    "password": "NewClientPass123!",
    "nombre": "Nuevo Cliente"
  }'
```

**Respuesta (201)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Nota**: El cliente se crea sin veterinario asignado. El admin debe crear un perfil de cliente completo con `POST /admin/clientes`.

## Scripts útiles

### Script bash para test completo

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"

# 1. Crear admin
echo "1. Creating admin..."
ADMIN_RESPONSE=$(curl -s -X POST $BASE_URL/admin/init \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "AdminTest123!",
    "nombre": "Admin Test"
  }')

# 2. Login admin
echo "2. Logging in as admin..."
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "AdminTest123!"
  }')

ADMIN_TOKEN=$(echo $ADMIN_LOGIN | jq -r '.access_token')
echo "Admin token: $ADMIN_TOKEN"

# 3. Create veterinarian
echo "3. Creating veterinarian..."
VET_RESPONSE=$(curl -s -X POST $BASE_URL/admin/veterinarios \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "vet@test.com",
    "password": "VetTest123!",
    "nombre": "Dr. Test",
    "especialidad": "Rumiantes",
    "activo": true
  }')

VET_ID=$(echo $VET_RESPONSE | jq -r '.veterinario_id')
echo "Veterinarian ID: $VET_ID"

# 4. Create client
echo "4. Creating client..."
CLIENT_RESPONSE=$(curl -s -X POST $BASE_URL/admin/clientes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d "{
    \"email\": \"client@test.com\",
    \"password\": \"ClientTest123!\",
    \"nombre\": \"Test Client\",
    \"veterinario_id\": $VET_ID,
    \"razon_social\": \"Test Farm\",
    \"activo\": true
  }")

echo "Client created:"
echo $CLIENT_RESPONSE | jq '.'

echo "✓ Bootstrap complete!"
```

## Usar con Python requests

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Create admin
response = requests.post(
    f"{BASE_URL}/admin/init",
    json={
        "email": "admin@example.com",
        "password": "AdminSecure123!",
        "nombre": "Admin"
    }
)
print(f"Admin created: {response.status_code}")

# 2. Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "admin@example.com",
        "password": "AdminSecure123!"
    }
)
admin_token = response.json()["access_token"]
print(f"Token: {admin_token}")

# 3. Get summary
response = requests.get(
    f"{BASE_URL}/admin/summary",
    headers={"Authorization": f"Bearer {admin_token}"}
)
print(f"Summary: {response.json()}")
```
