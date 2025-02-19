from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    foto_perfil = Column(String(255))
    biografia = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Publicacion(Base):
    __tablename__ = "publicaciones"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    es_recomparte = Column(Boolean, default=False)
    id_publicacion_original = Column(Integer, ForeignKey("publicaciones.id", ondelete="SET NULL"), nullable=True)

    # Relaciones con archivos multimedia
    archivos_multimedia = relationship("ArchivoMultimedia", back_populates="publicacion")

class ArchivoMultimedia(Base):
    __tablename__ = "archivos_multimedia"

    id = Column(Integer, primary_key=True, index=True)
    id_publicacion = Column(Integer, ForeignKey("publicaciones.id", ondelete="CASCADE"))
    tipo_medio = Column(String(50), nullable=False)
    url_medio = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con publicación
    publicacion = relationship("Publicacion", back_populates="archivos_multimedia")