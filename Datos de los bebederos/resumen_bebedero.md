# Dosificador de Bebedero - Documentación del Proyecto y API REST

## Descripción del Proyecto

Sistema IoT desarrollado en Python con FastAPI para el monitoreo y dosificación automática de un bebedero de agua. El sistema utiliza un sensor ultrasónico para medir el nivel de agua, una cámara para capturar fotos del bebedero y un analizador de imágenes para calcular el porcentaje de cobertura de cápsulas en la superficie del agua.

Si la cobertura detectada está por debajo del objetivo configurado, el sistema inicia automáticamente el proceso de dosificación hasta alcanzar el nivel deseado.

## Arquitectura

El proyecto está organizado en los siguientes módulos:

| Módulo | Descripción |
|--------|-------------|
| `api_main.py` | Entry point de la API REST (FastAPI) |
| `main.py` | Workflow principal de dosificación automática |
| `core/` | Lógica de hardware: sensor, cámara, analizador, dosificador |
| `api/` | API REST: routes, controllers, models |
| `utilities/` | Helpers: scheduler, file_handler, logging |
| `error_handling/` | Manejo de errores y troubleshooting |
| `send_info/` | Envío de información y alertas |

---

## Endpoints de la API

### Configuración

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/config` | Obtiene la configuración completa |
| `PATCH` | `/basic-config` | Actualiza configuraciones básicas |
| `PATCH` | `/config` | Actualiza configuración (permite campos nuevos) |

**Ejemplos:**

```bash
# Obtener configuración
curl http://localhost:8000/config

# Actualizar configuración básica
curl -X PATCH http://localhost:8000/basic-config \
  -H "Content-Type: application/json" \
  -d '{
    "watertank": {"coverage": 85},
    "set_active": true,
    "reschedule_hours": {"normal": 24, "error": 2}
  }'

# Actualizar configuración arbitraria
curl -X PATCH http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{
    "watertank": {"coverage": 90},
    "nuevo_campo": "valor"
  }'
```

---

### Cámara

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/camera/capture` | Toma una foto y la devuelve en base64 |
| `GET` | `/camera/last-image` | Obtiene la última imagen tomada |
| `GET` | `/camera/photo/{photo_name}` | Obtiene una imagen específica por nombre |

**Ejemplos:**

```bash
# Capturar foto
curl -X POST http://localhost:8000/camera/capture
# Respuesta: {"nombre": "foto_manual.jpg", "imagen": "base64..."}

# Obtener última imagen
curl http://localhost:8000/camera/last-image

# Obtener foto específica
curl http://localhost:8000/camera/photo/ultima_foto.jpg
```

---

### Sensores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/water-status` | Estado del agua (distancia y nivel) |
| `GET` | `/health` | Estado de salud de todos los componentes |

**Ejemplos:**

```bash
# Estado del agua
curl http://localhost:8000/water-status
# Respuesta exitosa: {"distancia": 50, "nivel_de_agua": "50/100", "error": null}
# Respuesta sin agua: {"distancia": 120, "nivel_de_agua": "0/100", "error": "No hay suficiente agua..."}

# Health check
curl http://localhost:8000/health
# Respuesta: {
#   "ultrasonic_sensor": true,
#   "camera": true,
#   "analyzer": true,
#   "config": true,
#   "log": true
# }
```

---

### Análisis de Imágenes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/analyze/image/{photo_name}` | Analiza una imagen específica |
| `GET` | `/analyze/last-image` | Analiza la última imagen tomada |

**Ejemplos:**

```bash
# Analizar imagen específica
curl http://localhost:8000/analyze/image/ultima_foto.jpg
# Respuesta: {"resultado": 0.75, "nombre": "ultima_foto.jpg"}

# Analizar última imagen
curl http://localhost:8000/analyze/last-image
```

---

### Logs

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/log/full` | Log completo con imágenes en base64 |
| `GET` | `/log/text` | Solo texto del log |
| `GET` | `/log/photos` | Descarga todas las imágenes en ZIP |

**Ejemplos:**

```bash
# Log completo con imágenes
curl http://localhost:8000/log/full

# Solo texto del log
curl http://localhost:8000/log/text
# Respuesta: {"log": "2025-03-12 18:00:00 - INFO - Analisis realizado..."}

# Descargar imágenes del log como ZIP
curl -o log_imagenes.zip http://localhost:8000/log/photos
```

---

### Scheduler

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/scheduler/clear-jobs` | Elimina todas las tareas programadas |
| `POST` | `/scheduler/run-job` | Programa la ejecución de un script |
| `GET` | `/scheduler/list-jobs` | Lista tareas pendientes |

**Ejemplos:**

```bash
# Limpiar tareas programadas
curl -X POST http://localhost:8000/scheduler/clear-jobs
# Respuesta: {"message": "Todas las tareas programadas han sido eliminadas."}

# Programar ejecución de script
curl -X POST http://localhost:8000/scheduler/run-job \
  -H "Content-Type: application/json" \
  -d '{"script": "main.py", "minutes": 30}'
# Respuesta: {"message": "Se ha programado 'main.py' para ejecutarse en 30 minutos."}

# Listar tareas pendientes
curl http://localhost:8000/scheduler/list-jobs
# Respuesta: {"lista": [...]}
```

---

## Configuración por Defecto (config.yml)

```yaml
camera:
  total_photo: 3          # Fotos por análisis
reschedule_hours:
  error: 1                # Reintentar tras error (horas)
  normal: 24              # Reintentar normal (horas)
set_active: true          # Sistema activado
ultrasound:
  empty: 100              # Distancia cuando está vacío
  full: 0                 # Distancia cuando está lleno
volumetric:
  deep: 100               # Profundidad del bebedero
  height: 100             # Altura
  length: 200             # Largo
watertank:
  coverage: 80            # Cobertura objetivo (%)
```

## Cómo iniciar la API

```bash
cd dosificador
uvicorn api_main:app --host 0.0.0.0 --port 8000
```

Una vez iniciada, la documentación interactiva de Swagger estará disponible en:
**http://localhost:8000/docs**
