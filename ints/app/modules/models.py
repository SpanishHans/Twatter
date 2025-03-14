from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from modules.db_engine import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)

class Publicacion(Base):
    __tablename__ = "publicaciones"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=False)

class MeGusta(Base):
    __tablename__ = "me_gusta"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    id_publicacion = Column(Integer, ForeignKey("publicaciones.id", ondelete="CASCADE"))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

class Comentario(Base):
    __tablename__ = "comentarios"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    id_publicacion = Column(Integer, ForeignKey("publicaciones.id", ondelete="CASCADE"))
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())