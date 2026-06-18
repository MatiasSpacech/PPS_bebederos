# El administrador es el rol con acceso total al sistema. Estas serían sus funciones principales:
Gestión de usuarios

Crear, editar y desactivar cuentas de veterinarios y clientes
Asignar qué veterinario supervisa a qué cliente
Resetear contraseñas y gestionar permisos

Gestión de dispositivos

Registrar nuevos bebederos en el sistema y asignarlos a un cliente
Ver el estado de conexión de todos los dispositivos (online / offline)
Configurar parámetros de los bebederos (umbrales de alerta, frecuencia de envío de datos, etc.)

Visibilidad total

Ver el dashboard de cualquier cliente o veterinario
Acceder al historial completo de datos de cualquier bebedero
Ver todas las alertas del sistema, no solo las de un cliente

Configuración del sistema

Definir los tipos de alertas y sus condiciones (ej: "nivel menor al 20% → alerta crítica")
Gestionar integraciones (si los datos llegan por MQTT, HTTP, etc.)

Reportes globales

Generar reportes de todo el sistema o filtrados por cliente, veterinario, región, etc.
Ver métricas generales: cuántos bebederos activos, cuántas alertas en el mes, etc.


En resumen, el admin es el único que puede crear y conectar las piezas del sistema. Los veterinarios y clientes solo ven datos, el admin configura todo.

# Veterinarios
Vista de supervisión general — el veterinario ve todos sus clientes en una lista, con un estado rápido de cada uno (todo bien / hay alertas). Desde ahí puede entrar al detalle de un cliente y ver sus bebederos.
Dashboard del veterinario → lista de sus clientes con estado general (verde / amarilla / roja)
Al entrar a un cliente → ve el resumen de todos los bebederos de ese cliente (igual que vería el cliente mismo)
Sección de alertas → historial de alertas de todos sus clientes en un solo lugar

# Clientes
Los clientes solo visualizan sus propios establecimientos y los bebederos contenidos en ellos. Un establecimiento agrupa uno o varios bebederos para facilitar la gestión cuando un cliente posee múltiples bebederos.

- Acceso: ver solo sus establecimientos (no puede ver establecimientos de otros clientes).
- Dentro de un establecimiento: ver la lista de bebederos, estado actual y datos de monitoreo (monitoreo diario, imágenes y eventos) en modo solo lectura.
- Relación con veterinarios: cada cliente tiene un único veterinario asignado (campo `veterinario_id` en la entidad `CLIENTES`); un veterinario puede supervisar varios clientes.
- Eventos: los clientes pueden ver el historial de eventos asociados a sus bebederos, pero no pueden editarlos ni resolverlos (solo visualización).

# Eventos y visibilidad
Todos los roles del sistema (admin, veterinario y cliente) pueden visualizar los eventos asociados a los bebederos. En esta etapa los eventos son de solo lectura para todos los roles; la capacidad de editar o resolver eventos se definirá posteriormente.

