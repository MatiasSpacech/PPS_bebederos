# RBAC - Control de Acceso Basado en Roles

## Roles disponibles

### 1. Admin (`admin`)
- **Descripción**: Control total del sistema
- **Permisos**: 
  - Ver todos los usuarios, veterinarios, clientes
  - Crear veterinarios y clientes
  - Activar/desactivar usuarios
  - Ver métricas globales
  - Acceso a todos los recursos

**Endpoints exclusivos**:
- `GET /api/v1/admin/dashboard`
- `GET /api/v1/admin/summary`
- `POST /api/v1/admin/veterinarios`
- `POST /api/v1/admin/clientes`
- `PATCH /api/v1/admin/usuarios/{user_id}/estado`

### 2. Veterinario (`veterinario`)
- **Descripción**: Profesional de salud animal
- **Permisos**:
  - Ver sus clientes asignados
  - Ver establecimientos y bebederos de sus clientes
  - Ver monitoreos e imágenes
  - Acceso solo a datos de clientes asignados

**Endpoints disponibles**:
- `GET /api/v1/veterinarios/me` - Ver su perfil
- `GET /api/v1/veterinarios/{id}` - Ver otro veterinario (solo lectura)
- `GET /api/v1/veterinarios/clientes` - Ver sus clientes
- `GET /api/v1/clientes/{id}` - Ver clientes asignados
- `GET /api/v1/establecimientos/{id}` - Ver establecimientos de clientes asignados
- `GET /api/v1/bebederos/{id}` - Ver bebederos asignados

### 3. Cliente (`cliente`)
- **Descripción**: Propietario de establecimientos y bebederos
- **Permisos**:
  - Ver solo sus establecimientos
  - Ver solo sus bebederos
  - Ver monitoreos e imágenes de sus bebederos
  - No puede crear recursos

**Endpoints disponibles**:
- `GET /api/v1/clientes/me` - Ver su perfil
- `GET /api/v1/clientes/mis-establecimientos` - Ver sus establecimientos
- `GET /api/v1/establecimientos/{id}` - Ver detalles de establecimiento (si es suyo)
- `GET /api/v1/bebederos/{id}` - Ver detalles de bebedero (si es suyo)

## Jerarquía de acceso

```
Admin
 ├── Ve todo
 ├── Crea veterinarios
 └── Crea clientes

Veterinario (creado por admin)
 ├── Ve sus clientes asignados
 ├── Ve establecimientos de clientes
 └── Ve bebederos de clientes

Cliente (creado por admin, asignado a veterinario)
 ├── Ve sus establecimientos
 ├── Ve sus bebederos
 └── Ve monitoreos de sus bebederos
```

## Matriz de permisos detallada

### Auth (sin rol)
| Endpoint | GET | POST | PATCH | DELETE |
|----------|-----|------|-------|--------|
| `/auth/register` | - | ✅ | - | - |
| `/auth/login` | - | ✅ | - | - |
| `/auth/me` | ✅ | - | - | - |

### Admin
| Endpoint | GET | POST | PATCH | DELETE |
|----------|-----|------|-------|--------|
| `/admin/dashboard` | ✅ | - | - | - |
| `/admin/summary` | ✅ | - | - | - |
| `/admin/veterinarios` | - | ✅ | - | - |
| `/admin/clientes` | - | ✅ | - | - |
| `/admin/usuarios/{id}/estado` | - | - | ✅ | - |

### Clientes
| Endpoint | Requisito | Admin | Vet | Cliente |
|----------|-----------|-------|-----|---------|
| `/clientes/me` | Autenticado | ✅ | ❌ | ✅ |
| `/clientes/{id}` | Es suyo O admin | ✅ | ❌ | ✅ |
| `/clientes/mis-establecimientos` | Cliente autenticado | ✅ | ❌ | ✅ |

### Veterinarios
| Endpoint | Requisito | Admin | Vet | Cliente |
|----------|-----------|-------|-----|---------|
| `/veterinarios/me` | Vet autenticado | ✅ | ✅ | ❌ |
| `/veterinarios/{id}` | Es él O admin | ✅ | ✅ | ❌ |
| `/veterinarios/clientes` | Vet autenticado | ✅ | ✅ | ❌ |

