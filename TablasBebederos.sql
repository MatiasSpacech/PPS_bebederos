-- MySQL-compatible schema for Dosificador de Bebedero
-- Adjustments: AUTO_INCREMENT, TINYINT(1) for booleans, ENUM for role/gravity,
-- removed identifier with non-ascii

-- ============================================
-- 1. TABLA DE USUARIOS (Base para todos los roles)
-- ============================================
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    rol ENUM('admin','veterinario','cliente') NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_ultimo_acceso DATETIME NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);

-- ============================================
-- 2. TABLA DE VETERINARIOS
-- ============================================
CREATE TABLE veterinarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT UNIQUE NOT NULL,
    especialidad VARCHAR(255),
    telefono VARCHAR(20),
    ubicacion VARCHAR(255),
    foto_perfil VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_veterinarios_usuario ON veterinarios(usuario_id);

-- ============================================
-- 3. TABLA DE CLIENTES
-- ============================================
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT UNIQUE NOT NULL,
    veterinario_id INT NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    contacto_principal VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id) ON DELETE RESTRICT
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_clientes_usuario ON clientes(usuario_id);
CREATE INDEX idx_clientes_veterinario ON clientes(veterinario_id);

-- ============================================
-- 4. TABLA DE ESTABLECIMIENTOS
-- ============================================
CREATE TABLE establecimientos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    ubicacion VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    UNIQUE(cliente_id, nombre)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_establecimientos_cliente ON establecimientos(cliente_id);

-- ============================================
-- 5. TABLA DE RELACIONES VETERINARIO-CLIENTE
-- ============================================
-- La relación veterinario-cliente se maneja mediante la FK `clientes.veterinario_id`.
-- Tabla `veterinario_cliente` eliminada para evitar redundancia (1 cliente tiene 1 veterinario).

-- ============================================
-- 6. TABLA DE BEBEDEROS
-- ============================================
CREATE TABLE bebederos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    establecimiento_id INT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    ubicacion VARCHAR(255),
    ip_address VARCHAR(45),
    puerto INT DEFAULT 8000,
    cobertura_objetivo FLOAT DEFAULT 80.0,
    estado TINYINT(1) DEFAULT 1,
    ultima_medicion DATETIME NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(establecimiento_id, nombre),
    FOREIGN KEY (establecimiento_id) REFERENCES establecimientos(id) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_bebederos_establecimiento ON bebederos(establecimiento_id);
CREATE INDEX idx_bebederos_estado ON bebederos(estado);

-- ============================================
-- 7. TABLA DE MONITOREO DIARIO
-- ============================================
CREATE TABLE monitoreo_diario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bebedero_id INT NOT NULL,
    fecha DATE NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    nivel_agua_cm FLOAT,
    distancia_sensor_cm FLOAT,
    cobertura_capsulas_porciento FLOAT,
    sensor_ultrasound TINYINT(1),
    camera_activa TINYINT(1),
    analyzer_activo TINYINT(1),
    config_ok TINYINT(1),
    error_message TEXT,
    UNIQUE(bebedero_id, fecha),
    FOREIGN KEY (bebedero_id) REFERENCES bebederos(id) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_monitoreo_bebedero_fecha ON monitoreo_diario(bebedero_id, fecha);

-- ============================================
-- 8. TABLA DE IMAGENES
-- ============================================
CREATE TABLE imagenes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    monitoreo_id INT NOT NULL,
    bebedero_id INT NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_filesystem VARCHAR(500) NOT NULL,
    fecha_captura DATETIME DEFAULT CURRENT_TIMESTAMP,
    tamano_bytes BIGINT,
    checksum VARCHAR(64),
    FOREIGN KEY (monitoreo_id) REFERENCES monitoreo_diario(id) ON DELETE CASCADE,
    FOREIGN KEY (bebedero_id) REFERENCES bebederos(id) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_imagenes_bebedero_fecha ON imagenes(bebedero_id, fecha_captura);

-- Si quieres evitar nombres duplicados por monitoreo:
-- CREATE UNIQUE INDEX uq_imagen_monitoreo_nombre ON imagenes(monitoreo_id, nombre_archivo);

-- ============================================
-- 9. TABLA DE EVENTOS
-- ============================================
CREATE TABLE eventos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bebedero_id INT NOT NULL,
    tipo_evento VARCHAR(100),
    descripcion TEXT,
    gravedad ENUM('info','warning','error','critical'),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    resuelta TINYINT(1) DEFAULT 0,
    fecha_resolucion DATETIME NULL,
    FOREIGN KEY (bebedero_id) REFERENCES bebederos(id) ON DELETE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_eventos_bebedero_sin_resolver ON eventos(bebedero_id, resuelta);
CREATE INDEX idx_eventos_gravedad ON eventos(gravedad, resuelta);

-- End of schema
