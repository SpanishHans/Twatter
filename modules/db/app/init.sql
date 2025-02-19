-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear las tablas
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    foto_perfil VARCHAR(255),
    biografia TEXT,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE publicaciones (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    contenido TEXT NOT NULL,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    es_recomparte BOOLEAN DEFAULT FALSE,
    id_publicacion_original INTEGER REFERENCES publicaciones(id) ON DELETE SET NULL
);

CREATE TABLE me_gusta (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    id_publicacion INTEGER REFERENCES publicaciones(id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_usuario, id_publicacion)
);

CREATE TABLE seguidores (
    id SERIAL PRIMARY KEY,
    id_seguidor INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    id_seguido INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_seguidor, id_seguido)
);

CREATE TABLE comentarios (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    id_publicacion INTEGER REFERENCES publicaciones(id) ON DELETE CASCADE,
    contenido TEXT NOT NULL,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE archivos_multimedia (
    id SERIAL PRIMARY KEY,
    id_publicacion INTEGER REFERENCES publicaciones(id) ON DELETE CASCADE,
    tipo_medio VARCHAR(50) NOT NULL,
    url_medio VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_usuarios_nombre_usuario ON usuarios(nombre_usuario);
CREATE INDEX idx_usuarios_correo ON usuarios(correo);
CREATE INDEX idx_publicaciones_usuario ON publicaciones(id_usuario);
CREATE INDEX idx_publicaciones_fecha ON publicaciones(fecha_creacion);
CREATE INDEX idx_me_gusta_usuario ON me_gusta(id_usuario);
CREATE INDEX idx_me_gusta_publicacion ON me_gusta(id_publicacion);
CREATE INDEX idx_seguidores_seguidor ON seguidores(id_seguidor);
CREATE INDEX idx_seguidores_seguido ON seguidores(id_seguido);
CREATE INDEX idx_comentarios_usuario ON comentarios(id_usuario);
CREATE INDEX idx_comentarios_publicacion ON comentarios(id_publicacion);