### Establecimientos
| Endpoint | Requisito | Admin | Vet | Cliente |
|----------|-----------|-------|-----|---------|
| `/establecimientos/{id}` | Es suyo O asignado a vet | ✅ | ✅* | ✅ |
| `/establecimientos/{id}/bebederos` | Es suyo O asignado a vet | ✅ | ✅* | ✅ |

*Vet: Solo si el cliente está asignado a él

### Bebederos
| Endpoint | Requisito | Admin | Vet | Cliente |
|----------|-----------|-------|-----|---------|
| `/bebederos/{id}` | Es suyo O asignado a vet | ✅ | ✅* | ✅ |

*Vet: Solo si el bebedero pertenece a un cliente asignado

## Implementación técnica

### Dependency Injection

Todos los endpoints protegidos usan dependencias que validan el rol:

```python
from app.core.dependencies import require_admin, require_roles

# Solo admin
@router.post("/veterinarios")
def create_vet(
    payload: VeterinarioCreateRequest,
    db: Session = Depends(get_db),
    _: TokenPayload = Depends(require_admin),
):
    ...

# Admin o veterinario
@router.get("/clientes/{cliente_id}")
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    user: TokenPayload = Depends(require_roles("admin", "veterinario")),
):
    ...
```

### Service Layer

La validación también se realiza en la capa de servicios:

```python
def get_cliente_detalle(db: Session, cliente_id: int, current_user: Usuario) -> ClienteResumen:
    cliente = db.get(Cliente, cliente_id)
    
    # Admin ve todos
    if current_user.rol == RoleName.admin:
        return ClienteResumen.model_validate(cliente)
    
    # Veterinario ve solo clientes asignados
    if current_user.rol == RoleName.veterinario:
        if cliente.veterinario_id != current_user.veterinario.id:
            raise HTTPException(403, "No tienes acceso")
    
    # Cliente ve solo a sí mismo
    if current_user.rol == RoleName.cliente:
        if cliente.usuario_id != current_user.id:
            raise HTTPException(403, "No tienes acceso")
    
    return ClienteResumen.model_validate(cliente)
```

## Patrones de seguridad

### 1. Defense in Depth
Validación en múltiples capas:
1. Router: `require_admin` / `require_roles`
2. Service: `_can_view_*` helpers
3. Database: Solo datos accesibles

### 2. Fail Secure
Si hay duda sobre acceso, se rechaza (403 Forbidden)

### 3. Zero Trust
Cada endpoint valida credenciales, incluso si viene de cliente confiable

## Escalarios comunes

### Veterinario no ve clientes asignados
**Síntoma**: Error 403 "No tienes acceso"
**Causa**: El cliente no está asignado al veterinario
**Solución**: Admin debe crear cliente con `veterinario_id` correcto

### Cliente ve datos de otro cliente
**Síntoma**: Está viendo establecimientos ajenos
**Causa**: Bug en service layer o acceso directo a BD
**Solución**: Verificar que `_can_view_cliente` se ejecuta en todas las rutas

### Admin no puede ver nada
**Síntoma**: Error 401 o 403
**Causa**: Token expirado o rol no es "admin"
**Solución**: Hacer login nuevamente, verificar JWT

## Testing RBAC

Para testear control de acceso:

```bash
# 1. Crear admin
POST /api/v1/admin/init

# 2. Login como admin
POST /api/v1/auth/login (admin credentials)

# 3. Crear veterinario
POST /api/v1/admin/veterinarios (with admin token)

# 4. Crear cliente
POST /api/v1/admin/clientes (with admin token)

# 5. Login como veterinario
POST /api/v1/auth/login (vet credentials)

# 6. Intentar crear cliente (debe fallar 403)
POST /api/v1/admin/clientes (with vet token)
→ Response: 403 Forbidden

# 7. Login como cliente
POST /api/v1/auth/login (cliente credentials)

# 8. Ver su establecimiento (debe funcionar)
GET /api/v1/establecimientos/{id} (with client token)
→ Response: 200 OK

# 9. Ver establecimiento de otro cliente (debe fallar 403)
GET /api/v1/establecimientos/{id_otro} (with client token)
→ Response: 403 Forbidden
```

## Próximas mejoras

- [ ] Permisos granulares (por acciones específicas)
- [ ] Roles personalizados
- [ ] Auditoría de accesos
- [ ] IP whitelisting
- [ ] 2FA (autenticación de dos factores)
