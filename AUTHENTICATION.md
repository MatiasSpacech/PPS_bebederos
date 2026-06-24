# Autenticación y Autorización

## Flujo de autenticación

### 1. Registro (crear cuenta cliente)

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "cliente@example.com",
  "password": "MiContraseña123",
  "nombre": "Juan Pérez"
}
```

**Respuesta (201)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Lo que sucede internamente**:
1. Se valida que el email sea único
2. Se valida que la contraseña tenga mínimo 8 caracteres
3. Se hashea la contraseña con bcrypt
4. Se crea un usuario con rol `cliente`
5. Se crea un perfil de cliente vinculado
6. Se genera un JWT con expiración de 30 minutos
7. Se retorna el token

### 2. Login

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "cliente@example.com",
  "password": "MiContraseña123"
}
```

**Respuesta (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Lo que sucede internamente**:
1. Se busca el usuario por email
2. Se valida que el usuario sea activo
3. Se compara la contraseña con el hash usando bcrypt
4. Se genera un nuevo JWT
5. Se actualiza `fecha_ultimo_acceso`

### 3. Usar token autenticado

Todos los endpoints protegidos requieren el header `Authorization`:

```bash
GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Estructura del JWT

El token contiene los siguientes claims:

```json
{
  "sub": "1",           // user_id (como string)
  "email": "user@example.com",
  "role": "cliente",    // admin, veterinario, cliente
  "nombre": "Juan",
  "exp": 1626872345     // timestamp de expiración
}
```

## Control de Acceso por Rol

### Bootstrap: Crear el primer admin

```bash
POST /api/v1/admin/init
Content-Type: application/json

{
  "email": "admin@bebederos.com",
  "password": "SuperSecure123!",
  "nombre": "Administrador"
}
```

**Importante**: Este endpoint solo funciona si no existe ningún admin en la BD.

**Errores posibles**:
- `409 Conflict`: Ya existe un admin
- `409 Conflict`: Email duplicado
- `422 Unprocessable Entity`: Contraseña < 8 caracteres

### Admin: Crear veterinarios

Una vez con token de admin:

```bash
POST /api/v1/admin/veterinarios
Authorization: Bearer <token_admin>
Content-Type: application/json

{
  "email": "vet@example.com",
  "password": "VetPass123!",
  "nombre": "Dr. González",
  "especialidad": "Rumiantes",
  "telefono": "+34-666-777-888",
  "ubicacion": "Madrid",
  "activo": true
}
```

**Errores posibles**:
- `401 Unauthorized`: Token inválido o expirado
- `403 Forbidden`: Usuario no es admin
- `409 Conflict`: Email duplicado
- `422 Unprocessable Entity`: Datos inválidos

### Admin: Crear clientes

```bash
POST /api/v1/admin/clientes
Authorization: Bearer <token_admin>
Content-Type: application/json

{
  "email": "farm@example.com",
  "password": "FarmPass123!",
  "nombre": "Juan Granjero",
  "veterinario_id": 1,
  "razon_social": "Granja Pérez S.L.",
  "telefono": "+34-666-999-888",
  "contacto_principal": "Juan Pérez",
  "activo": true
}
```

**Validaciones**:
- El `veterinario_id` debe existir y ser activo
- El veterinario debe tener rol `veterinario`
- El email debe ser único

## Matrix de Control de Acceso

| Recurso | Admin | Veterinario | Cliente | No Autenticado |
|---------|-------|-------------|---------|-----------------|
| `/admin/*` | ✅ | ❌ | ❌ | ❌ |
| `/auth/register` | ✅ | ✅ | ✅ | ✅ |
| `/auth/login` | ✅ | ✅ | ✅ | ✅ |
| `/auth/me` | ✅ | ✅ | ✅ | ❌ |
| `/clientes/me` | ✅ (todos) | ✅ (sus asignados) | ✅ (solo él) | ❌ |
| `/veterinarios/me` | ✅ (todos) | ✅ (solo él) | ❌ | ❌ |
| `/establecimientos/{id}` | ✅ | ✅ (asignados) | ✅ (suyos) | ❌ |
| `/bebederos/{id}` | ✅ | ✅ (asignados) | ✅ (suyos) | ❌ |

## Seguridad

### Hashing de contraseñas

Las contraseñas se hashean usando **bcrypt** con salt:

```
Contraseña entrada: "MiContraseña123"
           ↓
    bcrypt.hash()
           ↓
Hash almacenado: "$2b$12$N9qo8uLOickgx2..."
```

Cuando el usuario intenta login:
```
Contraseña entrada: "MiContraseña123"
          +
Hash almacenado: "$2b$12$N9qo8uLOickgx2..."
          ↓
   bcrypt.verify()
          ↓
Resultado: True/False
```

### JWT Token

- **Algoritmo**: HS256 (HMAC-SHA256)
- **Clave secreta**: Definida en `JWT_SECRET_KEY` del `.env`
- **Expiración**: 30 minutos (configurable en `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Validación**: Se verifica firma y expiración en cada request

### Validaciones

1. **Email**:
   - Formato válido (validado por Pydantic `EmailStr`)
   - Único en el sistema

2. **Contraseña**:
   - Mínimo 8 caracteres
   - No hay validación de complejidad (recomendado agregar)

3. **Token**:
   - Debe estar en header `Authorization: Bearer <token>`
   - Debe ser válido (firma correcta)
   - No debe estar expirado

## Errores comunes

### Token expirado
```
Error: 401 Unauthorized
detail: "Token expirado"
```
**Solución**: Hacer login nuevamente para obtener un nuevo token

### Usuario no activo
```
Error: 401 Unauthorized
detail: "Usuario no activo"
```
**Solución**: El admin debe activar el usuario con `PATCH /admin/usuarios/{user_id}/estado`

### No es admin
```
Error: 403 Forbidden
detail: "Acceso denegado. Se requiere rol: admin"
```
**Solución**: Solo admins pueden acceder a endpoints de admin

### Email duplicado
```
Error: 409 Conflict
detail: "Ya existe un usuario con ese email"
```
**Solución**: Usar un email diferente

## Mejores prácticas

1. **Guardar token de forma segura**:
   - En aplicaciones web: localStorage o sessionStorage (con cuidado)
   - En aplicaciones móviles: Keychain (iOS) o KeyStore (Android)
   - Nunca en URLs o logs

2. **Renovar tokens**:
   - Los tokens expiran después de 30 minutos
   - Hacer login nuevamente cuando expire

3. **HTTPS**:
   - Usar HTTPS en producción
   - Tokens pueden ser interceptados en HTTP

4. **Secreto JWT**:
   - Cambiar `JWT_SECRET_KEY` en producción
   - No compartir ni versionar en git
   - Usar `.env` local

5. **Contraseñas de usuario**:
   - Recomendación: mínimo 12 caracteres
   - Recomendación: incluir mayúsculas, números, símbolos
   - Recomendación: educación a usuarios sobre contraseñas fuertes
