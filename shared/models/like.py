from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from shared.models.user import Base

class Like(Base):
    __tablename__ = "me_gusta"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    id_publicacion = Column(Integer, ForeignKey("publicaciones.id", ondelete="CASCADE"))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
