from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from modules.db_engine import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)

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