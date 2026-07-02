# Configuración de Postman - Bebederos API

Esta guía explica cómo importar y configurar la colección de Postman para probar todos los endpoints de la API.

## Requisitos

- Descargar e instalar [Postman](https://www.postman.com/downloads/)
- Tener la API ejecutándose en `http://localhost:8000`

## Importar la colección

### Opción 1: Desde archivo (recomendado)

1. Abre Postman
2. Haz clic en **Import** (arriba a la izquierda)
3. Selecciona **Upload Files** o arrastra el archivo `Bebederos_API.postman_collection.json`
4. Se importará automáticamente con todos los endpoints organizados por categorías

### Opción 2: Desde URL

Si tienes un servidor que hospeda el archivo, puedes pegar la URL en Postman.

## Variables de entorno

La colección incluye 2 variables globales que puedes configurar:

### `base_url`
- **Valor por defecto**: `http://localhost:8000`
- **Descripción**: URL base de la API
- **Cambiar**: Haz clic en el nombre de la variable en la esquina superior derecha → Manage Environments

### `token`
- **Valor inicial**: vacío
- **Descripción**: Token JWT obtenido del endpoint `/api/v1/auth/login`
- **Nota**: Se asigna automáticamente cuando ejecutas "Login" gracias al script en el body

## Flujo de inicio rápido

### 1. Crear el primer admin

1. Ve a **Admin** → **Init - Crear primer admin**
2. Edita el body con tu email y contraseña (p.ej. `admin@example.com`, `MyPassword123!`)
3. Presiona **Send**
4. Verifica que recibas un `201 Created`

### 2. Login

1. Ve a **Autenticación** → **Login**
2. Cambia el email a el que creaste en el paso anterior
3. Cambia la contraseña a la que usaste
4. Presiona **Send**
5. El script en el body automáticamente guardará el `access_token` en la variable `{{token}}`

Verifica que el token se guardó:
- Haz clic en el ícono del ojo (variables) en la esquina superior derecha
- Busca la variable `token` en la sección de ambiente

### 3. Probar endpoints autenticados

Ahora puedes probar cualquier endpoint que requiera autenticación:

1. Ve a **Auth** → **Me - Usuario autenticado**
2. Presiona **Send**
3. Deberías ver los datos del usuario autenticado

## Estructura de la colección

```
Bebederos API
├── Autenticación
│   ├── Register - Crear cliente
│   ├── Login
│   └── Me - Usuario autenticado
├── Admin
│   ├── Init - Crear primer admin
│   ├── Dashboard
│   ├── Summary
│   ├── Crear veterinario
│   ├── Crear cliente
│   └── Actualizar estado de usuario
├── Clientes
│   ├── Dashboard
│   ├── Me
│   ├── Detalle de cliente
│   └── Mis establecimientos
├── Veterinarios
│   ├── Dashboard
│   ├── Me
│   ├── Detalle de veterinario
│   ├── Mis clientes
│   └── Establecimientos de cliente
├── Establecimientos
│   ├── Detalle de establecimiento
│   └── Bebederos del establecimiento
├── Bebederos
│   └── Detalle con monitoreos e imágenes
└── Imágenes
    └── Descargar imagen
```

## Ejemplos de uso

### Crear un veterinario

1. Primero, haz login como admin (pasos arriba)
2. Ve a **Admin** → **Crear veterinario**
3. Edita el body con los datos del veterinario
4. Presiona **Send**
5. Debería responder con `201 Created`

### Crear un cliente

1. Ve a **Admin** → **Crear cliente**
2. **Importante**: Usa el `veterinario_id` de un veterinario que creaste previamente
3. Edita el body con los datos del cliente
4. Presiona **Send**

### Ver detalles de un bebedero

1. Ve a **Bebederos** → **Detalle de bebedero con monitoreos e imágenes**
2. Reemplaza el `1` en la URL con el ID del bebedero que quieras consultar
3. Presiona **Send**
4. Verás monitoreos, imágenes y el campo `image_url` para cada imagen

### Descargar una imagen

1. Ve a **Imágenes** → **Descargar imagen**
2. Reemplaza el `1` en la URL con el ID de la imagen que quieras descargar
3. Presiona **Send**
4. Postman te mostrará la imagen en la pestaña Preview

## Códigos de error comunes

| Código | Significado | Solución |
|--------|-----------|----------|
| `400` | Bad Request | Valida el JSON del body |
| `401` | Unauthorized | Verifica que el token sea válido (usa Login) |
| `403` | Forbidden | No tienes permisos para acceder a este recurso |
| `404` | Not Found | El recurso no existe (verifica el ID) |
| `409` | Conflict | Ya existe (p. ej. email duplicado) |
| `422` | Unprocessable Entity | Datos inválidos (p. ej. contraseña < 8 caracteres) |

## Tips y trucos

### Ver todos los headers de una respuesta

1. Presiona **Send**
2. Ve a la pestaña **Headers** debajo de la respuesta
3. Verás `Content-Type`, `Authorization` (si aplica), etc.

### Guardar respuestas como ejemplos

1. Presiona **Send**
2. En la sección de respuesta, haz clic en **Save as example**
3. Dale un nombre descriptivo
4. Ahora puedes ver los ejemplos previos haciendo clic en **Examples** arriba de la respuesta

### Usar scripts pre-request

Algunos endpoints tienen scripts que se ejecutan **antes** de enviar el request (p. ej. validar que el token exista). Puedes verlos en la pestaña **Pre-request Script**.

### Usar scripts test

Algunos endpoints tienen scripts que se ejecutan **después** de recibir la respuesta (p. ej. guardar el token). Puedes verlos en la pestaña **Tests**.

## Troubleshooting

### El token no se guarda automáticamente

1. Abre el endpoint **Login**
2. Ve a la pestaña **Tests** (abajo)
3. Verifica que haya un script que inicie con:
   ```js
   if (pm.response.code === 200) {
     const jsonData = pm.response.json();
     pm.environment.set('token', jsonData.access_token);
   }
   ```
4. Si no está, añádelo

### No puedo conectarme a `http://localhost:8000`

1. Asegúrate de que la API esté corriendo:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Verifica el puerto (por defecto es 8000)
3. Si usas otro puerto, actualiza la variable `base_url` en Postman

### Recibo error 401 en todos los endpoints

1. Ve a **Autenticación** → **Login**
2. Asegúrate de usar las credenciales correctas
3. Presiona **Send**
4. Verifica que recibas un `access_token`
5. El script debería guardar el token automáticamente en `{{token}}`

## Próximos pasos

- Crea un ambiente de desarrollo y otro de producción con diferentes valores de `base_url`
- Usa **Collection Runner** para ejecutar toda la colección automáticamente
- Exporta logs y respuestas para auditoría
