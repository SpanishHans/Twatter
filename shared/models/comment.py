from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from shared.models.user import Base

class Comment(Base):
    __tablename__ = "comentarios"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    id_publicacion = Column(Integer, ForeignKey("publicaciones.id", ondelete="CASCADE"))
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())